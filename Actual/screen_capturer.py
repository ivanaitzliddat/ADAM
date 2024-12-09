import time
import cv2
import threading
import subprocess
from subthread_config import Thread_Config
from screenshots import Screenshot
from messages import MessageQueue

'''
    Represents a screen capturer that checks the current availability of the capture cards and takes screenshots when called.
'''
class ScreenCapturer:
    available_devices = []
    lock = threading.Lock()

    '''
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        with MessageQueue.lock:
            MessageQueue.status_queue.put(message)
    
    def get_usb_video_devices():
        # Run the 'wmic' command to list all USB devices that are of type 'video capture'
        result = subprocess.run(['wmic', 'path', 'Win32_PnPEntity', 'where', "(Name like '%camera%' or Name like '%capture%') and (PNPClass like '%camera%')"], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Decode the result and split by lines
        devices = result.stdout.decode().splitlines()
        print(devices)
        
        # The first line is a header, so we skip it
        # The rest are the devices that match the filter
        video_devices = [device for device in devices if device.strip() != '']

        for i in video_devices:
            cap = cv2.VideoCapture(i)

            if not cap.isOpened():
                print(f"Error: Could not open device {i}")

            # Capture one frame
            ret, frame = cap.read()

            if ret:
                image_path = "C:\\Users\\ivana\\Downloads\\image.png"
                cv2.imwrite(image_path)
    
        return len(video_devices) - 1   # Subtract 1 to exclude the header line

    '''
        Updates the list of available devices by checking if the capture cards are recognised. If it is recognised, the device's index is appended to the available_devices array.
    '''
    def update_available_devices(self):
        for i in range(20):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                if i not in ScreenCapturer.available_devices:
                    with ScreenCapturer.lock:
                        ScreenCapturer.available_devices.append(i)
                cap.release()
            else:
                if i in ScreenCapturer.available_devices:
                    self.send_message(f"WARNING: Device {i} is no longer detected!")
                    with ScreenCapturer.lock:
                        ScreenCapturer.available_devices.remove(i)
                    
        # self.send_message(f"Successfully updated number of devices. The devices are:\n{ScreenCapturer.available_devices}")
        return

    '''
        Iterates through the list of available devices and captures a screenshot for every device and saves it in a folder.
    '''
    def capture_screenshots(self):

        while Thread_Config.running:
            time.sleep(3)
            self.update_available_devices()
            for i in self.available_devices:
                # Check if ADAM GUI application is still running
                if not Thread_Config.running:
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
                    with Screenshot.lock:
                        # Store the current frame in RAM
                        Screenshot.frames[i] = {
                            'current': frame,
                            'processed': False
                        }
                        print(f"Screenshot from device {i} added to Screenshot.frames")
                else:
                    message = f"Error: Could not capture frame from device {i}"
                    self.send_message(message)

                # Release the video capture object
                cap.release()
        print("Screencapturer has ended.")