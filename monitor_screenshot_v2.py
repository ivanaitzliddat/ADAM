import cv2
import time

def capture_screenshot(device_index, save_path):
    # Open the video feed from the USB capture card
    cap = cv2.VideoCapture(device_index)

    if not cap.isOpened():
        print(f"Error: Could not open device {device_index}")
        return

    # Capture one frame
    ret, frame = cap.read()
    
    if ret:
        # Save the frame as an image
        cv2.imwrite(save_path, frame)
        print(f"Screenshot saved from device {device_index} to {save_path}")
    else:
        print(f"Error: Could not capture frame from device {device_index}")

    # Release the video capture object
    cap.release()

def capture_from_multiple_devices(device_count, save_folder):
    for i in range(device_count):
        save_path = f"{save_folder}/capture_device_{i}.png"
        capture_screenshot(i, save_path)
        # Adding a small delay between captures
        time.sleep(1)

# Usage
device_count = 2  # Number of USB capture devices you have
save_folder = "./screenshots"  # Folder to save screenshots

capture_from_multiple_devices(device_count, save_folder)