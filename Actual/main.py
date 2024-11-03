from screen_capturer import ScreenCapturer
from gui import ADAM
from config import Config
import threading

device_count = 0

'''
    Updates the global variable device_count.
'''
def update_device_count(new_count):
    global device_count
    device_count = new_count

'''
    Starts the screen capturer.
'''
def start_screen_capturer(save_folder):
    ss_object = ScreenCapturer(save_folder, device_count)
    ss_object.update_available_devices()
    try:
        ss_object.capture_screenshots()
    except Exception as e:
        print(f"Screen capturer encountered an error: {e}")

'''
    Starts the ADAM GUI application.
'''
def run_ADAM(update_callback):
    app = ADAM(update_callback)
    try:
        app.run()
    except Exception as e:
        print(f"ADAM GUI application encountered an error: {e}")

'''
    Handles the signals that are sent to the script, for example, when pressing the ctrl + c button.
'''
def signal_handler(sig, frame):
    Config.running = False
    print("Gracefully shutting down...")

if __name__ == "__main__":
    save_folder = "./screenshots"

    # Start the GUI thread
    gui_thread = threading.Thread(target=run_ADAM, args=(update_device_count,))
    gui_thread.start()

    # Start the screen capturer thread
    screen_capturer_thread = threading.Thread(target=start_screen_capturer, args=(save_folder,))
    screen_capturer_thread.start()

    # Wait for the GUI thread to finish
    gui_thread.join()

    # Stop the screen capturer if the GUI is closed
    Config.running = False

    # Wait for the screen capturer to finish
    screen_capturer_thread.join()

    print("Thank you for using ADAM!")