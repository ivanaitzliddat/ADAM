from config_handler import ConfigHandler
import ast
ConfigHandler.init()

trigger_dict = (ConfigHandler.get_triggers())
#print(type(trigger_dict["device0"]))
#print(trigger_dict["device0"])

for key, value in trigger_dict.items():
    print("Key is = " + key)
    print("Value = " + value)   # value is in String format
    print("Value in dict format is")
    print(ast.literal_eval(value))  # Convert String value with dict structure into a dict with ast.literal_eval
