import tkinter as tk
from tkinter import ttk, font as tkFont
import pyttsx3
import pygame
from config_handler import ConfigHandler 


class TTSSettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.parent = parent

        self.create_widgets()

    def create_widgets(self):
        # Set the window title
        self.title_label = tk.Label(self, text="Configure Text-to-Speech Settings", font=("Malgun Gothic Semilight", 38))
        self.title_label.pack(pady=20)

        # Voice Gender
        self.voice_gender_var = tk.StringVar(value="male")
        self.voice_gender_label = tk.Label(self, text="Voice Gender:")
        self.voice_gender_label.pack(pady=5)
        self.voice_gender_combo = ttk.Combobox(self, textvariable=self.voice_gender_var, values=["male", "female"], state="readonly")
        self.voice_gender_combo.pack(pady=5)

        # Volume
        self.volume_var = tk.StringVar(value="5")
        self.volume_label = tk.Label(self, text="Volume (1-10):")
        self.volume_label.pack(pady=5)
        self.volume_spinbox = tk.Spinbox(self, from_=1, to=10, textvariable=self.volume_var, width=5)
        self.volume_spinbox.pack(pady=5)

        # Speech Rate
        self.speech_rate_var = tk.StringVar(value="normal")
        self.speech_rate_label = tk.Label(self, text="Speech Rate:")
        self.speech_rate_label.pack(pady=5)
        self.speech_rate_combo = ttk.Combobox(self, textvariable=self.speech_rate_var, values=["slow", "normal", "fast"], state="readonly")
        self.speech_rate_combo.pack(pady=5)

        # Repeat No. Of Times
        self.repeat_var = tk.StringVar(value="1")
        self.repeat_label = tk.Label(self, text="Repeat (1-3):")
        self.repeat_label.pack(pady=5)
        self.repeat_spinbox = tk.Spinbox(self, from_=1, to=3, textvariable=self.repeat_var, width=5)
        self.repeat_spinbox.pack(pady=5)

        # Alert Sound
        self.alert_sound_var = tk.StringVar(value="buzzer")
        self.alert_sound_label = tk.Label(self, text="Alert Sound:")
        self.alert_sound_label.pack(pady=5)
        self.alert_sound_combo = ttk.Combobox(self, textvariable=self.alert_sound_var, values=["buzzer", "alarm", "notification"], state="readonly")
        self.alert_sound_combo.pack(pady=5)

        # Message Input
        self.message_label = tk.Label(self, text="Message:")
        self.message_label.pack(pady=5)
        self.text_input = tk.Entry(self, width=50)
        self.text_input.pack(pady=5)

        # Simulate Button
        self.simulate_button = tk.Button(self, text="Simulate", command=self.simulate_alert)
        self.simulate_button.pack(pady=20)

        # Save button (Third Row)
        save_button_font = tkFont.Font(family="Helvetica", size=26, weight="bold")
        self.save_button_font = tk.Button(self, text="Save", font=save_button_font, command=self.edit_tts_settings)
        self.save_button_font.pack(pady=10)

    def edit_tts_settings(self):
        self.existing_tts_settings = ConfigHandler.get_TTS_settings()
        # print(self.existing_tts_settings)
        ConfigHandler.edit_list_item("TTS Settings", "gender", self.existing_tts_settings["gender"], self.voice_gender_var.get())
        ConfigHandler.edit_list_item("TTS Settings", "volume", self.existing_tts_settings["volume"], self.volume_var.get())
        if(self.speech_rate_var.get() == "slow"):
            ConfigHandler.edit_list_item("TTS Settings", "rate", self.existing_tts_settings["rate"], "25")
        elif(self.speech_rate_var.get() == "normal"):
            ConfigHandler.edit_list_item("TTS Settings", "rate", self.existing_tts_settings["rate"], "50")
        elif(self.speech_rate_var.get() == "fast"):
            ConfigHandler.edit_list_item("TTS Settings", "rate", self.existing_tts_settings["rate"], "75")
        ConfigHandler.edit_list_item("TTS Settings", "repeat", self.existing_tts_settings["repeat"], self.repeat_var.get())


    def play_audio_alert(self, sound_file):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def simulate_alert(self):
        text = self.text_input.get().strip() or "This is a default message."
        voice_gender = self.voice_gender_var.get()
        volume = int(self.volume_var.get())
        speech_rate = self.speech_rate_var.get()
        alert_sound = self.alert_sound_var.get()

        self.text_to_speech_with_audio(text, voice_gender, volume, speech_rate, alert_sound)

    def text_to_speech_with_audio(self, text, voice_gender="male", volume=5, speech_rate="normal", alert_sound="buzzer"):
        alert_sounds = {
            "buzzer": r"C:\Users\user\Desktop\ADAM\Sound\alarm.mp3",
            "alarm": r"C:\Users\user\Desktop\ADAM\Sound\buzzer.mp3",
            "notification": r"C:\Users\user\Desktop\ADAM\Sound\notification.mp3",
        }

        sound_file = alert_sounds.get(alert_sound)
        self.play_audio_alert(sound_file)

        engine = pyttsx3.init()
        voices = engine.getProperty("voices")

        engine.setProperty("voice", voices[0].id if voice_gender == "male" else voices[1].id)
        engine.setProperty("volume", volume / 10)
        rate = engine.getProperty("rate")
        engine.setProperty("rate", rate + (50 if speech_rate == "fast" else -50 if speech_rate == "slow" else 0))

        engine.say(text)
        engine.runAndWait()
