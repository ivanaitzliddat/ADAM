import easyocr
import matplotlib.pyplot as plt
import cv2
import time  # Import time module to measure runtime

class OCRProcessor:
    def __init__(self, lang='en', font_path=None):
        # Initialize EasyOCR reader
        self.reader = easyocr.Reader([lang])  # Use the desired language (e.g., 'en' for English)
        self.font_path = font_path

    def perform_ocr(self, frame):
        print("Performing OCR...")
        start_time = time.time()  # Start timing the OCR process
        result = self.reader.readtext(frame)
        end_time = time.time()  # End timing the OCR process
        
        # Calculate the time taken for OCR
        ocr_runtime = end_time - start_time
        print(f"OCR Runtime: {ocr_runtime:.4f} seconds")  # Display runtime

        return result, ocr_runtime

    def display_ocr_results(self, frame, filtered_results):
        # Draw the filtered OCR results on the image
        for (bbox, text, score) in filtered_results:
            top_left = tuple(bbox[0])
            bottom_right = tuple(bbox[2])
            
            # Draw bounding box around the text
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            # Put the text on the image
            cv2.putText(frame, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Display the image
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

    def run(self):
        image_path = './screenshots/screenshot.png'
        image = cv2.imread(image_path)
        print("Completed image reading!")
        
        # Perform OCR and filter results by keyword
        ocr_results, ocr_runtime = self.perform_ocr(image)
        
        # Filter the results by keyword "monitor"
        keyword = "monitor"
        filtered_results = []
        for (bbox, text, score) in ocr_results:
            if keyword.lower() in text.lower():  # Case-insensitive check
                filtered_results.append((bbox, text, score))
                print(f"Detected text containing keyword '{keyword}': {text}")  # Print the filtered text
        
        if not filtered_results:
            print(f"No results with the keyword '{keyword}'.")
        else:
            print(f"Found {len(filtered_results)} results with the keyword '{keyword}'.")
            print("Displaying OCR Result...")
            self.display_ocr_results(image, filtered_results)

if __name__ == "__main__":
    ocr = OCRProcessor()
    ocr.run()
