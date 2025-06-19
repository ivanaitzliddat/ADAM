import os, threading, traceback
import signal

from screen_capturer import ScreenCapturer
from paddle_ocr import OCRProcessor
from subthread_config import Thread_Config
from config_handler import ConfigHandler
from TTS import TTS
from gui import ADAM

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
    #   Mobile detection model is ~17x smaller and 7.2x faster, but ~4.8% less accurate than server model
    #   Mobile recognition model is 5x smaller and 1.3x faster, but ~5.09% less accurate than server model
    ocr_model = "PP-OCRv5_server"

    #   To force a download of OCR models to default location "%userprofile%/.paddlex/",
    #   set text_detection_model_dir and text_recognition_model_dir to None
    ocr = OCRProcessor(font_path="./Actual/arial.ttf",
                       text_detection_model_name = ocr_model+"_det",
                       text_detection_model_dir = os.path.dirname(ConfigHandler.dirname) + "/paddlex/official_models/"+ocr_model+"_det",
                       text_recognition_model_name = ocr_model+"_rec",
                       text_recognition_model_dir = os.path.dirname(ConfigHandler.dirname) + "/paddlex/official_models/"+ocr_model+"_rec",
                       use_doc_orientation_classify = False,
                       use_doc_unwarping = False,
                       use_textline_orientation = False,
                       )
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
        print(f"TTS encountered an error.")
        traceback.print_exc()

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
        #check_if_fresh_setup()
        run_ADAM()
    except RuntimeError:   
        ADAM.close()
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
