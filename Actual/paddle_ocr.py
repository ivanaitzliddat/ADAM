import time
from datetime import datetime
import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
from screenshots import Screenshot
from processed_screenshot import Processed_Screenshot
from config_handler import ConfigHandler
from subthread_config import Thread_Config
from messages import MessageQueue

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
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        with MessageQueue.lock:
            MessageQueue.status_queue.put(message)

    '''
        Performs OCR on a given frame.

        Parameters:
        - frame (np.ndarray): The frame to perform OCR on, in RGB format.

        Returns:
        - result (list): OCR results, each containing bounding boxes, text, and confidence scores.
    '''
    def perform_ocr(self, frame, keywords):
        has_keyword = False
        # Filter the results to include only texts containing the keyword
        filtered_boxes = []
        filtered_texts = []
        filtered_scores = []
        print("Performing OCR...")
        result = self.ocr.ocr(frame, cls=True)

        # Display OCR results that contain the keyword "monitor"
        if not None in result:
            for line in result:
                for box, (text, score) in line:
                    for keyword in keywords:
                        if keyword.lower() in text.lower():  # Case-insensitive search
                            has_keyword = True
                            if text not in filtered_texts:
                                filtered_boxes.append(box)
                                filtered_texts.append(text)
                                filtered_scores.append(score)
        
        if has_keyword:
            # Draw filtered OCR results on the image
            for box in filtered_boxes:
                # Convert the box points to integers
                points = np.array(box, dtype=np.int32)
                # Draw the polygon
                cv2.polylines(frame, [points], isClosed=True, color=(0, 0, 255), thickness=2)
            # image_with_boxes = draw_ocr(frame, filtered_boxes, filtered_texts, filtered_scores, font_path=self.font_path)

            # Save the image
            with Processed_Screenshot.lock:
                Processed_Screenshot.frames[Processed_Screenshot.index % 20] = frame
            
            self.send_message((f"[{datetime.now().replace(microsecond=0)}] Alert: {filtered_texts} has been detected.", Processed_Screenshot.index % 20))
            Processed_Screenshot.index += 1
        
        return has_keyword

    '''
        Iterates through the frames that were captured previously and runs the OCR.
    '''
    def run(self):
        while Thread_Config.running:
            time.sleep(3)
            keywords = ConfigHandler.get_list("Settings", "keywords")
            try:
                for frame in Screenshot.frames:
                    # Check if the frame is new
                    processed = frame.get('processed')
                    if not processed:
                        # Convert the frame to RGB
                        screenshot = frame.get('current')
                        frame_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

                        # Perform the OCR
                        has_keyword = self.perform_ocr(frame_rgb, keywords)

                        # Set to show that the frame has been processed
                        with Screenshot.lock:
                            frame['processed'] = True

                        if not has_keyword:
                            print("No keywords Found.")
                    else:
                        Screenshot.frames.remove(frame)
            except Exception as e:
                print(f"OCR has encountered the exception: {e}")
            finally:
                pass
        print("OCR Processor has ended.")