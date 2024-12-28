import imageio.v3 as iio
import matplotlib.pyplot as plt

# Try to use '/dev/video0' on Linux or 'video=0' on Windows or macOS
device_path = 'video=0'  # Adjust for your system (Linux path example)

# Create a reader for the video device
try:
    generator = next(iio.imiter(video=0, plugin="ffmpeg"))
    
    # Display the frame using matplotlib
    plt.imshow(generator)
    plt.axis('off')  # Turn off axis
    plt.show()

except Exception as e:
    print(f"Error capturing frame: {e}")
