import time
import matplotlib.pyplot as plt
import cv2
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
        if None in result:
            print("No words were detected")
        else:
            for line in result:
                for box, (text, score) in line:
                    for keyword in keywords:
                        # print(keyword)
                        if keyword.lower() in text.lower():  # Case-insensitive search
                            has_keyword = True
                            filtered_boxes.append(box)
                            filtered_texts.append(text)
                            filtered_scores.append(score)
        
        if has_keyword:
            # Draw filtered OCR results on the image
            image_with_boxes = draw_ocr(frame, filtered_boxes, filtered_texts, filtered_scores, font_path=self.font_path)

            '''# Display the image
            plt.imshow(image_with_boxes)
            plt.axis('off')
            plt.show()'''

            # Save the image
            with Processed_Screenshot.lock:
                Processed_Screenshot.frames.append(image_with_boxes)
        
            self.send_message(f"Detected text: {keywords} (Confidence: {score:.2f}). Screenshot saved in index {Processed_Screenshot.index}")
            if Processed_Screenshot.index < 19:
                Processed_Screenshot.index += 1
            else:
                Processed_Screenshot.index = 0
        
        return has_keyword

    '''
        Iterates through the frames that were captured previously and runs the OCR.
    '''
    def run(self):
        while Thread_Config.running:
            # print("Running OCR...")
            time.sleep(3)
            keywords = ConfigHandler.get_keywords()
            print(keywords)
            try:
                for frame in Screenshot.frames:
                    # Check if the frame is new
                    processed = frame.get('processed')
                    if not processed:
                        
                        # Convert the frame to RGB
                        screenshot = frame.get('current')
                        frame_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
                        print("Completed frame conversion!")

                        # Perform the OCR
                        has_keyword = self.perform_ocr(frame_rgb, keywords)
                        print("Completed OCR!")

                        # Set to show that the frame has been processed
                        with Screenshot.lock:
                            frame['processed'] = True

                        if not has_keyword:
                            print("No keywords Found.")
            except Exception as e:
                print(f"OCR has encountered the exception: {e}")
            finally:
                pass
        print("OCR Processor has ended.")