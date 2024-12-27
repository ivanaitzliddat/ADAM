import configparser
import threading
import os

class ConfigHandler:
    # Config file path and default structure
    CONFIG_FILE = "config.ini"
    DEFAULTconfig = {
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
    config = configparser.ConfigParser()
    lock = threading.Lock()

    @staticmethod
    def init():
        """Initializes the configuration: creates or validates the config file."""
        if not os.path.exists(ConfigHandler.CONFIG_FILE):
            ConfigHandler.create_defaultconfig()
            print("Config file created with default settings.")
        else:
            try:
                ConfigHandler.config.read(ConfigHandler.CONFIG_FILE)
                ConfigHandler.validateconfig()
            except Exception as e:
                print(f"The config.ini file has been corrupted.")
                ConfigHandler.validateconfig()

    @staticmethod
    def create_defaultconfig():
        """Creates a new config.ini file with default settings."""
        for section, options in ConfigHandler.DEFAULTconfig.items():
            ConfigHandler.config[section] = options
        ConfigHandler.saveconfig()

    @staticmethod
    def validateconfig():
        """Validates the presence of all required sections and options."""
        updated = False

        for section, options in ConfigHandler.DEFAULTconfig.items():
            if section not in ConfigHandler.config:
                ConfigHandler.config[section] = options
                updated = True
            else:
                for option, default_value in options.items():
                    if option not in ConfigHandler.config[section]:
                        ConfigHandler.config[section][option] = default_value
                        updated = True

        if updated:
            ConfigHandler.saveconfig()
            print("Config file updated with missing sections/options.")

    @staticmethod
    def saveconfig():
        """Saves the current config to the file."""
        with open(ConfigHandler.CONFIG_FILE, "w") as file:
            ConfigHandler.config.write(file)

    @staticmethod
    def get_list(section, option):
        """Gets a list value from the config file."""
        value = ConfigHandler.config.get(section, option, fallback="")
        return [item.strip() for item in value.split(",")] if value else []

    @staticmethod
    def set_list(section, option, values):
        """Sets a list value in the config file."""
        if section not in ConfigHandler.config:
            ConfigHandler.config[section] = {}
        ConfigHandler.config[section][option] = ",".join(values)
        ConfigHandler.saveconfig()

    @staticmethod
    def add_to_list(section, option, value):
        """Adds an item to the list in the config."""
        items = ConfigHandler.get_list(section, option)
        if value not in items:  # Avoid duplicates
            items.append(value)
            ConfigHandler.set_list(section, option, items)

    @staticmethod
    def edit_list_item(section, option, old_value, new_value):
        """Edits an item in the list."""
        items = ConfigHandler.get_list(section, option)
        if old_value in items:
            index = items.index(old_value)
            items[index] = new_value
            ConfigHandler.set_list(section, option, items)

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
        return ConfigHandler.config.get(section, option, fallback="")

    @staticmethod
    def set_value(section, option, value):
        """Sets a single value in the config file."""
        if section not in ConfigHandler.config:
            ConfigHandler.config[section] = {}
        ConfigHandler.config[section][option] = value

        with open(ConfigHandler.config_file, "w") as file:
            ConfigHandler.config.write(file)

    @staticmethod
    def get_all_settings():
        """Returns all settings in the 'Settings' section as a dictionary."""
        if "Settings" in ConfigHandler.config:
            return {key: value for key, value in ConfigHandler.config["Settings"].items()}
        return {}

    @staticmethod
    def get_TTS_settings():
        """Returns all TTS settings as a dictionary."""
        if "TTS Settings" in ConfigHandler.config:
            return {key: value for key, value in ConfigHandler.config["TTS Settings"].items()}
        return {}