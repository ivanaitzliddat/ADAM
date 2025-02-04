import tkinter as tk
from tkinter import ttk, font as tkFont
import pyttsx3
import pygame


class VideoCaptureSetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to ADAM")
        self.root.geometry("1920x1080")

        # Main frame
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        # Create rows
        self.first_row = tk.Frame(self.frame)
        self.first_row.pack(fill="both")

        self.second_row = tk.Frame(self.frame)
        self.second_row.pack(fill="both")

        self.third_row = tk.Frame(self.frame)
        self.third_row.pack(fill="both")

        # Logo (First Row)
        tk.Label(
            self.first_row,
            text="Configure Text-to-Speech Settings",
            font=("Malgun Gothic Semilight", 38),
        ).pack()
        tk.Label(
            self.first_row,
            text="Don't worry, you can setup again later...",
            font=("Malgun Gothic Semilight", 16),
        ).pack()

        # Center the window after initializing
        self.root.after(100, self.center_window)

        # Row 1: Voice and Alert Options
        row1_frame = tk.Frame(self.second_row, pady=10)
        row1_frame.grid(row=0, column=0, sticky="ew")

        # Voice Gender
        tk.Label(row1_frame, text="Voice Gender:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.voice_gender_var = tk.StringVar(value="male")
        ttk.Combobox(
            row1_frame, textvariable=self.voice_gender_var, values=["male", "female"], state="readonly"
        ).grid(row=0, column=1, padx=5, pady=5)

        # Volume
        tk.Label(row1_frame, text="Volume (1-10):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.volume_var = tk.StringVar(value="5")
        tk.Spinbox(row1_frame, from_=1, to=10, textvariable=self.volume_var, width=5).grid(
            row=0, column=3, padx=5, pady=5
        )

        # Speech Rate
        tk.Label(row1_frame, text="Speech Rate:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.speech_rate_var = tk.StringVar(value="normal")
        ttk.Combobox(
            row1_frame, textvariable=self.speech_rate_var, values=["slow", "normal", "fast"], state="readonly"
        ).grid(row=0, column=5, padx=5, pady=5)

        # Alert Sound
        tk.Label(row1_frame, text="Alert Sound:").grid(row=0, column=6, padx=5, pady=5, sticky="w")
        self.alert_sound_var = tk.StringVar(value="buzzer")
        ttk.Combobox(
            row1_frame,
            textvariable=self.alert_sound_var,
            values=["buzzer", "alarm", "notification"],
            state="readonly",
        ).grid(row=0, column=7, padx=5, pady=5)

        # Row 2: Text Input and Simulate Button
        row2_frame = tk.Frame(self.second_row, pady=10)
        row2_frame.grid(row=1, column=0, sticky="ew")

        # Text Input
        tk.Label(row2_frame, text="Message:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.text_input = tk.Entry(row2_frame, width=50)
        self.text_input.grid(row=0, column=1, padx=5, pady=5)

        # Simulate Button
        tk.Button(row2_frame, text="Simulate", command=self.simulate_alert).grid(
            row=0, column=2, padx=5, pady=5
        )

        # Save button (Third Row)
        save_button_font = tkFont.Font(family="Helvetica", size=26, weight="bold")
        self.save_button_font = tk.Button(self.third_row, text="Save", font=save_button_font)
        self.save_button_font.pack(pady=10)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

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


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCaptureSetupApp(root)
    root.mainloop()
