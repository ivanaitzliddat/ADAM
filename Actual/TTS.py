import pyttsx3
import queue
import threading
import pygame
import time
from config_handler import ConfigHandler
from subthread_config import Thread_Config

class TTS:

    alert_queue = queue.Queue()
    lock = threading.Lock()

    def __init__(self):
        self.settings = ConfigHandler.get_TTS_settings()
        if not self.settings["tts_enabled"]:
            print("TTS is not enabled!")
            return

        self.engine = pyttsx3.init()

        # Configure the voices
        voices = self.engine.getProperty('voices')
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

    def run(self):
        while Thread_Config.running:
            alert = TTS.alert_queue.get()
            if alert:

                import os
                import sys
                # This if...else needs to occur first before any subsequent references to file directories
                if getattr(sys, 'frozen', False):
                    ''' If the application is run as a bundle, the PyInstaller bootloader
                    extends the sys module by a flag frozen=True and sets the app 
                    path into variable _MEIPASS'.
                    Directory of .exe is in os.path.dirname(sys.executable)'''
                    dirname = os.path.dirname(sys.executable)
                else:
                    dirname = os.path.dirname(__file__)

                pygame.init()
                pygame.mixer.music.load(f"{dirname}\\Sound\\notification.mp3")
                pygame.mixer.music.play()
                time.sleep(3)
                for i in range(int(self.settings["repeat"])):
                    self.engine.say(alert)
                    self.engine.runAndWait()
