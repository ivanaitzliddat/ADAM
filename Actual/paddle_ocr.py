from paddleocr import PaddleOCR, draw_ocr
from screenshots import Screenshot
from config import Config
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
        print(f"Results as shown:\n{result}")
        return result

    '''
        Displays OCR results on the frame.

        Parameters:
        - frame (np.ndarray): The original frame in RGB format.
        - result (list): OCR results from perform_ocr.
    '''
    def display_ocr_results(self, frame, result):
        # Extract bounding boxes, texts, and scores
        boxes = [item[0] for line in result for item in line]
        texts = [item[1][0] for line in result for item in line]
        scores = [item[1][1] for line in result for item in line]

        # Draw results on the image
        image_with_boxes = draw_ocr(frame, boxes, texts, scores, font_path=self.font_path)

        # Display the image
        plt.imshow(image_with_boxes)
        plt.axis('off')
        plt.show()

    '''
        Iterates through the frames that were captured previously and runs the OCR.
    '''
    def run(self):
        while Config.running:
            # print("Running OCR...")
            try:
                for frame in Screenshot.frames:
                    # Convert the frame to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    print("Completed frame conversion!")
                    ocr_results = self.perform_ocr(frame_rgb)
                    print("Compelted OCR!")
                    if None in ocr_results:
                        print("No Text Found.")
                    else:
                        print("Displaying OCR Result...")
                        self.display_ocr_results(frame, ocr_results)
            finally:
                pass
        print("OCR Processor has ended.")