import subprocess
import imageio.v3 as iio
import numpy as np
import matplotlib.pyplot as plt
import time
import psutil
import os

def get_usb_video_devices():
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

def getCurrentMemUsage(processName):
    """Get memory usage of all processes with the specified name (default "ADAM")"""
    process_name=processName
    total_memory = 0
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                total_memory += proc.info['memory_info'].rss  # in bytes
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return total_memory / (1024 ** 2)  # Convert to MB

def getCurentProcessName():
    pid = os.getpid()

    # Get the process info using psutil
    process = psutil.Process(pid)

    # Get the process name
    process_name = process.name()
    # print(f"Current process name: {process_name}")

    return process_name

def manage_memory_usage(currentMemUsage,currentScreenshotMemUsage):
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
            print(f"Screenshot removed. Current total memory usage by ADAM: {currentMemUsage} MB")
            return False
    else:
        return False

def captureSS(number_of_devices):
    screenshots = []
    
    while True:
        currentMemUsage = getCurrentMemUsage(getCurentProcessName())

        for i in range(number_of_devices):
            try:
                generator = next(iio.imiter(f"<video{i}>"))
                #process = psutil.Process()
                #print(process.memory_info().rss/1024/1024)
                screenshot_memory_usage = sum([screenshot.nbytes for screenshot in screenshots]) / (1024 ** 2)  # In MB
                #print(screenshot_memory_usage)
                if not manage_memory_usage(currentMemUsage,screenshot_memory_usage):
                    print("Memory limit exceeded, deleting oldest screenshot...")
                    screenshots.pop(0)
                else:
                    screenshots.append(generator)

            except Exception as e:
                print(f"{i} is not in range")

# Call the function to get the number of USB video devices
number_of_devices = get_usb_video_devices()
print(number_of_devices)
captureSS(number_of_devices)
