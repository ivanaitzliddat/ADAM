import ast, os, sys, threading, traceback
import tkinter.messagebox as tk_msgbox
import configparser

from datetime import datetime

class ConfigHandler:
    # Config file path and default structure
    CONFIG_FILE = "config.ini"

    DEFAULT_CONFIG = {
        "GUI": {
            "gui_fonts": "Arial 12,Times 14,ComicSans 10",
        },
        "TTS": {
            "tts_enabled": "True",
            "gender": "male",
            "rate": "75",
            "volume": "0.5",
            "repeat": "1",
        },
        "Input Device 0": {
            "usb_alt_name": "",
            "custom_name": "",
            "triggers": {"cond0":{"keywords":["keyword 1","keyword 2",], "tts_text": "hello", "bg_colour": "RED"}},
        }
    }

    cp = configparser.ConfigParser()
    lock = threading.Lock()
    dirname = ""
    
    @staticmethod
    def init():
        global dirname
        # This if...else needs to occur first before any subsequent references to file directories
        if getattr(sys, 'frozen', False):
            ''' If the application is run as a bundle, the PyInstaller bootloader
            extends the sys module by a flag frozen=True and sets the app 
            path into variable _MEIPASS'.
            Directory of .exe is in os.path.dirname(sys.executable)'''
            dirname = os.path.dirname(sys.executable)
        else:
            dirname = os.path.dirname(__file__)
        
        """Initializes the configuration: creates or validates the config file."""
        if not os.path.exists(ConfigHandler.CONFIG_FILE):
            ConfigHandler.create_default_config()
            print("No config.ini detected. New config.ini has been created with default settings.")
        else:
            try:
                ConfigHandler.cp.read(ConfigHandler.CONFIG_FILE)
            except:
                traceback.print_exc()
                print("The config.ini file is corrupted. A new config.ini will be created with default settings.")
                ConfigHandler.create_default_config()
                tk_msgbox.showinfo("Error in config.ini",  "The config.ini file is corrupted.\nA new config.ini has been created with default settings.")
            ConfigHandler.validate_config()

    @staticmethod
    def create_default_config():
        """Creates a new config.ini file with default settings."""
        for sections in ConfigHandler.cp.sections():
            ConfigHandler.cp.remove_section(sections)
        for section, options in ConfigHandler.DEFAULT_CONFIG.items():
            ConfigHandler.cp[section] = options
        if os.path.exists(ConfigHandler.CONFIG_FILE):
            old_cfg_name = "old_config("+datetime.now().strftime("%Y-%m-%d %H%M%S")+").ini"
            if os.path.exists(old_cfg_name):
                os.remove(old_cfg_name)
                os.rename(ConfigHandler.CONFIG_FILE, old_cfg_name)
            else:
                os.rename(ConfigHandler.CONFIG_FILE, old_cfg_name)
        ConfigHandler.save_config()
    
    @staticmethod
    def validate_config():
        print("Validating config.ini...")
        ### CHECK SECTIONS FOR VALIDITY
        cfg_file_sections = set(ConfigHandler.cp.sections())
        default_cfg_sections = set(ConfigHandler.DEFAULT_CONFIG.keys())
        
        # Check if any sections in DEFAULT_CONFIG cannot be found in config.ini. If yes, condition is True.
        if default_cfg_sections - cfg_file_sections:
            print("\tSome config.ini sections are missing. A new config.ini will be created with default settings.")
            ConfigHandler.create_default_config()
            tk_msgbox.showinfo("Error in config.ini",  "Some config.ini sections are missing.\nA new config.ini has been created with default settings.")
            return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
        # Check if any sections in config.ini cannot be found in DEFAULT_CONFIG. If yes, condition is True.
        elif diff_sections := cfg_file_sections - default_cfg_sections:
            for val in diff_sections:
                if not val.startswith("Input Device "):
                    print("\tInvalid section(s) found in config.ini sections. A new config.ini will be created with default settings.")
                    ConfigHandler.create_default_config()
                    tk_msgbox.showinfo("Error in config.ini",  "Invalid section(s) found in config.ini sections.\nA new config.ini has been created with default settings.")
                    return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
        else:
            print("\tAll sections are valid in config.ini.")

        ### CHECK KEYS AND VALUE TYPES IN [GUI] AND [TTS] 
        # Check if keys under [GUI] and [TTS] in config.ini match DEFAULT_CONFIG
        if (dict(ConfigHandler.cp.items("GUI")).keys() !=  ConfigHandler.DEFAULT_CONFIG["GUI"].keys()
            or dict(ConfigHandler.cp.items("TTS")).keys() !=  ConfigHandler.DEFAULT_CONFIG["TTS"].keys()):
            print("\tSome config.ini keys are missing or invalid. A new config.ini will be created with default settings.")
            ConfigHandler.create_default_config()
            tk_msgbox.showinfo("Error in config.ini",  "Some config.ini keys are missing or invalid.\nA new config.ini has been created with default settings.")
            return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
        # Check if their value types in config.ini match DEFAULT_CONFIG
        else:
            for key, val in dict(ConfigHandler.cp.items("GUI")).items():
                try:
                    cfg_val_type = type(ast.literal_eval(val))
                except (ValueError, SyntaxError):
                    cfg_val_type = type(val)
                except:
                    traceback.print_exc()
                    
                try:
                    default_val_type = type(ast.literal_eval(ConfigHandler.DEFAULT_CONFIG["GUI"][key]))
                except (ValueError, SyntaxError):
                    default_val_type = type(ConfigHandler.DEFAULT_CONFIG["GUI"][key])
                except:
                    traceback.print_exc()     
            
                if cfg_val_type != default_val_type:
                    print("\tInvalid value type found under [GUI] in config.ini. A new config.ini will be created with default settings.")
                    ConfigHandler.create_default_config()
                    tk_msgbox.showinfo("Error in config.ini",  "Invalid value type found under [GUI] in config.ini.\nA new config.ini has been created with default settings.")
                    return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
                        
            for key, val in dict(ConfigHandler.cp.items("TTS")).items():
                try:
                    cfg_val_type = type(ast.literal_eval(val))
                except (ValueError, SyntaxError):
                    cfg_val_type = type(val)
                except:
                    traceback.print_exc()
                    
                try:
                    default_val_type = type(ast.literal_eval(ConfigHandler.DEFAULT_CONFIG["TTS"][key]))
                except (ValueError, SyntaxError):
                    default_val_type = type(ConfigHandler.DEFAULT_CONFIG["TTS"][key])
                except:
                    traceback.print_exc()

                if cfg_val_type != default_val_type:
                    print("\tInvalid value type found under [TTS] in config.ini. A new config.ini will be created with default settings.")
                    ConfigHandler.create_default_config()
                    tk_msgbox.showinfo("Error in config.ini",  "Invalid value type found under [TTS] in config.ini.\nA new config.ini has been created with default settings.")
                    return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
            print("\t[GUI] and [TTS] sections, keys and value types are valid.")        

        ### CHECK KEYS AND VALUE TYPES IN [INPUT DEVICE X]
        # Loop through every section in config.ini that starts with "Input Device "
        for section in (temp for temp in ConfigHandler.cp.sections() if temp.startswith("Input Device ")):
            # Check if the keys can be found in DEFAULT_CONFIG.
            if dict(ConfigHandler.cp.items(section)).keys() !=  ConfigHandler.DEFAULT_CONFIG["Input Device 0"].keys():
                print("\tSome config.ini keys are missing or invalid. A new config.ini will be created with default settings.")
                ConfigHandler.create_default_config()
                tk_msgbox.showinfo("Error in config.ini",  "Some config.ini keys are missing or invalid.\nA new config.ini has been created with default settings.")
                return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
            # Check if the type of dict values in "triggers" key in config.ini match DEFAULT_CONFIG.
            # No need to check "usb_alt_name" and "custom_name" values since both are just Strings.
            else:
                try:
                    cfg_triggers_dict = ast.literal_eval(ConfigHandler.cp[section]["triggers"])
                    if not isinstance(cfg_triggers_dict, dict):
                        raise ValueError
                except (ValueError, SyntaxError):
                    print(f"\tInvalid value type found under [{section}]-triggers in config.ini. A new config.ini will be created with default settings.")
                    ConfigHandler.create_default_config()
                    tk_msgbox.showinfo("Error in config.ini",  f"Invalid value type found under [{section}]-triggers in config.ini.\nA new config.ini has been created with default settings.")
                    return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.                  
                except:
                    traceback.print_exc()

                # Set a temp dict with the sub-value (dict) of "triggers" to make type comparison less complicated later
                default_triggers_dict = {}
                for sub_val in ConfigHandler.DEFAULT_CONFIG["Input Device 0"]["triggers"].values():
                    default_triggers_dict = sub_val

                # Loop through all items in cfg_triggers_dict
                for sub_key, sub_val in cfg_triggers_dict.items():
                    # Check if inner dict keys in cfg_triggers_dict match the inner dict keys in default_triggers_dict
                    if sub_val.keys() != default_triggers_dict.keys():
                        print(f"\tInvalid sub-value key found under [{section}]-triggers in config.ini. A new config.ini will be created with default settings.")
                        ConfigHandler.create_default_config()
                        tk_msgbox.showinfo("Error in config.ini",  f"Invalid sub-value key found under [{section}]-triggers in config.ini.\nA new config.ini has been created with default settings.")
                        return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
                    else:
                        # Loop through all items in the inner dict of cfg_triggers_dict
                        for cfg_sub_sub_key, cfg_sub_sub_val in sub_val.items():
                            # Loop through all items in inner dict of default_triggers_dict
                            for default_sub_sub_key, default_sub_sub_val in default_triggers_dict.items():
                                if cfg_sub_sub_key == default_sub_sub_key:
                                    if type(cfg_sub_sub_val) != type(default_sub_sub_val):
                                        print(f"\tInvalid sub-value type found under [{section}]-triggers in config.ini. A new config.ini will be created with default settings.")
                                        ConfigHandler.create_default_config()
                                        
                                        return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.                  
        print("\t[Input Device X] sections, keys and value types are valid.")
        
        # If function has run up till this point, then config.ini is fully validated. Hence, return True.
        print("\tRESULT: Config.ini is valid.")
        return True
            
    @staticmethod
    def save_config():
        """Saves the current config to the file."""
        with open(ConfigHandler.CONFIG_FILE, "w", encoding = "utf-8") as file:
            ConfigHandler.cp.write(file)

    #DONE
    @staticmethod
    def is_fresh_setup():
        """Returns True if it detects a fresh setup (fresh setup requires user to be brought straight to setup page)"""
        for section in (temp for temp in ConfigHandler.cp.sections() if temp.startswith("Input Device ")):
            cfg_usb_alt_name = dict(ConfigHandler.cp.items(section))["usb_alt_name"]
            try:
                cfg_triggers_dict = ast.literal_eval(ConfigHandler.cp[section]["triggers"])
                if not isinstance(cfg_triggers_dict, dict):
                    raise ValueError
            except (ValueError, SyntaxError):
                print(f"Invalid value type found under [{section}]-triggers in config.ini. A new config.ini will be created with default settings.")
                ConfigHandler.create_default_config()
                tk_msgbox.showinfo("Error in config.ini",  f"Invalid value type found under [{section}]-triggers in config.ini.\nA new config.ini has been created with default settings.")
                return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.                  
            except:
                traceback.print_exc()

            # Check if the usb_alt_name is empty/spaces, and if the triggers in config.ini matches DEFAULT_CONFIG. This is a sign that user has not set up ADAM yet.
            if (cfg_usb_alt_name == "" or cfg_usb_alt_name.isspace()) and (cfg_triggers_dict == ConfigHandler.DEFAULT_CONFIG[section]["triggers"]):
                print("Fresh setup detected. Bringing you to the setup page.")
                return True
            else:
                return False

    # Returns all options and values in [GUI] section as a dictionary.
    @staticmethod
    def get_cfg_gui():
        # Check if [GUI] section exists in config.ini
        if "GUI" in ConfigHandler.cp.sections():
            return {key: value for key, value in ConfigHandler.cp["GUI"].items()}
        return {}

    # Returns all options and values in [TTS] section as a dictionary.
    @staticmethod
    def get_cfg_tts():
        # Check if [TTS] section exists in config.ini
        if "TTS" in ConfigHandler.cp.sections():
            return {key: value for key, value in ConfigHandler.cp["TTS"].items()}
        return {}

    # Returns all options and values in [Input Device X] section as a dictionary.
    @staticmethod
    def get_cfg_input_devices(**kwargs):
        usb_alt_name = kwargs.get("usb_alt_name")
        input_devices_dict = {}
        
        # Check if [Input Device X] section exists in config.ini
        for section in (temp for temp in ConfigHandler.cp.sections() if temp.startswith("Input Device ")):
            # Check if usb_alt_name kwargs was passed in as String
            if isinstance(usb_alt_name, str):
                if ConfigHandler.cp.get(section, "usb_alt_name") == usb_alt_name:
                    for key, value in ConfigHandler.cp[section].items():
                        if key != "triggers":
                            input_devices_dict.setdefault(section, {}).update({key: value})
                        else:
                            try:
                                cfg_triggers_dict = ast.literal_eval(ConfigHandler.cp[section]["triggers"])
                                if not isinstance(cfg_triggers_dict, dict):
                                    raise ValueError
                                else:
                                    input_devices_dict.setdefault(section, {}).update({key: cfg_triggers_dict})
                            except (ValueError, SyntaxError):
                                print(f"Invalid value type found under [{section}]-triggers in config.ini.")
                                return {}
                            except:
                                traceback.print_exc()
                                return {}    
            # Check if usb_alt_name kwargs was passed in (value is None if not passed in)
            elif usb_alt_name is None:
                for key, value in ConfigHandler.cp[section].items():
                    if key != "triggers":
                        input_devices_dict.setdefault(section, {}).update({key: value})
                    else:
                        try:
                            cfg_triggers_dict = ast.literal_eval(ConfigHandler.cp[section]["triggers"])
                            if not isinstance(cfg_triggers_dict, dict):
                                raise ValueError
                            else:
                                input_devices_dict.setdefault(section, {}).update({key: cfg_triggers_dict})
                                
                        except (ValueError, SyntaxError):
                            print(f"Invalid value type found under [{section}]-triggers in config.ini.")
                            return {}
                        except:
                            traceback.print_exc()
                            return {}
            # 'Catch-all' if usb_alt_name was passed in as non-String value.
            else:
                print("Invalid value type for 'usb_alt_name' (String needed).")
                return {}
        else:
            return input_devices_dict

    # Set values of options in [GUI] section.
    # This only sets the values, but does not write to config.ini to reduce write operations. Call save_config() separately.
    @staticmethod
    def set_cfg_gui(**kwargs):
        for key, val in kwargs.items():
            # Check if the keys can be found under [GUI] in config.ini
            if ConfigHandler.cp.has_option("GUI", key):
                try:
                    cfg_val = ast.literal_eval(val)
                    cfg_val_type = type(cfg_val)
                except (ValueError, SyntaxError):
                    cfg_val = val
                    cfg_val_type = type(cfg_val)
                except:
                    traceback.print_exc()
                    
                try:
                    default_val_type = type(ast.literal_eval(ConfigHandler.DEFAULT_CONFIG["GUI"][key]))
                except (ValueError, SyntaxError):
                    default_val_type = type(ConfigHandler.DEFAULT_CONFIG["GUI"][key])
                except:
                    traceback.print_exc()     
            
                if cfg_val_type == default_val_type:
                    ConfigHandler.cp["GUI"][key] = str(val)
                    print(f"[GUI]-{key} was set to {val}. You need to call save_config() separately to write to config.ini.")
                else:
                    print(f"Invalid value type for [GUI]-{key}. Expected {default_val_type} but got {cfg_val_type} instead.")
            else:
                print(f"Unable to find {key} under [GUI] section of config.ini.")

    # Set values of options in [TTS] section.
    # This only sets the values, but does not write to config.ini to reduce write operations. Call save_config() separately.
    @staticmethod
    def set_cfg_tts(**kwargs):
        for key, val in kwargs.items():
            # Check if the keys can be found under [TTS] in config.ini
            if ConfigHandler.cp.has_option("TTS", key):
                try:
                    cfg_val = ast.literal_eval(val)
                    cfg_val_type = type(cfg_val)
                except (ValueError, SyntaxError):
                    cfg_val = val
                    cfg_val_type = type(cfg_val)
                except:
                    traceback.print_exc()

                try:
                    default_val_type = type(ast.literal_eval(ConfigHandler.DEFAULT_CONFIG["TTS"][key]))
                except (ValueError, SyntaxError):
                    default_val_type = type(ConfigHandler.DEFAULT_CONFIG["TTS"][key])
                except:
                    traceback.print_exc()     
            
                if cfg_val_type == default_val_type:
                    ConfigHandler.cp["TTS"][key] = str(val)
                    print(f"[TTS]-{key} section was set to {val}. You need to call save_config() separately to write to config.ini.")
                else:
                    print(f"Invalid value type for [TTS]-{key}. Expected {default_val_type} but got {cfg_val_type} instead.")
            else:
                print(f"Unable to find {key} under [TTS] section of config.ini.")               

    # Set values of options in [Input Device X] section.
    # This only sets the values, but does not write to config.ini to reduce write operations. Call save_config() separately.
    @staticmethod
    def set_cfg_input_device(**kwargs):
        usb_alt_name_arg = kwargs.get("usb_alt_name")
        condition_arg = kwargs.get("condition")
        cfg_triggers_dict = {}
        initial_cfg_triggers_dict = {}
        # Check if "usb_alt_name" is one of the kwargs and if its value is a String
        if isinstance(usb_alt_name_arg, str):
            # Loop through kwargs and do if the kwarg is not usb_alt_name and condition
            for key, val in (temp for temp in kwargs.items() if ("usb_alt_name" not in temp and "condition" not in temp)):
                # Access [Input Device X] section that contains the specific "usb_alt_name" value
                for section in (temp for temp in ConfigHandler.cp.sections() if (temp.startswith("Input Device ") and ConfigHandler.cp.get(temp, "usb_alt_name") == usb_alt_name_arg)):
                    try:
                        cfg_val = ast.literal_eval(val)
                        cfg_val_type = type(cfg_val)
                    except (ValueError, SyntaxError):
                        cfg_val = val
                        cfg_val_type = type(cfg_val)
                    except:
                        traceback.print_exc()
                    
                    if ConfigHandler.cp.has_option(section, key):
                        try:
                            default_val_type = type(ast.literal_eval(ConfigHandler.DEFAULT_CONFIG["Input Device 0"][key]))
                        except (ValueError, SyntaxError):
                            default_val_type = type(ConfigHandler.DEFAULT_CONFIG["Input Device 0"][key])
                        except:
                            traceback.print_exc()

                        if cfg_val_type == default_val_type:
                            ConfigHandler.cp[section][key] = str(val)
                            print(f"[{section}]-{key} was set to {val}. You need to call save_config() separately to write to config.ini.")
                        else:
                            print(f"Invalid value type for [{section}]-{key}. Expected {default_val_type} but got {cfg_val_type} instead.")
                    else:
                        default_triggers_dict = ConfigHandler.DEFAULT_CONFIG["Input Device 0"]["triggers"]  # No need ast.literal_eval since type is already dict in DEFAULT_CONFIG
                        cond_name = ""
                        for sub_key, sub_val in default_triggers_dict.items():
                            default_val_type = type(sub_val.get(key))

                            if key in sub_val and cfg_val_type == default_val_type:
                                try:
                                    # Set cfg_triggers_dict if it is empty
                                    if len(cfg_triggers_dict)==0:
                                        cfg_triggers_dict = ast.literal_eval(ConfigHandler.cp.get(section, "triggers"))
                                        
                                    initial_cfg_triggers_dict = ast.literal_eval(ConfigHandler.cp.get(section, "triggers"))
                                    if not isinstance(cfg_triggers_dict, dict):
                                        raise ValueError
                                except (ValueError, SyntaxError):
                                    print(f"Invalid value type found under [{section}]-triggers in config.ini.")
                                except:
                                    traceback.print_exc()

                                if condition_arg is not None:
                                    cond_name = condition_arg
                                    if condition_arg not in cfg_triggers_dict:
                                        cfg_triggers_dict[cond_name] = default_triggers_dict["cond0"]   # Create new condition with default values
                                        
                                    cfg_triggers_dict[cond_name][key] = cfg_val # Set with user-specified value
                                else:
                                    cond_count = []
                                    for item in (temp for temp in initial_cfg_triggers_dict if temp.startswith("cond")):
                                        cond_count.append(int(item.replace("cond", "")))
                                    cond_name = "cond"+str(max(cond_count)+1)
                                    cfg_triggers_dict[cond_name] = default_triggers_dict["cond0"]   # Create new condition with default values
                                    cfg_triggers_dict[cond_name][key] = cfg_val   # Set with user-specified value
                            else:
                                print(f"Invalid value type for [{section}]-triggers-cond-{key}. Expected {default_val_type} but got {cfg_val_type} instead.")
                                return
            else:
                for cond, cond_val in initial_cfg_triggers_dict.items():
                    # Check if trigger values for the condition exists (i.e. duplicate)
                    if cfg_triggers_dict[cond_name].items() <= cond_val.items():
                        print(f"The trigger condition values under [{section}] for '{cond_name}' is a duplicate of '{cond}'. '{cond_name}' will not be saved.")
                        tk_msgbox.showinfo("Duplicate trigger condition values in config.ini.",
                                           f"Duplicate trigger condition values detected for this input device. Trigger changes will not be saved.")
                        return  # Exit function if duplicate condition values detected
                else:
                    if len(cfg_triggers_dict) != 0:
                        try:
                            ConfigHandler.cp[section]["triggers"] = str(cfg_triggers_dict)
                            print(f"[{section}]-{key} was set to {str(cfg_triggers_dict)}. You need to call save_config() separately to write to config.ini.")
                        except UnboundLocalError:
                            traceback.print_exc()
                            print("Invalid argument value for 'usb_alt_name'.")
                        except:
                            traceback.print_exc()
        else:
            print("Missing argument 'usb_alt_name'.")

    # Add input devices
    @staticmethod
    def add_input_device(usb_alt_name: str):
        device_count = []
        if usb_alt_name == "" or usb_alt_name.isspace():
            print("Empty/blank space for 'usb_alt_name' is not allowed.")
            return
        else:
            for section in (temp for temp in ConfigHandler.cp.sections() if temp.startswith("Input Device ")):
                device_count.append(int(section.replace("Input Device ", "")))
                
                if ConfigHandler.cp.get(section, "usb_alt_name") == usb_alt_name:
                    print(f"usb_alt_name '{usb_alt_name}' already exists as an Input Device.")
                    return
            else:
                new_device = "Input Device "+str(max(device_count)+1)
                ConfigHandler.cp.add_section(new_device)
                ConfigHandler.cp[new_device] = ConfigHandler.DEFAULT_CONFIG["Input Device 0"]
                ConfigHandler.cp[new_device]["usb_alt_name"] = usb_alt_name
                print(f"Added [{new_device}]. You need to call save_config() separately to write to config.ini.")

    # Delete input devices
    @staticmethod
    def del_input_device(usb_alt_name: str):
        for section in (temp for temp in ConfigHandler.cp.sections() if (temp.startswith("Input Device ") and ConfigHandler.cp.get(temp, "usb_alt_name") == usb_alt_name)):
            ConfigHandler.cp.remove_section(section)
            print(f"Deleted [{section}]. You need to call save_config() separately to write to config.ini.")



