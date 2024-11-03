import cv2
import os
import time
from config import Config

'''
    Represents a screen capturer that checks the current availability of the capture cards and takes screenshots when called.
'''
class ScreenCapturer:

    def __init__(self, save_path, device_count, status_queue):
        self.save_path = save_path
        self.device_count = device_count
        self.available_devices = []
        self.status_queue = status_queue

    '''
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        print(message)
        self.status_queue.put(message)

    '''
        Updates the list of available devices by checking if the capture cards are recognised. If it is recognised, the device's index is appended to the available_devices array.
    '''
    def update_available_devices(self):
        for i in range(self.device_count):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.available_devices.append(i)
                cap.release()
            else:
                message = f"Device {i} is not found."
                self.send_message(message)
                
    
    '''
        Iterates through the list of available devices and captures a screenshot for every device and saves it in a folder.
    '''
    def capture_screenshots(self):

        while Config.running:
            for i in self.available_devices:
                # Check if ADAM GUI application is still running
                if not Config.running:
                    break

                # Open the video feed from the USB capture card
                cap = cv2.VideoCapture(i)

                if not cap.isOpened():
                    message = f"Error: Could not open device {i}"
                    self.send_message(message)
                    continue

                # Capture one frame
                ret, frame = cap.read()
                
                if ret:
                    # Check whether the save_path exists, if not create one
                    if not os.path.exists(self.save_path):
                        os.makedirs(self.save_path)
                    # Save the frame as an image
                    filename = os.path.join(self.save_path, f"screenshot_device_{i}_{int(time.time())}.png")
                    cv2.imwrite(filename, frame)
                    message = f"Screenshot saved from device {i} to {self.save_path}"
                    self.send_message(message)
                else:
                    message = f"Error: Could not capture frame from device {i}"
                    self.send_message(message)

                # Release the video capture object
                cap.release()