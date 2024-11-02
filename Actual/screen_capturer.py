import cv2
'''
    Represents a screen capturer that checks the current availability of the capture cards and takes screenshots when called.
'''
class ScreenCapturer:

    def __init__(self, save_folder, device_count):
        self.save_folder = save_folder
        self.device_count = device_count