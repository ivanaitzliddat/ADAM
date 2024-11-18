from paddleocr import PaddleOCR
import numpy as np

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Perform OCR on the image
image_path = 'C:/Users/kairo/Documents/ADAM/screenshots/H.jpg'
result = ocr.ocr(image_path, cls=True)

# Process the result to extract text and bounding boxes
lines = []
for line in result[0]:  # Assuming result[0] contains the line-by-line detections
    text = line[1][0]  # The detected text
    box = line[0]  # The bounding box coordinates
    lines.append((box, text))

# Sort lines by the top y-coordinate of the bounding box
lines.sort(key=lambda x: min(y for _, y in x[0]))

# Group lines into paragraphs based on vertical distance
paragraphs = []
current_paragraph = [lines[0][1]]  # Start with the first line text
line_spacing_threshold = 15  # Adjust this threshold as needed

for i in range(1, len(lines)):
    prev_box = lines[i - 1][0]
    curr_box = lines[i][0]
    # Calculate the vertical distance between current line and the previous line
    vertical_distance = min(y for _, y in curr_box) - max(y for _, y in prev_box)
    
    # If lines are close enough vertically, treat them as the same paragraph
    if vertical_distance < line_spacing_threshold:
        current_paragraph.append(lines[i][1])
    else:
        # Otherwise, start a new paragraph
        paragraphs.append(" ".join(current_paragraph))
        current_paragraph = [lines[i][1]]

# Append the last paragraph
if current_paragraph:
    paragraphs.append(" ".join(current_paragraph))

# Output the paragraphs
for idx, paragraph in enumerate(paragraphs):
    print(f"Paragraph {idx + 1}:\n{paragraph}\n")
