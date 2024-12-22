import pyttsx3
from config_handler import ConfigHandler

class TTS:
    def __init__(self):

        self.settings = ConfigHandler.get_TTS_settings()
        print(self.settings)
        if not self.settings["tts_enabled"]:
            print("TTS is not enabled!")
            return

        self.engine = pyttsx3.init()

        # Configure the voices
        voices = self.engine.getProperty('voices')
        print(voices)
        if self.settings["gender"].lower() == "male":
            self.engine.setProperty('voice', voices[0].id)
        else:
            self.engine.setProperty('voice', voices[1].id)

        # Configure the rate
        if self.settings["rate"] == "slow":
            self.engine.setProperty('rate', 25)
        elif self.settings["rate"] == "fast":
            self.engine.setProperty('rate', 75)

        # Configure the volume
        self.engine.setProperty('volume', self.settings["volume"])

    def run(self, text):
        for i in range(int(self.settings["repeat"])):
            self.engine.say(text)
            self.engine.runAndWait()
        
'''# Speak the text
ConfigHandler.init()
text = "Hello! This is pyttsx3 speaking offline."
engine = TTS()
engine.run(text)'''

