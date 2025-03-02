import time
import threading
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
        Calls iio.imiter once by passing video0 so as to populate DevicesList.device_list.
    '''
    def get_num_of_devices():
        try:
            generator = next(iio.imiter(f"<video0>"))
        except Exception as e:
            print(f"Unable to identify any video inputs. Exited with error: {e}")
        print("Managed to populate the first DevicesList.device_list")
        return len(DevicesList.device_list)

    '''
        Iterates through the list of available devices and captures a screenshot for every device and saves it in a folder.
    '''
    def capture_screenshots(self):

        iteration = 0
        while Thread_Config.running:
            time.sleep(3)
            print(f"Going for iteration number {iteration}")
            i = 0
            num_of_devices = len(DevicesList.device_list)

            if num_of_devices == 0:
                num_of_devices = ScreenCapturer.get_num_of_devices()

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
            iteration += 1

    '''
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        with MessageQueue.lock:
            MessageQueue.status_queue.put(message)