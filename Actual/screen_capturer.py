import time, threading, traceback
import imageio.v3 as iio
import numpy as np
from subthread_config import Thread_Config
from screenshots import Screenshot
from messages import MessageQueue
from imageio.plugins.deviceslist import DevicesList
from config_handler import ConfigHandler

'''
    Represents a screen capturer that checks the current availability of the capture cards and takes screenshots when called.
'''
class ScreenCapturer:

    '''
        Calls iio.imiter once by passing video0 so as to populate DevicesList.device_list.
    '''
    def get_devices():
        try:
            generator = next(iio.imiter(f"<video0>"))
        except Exception as e:
            print(f"Unable to identify any video inputs. Exited with error: {e}")

    '''
        Iterates through the list of available devices and captures a screenshot for every device and saves it in a folder.
    '''
    def capture_screenshots(self):

        iteration = 0

        while Thread_Config.running:
            time.sleep(3)
            ScreenCapturer.get_devices()

            if ConfigHandler.get_cfg_input_devices(usb_alt_name = ""):
                ConfigHandler.del_input_device(usb_alt_name = "")
                print("Successfully deleted input device")

            for device in DevicesList.device_list:
                if(len(ConfigHandler.get_cfg_input_devices(usb_alt_name = device)) == 0): # does not exist in config.ini, need to add device
                    with ConfigHandler.lock:
                        default_custom_name = "Input Device " + str(len(DevicesList.device_list) - 1)
                        default_condition_name = "Default Condition Name " + str(len(DevicesList.device_list) - 1)
                        ConfigHandler.add_input_device(usb_alt_name=device)
                        ConfigHandler.set_cfg_input_device(usb_alt_name=device, custom_name=default_custom_name)
                        ConfigHandler.set_cfg_input_device(usb_alt_name=device, condition = "cond0", condition_name = default_condition_name)
                        ConfigHandler.save_config()

            retry_counter = 0
            i = 0
            while i < len(DevicesList.device_list):
                if not Thread_Config.running:
                    break
                
                generator = None
                is_black = False
                try:
                    alt_name = DevicesList.device_list[i]

                    # Check if the Input Device in DevicesList.device_list[i] is set to disabled in config file.
                    if ConfigHandler.get_cfg_disabled_input_devices(usb_alt_name = alt_name):
                        # Define the pixel size of the square
                        square_size = 300
                        # Create a black square in RGB (shape: height x width x 3)
                        black_square = np.zeros((square_size, square_size, 3), dtype=np.uint8)
                        # Set generator to black_square
                        generator = black_square
                        is_black = True
                    else:
                        # Set generator to the captured frame in <video{i}>
                        generator = next(iio.imiter(f"<video{i}>"))
                    
                    if not is_black:
                        frame_colour_sum = np.sum(generator, axis=-1)  # Sum over the last axis in the Shape frame, which is the colour channel (R, G, B)
 
                        # Identify pure black pixels (where RGB sum is exactly 0)
                        black_pixels = frame_colour_sum == 0  # True if the pixel is exactly black
                        black_pixel_count = np.sum(black_pixels)  # Count the number of black pixels

                        # Calculate the total number of pixels in the frame
                        total_pixels = generator.shape[0] * generator.shape[1]  # Height * Width
                        
                        # Calculate the percentage of black pixels
                        black_pixel_ratio = black_pixel_count / total_pixels

                        # Check if the majority of the frame is black
                        if black_pixel_ratio > 0.95:
                            is_black = True
                    frame = {
                                'current': generator,
                                'processed': False,
                                'alt_name': alt_name,
                                'is_black': is_black
                            }
                    with Screenshot.lock:
                        for screenshot in Screenshot.frames:
                            if screenshot.get('processed') or screenshot.get('is_black'):
                                Screenshot.frames.remove(screenshot)
                        Screenshot.frames.append(frame)
                        print("The current number of screenshots is", len(Screenshot.frames))

                    retry_counter = 0
                    i += 1

                except IndexError as e:
                    if "No (working) camera at" in str(e):
                        if retry_counter > 2:
                            with ConfigHandler.lock:
                                ConfigHandler.set_cfg_input_device(usb_alt_name=alt_name, device_enabled=False)
                                ConfigHandler.save_config()
                            i += 1
                        else:
                            retry_counter += 1
                    if "list index out of range" in str(e):
                        i += 1

                except Exception:
                    i += 1
                    # traceback.print_exc()
                    print(f"Capture Screenshot has failed.")

            iteration += 1

    '''
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        with MessageQueue.lock:
            MessageQueue.status_queue.put(message)
