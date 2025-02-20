from screen_capturer import ScreenCapturer
from paddle_ocr import OCRProcessor
from subthread_config import Thread_Config
from config_handler import ConfigHandler
from InitialWelcomeScreen import welcomeScreen
from TTS import TTS
from gui import ADAM
import threading
import signal
from imageio.plugins.deviceslist import DevicesList
import time
import tkinter as tk
from tkinter import ttk

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
    Loads a window popup to display progress bar
'''
def show_loading_popup():
    popup = tk.Tk()
    popup.title("Fetching info from connected devices")
    popup.geometry("500x100")
    label = ttk.Label(popup, text="Please wait while ADAM is fetching information from the connected devices")
    label.pack(pady=10)

    # Calculate the center position
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    window_width = 500
    window_height = 100
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    #Progress bar with percentage
    progress_bar = ttk.Progressbar(popup, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(pady=10)
    progress_label = ttk.Label(popup, text="0%")
    progress_label.pack()

    return popup, progress_bar, progress_label

'''
    Starts the ADAM GUI application.
'''
def check_if_fresh_setup():
    if ConfigHandler.is_fresh_setup():
        #use ScreenCapturer to return the number of connected devices
        number_of_devices = ScreenCapturer.get_num_of_devices()
        #number_of_devices = 10 #for testing purposes

        # Show loading popup
        popup, progress_bar, progress_label = show_loading_popup()
        progress_bar["maximum"] = number_of_devices

        #DevicesList.device_list takes time to populate. Create a While loop to wait till device_list is fully populated
        while len(DevicesList.device_list)!=number_of_devices:
            current_devices = len(DevicesList.device_list)
            progress_bar["value"] = current_devices
            progress_label.config(text=f"{int((current_devices / number_of_devices) * 100)}%")
            popup.update()  # Update the popup window
            time.sleep(0.1)  # Sleep for 100 milliseconds
        
        #Close the popup window once device_list is fully populated
        popup.destroy()
        
        ConfigHandler.del_input_device(usb_alt_name = "")

        #Proceed to create new input device into Config.ini
        for i in DevicesList.device_list:
            ConfigHandler.add_input_device(usb_alt_name = i) #to replace with the actual alt device name
            
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