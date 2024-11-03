from screen_capturer import ScreenCapturer
from gui import ADAM

if __name__ == "__main__":
    device_count = 1
    save_folder = "./screenshots"
    app = ADAM()
    app.run()
    ss_object = ScreenCapturer(save_folder, device_count)
    ss_object.update_available_devices()
    ss_object.capture_screenshots()