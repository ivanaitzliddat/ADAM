import os
import easyocr

# Initialize the EasyOCR reader for English
reader = easyocr.Reader(['en'])

# Path to the folder containing the images
screenshots_folder = "screenshots/"

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
        result = reader.readtext(image_path, detail=0)  # detail=0 for plain text output
        print(result)

        # Join all detected text into a single string
        detected_text = ' '.join(result)
        
        # Check if any of the keywords are found
        if check_for_keywords(detected_text, keywords):
            print(f"Alert: Keyword found in {filename}")
        else:
            print(f"No keyword found in {filename}")
