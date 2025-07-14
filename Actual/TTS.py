import queue, os, time, threading, traceback
import comtypes.client
comtypes.CoInitialize()  # Ensure COM library is initialised before using COM-based libraries like pyttsx3. Required for WinPython/embedded Python.

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
        self.tts_engine.setProperty('rate', self.settings["rate"])

        # Configure the volume
        self.tts_engine.setProperty('volume', float(self.settings["volume"]))

        # Configure the sound clip
        self.sound_clip_path = os.path.join(ConfigHandler.dirname, self.settings["sound_clip"])
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.sound_clip_path)
        except Exception as e:
            print(f"Failed with error: {e}")


    def run(self):
        while Thread_Config.running:
            alert = TTS.alert_queue.get()
            if alert:
                # Check if alert is a dict. It will be a dict if tts_settings_page.py is used to change TTS and audio properties.
                if isinstance(alert, dict):
                    alert_text = alert["text"]
                    alert_voice = alert["voice"]
                    alert_volume = alert["volume"]
                    alert_speech_rate = alert["speech_rate"]
                    alert_sound = alert["alert_sound"]

                    # Check if the TTS and audio properties have been saved or not to config.ini in tts_settings_page.py
                    # "is_saved" is False if the TTS and audio properties were not saved, which means user only pressed the "Simulate" button to play test message using modified TTS and audio properties
                    if alert["is_saved"] == False:
                        initial_voice = self.tts_engine.getProperty('voice')
                        initial_volume = self.tts_engine.getProperty('volume')
                        initial_speech_rate = self.tts_engine.getProperty('rate')
                        initial_alert_sound = self.sound_clip_path

                        # Load the temporary new alert sound clip and play it
                        pygame.mixer.music.load(os.path.join(ConfigHandler.dirname, alert_sound))
                        pygame.mixer.music.play()
                        time.sleep(3)

                        if self.tts_engine._inLoop:
                            self.tts_engine.endLoop()    # Ends the existing engine loop that was created on the previous call of .runAndWait()
                    
                        # Set tts_engine to use the temporary new audio properties
                        self.tts_engine.setProperty('voice', alert_voice)
                        self.tts_engine.setProperty('volume', alert_volume)
                        self.tts_engine.setProperty('rate', alert_speech_rate)

                        self.tts_engine.say(alert_text)    # Need to call .say() again 
                        self.tts_engine.runAndWait()

                        if self.tts_engine._inLoop:
                            self.tts_engine.endLoop()   # Ends the existing engine loop that was created on the previous call of .runAndWait()
                    
                        # Set the audio parameters back to previous setting
                        self.tts_engine.setProperty('voice', initial_voice)
                        self.tts_engine.setProperty('volume', initial_volume)
                        self.tts_engine.setProperty('rate', initial_speech_rate)

                    # "is_saved" is True if the TTS and audio properties were saved, which means user pressed the "Save" button.
                    # Hence, set self.sound_clip_path and tts_engine properties to the newly-saved values.
                    elif alert["is_saved"] == True:
                        self.sound_clip_path = os.path.join(ConfigHandler.dirname, alert_sound)
                        pygame.mixer.music.load(self.sound_clip_path)

                        if self.tts_engine._inLoop:
                            self.tts_engine.endLoop()    # Ends the existing engine loop that was created on the previous call of .runAndWait()

                        # Set tts_engine to use the permanent new audio properties
                        self.tts_engine.setProperty('voice', alert_voice)
                        self.tts_engine.setProperty('volume', alert_volume)
                        self.tts_engine.setProperty('rate', alert_speech_rate)
                # Else (alert is not a dict), then just play TTS and audio clip using existing settings.
                else:
                    pygame.mixer.music.load(self.sound_clip_path)
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
                    
