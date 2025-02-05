import subprocess
import imageio_ffmpeg as ffmpeg
import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio
from imageio.plugins.ffmpeg import parse_device_names

def list_devices():
    try:
        # Path to the bundled FFmpeg executable within imageio_ffmpeg
        ffmpeg_executable = ffmpeg.get_ffmpeg_exe()

        # Run the FFmpeg command to list devices (stderr contains the list)
        result = subprocess.run(
            [ffmpeg_executable, '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # Get the device information from stderr
        devices_info = result.stderr
        print(devices_info)  # Optional: print the full list of devices

        # Extract video devices
        video_devices = []
        in_video_section = False

        for line in devices_info.splitlines():
            if "DirectShow video devices" in line:
                in_video_section = True
            elif in_video_section and '"' in line:
                device_name = line.split('"')[1]
                video_devices.append(device_name)

        return {"video_devices": video_devices}

    except Exception as e:
        print(f"Error listing devices: {e}")
        return {}

ffmpeg_api = ffmpeg
cmd = [
    ffmpeg_api.get_ffmpeg_exe(),
        "-list_devices",
        "true",
        "-f",
        "dshow",
        "-i",
        "dummy",
    ]
completed_process = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    encoding="utf-8",
                    shell=True,
                    check=False,
                )
name = parse_device_names(completed_process.stderr)[0]
print(name)

def capture_frame(device_name, output_file):
    # try:
        # Ensure that the device name is correctly quoted
        # device_name = f'"{device_name}"'  # Wrap in quotes if there are spaces or special chars
        # device_name = "@device_pnp_\\\\?\\usb#vid_1de1&pid_f104&mi_00#8&128c45c9&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\\global"
        # print("\nThe device_name type is: ", type(device_name))
        # print("\n The device_name is as shown below:\n", device_name)

        # # Use the device name to create the input stream URL
        # input_url = "dshow://video=" + device_name
        # print("\n The input_url is as shown below:\n", input_url)
        
    # Specify the device by index
    device_index = 40  # Use 0 or 1 based on your test results
    device_name = f"video={device_index}"

    reader = ffmpeg.read_frames(device_name, input_params=['-f', 'dshow'])

        # # Open the video stream and read frames
        # reader = ffmpeg.read_frames(input_url)

        # # Capture a single frame
        # frame = next(reader)
        
        # Display the frame using Matplotlib
        # plt.imshow(frame)
        # plt.axis('off')  # Hide the axis
        # plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
        # print(f"Frame captured and saved to {output_file}")
    
    # except Exception as e:
    #     print(f"\nError capturing frame: {e}")

'''# Example usage
devices = list_devices()
# print("Video Devices:", devices["video_devices"])

# if devices["video_devices"]:
#     device_name = devices["video_devices"][1]  # Select the first video device
#     capture_frame(device_name, "output_frame.png")

device_index = 0  # Use 0 or 1 based on your test results
device_name_num = f"video={device_index}"

device_name = "Display capture-UVC0"

reader = ffmpeg.read_frames(device_name, input_params=['-f', 'dshow'])
frame = next(reader)

# import imageio
# import matplotlib.pyplot as plt
# devices = list_devices()
# print("Video Devices:", devices["video_devices"])
# reader = imageio.get_reader("<video2>")
'''