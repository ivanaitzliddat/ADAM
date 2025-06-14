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
        alt_name = frame.get('alt_name')
        if not processed and not is_black:
            # Convert the frame to RGB
            frame_rgb = self.convert_frame(frame)
            # Get alt_name to find the relevant triggers
            self.perform_ocr_using_triggers(alt_name, frame_rgb)
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
    def perform_ocr_using_triggers(self, alt_name, frame_rgb):
        keywords_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name = alt_name)

        if not bool(keywords_dict):
            print("The keywords dictionary is empty.")
            return
        
        for key, val in keywords_dict.items():
            for condition in val["triggers"]:
                self.perform_ocr_using_conditions(val, condition, frame_rgb, alt_name)
    
    '''
        Obtain the keyword list from the conditions and perform the actual OCR using the keyword list.
    '''
    def perform_ocr_using_conditions(self, val, condition, frame_rgb, alt_name):
        # Identify the keywords for the condition, as well as the tts message for each condition
        keyword_list = val["triggers"][condition]["keywords"]
        tts_message = val["triggers"][condition]['tts_text']

        # Perform the OCR
        result = self.ocr.ocr(frame_rgb, cls=True)
        if None in result:
            print("This screenshot has no words.")
            return
        
        # Create a dictionary with the text as the key, and the boxes in an array
        text_to_boxes = {}

        # Iterate through each line of the results to identify sentences that contain the keywords
        for line in result:
            for box, (text, score) in line:
                if all(keyword.lower() in text.lower() for keyword in keyword_list):
                    text_to_boxes.setdefault(text, []).append(box)

        print("This is the entire text_to_boxes:")
        print(text_to_boxes)
        print("This is just the keys:")
        print(text_to_boxes.keys())
        print("This is the keys stripped:")
        print([s.strip() for s in text_to_boxes.keys()])

        # Identify the sentence_list tagged to the condition of the current screenshot
        condition_list = Processed_Screenshot.sentence_dict.get(alt_name, [])
        if condition_list:
            existing_sentences = set(condition_list.get(condition, []))
        else:
            existing_sentences = set()
        print("Existing sentence list:\n", existing_sentences)

        # Check what are the new sentences in text_to_boxes
        new_sentences = list(set(set(text_to_boxes.keys()) - existing_sentences))
        print("New sentence list:\n", new_sentences)

        if not new_sentences:
            return

        # Draw boxes around those new sentences
        for sentence in new_sentences:
            boxes = text_to_boxes[sentence]
            print("The current box that I am drawing is:")
            print(boxes)
            frame_rgb_copy = frame_rgb.copy()
            self.draw_boxes(frame_rgb_copy, boxes)
            
            # Save the screenshot
            timestamp = datetime.now().strftime("%Y%m%d %H%M%S")
            self.save_processed_screenshot(alt_name, frame_rgb_copy, timestamp, sentence)
        
        # Update the sentence_list
        self.update_sentence_list(alt_name, condition, text_to_boxes.keys())
            
        # Send message to GUI
        self.send_message((timestamp, sentence, alt_name, tts_message))
        
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
    def save_processed_screenshot(self, alt_name, frame, timestamp, sentence):
        with Processed_Screenshot.lock:
            # Insert new screenshot
            Processed_Screenshot.frames.setdefault(alt_name, {}).update({(timestamp, sentence): frame})
            print("New screenshot has been added to processed screenshot")

            # Filter to keep only screenshots from the last 5 minutes
            now = datetime.now()
            time_threshold = now - timedelta(minutes=5)
            frames_dict = {k: v for k, v in Processed_Screenshot.frames[alt_name].items() if datetime.strptime(k[0], "%Y%m%d %H%M%S") >= time_threshold}

            # Save back the cleaned dictionary
            Processed_Screenshot.frames[alt_name] = frames_dict

            print("Successfully filtered processed screenshots such that only freshly processed screenshots are kept.")

    '''
    Update the sentence_list in Processed_Screenshot class.
    '''
    def update_sentence_list(self, alt_name, condition, sentences):
        # Update the sentence_list
        if not Processed_Screenshot.sentence_dict.get(alt_name):
            Processed_Screenshot.sentence_dict[alt_name] = {}
        Processed_Screenshot.sentence_dict[alt_name][condition] = sentences

    '''
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        with MessageQueue.lock:
            print("The message that I am sending is:")
            print(message)
            MessageQueue.status_queue.put(message)