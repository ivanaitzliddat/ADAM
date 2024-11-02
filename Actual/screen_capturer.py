import cv2

'''
    Represents a screen capturer that checks the current availability of the capture cards and takes screenshots when called.
'''
class ScreenCapturer:

    def __init__(self, save_folder, device_count):
        self.save_folder = save_folder
        self.device_count = device_count
        self.available_devices = []
    
    '''
        Updates the list of available devices by checking if the capture cards are recognised. If it is recognised, the device's index is appended to the available_devices array.
    '''
    def update_available_devices(self):
        for i in range(self.device_count):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.available_devices.append(i)
                cap.release()
    
    '''
        Iterates through the list of available devices and captures a screenshot for every device and saves it in a folder.

        @param device_index The index of the device which the screenshot will be taken.
    '''
    def capture_screenshots(self):

        while True:
            for i in self.available_devices:
                # Open the video feed from the USB capture card
                cap = cv2.VideoCapture(i)

                if not cap.isOpened():
                    print(f"Error: Could not open device {i}")
                    return

                # Capture one frame
                ret, frame = cap.read()
                
                if ret:
                    # Save the frame as an image
                    cv2.imwrite(self.save_path, frame)
                    print(f"Screenshot saved from device {i} to {self.save_path}")
                else:
                    print(f"Error: Could not capture frame from device {i}")

                # Release the video capture object
                cap.release()