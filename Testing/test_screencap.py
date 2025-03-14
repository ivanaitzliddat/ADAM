import time
import imageio.v3 as iio
import numpy as np

'''
This script deals with the following issues:
1) Incomplete frame capture (a portion shows the screen while the rest is green).
When frame is incomplete, the subsequent frames are will be the same. This continues till
a "No signal detected" black frame is captured. Maybe because imageio needs time to "start up",
the frames are incomplete/frozen at the beginning, and only capturing normally after the black frame.
- Not 100% sure if its an imageio issue or due to capture card specs.

2) Black screen detection.
Useful when no input is going into a Capture Card, as the screen will be black. Also useful to detect the
"No signal detected" black frame when Capture Card is still prepping, or maybe if it hanged.

'''

black_pixel_percentage = 0.95  # Define the percentage of black pixels needed to classify the frame as mostly black
iio_prep_end = time.time() + 2.5    # Let imageio prep for 2.5s from current time.

for index, frame in enumerate(iio.imiter("<video0>")):
    # Skip iterations until iio_prep_end is reached
    if time.time() < iio_prep_end:
        continue

    print(f"Frame{index}")

    ### BLACK SCREEN DETECTION ###
    # Sum the RGB values for each pixel (resulting in a 2D array of sums)
    frame_colour_sum = np.sum(frame, axis=-1)  # Sum over the last axis in the Shape frame, which is the colour channel (R, G, B)
    
    # Identify pure black pixels (where RGB sum is exactly 0)
    black_pixels = frame_colour_sum == 0  # True if the pixel is exactly black
    black_pixel_count = np.sum(black_pixels)  # Count the number of black pixels
    
    # Calculate the total number of pixels in the frame
    total_pixels = frame.shape[0] * frame.shape[1]  # Height * Width
    
    # Calculate the percentage of black pixels
    black_pixel_ratio = black_pixel_count / total_pixels

    # Check if the majority of the frame is black
    if black_pixel_ratio > black_pixel_percentage:
        # Change this to handle the black screen       
        print("Black frame detected!!")
        print(f"Frame {index}: black pixel ratio = {black_pixel_ratio:.4f}")

    ### END OF BLACK SCREEN DETECTION ###
    
    
