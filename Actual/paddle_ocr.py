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

from PIL import Image, ImageDraw
from collections import Counter

'''
    An OCRProcessor using PaddleOCR.

    Parameters:
    - lang (str): Language to be used by PaddleOCR.
    - use_angle_cls (bool): Whether to use angle classification.
    - font_path (str): Path to a .ttf font file for text rendering in draw_ocr.
    - text_detection_model_dir (str): Path to the text detection model folder.
    - text_recognition_model_dir (str): Path to the text recognition model folder.
    - use_doc_orientation_classify (bool): Enables/disables document orientation classification model (PP-LCNet_x1_0_doc_ori). This model is mainly useful for photos of text/docs.
    - use_doc_unwarping (bool): Enables/disables image unwarping model (UVDoc). This model is mainly useful for photos of text/docs. On an unwarped image (e.g. screenshot of computer screen), unwarping it results in a warped image.
    - use_textline_orientation (bool): Enables/disables text line orientation classification model (PP-LCNet_x1_0_textline_ori). This model is mainly useful for photos of text/docs.
'''

class OCRProcessor:
    '''
    # This init function is for PaddleOCR version v3.0.0 onwards
    '''
    def __init__(self, lang = 'en', font_path = None,
                 text_detection_model_name = None,
                 text_detection_model_dir = None,
                 text_recognition_model_name = None,
                 text_recognition_model_dir = None,
                 use_doc_orientation_classify=None,
                 use_doc_unwarping=None,
                 use_textline_orientation=None,
                 ):
        self.ocr = PaddleOCR(lang=lang,
                             text_detection_model_name = text_detection_model_name,
                             text_detection_model_dir = text_detection_model_dir,
                             text_recognition_model_name = text_recognition_model_name,
                             text_recognition_model_dir = text_recognition_model_dir,
                             use_doc_orientation_classify = use_doc_orientation_classify,
                             use_doc_unwarping = use_doc_unwarping,
                             use_textline_orientation = use_textline_orientation
                             )
        self.font_path = font_path
        self.text_detection_model_name = text_detection_model_name
        self.text_detection_model_dir = text_detection_model_dir
        self.text_recognition_model_name = text_recognition_model_name
        self.text_recognition_model_dir = text_recognition_model_dir
        self.use_doc_orientation_classify = use_doc_orientation_classify
        self.use_doc_unwarping = use_doc_unwarping
        self.use_textline_orientation = use_textline_orientation
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
            frame_rgb = frame.get("current")
            # Get alt_name to find the relevant triggers
            self.perform_ocr_using_triggers(alt_name, frame_rgb)
            # Set to show that the frame has been processed
            with Screenshot.lock:
                frame['processed'] = True

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
        colour = val["triggers"][condition]["bg_colour"]

        # Create a dictionary with the text as the key, and the boxes in an array
        text_to_boxes = {}

        # Perform the OCR
        # .predict() returns a list with length corresponding to the number of input images (length of 1 for 1 input image)
        result = self.ocr.predict(frame_rgb)

        for ocr_data in result:
            texts = ocr_data.get('rec_texts', [])

            if not texts:   # If screenshot is empty, there will not be any recognised text data
                print("This screenshot has no words.")
                return

            scores = ocr_data.get('rec_scores', [])
            boxes = ocr_data.get('rec_polys', [])

            for text, score, box in zip(texts, scores, boxes):
                bg_colour = self.get_box_majority_color_hex(frame_rgb, box)
                if all(keyword.lower() in text.lower() for keyword in keyword_list) and bg_colour == colour:
                    text_to_boxes.setdefault(text, []).append(box.tolist())

                    # For Testing
                    bg_colour = self.get_box_majority_color_hex(frame_rgb, box)
                    print("The bg_colour is:", bg_colour)
                    print("The colour I am looking for is:", colour)

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
            frame_rgb_copy = frame_rgb.copy()
            self.draw_boxes(frame_rgb_copy, boxes)
            
            # Save the screenshot
            timestamp = datetime.now().strftime("%Y%m%d %H%M%S")
            self.save_processed_screenshot(alt_name, frame_rgb_copy, timestamp, sentence)

            # Send message to GUI
            self.send_message((timestamp, sentence, alt_name, tts_message))
        
        # Update the sentence_list
        self.update_sentence_list(alt_name, condition, text_to_boxes.keys())
    
    """
        Get the most frequent RGB color inside the polygon box area.
        Returns hex string like '#aabbcc'
    """
    def get_box_majority_color_hex(self, frame_rgb, box):

        # Convert frame to PIL image
        image = Image.fromarray(frame_rgb)

        # Create a black mask image (same size as frame)
        mask = Image.new("L", image.size, 0)

        # Draw the polygon (OCR box) as a white area (255) in the mask
        ImageDraw.Draw(mask).polygon([tuple(p) for p in box], fill=255)

        # Convert to NumPy arrays
        np_image = np.array(image)
        np_mask = np.array(mask)

        # Extract pixels inside the polygon mask
        masked_pixels = np_image[np_mask == 255]

        if len(masked_pixels) == 0:
            return None

        # Convert each pixel to tuple and count frequencies
        color_counts = Counter(map(tuple, masked_pixels))
        most_common_color = color_counts.most_common(1)[0][0]  # (r, g, b)

        r, g, b = most_common_color
        return f'#{r:02x}{g:02x}{b:02x}'


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

            # Filter to keep only screenshots from the last X minutes
            now = datetime.now()
            time_threshold = now - timedelta(minutes=60)
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
            MessageQueue.status_queue.put(message)
