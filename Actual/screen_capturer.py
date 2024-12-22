import time
import cv2
import threading
import subprocess
import psutil
import os
import imageio.v3 as iio
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

    def get_usb_video_devices_new():
        try:
            # Use PowerShell command to list USB video devices (trying to filter as much as possible to reduce iterations)
            ps_command = """ 
            Get-PnpDevice | Where-Object { 
                ($_.Class -like '*Camera*' -or 
                $_.Class -like '*Video*' -or 
                $_.Class -like '*Media*' -or 
                $_.Name -match 'camera|capture|video') -and 
                $_.Status -eq 'OK' -and 
                $_.Class -notlike '*Audio*' -and 
                $_.Name -notmatch 'audio' -and
                $_.InstanceID -like '*USB*'
            }
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check if the command was successful and list the filtered devices
            if result.returncode == 0:
                print(f"Raw PowerShell Output:{result.stdout}")
                # Split by newline and filter out any empty or non-device lines
                devices = [line for line in result.stdout.strip().split('\n') if line.strip() and 'usb' in line.lower()]
                print(f"Number of Valid USB Video Devices: {len(devices)}")
                # Return the number of valid devices
                return len(devices)
            else:
                print(f"Error running PowerShell command:{result.stderr}")
            
        except Exception as e:
            print(f"An error occurred: {e}")

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

    def getCurrentMemUsage(self, processName):
        # Get memory usage of all processes with the specified name (default "ADAM")
        process_name=processName
        total_memory = 0
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    total_memory += proc.info['memory_info'].rss  # in bytes
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return total_memory / (1024 ** 2)  # Convert to MB

    def getCurentProcessName(self):
        pid = os.getpid()

        # Get the process info using psutil
        process = psutil.Process(pid)

        # Get the process name
        process_name = process.name()
        # print(f"Current process name: {process_name}")

        return process_name

    def manage_memory_usage(self, currentMemUsage,currentScreenshotMemUsage):
        max_ADAM_mem_usage = float(1536) #1.5GB
        max_screenshot_mem = float(600) #600MB
        # print(currentScreenshotMemUsage)

        # ADAM's total memory usage is under 1.5GB
        if currentMemUsage < max_ADAM_mem_usage:
            print(f"ADAM memory usage: {currentMemUsage / (1024 ** 2)} MB")  # Convert to MB
            if currentScreenshotMemUsage < max_screenshot_mem:
                # Screenshots in memory are less than 600MB, safe to add more
                return True
            else:
                # Screenshots in memory exceed 600MB, remove oldest screenshot
                return False
        else:
            return False

    '''
        Iterates through the list of available devices and captures a screenshot for every device and saves it in a folder.
    '''
    def capture_screenshots(self):

        while Thread_Config.running:
            # print(len(Screenshot.frames))
            time.sleep(3)
            self.update_available_devices()

            for i in self.available_devices:
                # Check if ADAM GUI application is still running
                if not Thread_Config.running:
                    break

                try:
                    generator = next(iio.imiter(f"<video{i}>"))
                    # Check the current memory usage
                    currentMemUsage = self.getCurrentMemUsage(self.getCurentProcessName())
                    # Check the current screenshots memory usage
                    screenshot_memory_usage = sum([screenshot.get('current').nbytes for screenshot in Screenshot.frames]) / (1024 ** 2)
                    frame = {
                                'current': generator,
                                'processed': False
                            }
                    if not self.manage_memory_usage(currentMemUsage,screenshot_memory_usage):
                        print("Memory limit exceeded, deleting oldest screenshot...")
                        with Screenshot.lock:
                            Screenshot.frames.pop(0)
                        print(f"Screenshot removed. Current total memory usage by ADAM: {self.getCurrentMemUsage(self.getCurentProcessName())} MB")
                    with Screenshot.lock:
                        Screenshot.frames.append(frame)

                except Exception as e:
                    print(f"Capture Screenshot has failed with error: {e}")

            '''for i in self.available_devices:
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
                cap.release()'''
            
        print("Screencapturer has ended.")