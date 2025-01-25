import configparser
import ast, os, threading, traceback

class ConfigHandler:
    # Config file path and default structure
    CONFIG_FILE = "config.ini"
    
    '''
    # Old DEFAULT_CONFIG
    DEFAULT_CONFIG = {
        "Settings": {
            "keywords": "",
            "colors": "#FFFFFF,#FF5733,#D3D3D3",
            "gui_fonts": "Arial 12,Times 14,ComicSans 10",
        },
        "TTS Settings": {
            "tts_enabled": "True",
            "gender": "male",
            "rate": "75",
            "volume": "0.5",
            "repeat": "1",
        }
    }
    '''

    DEFAULT_CONFIG = {
        "GUI": {
            "gui_fonts": "Arial 12,Times 14,ComicSans 10",
        },
        "TTS Settings": {
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

    @staticmethod
    def init():
        """Initializes the configuration: creates or validates the config file."""
        if not os.path.exists(ConfigHandler.CONFIG_FILE):
            ConfigHandler.create_default_config()
            print("No config.ini detected. New config.ini has been created with default settings.")
            #ConfigHandler.is_fresh_setup() # TO REMOVE?
        else:
            try:
                ConfigHandler.cp.read(ConfigHandler.CONFIG_FILE)
            except Exception as e:
                traceback.print_exc()
                print("The config.ini file is corrupted. New config.ini has been created with default settings.")
                ConfigHandler.create_default_config()    
                #ConfigHandler.is_fresh_setup() # TO REMOVE?
            ConfigHandler.validate_config()
            ''' #### TO REMOVE?? ####
            cfg_validity = ConfigHandler.validate_config()
            if cfg_validity == False:
                ConfigHandler.is_fresh_setup()
            '''

    @staticmethod
    def create_default_config():
        """Creates a new config.ini file with default settings."""
        for sections in ConfigHandler.cp.sections():
            ConfigHandler.cp.remove_section(sections)
        for section, options in ConfigHandler.DEFAULT_CONFIG.items():
            ConfigHandler.cp[section] = options
        ConfigHandler.save_config()

    @staticmethod
    def validate_config():
        print("Validating config.ini...")
        ### CHECK SECTIONS FOR VALIDITY
        cfg_file_sections = set(ConfigHandler.cp.sections())
        default_cfg_sections = set(ConfigHandler.DEFAULT_CONFIG.keys())
        
        # Check if any sections in DEFAULT_CONFIG cannot be found in config.ini. If yes, condition is True.
        if default_cfg_sections - cfg_file_sections:
            print("Some config.ini sections are missing. New config.ini has been created with default settings.")
            ConfigHandler.create_default_config()
            return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
        # Check if any sections in config.ini cannot be found in DEFAULT_CONFIG. If yes, condition is True.
        elif diff_sections := cfg_file_sections - default_cfg_sections:
            for val in diff_sections:
                if not val.startswith("Input Device "):
                    print("Invalid section(s) found in config.ini sections. New config.ini has been created with default settings.")
                    ConfigHandler.create_default_config()
                    return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
        else:
            print("All sections are valid in config.ini.")

        ### CHECK KEYS AND VALUE TYPES IN [GUI] AND [TTS SETTINGS] 
        # Check if keys under [GUI] and [TTS Settings] in config.ini match DEFAULT_CONFIG
        if (dict(ConfigHandler.cp.items("GUI")).keys() !=  ConfigHandler.DEFAULT_CONFIG["GUI"].keys()
            or dict(ConfigHandler.cp.items("TTS Settings")).keys() !=  ConfigHandler.DEFAULT_CONFIG["TTS Settings"].keys()):
            ConfigHandler.create_default_config()
            print("Some config.ini keys are missing or invalid. New config.ini has been created with default settings.")
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
                    print("Invalid value type found under [GUI] in config.ini. New config.ini has been created with default settings.")
                    ConfigHandler.create_default_config()
                    return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
                        
            for key, val in dict(ConfigHandler.cp.items("TTS Settings")).items():
                try:
                    cfg_val_type = type(ast.literal_eval(val))
                except (ValueError, SyntaxError):
                    cfg_val_type = type(val)
                except:
                    traceback.print_exc()
                    
                try:
                    default_val_type = type(ast.literal_eval(ConfigHandler.DEFAULT_CONFIG["TTS Settings"][key]))
                except (ValueError, SyntaxError):
                    default_val_type = type(ConfigHandler.DEFAULT_CONFIG["TTS Settings"][key])
                except:
                    traceback.print_exc()

                if cfg_val_type != default_val_type:
                    print("Invalid value type found under [TTS Settings] in config.ini. New config.ini has been created with default settings.")
                    ConfigHandler.create_default_config()
                    return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
            print("[GUI] and [TTS Settings] sections, keys and value types are valid.")        

        ### CHECK KEYS AND VALUE TYPES IN [INPUT DEVICE X]
        # Loop through every section in config.ini that starts with "Input Device "
        for section in (temp for temp in ConfigHandler.cp.sections() if temp.startswith("Input Device ")):
            # Check if the keys can be found in DEFAULT_CONFIG.
            if dict(ConfigHandler.cp.items(section)).keys() !=  ConfigHandler.DEFAULT_CONFIG["Input Device 0"].keys():
                ConfigHandler.create_default_config()
                print("Some config.ini keys are missing or invalid. New config.ini has been created with default settings.")
                return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
            # Check if the type of dict values in "triggers" key in config.ini match DEFAULT_CONFIG.
            # No need to check "usb_alt_name" and "custom_name" values since both are just Strings.
            else:
                try:
                    cfg_triggers_dict = ast.literal_eval(ConfigHandler.cp[section]["triggers"])
                    if not isinstance(cfg_triggers_dict, dict):
                        raise ValueError
                except (ValueError, SyntaxError):
                    print(f"Invalid value type found under [{section}]-triggers in config.ini. New config.ini has been created with default settings.")
                    ConfigHandler.create_default_config()
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
                        print(f"Invalid sub-value key found under [{section}]-triggers in config.ini. New config.ini has been created with default settings.")
                        ConfigHandler.create_default_config()
                        return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
                    else:
                        # Loop through all items in the inner dict of cfg_triggers_dict
                        for cfg_sub_sub_key, cfg_sub_sub_val in sub_val.items():
                            # Loop through all items in inner dict of default_triggers_dict
                            for default_sub_sub_key, default_sub_sub_val in default_triggers_dict.items():
                                if cfg_sub_sub_key == default_sub_sub_key:
                                    if type(cfg_sub_sub_val) != type(default_sub_sub_val):
                                        print(f"Invalid sub-value type found under [{section}]-triggers in config.ini. New config.ini has been created with default settings.")
                                        ConfigHandler.create_default_config()
                                        return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.                  
        print("[Input Device X] sections, keys and value types are valid.")
        
        # If function has run up till this point, then config.ini is fully validated. Hence, return True.
        print("Result: Config.ini is valid.")
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
                print(f"Invalid value type found under [{section}]-triggers in config.ini. New config.ini has been created with default settings.")
                ConfigHandler.create_default_config()
                return False    # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.                  
            except:
                traceback.print_exc()

            # Check if the usb_alt_name is empty/spaces, and if the triggers in config.ini matches DEFAULT_CONFIG. This is a sign that user has not set up ADAM yet.
            if (cfg_usb_alt_name == "" or cfg_usb_alt_name.isspace()) and (cfg_triggers_dict == ConfigHandler.DEFAULT_CONFIG[section]["triggers"]):
                print("Fresh setup detected. Bringing you to the setup page.")
                return True
            else:
                return False
    
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
        """Returns all TTS settings as a dictionary."""
        if "TTS Settings" in ConfigHandler.cp:
            return {key: value for key, value in ConfigHandler.cp["TTS Settings"].items()}
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
