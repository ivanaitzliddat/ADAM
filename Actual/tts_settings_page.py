import tkinter as tk
from tkinter import ttk, font as tkFont
import pyttsx3
import pygame
from config_handler import ConfigHandler
import threading, traceback
from tkinter import messagebox

#To request config ini to store the following theme colours:
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 ="#FF934F"
GRAB_ATTENTION_COLOUR_2 ="#C3423F"

class TTS_setup_page(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOUR)

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
        try:
            # .runAndWait() blocks code from running after it until its event loop queue is cleared.
            # However, its event loop queue never seems to clear, so it blocks indefinitely and makes it impossible to stop with .endLoop().
            engine.runAndWait() 
        except RuntimeError:    # engine throws RuntimeError on subsequent calls to .runAndWait() as the engine loop already exists.
            if engine._inLoop:
                engine.endLoop()    # Ends the existing engine loop that was created on the previous call of .runAndWait()
                engine.say(text)    # Need to call .say() again 
                engine.runAndWait()
        except:
            traceback.print_exc()

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
    app = TTS_setup_page(root)
    app = TTS_setup_page(root)
    app.pack(fill="both", expand=True)
    root.mainloop()