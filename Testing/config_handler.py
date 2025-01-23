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
    }'''

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
        "Input Devices": {
            "device0": {"usb_alt_name": "test alt name", "custom_name": "test custom name"}
        },
        "Triggers": {
            "device0": {"keywords": ["keyword 1","keyword 2",], "tts_text": "hello", "bg_colour": "RED"}
        }
    }

    cp = configparser.ConfigParser()
    lock = threading.Lock()

    @staticmethod
    def init():
        """Initializes the configuration: creates or validates the config file."""
        if not os.path.exists(ConfigHandler.CONFIG_FILE):
            ConfigHandler.create_default_config()
            print("Config file created with default settings.")
        else:
            try:
                ConfigHandler.cp.read(ConfigHandler.CONFIG_FILE)
                ConfigHandler.validateconfig()
            except Exception as e:
                traceback.print_exc()
                print(f"The config.ini file has been corrupted.")
                ConfigHandler.validateconfig()

    @staticmethod
    def create_default_config():
        """Creates a new config.ini file with default settings."""
        for section, options in ConfigHandler.DEFAULT_CONFIG.items():
            ConfigHandler.cp[section] = options
        ConfigHandler.saveconfig()

    @staticmethod
    def validateconfig():
        cfg_file_sections = set(ConfigHandler.cp.sections())
        default_cfg_sections = set(ConfigHandler.DEFAULT_CONFIG.keys())
        # Check if config.ini file's sections matches the sections in DEFAULT_CONFIG
        if cfg_file_sections != default_cfg_sections:
            diff_sections = cfg_file_sections.difference(default_cfg_sections)  # Check what sections the config.ini has that DEFAULT_CONFIG does not.
            for val in diff_sections:
                ConfigHandler.cp.remove_section(val)
            
            # If some sections are different = .ini file has different structure. Hence, need to overwrite with default config.ini.
            ConfigHandler.create_default_config()
            print("Some config.ini sections are different. New config.ini has been created with default settings.")

        else:
            # Check if the fixed keys in each applicable config.ini section matches DEFAULT_CONFIG
            if (dict(ConfigHandler.cp.items("GUI")).keys() !=  ConfigHandler.DEFAULT_CONFIG["GUI"].keys()
                or dict(ConfigHandler.cp.items("TTS Settings")).keys() !=  ConfigHandler.DEFAULT_CONFIG["TTS Settings"].keys()):
                
                # If some keys are not present = .ini file has different structure. Hence, need to overwrite with default config.ini.
                ConfigHandler.create_default_config()
                print("Some config.ini keys are MISSING. New config.ini has been created with default settings.")
            else:
                # All keys are present = .ini file has same structure. Hence, do nothing
                print("All config.ini keys are PRESENT.")
                
            # Check if the format of values in dynamic keys for each applicable config.ini section matches DEFAULT_CONFIG
            for cfg_options in dict(ConfigHandler.cp.items("Input Devices")).values():
                for default_options in ConfigHandler.DEFAULT_CONFIG["Input Devices"].values():
                    if ast.literal_eval(cfg_options).keys() != default_options.keys():
                        ConfigHandler.create_default_config()
                        print("Some config.ini values are MALFORMED. New config.ini has been created with default settings.")
                        return  # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
                    
            # Check if the format of values in dynamic keys for each applicable config.ini section matches DEFAULT_CONFIG                        
            for cfg_options in dict(ConfigHandler.cp.items("Triggers")).values():
                for default_options in ConfigHandler.DEFAULT_CONFIG["Triggers"].values():
                    if ast.literal_eval(cfg_options).keys() != default_options.keys():
                        ConfigHandler.create_default_config()
                        print("Some config.ini values are MALFORMED. New config.ini has been created with default settings.")
                        return  # Overwriting with default config only needs to happen once, and checks on remaining sections/options are not needed.
    @staticmethod
    def saveconfig():
        """Saves the current config to the file."""
        with open(ConfigHandler.CONFIG_FILE, "w", encoding = "utf-8") as file:
            ConfigHandler.cp.write(file)

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
        ConfigHandler.saveconfig()

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
