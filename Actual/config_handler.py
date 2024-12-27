import configparser
import threading
import os

SETTINGS = "Settings"
KEYWORDS = "keywords"
COLORS = "colors"
TTS = "tts_enabled"
FONTS = "gui_fonts"

class ConfigHandler:
    config_file = "config.ini"
    config = configparser.ConfigParser()
    lock = threading.Lock()

    def init():
        try:
            # Check if the file exists, if not, create it
            if not os.path.exists(ConfigHandler.config_file):
                ConfigHandler.create_default_config()
                print("A new config.ini has been created.")
            else:
                # Validate the config file structure
                ConfigHandler.validate_config()
                ConfigHandler.config.read(ConfigHandler.config_file)
                print("Read from config.ini.")
        except (configparser.ParsingError, configparser.DuplicateSectionError) as e:
            print(f"Config file is corrupted: {e}")
            print("Recreating the config.ini with default settings.")
            ConfigHandler.create_default_config()

    def validate_config():
        """Validates the presence of all required sections and options."""
        # Define the required structure
        required_structure = {
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

        updated = False  # Flag to track if updates were made

        # Check each section and option
        for section, options in required_structure.items():
            if section not in ConfigHandler.config:
                ConfigHandler.config[section] = {}
                updated = True

            for option, default_value in options.items():
                if option not in ConfigHandler.config[section]:
                    ConfigHandler.config[section][option] = default_value
                    updated = True

        # Save updates if needed
        if updated:
            with open(ConfigHandler.config_file, "w") as file:
                ConfigHandler.config.write(file)
            print("Config file updated with missing sections/options.")


    def create_default_config():
        """Creates a default config file."""
        ConfigHandler.config["Settings"] = {
            "keywords": "",
            "colors": "#FFFFFF,#FF5733,#D3D3D3",
            "gui_fonts": "Arial 12,Times 14,ComicSans 10"
        }
        ConfigHandler.config["TTS Settings"] = {
            "tts_enabled": "True",
            "gender": "male",
            "rate": "75",
            "volume": "0.5",
            "repeat": 1
        }
        with open(ConfigHandler.config_file, "w") as file:
            ConfigHandler.config.write(file)

    def get_list(section, option):
        """Gets a list value from the config file."""
        value = ConfigHandler.config.get(section, option, fallback="")
        return [item.strip() for item in value.split(",")] if value else []

    def set_list(section, option, values):
        """Sets a list value in the config file."""
        if section not in ConfigHandler.config:
            ConfigHandler.config[section] = {}
        ConfigHandler.config[section][option] = ",".join(values)

        with open(ConfigHandler.config_file, "w") as file:
            ConfigHandler.config.write(file)
            
    def add_to_list(section, option, value):
        """Adds an item to the list in the config."""
        items = ConfigHandler.get_list(section, option)
        if value not in items:  # Avoid duplicates
            items.append(value)
            ConfigHandler.set_list(section, option, items)
            
    def edit_list_item(section, option, old_value, new_value):
        """Edits an item in the list."""
        items = ConfigHandler.get_list(section, option)
        if old_value in items:
            index = items.index(old_value)
            items[index] = new_value
            ConfigHandler.set_list(section, option, items)

    def delete_from_list(section, option, value):
        """Deletes an item from the list."""
        items = ConfigHandler.get_list(section, option)
        if value in items:
            items.remove(value)
            ConfigHandler.set_list(section, option, items)

    def get_value(section, option):
        """Gets a single value from the config file."""
        return ConfigHandler.config.get(section, option, fallback="")

    def set_value(section, option, value):
        """Sets a single value in the config file."""
        if section not in ConfigHandler.config:
            ConfigHandler.config[section] = {}
        ConfigHandler.config[section][option] = value

        with open(ConfigHandler.config_file, "w") as file:
            ConfigHandler.config.write(file)

    def get_all_settings():
        """Returns all settings in the 'Settings' section as a dictionary."""
        if "Settings" in ConfigHandler.config:
            return {key: value for key, value in ConfigHandler.config["Settings"].items()}
        return {}

    '''Returns a list of all keywords.'''
    def get_keywords():
        return ConfigHandler.get_list(SETTINGS, KEYWORDS)
    
    '''Returns dictionary of TTS Settings'''
    def get_TTS_settings():
        """Returns all TTS settings as a dictionary."""
        if "TTS Settings" in ConfigHandler.config:
            return {key: value for key, value in ConfigHandler.config["TTS Settings"].items()}
        return {}