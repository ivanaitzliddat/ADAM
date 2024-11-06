import pytesseract
import cv2
import matplotlib.pyplot as plt
import time

# Set the path to Tesseract executable if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRProcessor:
    def __init__(self, lang='eng'):
        self.lang = lang

    def perform_ocr(self, frame, keyword):
        print("Performing OCR...")
        start_time = time.time()  # Start timing the OCR process

        # Use pytesseract to get detailed OCR data
        data = pytesseract.image_to_data(frame, lang=self.lang, output_type=pytesseract.Output.DICT)
        
        end_time = time.time()  # End timing the OCR process
        ocr_runtime = end_time - start_time
        print(f"OCR Runtime: {ocr_runtime:.4f} seconds")

        # Combine words into sentences if they are in proximity to each other
        keyword_results = []
        current_sentence = ""
        sentence_boxes = []
        
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 0:  # Only consider words with a confidence greater than 0
                word = data['text'][i]
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                
                # Add word to the current sentence
                current_sentence += word + " "
                sentence_boxes.append((x, y, w, h))

                # If we reach the end of a line, process the sentence
                if data['line_num'][i] != data['line_num'][i + 1] if i + 1 < len(data['text']) else True:
                    if keyword.lower() in current_sentence.lower():
                        print(f"Detected sentence containing '{keyword}': {current_sentence.strip()}")
                        keyword_results.append((current_sentence.strip(), sentence_boxes[:]))  # Save sentence and boxes
                    current_sentence = ""
                    sentence_boxes = []
        
        return keyword_results

    def display_ocr_results(self, frame, keyword_results):
        # Draw boxes around sentences containing the keyword
        for sentence, boxes in keyword_results:
            for (x, y, w, h) in boxes:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the image
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

    def run(self, image_path, keyword):
        start_time = time.time()  # Start overall timing
        image = cv2.imread(image_path)
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print("Completed frame conversion!")

        # Perform OCR and get sentences containing the keyword
        ocr_results = self.perform_ocr(frame_rgb, keyword)
        
        # Display results if there are any sentences with the keyword
        if ocr_results:
            print("Displaying OCR Result...")
            self.display_ocr_results(image, ocr_results)
        else:
            print("No Text Found.")

        end_time = time.time()  # End overall timing
        total_runtime = end_time - start_time
        print(f"Total Runtime: {total_runtime:.4f} seconds")

if __name__ == "__main__":
    ocr_processor = OCRProcessor()
    ocr_processor.run('./screenshots/screenshot.png', 'monitor')
