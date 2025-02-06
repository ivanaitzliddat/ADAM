from config_handler import ConfigHandler
import InitialWelcomeScreen
from mainPage import ADAMmain
from screen_capturer import ScreenCapturer

 #if fresh setup, open welcomeScreen, else open mainPage.py
 #get number of devices connected and auto populate the dictionary in config.ini
ConfigHandler.init()


print(ConfigHandler.dirname)
if ConfigHandler.is_fresh_setup():
    #get number of devices connected to ADAM
    number_of_devices = ScreenCapturer.get_usb_video_devices_new()
    ConfigHandler.del_input_device(usb_alt_name = "")

    #number_of_devices = 3 #temporary - assume 3 connected devices
    for i in range(number_of_devices):
        ConfigHandler.add_input_device(f"device{i}") #to replace with the actual alt device name
    ConfigHandler.save_config() #save the config file
    InitialWelcomeScreen.start_welcome_screen()
else:
    ADAMmain
