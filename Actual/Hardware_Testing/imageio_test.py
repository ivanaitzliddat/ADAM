import imageio.v3 as iio
import numpy as np
import matplotlib.pyplot as plt
import time
import psutil

'''for idx, frame in enumerate(iio.imiter("<video0>")):
    print(f"Frame {idx}: avg. color {np.sum(frame, axis=-1)}")
    iio.imwrite("output.png", frame)
    plt.imshow(frame)
    plt.axis('off')
    plt.show()
    break'''
screenshots = []
while True:
    for i in range(20):
        try:
            generator = next(iio.imiter(f"<video{i}>"))
            screenshots.append(generator)
            process = psutil.Process()
            print(process.memory_info().rss/1024/1024)
            if len(screenshots) > 10:
                screenshots.clear()
        except Exception as e:
            print(f"{i} is not in range")
