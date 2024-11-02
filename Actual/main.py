from screen_capturer import ScreenCapturer

if __name__ == "__main__":
    device_count = 1
    save_folder = "./screenshots"
    ss_object = ScreenCapturer(save_folder, device_count)
    ss_object.update_available_devices()
    ss_object.capture_screenshots()