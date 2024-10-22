import cv2
import time

def find_video_devices():
    """Find all available video capture devices."""
    index = 0
    devices = []
    
    while True:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            print(f"Device {index} is available")
            devices.append(index)
        else:
            print(f"Device {index} is not available or does not exist.")
            break
        cap.release()
        index += 1

    if devices:
        print(f"Available devices: {devices}")
    else:
        print("No devices found.")
    
    return devices

def capture_screenshot(device_index, save_path):
    """Capture and save a screenshot from the given device index."""
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

def capture_from_multiple_devices(save_folder):
    """Capture screenshots from all detected devices."""
    devices = find_video_devices()

    for i, device in enumerate(devices):
        save_path = f"{save_folder}/capture_device_{i}.png"
        capture_screenshot(device, save_path)
        # Adding a small delay between captures
        time.sleep(1)

# Usage
save_folder = "./screenshots"  # Folder to save screenshots

capture_from_multiple_devices(save_folder)