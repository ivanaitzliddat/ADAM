from screen_capturer import ScreenCapturer
from subthread_config import Thread_Config
from config_handler import ConfigHandler
from InitialWelcomeScreen import welcomeScreen

#TEST_main.py is copied from main.py in Actual folder

'''
    Starts the ADAM GUI application.
'''
def check_if_fresh_setup():
    if ConfigHandler.is_fresh_setup():
        number_of_devices = ScreenCapturer.get_usb_video_devices_new()
    
        ConfigHandler.del_input_device(usb_alt_name = "")
        number_of_devices = 3 #temporary - assume 3 connected devices

        for i in range(number_of_devices):
                #for testing purposes, the expected usb_alt_name should be the actual alt name provided by WMIC instead of ""
            ConfigHandler.add_input_device(f"device{i}") #to replace with the actual alt device name
        
        ConfigHandler.save_config() #save the config file
        #proceed to the function start_welcome_screen() in InitialWelcomeScreen.py
        welcomeScreen.start_welcome_screen()
    else:
        run_ADAM()

#do a check with the confighandler if ADAM requires to do a fresh setup
def run_ADAM():
    from TEST_GUI import ADAM
    try:
        app = ADAM()
        app.run()
    except Exception as e:
        print(f"ADAM has failed to run with exception: {e}")

'''
    Handles the signals that are sent to the script, for example, when pressing the ctrl + c button.
'''
def signal_handler(sig, frame):
    from TEST_GUI import ADAM
    ADAM.close()

if __name__ == "__main__":
    # Initialise the Config Handler
    ConfigHandler.init()

    # Start the GUI
    try:
        check_if_fresh_setup()
    except Exception as e:
        print(f"ADAM has failed to run with exception: {e}")

    # Completely shut down all of ADAM
    print("Thank you for using ADAM!")

    # Just for checking if all the threads have joined
    # for thread in threading.enumerate():
    #     print("Running threads = " + thread.name)