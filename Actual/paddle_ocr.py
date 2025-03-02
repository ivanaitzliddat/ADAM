import time
import traceback
import cv2
import numpy as np
from paddleocr import PaddleOCR
from screenshots import Screenshot
from processed_screenshot import Processed_Screenshot
from config_handler import ConfigHandler
from subthread_config import Thread_Config
from messages import MessageQueue
from datetime import datetime, timedelta

'''
    An OCRProcessor using PaddleOCR.

    Parameters:
    - lang (str): Language to be used by PaddleOCR.
    - use_angle_cls (bool): Whether to use angle classification.
    - font_path (str): Path to a .ttf font file for text rendering in draw_ocr.
'''
class OCRProcessor:

    def __init__(self, lang='en', use_angle_cls=True, font_path=None):
        self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
        self.font_path = font_path

    '''
        Iterates through the frames that were captured previously and runs the OCR.
    '''
    def run(self):
        while Thread_Config.running:
            time.sleep(3)
            try:
                self.interate_screenshots()
            except Exception as e:
                traceback.print_exc()
                print(f"OCR has encountered the exception: {e}")
            finally:
                pass
        print("OCR Processor has ended.")

    '''
        Iterate through the screenshots captured and process a particular frame.
    '''
    def interate_screenshots(self):
        temp_index = 0
        for frame in Screenshot.frames:
            self.process_frame(frame)
            temp_index += 1

    '''
    Process a particular frame by getting the triggers tagged to the particular capture cards
    '''
    def process_frame(self, frame):
        # Check if the frame is new
        processed = frame.get('processed')
        if not processed:
            # Convert the frame to RGB
            frame_rgb = self.convert_frame(frame)
            # Get alt_name to find the relevant triggers
            self.perform_ocr_using_triggers(frame, frame_rgb)
        else:
            with Screenshot.lock:
                Screenshot.frames.remove(frame)
                print("Successfully removed a screenshot from the screenshot list")
                print("The number of screenshots left is: ", len(Screenshot.frames))

    '''
        Converts the frame to allow the processing of frame using imageio.
    '''
    def convert_frame(self, frame):
        screenshot = frame.get('current')
        frame_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        return frame_rgb

    '''
        Iterate through the triggers that are tagged to the capture cards and process via the conditions.
    '''
    def perform_ocr_using_triggers(self, frame, frame_rgb):
        alt_name = frame.get('alt_name')
        keywords_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name = alt_name)
        if not bool(keywords_dict):
            print("The keywords dictionary is empty.")
        else:
            self.perform_ocr_using_conditions(frame, frame_rgb, alt_name, keywords_dict)
    
    '''
        Obtain the keyword list from the conditions and perform the actual OCR using the keyword list.
    '''
    def perform_ocr_using_conditions(self, frame, frame_rgb, alt_name, keywords_dict):
        for key, val in keywords_dict.items():
            for condition in val["triggers"]:
                keyword_list = val["triggers"][condition]["keywords"]
                tts_message = val["triggers"][condition]['tts_text']

                # Perform the OCR
                has_keyword = self.perform_ocr(frame_rgb, alt_name, keyword_list, tts_message)

                # Set to show that the frame has been processed
                with Screenshot.lock:
                    frame['processed'] = True

                if not has_keyword:
                    print("No keywords Found.")

    '''
        Performs OCR on a given frame using the keyword list provided.
    '''
    def perform_ocr(self, frame, alt_name, keywords, tts_message):
        has_keyword = False
        result = self.ocr.ocr(frame, cls=True)
        # Display OCR results that contain the keywords
        if not None in result:
            has_keyword = self.iterate_line_in_screenshot(frame, keywords, alt_name, result, tts_message)
        return has_keyword
    
    '''
        Disect the screenshot by looking through the words identified line by line.
    '''
    def iterate_line_in_screenshot(self, frame, keywords, alt_name, result, tts_message):
        for line in result:
            for box, (text, score) in line:
                has_keyword = self.search_keywords_in_line(frame, keywords, alt_name, box, text, score, tts_message)
        return has_keyword
    
    '''
        Search for the keywords in a single line.
    '''
    def search_keywords_in_line(self, frame, keywords, alt_name, box, text, score, tts_message):
        # Filter the results to include only texts containing the keyword
        filtered_boxes = []
        filtered_texts = []
        filtered_scores = []
        identified_keyword = all(keyword.lower() in text.lower() for keyword in keywords)
        if identified_keyword:
            filtered_boxes.append(box)
            filtered_texts.append(text)
            filtered_scores.append(score)

            # Draw filtered OCR results on the image
            self.draw_boxes(frame, filtered_boxes)

            # Get current time
            timestamp = datetime.now().strftime("%Y%m%d %H%M%S")

            # Save the image
            self.save_processed_screenshot(frame, alt_name, timestamp)

            # Send message to GUI
            self.send_message((timestamp, alt_name, tts_message))

        return identified_keyword

    '''
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        with MessageQueue.lock:
            MessageQueue.status_queue.put(message)

    '''
        Draw boxes around the identified keywords
    '''
    def draw_boxes(self, frame, filtered_boxes):
        for box in filtered_boxes:
                # Convert the box points to integers
            points = np.array(box, dtype=np.int32)
                # Draw the polygon
            cv2.polylines(frame, [points], isClosed=True, color=(0, 0, 255), thickness=2)

    '''
        Save the screenshots in the Processed Screenshot list.
    '''
    def save_processed_screenshot(self, frame, alt_name, timestamp):
        with Processed_Screenshot.lock:
            Processed_Screenshot.frames.setdefault(alt_name, {}).update({timestamp: frame})
            print("New screenshot has been added to processed screenshot")
            Processed_Screenshot.frames = {datetime.strptime(k, "%Y%m%d %H%M%S"): v for k, v in Processed_Screenshot.frames[alt_name].items()}
                # Get the current time
            now = datetime.now()
                # Define the time threshold (5 minutes ago)
            time_threshold = now - timedelta(minutes=5)
                # Filter dictionary to keep only recent timestamps
            Processed_Screenshot.frames = {k: v for k, v in Processed_Screenshot.frames.items() if k >= time_threshold}
            print("Successfully filtered processed screenshots such that only freshly processed screenshots are kept.")