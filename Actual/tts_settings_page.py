import tkinter as tk
from tkinter import ttk, font as tkFont
import pyttsx3
import pygame
from config_handler import ConfigHandler
import threading

#o request config ini to store the following theme colours:
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 ="#FF934F"
GRAB_ATTENTION_COLOUR_2 ="#C3423F"

class TTS_setup_page(tk.Frame):
    def __init__(self, parent):

        super().__init__(parent,bg=BG_COLOUR)
        #ConfigHandler.init() #for testing purposes, to be removed once done

        # Create the main frame
        self.frame = tk.Frame(self, bg=BG_COLOUR)
        self.frame.pack(pady=20)

        # Create rows
        self.first_row = tk.Frame(self.frame, bg=BG_COLOUR)
        self.first_row.pack(fill="both")

        self.second_row = tk.Frame(self.frame, bg=BG_COLOUR)
        self.second_row.pack(fill="both")

        self.third_row = tk.Frame(self.frame, bg=BG_COLOUR)
        self.third_row.pack(fill="both")

        # Logo (First Row)
        tk.Label(
            self.first_row,
            text="Text-to-Speech Settings",
            font=("Malgun Gothic Semilight", 38),
            bg=BG_COLOUR
        ).pack()
        tk.Label(
            self.first_row,
            text="Please customise the parameters below",
            font=("Malgun Gothic Semilight", 16),
            bg=BG_COLOUR
        ).pack()

        # Row 1: Voice and Alert Options
        self.row1_frame = tk.Frame(self.second_row, pady=10, bg=BG_COLOUR)
        self.row1_frame.grid(row=0, column=0, sticky="ew")

        # Voice Gender
        tk.Label(self.row1_frame, bg=BG_COLOUR, text="Voice Gender:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.voice_gender_var = tk.StringVar(value="male")
        ttk.Combobox(
            self.row1_frame, textvariable=self.voice_gender_var, values=["male", "female"], state="readonly"
        ).grid(row=0, column=1, padx=5, pady=5)

        # Volume
        tk.Label(self.row1_frame, bg=BG_COLOUR, text="Volume (1-10):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.volume_var = tk.StringVar(value="5")
        tk.Spinbox(self.row1_frame, from_=1, to=10, textvariable=self.volume_var, width=5).grid(
            row=0, column=3, padx=5, pady=5
        )

        # Speech Rate
        tk.Label(self.row1_frame, bg=BG_COLOUR, text="Speech Rate:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.speech_rate_var = tk.StringVar(value="normal")
        ttk.Combobox(
            self.row1_frame, textvariable=self.speech_rate_var, values=["slow", "normal", "fast"], state="readonly"
        ).grid(row=0, column=5, padx=5, pady=5)

        # Alert Sound
        tk.Label(self.row1_frame, bg=BG_COLOUR, text="Alert Sound:").grid(row=0, column=6, padx=5, pady=5, sticky="w")
        self.alert_sound_var = tk.StringVar(value="buzzer")
        ttk.Combobox(
            self.row1_frame,
            textvariable=self.alert_sound_var,
            values=["buzzer", "alarm", "notification"],
            state="readonly",
        ).grid(row=0, column=7, padx=5, pady=5)

        # Row 2: Text Input and Simulate Button
        row2_frame = tk.Frame(self.second_row, pady=10, bg=BG_COLOUR)
        row2_frame.grid(row=1, column=0, sticky="ew")

        # Text Input
        tk.Label(row2_frame, bg=BG_COLOUR, text="Message:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.text_input = tk.Entry(row2_frame, width=50)
        self.text_input.grid(row=0, column=1, padx=5, pady=5)

        # Simulate Button
        tk.Button(row2_frame, bg=BG_COLOUR, text="Simulate", command=self.simulate_alert).grid(
            row=0, column=2, padx=5, pady=5
        )

        # Save button (Third Row)
        save_button_font = tkFont.Font(family="Helvetica", size=26, weight="bold")
        self.save_button_font = tk.Button(self.third_row, text="Save", font=save_button_font, command=lambda: self.save_tts_settings())
        self.save_button_font.pack(pady=10)

    def play_audio_alert(self, sound_file):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def simulate_alert(self):
        # Run text-to-speech and audio alert in a separate thread
        thread = threading.Thread(target=self._simulate_alert_thread)
        thread.start()

    def _simulate_alert_thread(self):
        text = self.text_input.get().strip() or "This is a default message."
        voice_gender = self.voice_gender_var.get()
        volume = int(self.volume_var.get())
        speech_rate = self.speech_rate_var.get()
        alert_sound = self.alert_sound_var.get()        
        self.text_to_speech_with_audio(text, voice_gender, volume, speech_rate, alert_sound)

    def text_to_speech_with_audio(self, text, voice_gender="male", volume=5, speech_rate="normal", alert_sound="buzzer"):
        alert_sounds = {
            "buzzer": ConfigHandler.dirname+"\\Sound\\alarm.mp3",
            "alarm": ConfigHandler.dirname+"\\Sound\\buzzer.mp3",
            "notification": ConfigHandler.dirname+"\\Sound\\notification.mp3",
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

    def save_tts_settings(self):
        gender = self.voice_gender_var.get()
        vol = self.volume_var.get()
        speech_rate = self.speech_rate_var.get()
        
        if speech_rate == "fast":
            speech_rate = 50
        elif speech_rate == "normal":
            speech_rate = 0
        else:
            speech_rate = -50

        if vol == "":
            messagebox.showwarning("Warning", "Volume cannot be empty!")
        else:
            ConfigHandler.set_cfg_tts(gender = gender, volume = vol, rate = speech_rate, tts_enabled = True)
            ConfigHandler.save_config()

                
if __name__ == "__main__":
    root = tk.Tk()
    app = TTS_setup_page(root, lambda page: print(f"switch to {page}"))
    app.pack(fill="both", expand = True)
    root.mainloop()
