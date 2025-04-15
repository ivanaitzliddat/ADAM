import queue, os, time, threading, traceback

import pyttsx3
import pygame
from config_handler import ConfigHandler
from subthread_config import Thread_Config

class TTS:
    alert_queue = queue.Queue()
    lock = threading.Lock()

    def __init__(self):
        self.settings = ConfigHandler.get_cfg_tts()
        if not self.settings["tts_enabled"]:
            print("TTS is not enabled!")
            return

        # Initialise pyttsx3 and pygame
        self.tts_engine = pyttsx3.init()
        pygame.init()

        # Configure the voices
        voices = self.tts_engine.getProperty('voices')
        if self.settings["gender"].lower() == "male":
            self.tts_engine.setProperty('voice', voices[0].id)
        else:
            self.tts_engine.setProperty('voice', voices[1].id)

        # Configure the rate
        if self.settings["rate"] == "slow":
            self.tts_engine.setProperty('rate', 25)
        elif self.settings["rate"] == "fast":
            self.tts_engine.setProperty('rate', 75)

        # Configure the volume
        self.tts_engine.setProperty('volume', self.settings["volume"])

        # Configure the sound clip
        pygame.mixer.music.load(os.path.join(ConfigHandler.dirname,  self.settings["sound_clip"]))

    def run(self):
        while Thread_Config.running:
            alert = TTS.alert_queue.get()
            if alert:
                pygame.mixer.music.load(os.path.join(ConfigHandler.dirname,  self.settings["sound_clip"]))
                pygame.mixer.music.play()
                time.sleep(3)
                for i in range(int(self.settings["repeat"])):
                    self.tts_engine.say(alert)

                    try:
                        # .runAndWait() blocks code from running after it until its event loop queue is cleared.
                        # However, its event loop queue never seems to clear, so it blocks indefinitely and makes it impossible to stop with .endLoop().
                        self.tts_engine.runAndWait() 
                    except RuntimeError:    # engine throws RuntimeError on subsequent calls to .runAndWait() as the engine loop already exists.
                        if self.tts_engine._inLoop:
                            self.tts_engine.endLoop()    # Ends the existing engine loop that was created on the previous call of .runAndWait()
                            self.tts_engine.say(alert)    # Need to call .say() again 
                            self.tts_engine.runAndWait()
                    except:
                        traceback.print_exc()
                    