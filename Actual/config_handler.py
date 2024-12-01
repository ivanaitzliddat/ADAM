import configparser
import os


class ConfigHandler:
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config_file = config_file

        # Check if the file exists, if not, create it
        if not os.path.exists(self.config_file):
            self._create_default_config()
        else:
            self.config.read(self.config_file)

    def _create_default_config(self):
        """Creates a default config file."""
        self.config["Settings"] = {
            "keywords": "example,default,config",
            "colors": "#FFFFFF,#FF5733,#D3D3D3",
            "tts_enabled": "True",
            "gui_fonts": "Arial 12,Times 14,ComicSans 10"
        }
        with open(self.config_file, "w") as file:
            self.config.write(file)

    def get_list(self, section, option):
        """Gets a list value from the config file."""
        value = self.config.get(section, option, fallback="")
        return [item.strip() for item in value.split(",")] if value else []

    def set_list(self, section, option, values):
        """Sets a list value in the config file."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][option] = ",".join(values)

        with open(self.config_file, "w") as file:
            self.config.write(file)
            
    def add_to_list(self, section, option, value):
        """Adds an item to the list in the config."""
        items = self.get_list(section, option)
        if value not in items:  # Avoid duplicates
            items.append(value)
            self.set_list(section, option, items)
            
    def edit_list_item(self, section, option, old_value, new_value):
        """Edits an item in the list."""
        items = self.get_list(section, option)
        if old_value in items:
            index = items.index(old_value)
            items[index] = new_value
            self.set_list(section, option, items)

    def delete_from_list(self, section, option, value):
        """Deletes an item from the list."""
        items = self.get_list(section, option)
        if value in items:
            items.remove(value)
            self.set_list(section, option, items)

    def get_value(self, section, option):
        """Gets a single value from the config file."""
        return self.config.get(section, option, fallback="")

    def set_value(self, section, option, value):
        """Sets a single value in the config file."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][option] = value

        with open(self.config_file, "w") as file:
            self.config.write(file)

    def get_all_settings(self):
        """Returns all settings in the 'Settings' section as a dictionary."""
        if "Settings" in self.config:
            return {key: value for key, value in self.config["Settings"].items()}
        return {}


# Usage Example
"""
if __name__ == "__main__":
    config_handler = ConfigHandler()

    # Get a list from the config
    keywords = config_handler.get_list("Settings", "keywords")
    print("Keywords:", keywords)

    # Add a new keyword and save
    keywords.append("new_keyword")
    config_handler.set_list("Settings", "keywords", keywords)
    print("Updated Keywords:", config_handler.get_list("Settings", "keywords"))

    # Get and update a single value
    tts_enabled = config_handler.get_value("Settings", "tts_enabled")
    print("TTS Enabled:", tts_enabled)
    config_handler.set_value("Settings", "tts_enabled", "False")
    """
