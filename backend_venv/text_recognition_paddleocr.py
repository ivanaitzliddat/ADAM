import os
from paddleocr import PaddleOCR

# Initialize the PaddleOCR reader (English as the default language)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Path to the folder containing the images
screenshots_folder = "screenshots/"
if not os.path.exists(screenshots_folder): 
    # if the screenshots_folder directory is not present  
    # then create it. 
    os.makedirs(screenshots_folder)


# List of keywords to search for
keywords = ["alert", "keyword1", "keyword2"]  # Replace with your specific keywords

# Function to check for keywords in the OCR result
def check_for_keywords(text, keywords):
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return True
    return False

# Loop through all the files in the screenshots folder
for filename in os.listdir(screenshots_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # Ensure it's an image file
        image_path = os.path.join(screenshots_folder, filename)
        
        # Perform OCR on the image
        result = ocr.ocr(image_path)
        print(result)
        # Extract text from OCR results
        # detected_text = ' '.join([item[1][0] for line in result for item in line])
        
        # Check if any of the keywords are found
        # if check_for_keywords(detected_text, keywords):
        #     print(f"Alert: Keyword found in {filename}")
        # else:
        #     print(f"No keyword found in {filename}")
