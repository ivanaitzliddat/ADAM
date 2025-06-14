import time, traceback

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
    def __init__(self, lang = 'en', use_angle_cls = True, font_path = None,
                 cls_model_dir = None, det_model_dir = None, rec_model_dir = None):
        self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang,
                             cls_model_dir = cls_model_dir, det_model_dir = det_model_dir, rec_model_dir = rec_model_dir)
        self.font_path = font_path
        self.cls_model_dir = cls_model_dir
        self.det_model_dir = det_model_dir
        self.rec_model_dir = rec_model_dir
    '''
        Iterates through the frames that were captured previously and runs the OCR.
    '''
    def run(self):
        while Thread_Config.running:
            time.sleep(3)
            try:
                self.iterate_screenshots()
            except Exception as e:
                traceback.print_exc()
                print(f"OCR has encountered the exception: {e}")
            finally:
                pass
        print("OCR Processor has ended.")

    '''
        Iterate through the screenshots captured and process a particular frame.
    '''
    def iterate_screenshots(self):
        temp_index = 0
        for frame in Screenshot.frames:
            if Thread_Config.running:
                self.process_frame(frame)
                temp_index += 1
            else:
                return

    '''
    Process a particular frame by getting the triggers tagged to the particular capture cards
    '''
    def process_frame(self, frame):
        # Check if the frame is new
        processed = frame.get('processed')
        is_black = frame.get('is_black')
        if not processed and not is_black:
            # Convert the frame to RGB
            frame_rgb = self.convert_frame(frame)
            # Get alt_name to find the relevant triggers
            self.perform_ocr_using_triggers(frame, frame_rgb)
            # Set to show that the frame has been processed
            with Screenshot.lock:
                frame['processed'] = True

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
        # Create a list of lines that has the keywords in it

        for key, val in keywords_dict.items():
            for condition in val["triggers"]:
                keyword_list = val["triggers"][condition]["keywords"]
                tts_message = val["triggers"][condition]['tts_text']

                # Perform the OCR
                has_keyword, new_frame_rgb, sentence_list = self.perform_ocr(np.copy(frame_rgb), alt_name, keyword_list)
                
                if not has_keyword:
                    print("No keywords Found.")
                else:
                    condition_list = Processed_Screenshot.sentence_dict.get(alt_name, [])
                    if condition_list:
                        existing_sentences = set(condition_list.get(condition, []))
                    else:
                        existing_sentences = set()
                    print("Existing sentence list:", existing_sentences)
                    new_sentences = [s.strip() for s in sentence_list if s.strip() not in existing_sentences]
                    print("New sentence list:", new_sentences)
                    if not Processed_Screenshot.sentence_dict.get(alt_name):
                        Processed_Screenshot.sentence_dict[alt_name] = {}
                    Processed_Screenshot.sentence_dict[alt_name][condition] = [s.strip() for s in sentence_list]

                    if new_sentences:
                        # Get current time
                        timestamp = datetime.now().strftime("%Y%m%d %H%M%S")

                        # Save the image
                        self.save_processed_screenshot(new_frame_rgb, alt_name, timestamp)

                        # Send message to GUI
                        self.send_message((timestamp, alt_name, tts_message, sentence_list))

    '''
        Performs OCR on a given frame using the keyword list provided.
    '''
    def perform_ocr(self, frame, alt_name, keywords):
        has_keyword = False
        result = self.ocr.ocr(frame, cls=True)
        # Display OCR results that contain the keywords
        if not None in result:
            has_keyword, frame, sentence_list = self.iterate_line_in_screenshot(frame, keywords, alt_name, result)
        else:
            sentence_list = []
        return has_keyword, frame, sentence_list
    
    '''
        Disect the screenshot by looking through the words identified line by line.
    '''
    def iterate_line_in_screenshot(self, frame, keywords, alt_name, result):
        has_keyword = False
        sentence_list = []
        for line in result:
            for box, (text, score) in line:
                identified_keyword, frame, filtered_texts = self.search_keywords_in_line(frame, keywords, alt_name, box, text, score)
                has_keyword = has_keyword | identified_keyword
                if identified_keyword:
                    sentence_list.append(filtered_texts[0])
        return has_keyword, frame, sentence_list

    '''
        Search for the keywords in a single line.
    '''
    def search_keywords_in_line(self, frame, keywords, alt_name, box, text, score):
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

        return identified_keyword, frame, filtered_texts

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
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        with MessageQueue.lock:
            MessageQueue.status_queue.put(message)

    '''
    Save the screenshots in the Processed Screenshot list.
    '''
    def save_processed_screenshot(self, frame, alt_name, timestamp):
        with Processed_Screenshot.lock:
            # Insert new screenshot
            Processed_Screenshot.frames.setdefault(alt_name, {}).update({timestamp: frame})
            print("New screenshot has been added to processed screenshot")

            # Filter to keep only screenshots from the last 5 minutes
            now = datetime.now()
            time_threshold = now - timedelta(minutes=5)
            frames_dict = {k: v for k, v in Processed_Screenshot.frames[alt_name].items() if datetime.strptime(k, "%Y%m%d %H%M%S") >= time_threshold}

            # Save back the cleaned dictionary
            Processed_Screenshot.frames[alt_name] = frames_dict

            print("Successfully filtered processed screenshots such that only freshly processed screenshots are kept.")