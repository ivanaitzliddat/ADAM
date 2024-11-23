import time
from paddleocr import PaddleOCR, draw_ocr
from screenshots import Screenshot
from subthread_config import Thread_Config
import matplotlib.pyplot as plt
import cv2

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
        Performs OCR on a given frame.

        Parameters:
        - frame (np.ndarray): The frame to perform OCR on, in RGB format.

        Returns:
        - result (list): OCR results, each containing bounding boxes, text, and confidence scores.
    '''
    def perform_ocr(self, frame):
        print("Performing OCR...")
        result = self.ocr.ocr(frame, cls=True)

        keyword = "monitor"
        # Display OCR results that contain the keyword "monitor"
        if None in result:
            print("No words were detected")
        else:
            for line in result:
                for box, (text, score) in line:
                    if keyword.lower() in text.lower():  # Case-insensitive search
                        print(f"Detected text: {text} (Confidence: {score:.2f})")

        return result

    '''
        Displays OCR results on the frame.

        Parameters:
        - frame (np.ndarray): The original frame in RGB format.
        - result (list): OCR results from perform_ocr.
    '''
    def display_ocr_results(self, frame, result):
        keyword = "monitor"
        # Filter the results to include only texts containing the keyword
        filtered_boxes = []
        filtered_texts = []
        filtered_scores = []

        for line in result:
            for box, (text, score) in line:
                if keyword.lower() in text.lower():  # Case-insensitive search
                    filtered_boxes.append(box)
                    filtered_texts.append(text)
                    filtered_scores.append(score)

        # Draw filtered OCR results on the image
        image_with_boxes = draw_ocr(frame, filtered_boxes, filtered_texts, filtered_scores, font_path=self.font_path)

        # Display the image
        plt.imshow(image_with_boxes)
        plt.axis('off')
        plt.show()

    '''
        Iterates through the frames that were captured previously and runs the OCR.
    '''
    def run(self):
        while Thread_Config.running:
            # print("Running OCR...")
            time.sleep(3)
            try:
                for frame in Screenshot.frames:
                    # Check if the frame is new
                    processed = Screenshot.frames.get(frame).get('processed')
                    if not processed:
                        
                        # Convert the frame to RGB
                        screenshot = Screenshot.frames.get(frame).get('current')
                        frame_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
                        print("Completed frame conversion!")

                        # Perform the OCR
                        ocr_results = self.perform_ocr(frame_rgb)
                        print("Completed OCR!")

                        # Set to show that the frame has been processed
                        with Screenshot.lock:
                            Screenshot.frames[frame]['processed'] = True

                        if None in ocr_results:
                            print("No Text Found.")
                        else:
                            print("Displaying OCR Result...")
                            self.display_ocr_results(Screenshot.frames.get(frame).get('current'), ocr_results)
            finally:
                pass
        print("OCR Processor has ended.")