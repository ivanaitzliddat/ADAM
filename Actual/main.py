from screen_capturer import ScreenCapturer
from paddle_ocr import OCRProcessor
from subthread_config import Thread_Config
from config_handler import ConfigHandler
from InitialWelcomeScreen import welcomeScreen
from TTS import TTS
from gui import ADAM
import threading
import signal

'''
    Starts the screen capturer.
'''
def start_screen_capturer():
    ss_object = ScreenCapturer()
    try:
        ss_object.capture_screenshots()
    except Exception as e:
        print(f"Screen capturer encountered an error: {e}")

'''
    Starts the ocr.
'''
def start_ocr():
    ocr = OCRProcessor(font_path="./Actual/arial.ttf")
    try:
        ocr.run()
    except Exception as e:
        print(f"OCR Processor encountered an error: {e}")

'''
    Starts the TTS.
'''
def start_TTS():
    tts = TTS()
    try:
        tts.run()
    except Exception as e:
        print(f"TTS encountered an error: {e}")

'''
    Starts the ADAM GUI application.
'''
def check_if_fresh_setup():
    if ConfigHandler.is_fresh_setup():
        number_of_devices = ScreenCapturer.get_num_of_devices()
    
        ConfigHandler.del_input_device(usb_alt_name = "")

        for i in range(number_of_devices):
                #for testing purposes, the expected usb_alt_name should be the actual alt name provided by WMIC instead of ""
            ConfigHandler.add_input_device(f"device{i}") #to replace with the actual alt device name
        
        ConfigHandler.save_config() #save the config file
        #proceed to the function start_welcome_screen() in InitialWelcomeScreen.py
        welcomeScreen.start_welcome_screen()
    else:
        run_ADAM()

'''
    Starts the ADAM GUI application.
'''
def run_ADAM():
    app = ADAM()
    try:
        app.run()
    except Exception as e:
        print(f"ADAM GUI application encountered an error: {e}")

'''
    Handles the signals that are sent to the script, for example, when pressing the ctrl + c button.
'''
def signal_handler(sig, frame):
    ADAM.close()

if __name__ == "__main__":

    # Initialise the Config Handler
    ConfigHandler.init()

    # Register the signal handler for SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    # Start the screen capturer thread
    screen_capturer_thread = threading.Thread(target=start_screen_capturer)
    screen_capturer_thread.start()

    # Start the OCR Thread
    ocr_thread = threading.Thread(target=start_ocr)
    ocr_thread.start()

    # Start the TTS Thread
    tts_thread = threading.Thread(target=start_TTS)
    tts_thread.start()

    # Start the GUI
    try:
        check_if_fresh_setup()
    except Exception as e:
        print(f"ADAM has failed to run with exception: {e}")

    # Shutting down all of ADAM
    finally:
        print("Gracefully shutting down screen capturer and OCR Processor...")
        # Stop the screen capturer if the GUI is closed
        Thread_Config.running = False
        # Wait for the screen capturer to finish
        # for thread in threading.enumerate():
        #     print("Running threads = " + thread.name)
        screen_capturer_thread.join()
        print("Shutting down of Screen Capturer completed.")
        ocr_thread.join()
        print("Shutting down of OCR Processor completed.")
        with TTS.lock:
            TTS.alert_queue.put("")
        tts_thread.join()
        print("Shutting down of TTS completed.")

    # Completely shut down all of ADAM
    print("Thank you for using ADAM!")

    # Just for checking if all the threads have joined
    # for thread in threading.enumerate():
    #     print("Running threads = " + thread.name)