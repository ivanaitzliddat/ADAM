import configparser
import threading
import os

class ConfigHandler:
    config_file = "config.ini"
    config = configparser.ConfigParser()
    lock = threading.Lock()

    def init():
        # Check if the file exists, if not, create it
        if not os.path.exists(ConfigHandler.config_file):
            ConfigHandler.create_default_config()
            print("A new config.ini has been created.")
        else:
            ConfigHandler.config.read(ConfigHandler.config_file)
            print("Read from config.ini.")

    def create_default_config():
        """Creates a default config file."""
        ConfigHandler.config["Settings"] = {
            "keywords": "",
            "colors": "#FFFFFF,#FF5733,#D3D3D3",
            "tts_enabled": "True",
            "gui_fonts": "Arial 12,Times 14,ComicSans 10"
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

'''# Usage Example
if __name__ == "__main__":
    ConfigHandler.init()

    # Get a list from the config
    keywords = ConfigHandler.get_list("Settings", "keywords")
    print("Keywords:", keywords)

    # Add a new keyword and save
    keywords.append("new_keyword")
    ConfigHandler.set_list("Settings", "keywords", keywords)
    print("Updated Keywords:", ConfigHandler.get_list("Settings", "keywords"))

    # Get and update a single value
    tts_enabled = ConfigHandler.get_value("Settings", "tts_enabled")
    print("TTS Enabled:", tts_enabled)
    ConfigHandler.set_value("Settings", "tts_enabled", "False")'''
