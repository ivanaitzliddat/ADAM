import cv2
'''
    Represents a screen capturer that checks the current availability of the capture cards and takes screenshots when called.
'''
class ScreenCapturer:

    def __init__(self, save_folder, device_count):
        self.save_folder = save_folder
        self.device_count = device_count
    
    '''
        Returns the list of available devices.
        Uses the number of available devices and checks if the capture card is recognised. If it is recognised, the device's index is appended to the available_devices array.

        @param save_folder The file path of the folder where screenshots are saved to.
        @param device_count The number of capture cards connected to the computer.
        @return the list of available devices.
    '''
    def get_available_devices(self):
        available_devices = []
        for i in range(self.device_count):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_devices.append(i)
                cap.release()
        return available_devices