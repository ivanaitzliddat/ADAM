import subprocess
import cv2

def get_usb_video_devices():
    # Run the 'wmic' command to list all USB devices that are of type 'video capture'
    result = subprocess.run(['wmic', 'path', 'Win32_PnPEntity', 'where', "Name like '%camera%' or Name like '%Display capture%'"], 
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
    
    return len(video_devices) - 1   # Subtract 1 to exclude the header line

# Call the function and print the result
usb_video_ports = get_usb_video_devices()
print(f"Total USB cameras or video capture devices plugged in: {usb_video_ports}")