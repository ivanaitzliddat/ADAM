import cv2
from paddleocr import PaddleOCR, draw_ocr

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Load image
image_path = './screenshots/screenshot4.png'
image = cv2.imread(image_path)

# Run OCR
results = ocr.ocr(image_path)

# Extract detection results
for detection in results[0]:
    text = detection[1][0]
    confidence = detection[1][1]
    bbox = detection[0]
    print(f"Detected text: {text}, Confidence: {confidence}, Bounding box: {bbox}")

    # Draw bounding boxes on the image
    for point in bbox:
        cv2.circle(image, (int(point[0]), int(point[1])), 5, (0, 255, 0), -1)

# Show the image with bounding boxes
cv2.imshow("Detected Text Regions", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