################# Functions below this line might not be used and may be removed in the near future ################################
    '''            
    # TODO: Is this func really needed? Maybe just use get_triggers(), which returns a dict? Then use ast.literal_eval(key) to get the values into dict format.
    @staticmethod
    def get_list(section, option):
        """Gets a list value from the config file."""
        value = ConfigHandler.cp.get(section, option, fallback="")
        return [item.strip() for item in value.split(",")] if value else []

    # TODO: Is this func really needed? Seems like set_value() is sufficient.
    @staticmethod
    def set_list(section, option, values):
        """Sets a list value in the config file."""
        if section not in ConfigHandler.cp:
            ConfigHandler.cp[section] = {}
        ConfigHandler.cp[section][option] = ",".join(values)
        ConfigHandler.save_config()

    # TODO: Is this func really needed? Can just use set_value()
    @staticmethod
    def add_to_list(section, option, value):
        """Adds an item to the list in the config."""
        items = ConfigHandler.get_list(section, option)
        if value not in items:  # Avoid duplicates
            items.append(value)
            ConfigHandler.set_list(section, option, items)
            
    # TODO: Is this func really needed? Can just use set_value()
    @staticmethod
    def edit_list_item(section, option, old_value, new_value):
        """Edits an item in the list."""
        items = ConfigHandler.get_list(section, option)
        if old_value in items:
            index = items.index(old_value)
            items[index] = new_value
            ConfigHandler.set_list(section, option, items)
            
    # TODO: Is this func really needed? Can just use delete_value()
    @staticmethod
    def delete_from_list(section, option, value):
        """Deletes an item from the list."""
        items = ConfigHandler.get_list(section, option)
        if value in items:
            items.remove(value)
            ConfigHandler.set_list(section, option, items)

    @staticmethod
    def get_value(section, option):
        """Gets a single value from the config file."""
        return ConfigHandler.cp.get(section, option, fallback="")

    @staticmethod
    def set_value(section, option, value):
        """Sets a single value in the config file."""
        if section not in ConfigHandler.cp:
            ConfigHandler.cp[section] = {}
        if section == "Input Devices" or section == "Triggers":
            if not isinstance(value, dict):
                raise TypeError("Only dict values are allowed for Input Devices and Triggers sections.")
                
        ConfigHandler.cp[section][option] = str(value)

        with open(ConfigHandler.CONFIG_FILE, "w", encoding = "utf-8") as file:
            ConfigHandler.cp.write(file)

    @staticmethod
    def delete_option(section, option):
        """Deletes a single option in the config file."""
        ConfigHandler.cp.remove_option(section, option)

        with open(ConfigHandler.CONFIG_FILE, "w", encoding = "utf-8") as file:
            ConfigHandler.cp.write(file)

    @staticmethod
    def get_gui_settings():
        """Returns all settings in the 'GUI' section as a dictionary."""
        if "GUI" in ConfigHandler.cp:
            return {key: value for key, value in ConfigHandler.cp["GUI"].items()}
        return {}

    @staticmethod
    def get_TTS_settings():
        """Returns all TTS as a dictionary."""
        if "TTS" in ConfigHandler.cp:
            return {key: value for key, value in ConfigHandler.cp["TTS"].items()}
        return {}
    
    @staticmethod
    def get_devices():
        """Returns all settings in the 'Input Devices' section as a dictionary."""
        if "Input Devices" in ConfigHandler.cp:
            return {key: value for key, value in ConfigHandler.cp["Input Devices"].items()}
        return {}

    # TODO: Previously was named get_all_settings().
    @staticmethod
    def get_triggers():
        """Returns all settings in the 'Triggers' section as a dictionary."""
        if "Triggers" in ConfigHandler.cp:
            return {key: value for key, value in ConfigHandler.cp["Triggers"].items()}
        return {}
    '''
