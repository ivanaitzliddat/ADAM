from screen_capturer import ScreenCapturer
from gui import ADAM

device_count = 0

'''
    Updates the global variable device_count.
'''
def update_device_count(new_count):
    global device_count
    device_count = new_count

if __name__ == "__main__":
    save_folder = "./screenshots"

    # Create the ADAM GUI application
    app = ADAM(update_device_count)
    app.run()

    # Start the screen capturer
    ss_object = ScreenCapturer(save_folder, device_count)
    ss_object.update_available_devices()
    ss_object.capture_screenshots()