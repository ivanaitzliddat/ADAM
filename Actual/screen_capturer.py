import time
import cv2
import threading
import subprocess
import imageio.v3 as iio
from subthread_config import Thread_Config
from screenshots import Screenshot
from messages import MessageQueue
from imageio.plugins.deviceslist import DevicesList

'''
    Represents a screen capturer that checks the current availability of the capture cards and takes screenshots when called.
'''
class ScreenCapturer:
    available_devices = []
    lock = threading.Lock()

    '''
        Iterates through the list of available devices and captures a screenshot for every device and saves it in a folder.
    '''
    def capture_screenshots(self):

        while Thread_Config.running:
            time.sleep(3)
            i = 0
            num_of_devices = len(DevicesList.device_list)

            if num_of_devices == 0:
                print("The number of devices is 0.")
                try:
                    generator = next(iio.imiter(f"<video{i}>"))
                    num_of_devices = len(DevicesList.device_list)
                    print("Ran the imiter once and the generator the new number of devices is", num_of_devices)
                except Exception as e:
                    print(f"Unable to identify any video inputs. Exited with error: {e}")

            while i < num_of_devices:
                if not Thread_Config.running:
                    break

                try:
                    generator = next(iio.imiter(f"<video{i}>"))
                    alt_name = DevicesList.device_list[i]
                    frame = {
                                'current': generator,
                                'processed': False,
                                'alt_name': alt_name
                            }
                    with Screenshot.lock:
                        Screenshot.frames.append(frame)
                        print("Successfully appended a frame.")
                        print("The current number of screenshots is", len(Screenshot.frames))

                    i += 1

                except Exception as e:
                    print(f"Capture Screenshot has failed with error: {e}")

    '''
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        with MessageQueue.lock:
            MessageQueue.status_queue.put(message)