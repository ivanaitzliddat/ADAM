import os, threading, traceback
import tkinter as tk
from tkinter import messagebox, ttk, font as tkFont

import pyttsx3
import pygame
from config_handler import ConfigHandler
from TTS import TTS

#To request config ini to store the following theme colours:
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 ="#FF934F"
GRAB_ATTENTION_COLOUR_2 ="#C3423F"

class TTS_setup_page(tk.Frame):
    speech_rate_dict = {"fast": 230, "normal": 200, "slow": 150}

    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOUR)
        
        # Create a TTS instance and store it
        self.tts_instance = TTS()

        # Configure grid layout for 3 columns
        self.grid_columnconfigure(0, weight=2)  # Left spacer
        self.grid_columnconfigure(1, weight=3)  # Content column
        self.grid_columnconfigure(2, weight=2)  # Right spacer

        # Header Labels
        self.page_header = tk.Label(
            self,
            text="Text-to-Speech Settings",
            font=("Malgun Gothic Semilight", 38),
            bg=BG_COLOUR
        )
        self.page_header.grid(row=0, column=1, sticky="nsew", pady=(10, 10))

        self.sub_header = tk.Label(
            self,
            text="Please customise the parameters below",
            font=("Malgun Gothic Semilight", 16),
            bg=BG_COLOUR
        )
        self.sub_header.grid(row=1, column=1, sticky="nsew", pady=(0, 20))

        # Second row (Voice and Alert Options)
        self.row1_frame = tk.Frame(self, bg=BG_COLOUR)
        self.row1_frame.grid(row=2, column=1, sticky="nsew", pady=(10, 20))

        # Voice Gender
        tk.Label(self.row1_frame, bg=BG_COLOUR, text="Voice Gender:").pack(side="left", padx=5, pady=5)
        self.voice_gender_var = tk.StringVar(value="male")
        ttk.Combobox(
            self.row1_frame, textvariable=self.voice_gender_var, values=["male", "female"], state="readonly"
        ).pack(side="left", padx=5, pady=5)

        # Volume
        tk.Label(self.row1_frame, bg=BG_COLOUR, text="Volume (1-10):").pack(side="left", padx=5, pady=5)
        self.volume_var = tk.StringVar(value="5")
        tk.Spinbox(self.row1_frame, from_=1, to=10, textvariable=self.volume_var, width=5).pack(side="left", padx=5, pady=5)

        # Speech Rate
        tk.Label(self.row1_frame, bg=BG_COLOUR, text="Speech Rate:").pack(side="left", padx=5, pady=5)
        self.speech_rate_var = tk.StringVar(value="normal")
        ttk.Combobox(
            self.row1_frame, textvariable=self.speech_rate_var, values=["slow", "normal", "fast"], state="readonly"
        ).pack(side="left", padx=5, pady=5)

        # Alert Sound
        tk.Label(self.row1_frame, bg=BG_COLOUR, text="Alert Sound:").pack(side="left", padx=5, pady=5)
        self.alert_sound_var = tk.StringVar(value="buzzer")
        ttk.Combobox(
            self.row1_frame,
            textvariable=self.alert_sound_var,
            values=["buzzer", "alarm", "notification"],
            state="readonly",
        ).pack(side="left", padx=5, pady=5)

        # Third row (Text Input and Simulate Button)
        self.third_row = tk.Frame(self, bg=BG_COLOUR)
        self.third_row.grid(row=3, column=1, sticky="nsew", pady=(10, 20))

        # Text Input
        tk.Label(self.third_row, bg=BG_COLOUR, text="Message:").pack(side="left", padx=5, pady=5)
        self.text_input = tk.Entry(self.third_row, width=50)
        self.text_input.pack(side="left", padx=5, pady=5)

        # Simulate Button
        tk.Button(self.third_row, bg=BG_COLOUR, text="Simulate", command=self.simulate_alert).pack(side="left", padx=5, pady=5)

        # Fourth row (Save Button)
        self.fourth_row = tk.Frame(self, bg=BG_COLOUR)
        self.fourth_row.grid(row=4, column=1, sticky="nsew", pady=(10, 20))

        save_button_font = tkFont.Font(family="Arial", size=16, weight="bold")
        self.save_button = tk.Button(
            self.fourth_row, text="Save", font=save_button_font, command=self.save_tts_settings
        )
        self.save_button.pack(pady=10)

        # Bind the on_resize function to the <Configure> event
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        """Dynamically adjust the layout and font sizes based on window size."""
        # Get the root window (Tk instance)
        root = self.winfo_toplevel()

        # Set the minimum size for the window
        min_width = 820
        min_height = 450
        root.wm_minsize(min_width, min_height)

        # Adjust the page header font size dynamically
        current_width = max(self.winfo_width(), min_width)
        header_font_size = max(16, min(38, current_width // 30))
        self.page_header.config(font=("Malgun Gothic Semilight", header_font_size))

        # Adjust the sub-header font size dynamically
        sub_header_font_size = max(10, min(20, current_width // 50))
        self.sub_header.config(font=("Malgun Gothic Semilight", sub_header_font_size))


    def play_audio_alert(self, sound_file):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def simulate_alert(self):
        text = self.text_input.get().strip() or "This is a default message."
        voice_gender = self.voice_gender_var.get()
        volume = int(self.volume_var.get())/10  # Need to divide by 10 as "volume_var" is in whole numbers whereas pyttsx3's "volume" property uses a range from 0.0 - 1.0
        speech_rate = self.speech_rate_var.get()
        alert_sound = self.alert_sound_var.get()

        self.text_to_speech_with_audio(text = text, voice_gender = voice_gender, volume = volume, speech_rate = speech_rate, alert_sound = alert_sound)

    def text_to_speech_with_audio(self, text, voice_gender, volume, speech_rate, alert_sound):
        alert_sounds_dict = {
            "buzzer": os.path.join(ConfigHandler.dirname, "Sound/buzzer.mp3"),
            "alarm": os.path.join(ConfigHandler.dirname, "Sound/alarm.mp3"),
            "notification": os.path.join(ConfigHandler.dirname, "Sound/notification.mp3"),
        }
        voices = self.tts_instance.tts_engine.getProperty("voices")

        if voice_gender.lower() == "male":
            voice = voices[0].id
        else:
            voice = voices[1].id

        if speech_rate == "fast":
            speech_rate = TTS_setup_page.speech_rate_dict["fast"]
        elif speech_rate == "slow":
            speech_rate = TTS_setup_page.speech_rate_dict["slow"]
        else:
            speech_rate = TTS_setup_page.speech_rate_dict["normal"]

        # Create a dict to store the TTS text and audio parameters
        alert_audio_params_dict = {"text": "This is a test message: "+text, "voice": voice, "volume": volume,
                                   "speech_rate": speech_rate, "alert_sound": alert_sounds_dict.get(alert_sound), "is_saved": False}

        # Clear TTS.alert_queue so that audio alerts with the new keywords can take effect immediately
        with TTS.alert_queue.mutex:
            TTS.alert_queue.queue.clear()

        with TTS.lock:
            # Insert alert_audio_params_dict to start of TTS.alert_queue so it will play immediately after currently-played audio is done
            TTS.alert_queue.put(alert_audio_params_dict)

    def save_tts_settings(self):
        alert_sounds_dict = {
            "buzzer": os.path.join(ConfigHandler.dirname, "Sound/buzzer.mp3"),
            "alarm": os.path.join(ConfigHandler.dirname, "Sound/alarm.mp3"),
            "notification": os.path.join(ConfigHandler.dirname, "Sound/notification.mp3"),
        }
        gender = self.voice_gender_var.get()
        vol = int(self.volume_var.get())/10  # Need to divide by 10 as "volume_var" is in whole numbers whereas pyttsx3's "volume" property uses a range from 0.0 - 1.0
        speech_rate = self.speech_rate_var.get()
        alert_sound = alert_sounds_dict.get(self.alert_sound_var.get())

        if speech_rate == "fast":
            speech_rate = TTS_setup_page.speech_rate_dict["fast"]
        elif speech_rate == "slow":
            speech_rate = TTS_setup_page.speech_rate_dict["slow"]
        else:
            speech_rate = TTS_setup_page.speech_rate_dict["normal"]

        if vol == "":
            messagebox.showwarning("Warning", "Volume cannot be empty!")
        else:
            ConfigHandler.set_cfg_tts(gender = gender, volume = vol, rate = speech_rate, tts_enabled = True)
            ConfigHandler.save_config()
            
            voices = self.tts_instance.tts_engine.getProperty("voices")
            if gender.lower() == "male":
                voice = voices[0].id
            else:
                voice = voices[1].id

            # Create a dict to store the audio parameters
            alert_audio_params_dict = {"text": None, "voice": voice, "volume": vol,
                                   "speech_rate": speech_rate, "alert_sound": alert_sound, "is_saved": True}

            # Clear TTS.alert_queue so that audio alerts with the new audio properties can take effect immediately
            with TTS.alert_queue.mutex:
                TTS.alert_queue.queue.clear()

            with TTS.lock:
                # Insert alert_audio_params_dict to start of TTS.alert_queue so it will play immediately after currently-played audio is done
                TTS.alert_queue.queue.insert(0, alert_audio_params_dict)

                
if __name__ == "__main__":
    root = tk.Tk()
    app = TTS_setup_page(root)
    app = TTS_setup_page(root)
    app.pack(fill="both", expand=True)
    root.mainloop()