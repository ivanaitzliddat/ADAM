from config_handler import ConfigHandler

ConfigHandler.init()

###### EXAMPLES: ########
#Uncomment the function calls that you want to try out


'''
### Loads (reads) the config file, if any. ###
# If unable to read or file doesnt exist, auto create default config.
# If able to read, proceeds to validate the config file.
ConfigHandler.init()

### Valides the config file. ###
# If structure does not match default config, validation fails and (1) current config is renamed to old and (2) new default config is created.
ConfigHandler.validate_config.()

### Check if this is a fresh setup of ADAM ###
# Returns True if it is fresh setup
if ConfigHandler.is_fresh_setup():
    print("fresh setup!")
    

### Get GUI settings ###
# Returns a dict of GUI settings
print(ConfigHandler.get_cfg_gui())


### Get TTS settings ###
# Returns a dict of TTS settings
print(ConfigHandler.get_cfg_tts())


### Get Input Device settings. ###
# This function accepts OPTIONAL usb_alt_name kwarg.
# Returns a dict of all Input Device X settings if no usb_alt_name is passed in.
# Returns a dict of a specific Input Device X's settings if usb_alt_name is passed in.
device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name = "aaa") # Pass in usb_alt_name argument to get settings for that device only as dict
for key, val in device_dict.items():
    print(key)
    print(val)
    print(val["triggers"]["cond0"]["keywords"])

device_dict2 = ConfigHandler.get_cfg_input_devices()    # If usb_alt_name argument not passed in, settings for all input devices will be retrieved as dict
for key, val in device_dict2.items():
    print(key)
    print(val)
    print(val["triggers"]["cond0"]["keywords"])


### Set GUI settings. ###
# This function accepts OPTIONAL kwargs based on options in config.ini.
ConfigHandler.set_cfg_gui(gui_fonts = "Arial 20,Times 22,ComicSans 24")


### Set TTS settings. ###
#This function accepts OPTIONAL kwargs based on options in config.ini.
ConfigHandler.set_cfg_tts(volume = 2.0, tts_enabled = True)


### Set Input Device settings. ###
# This function requires MANDATORY usb_alt_name kwarg, and accepts OPTIONAL kwargs based on options in config.ini.
ConfigHandler.set_cfg_input_device(usb_alt_name = "aaa", custom_name = "teletubby", keywords = ["abc", "def"], bg_colour = "purple")
ConfigHandler.save_config()

# Additional 'condition' kwarg can be used to set parameters only for the specified condition name, or to create new condition with that name.
ConfigHandler.set_cfg_input_device(usb_alt_name = "aaa", condition = "cond0", keywords = ["abc", "def"], bg_colour = "black")
ConfigHandler.save_config()


### Add new Input Device ###
# This function requires MANDATORY usb_alt_name argument of String type.
ConfigHandler.add_input_device(usb_alt_name = "testing alt name")
ConfigHandler.save_config()


### Delete new Input Device ###
# This function requires MANDATORY usb_alt_name argument of String type.
ConfigHandler.del_input_device(usb_alt_name = "testing alt name")
ConfigHandler.save_config()

'''
