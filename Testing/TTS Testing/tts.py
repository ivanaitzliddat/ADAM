import tkinter as tk
from tkinter import ttk
import pyttsx3
import pygame

def play_audio_alert(sound_file):
    """
    Play an audio alert using pygame.
    """
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load(sound_file)  # Load the sound file
    pygame.mixer.music.play()  # Play the sound file
    while pygame.mixer.music.get_busy():  # Wait for the sound to finish
        continue

def text_to_speech_with_audio(text, voice_gender="male", volume=5, speech_rate="normal", alert_sound="buzzer"):
    """
    Text-to-Speech function with a short audio alert played first.
    """
    # Define alert sound file paths
    alert_sounds = {
        "buzzer": r"C:\Users\bai_j\Desktop\ADAM-main\Actual\TTS\buzzer.mp3",
        "alarm": r"C:\Users\bai_j\Desktop\ADAM-main\Actual\TTS\alarm.mp3",
        "notification": r"C:\Users\bai_j\Desktop\ADAM-main\Actual\TTS\notification.mp3"
    }

    # Get the correct alert sound file path
    sound_file = alert_sounds.get(alert_sound)
    play_audio_alert(sound_file)

    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Set voice based on gender
    if voice_gender == "male":
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)

    # Set volume (scale from 0.1 to 1.0)
    engine.setProperty('volume', volume / 10)

    # Set speech rate
    rate = engine.getProperty('rate')
    if speech_rate == "slow":
        engine.setProperty('rate', rate - 50)
    elif speech_rate == "fast":
        engine.setProperty('rate', rate + 50)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

def simulate_alert():
    """
    Function called when "Simulate" button is clicked.
    Plays a short alert sound, followed by text-to-speech.
    """
    text = text_input.get().strip()
    if not text:
        text = "Alert detected"  # Default message

    # Get user-selected values from the interface
    voice_gender = voice_gender_var.get()
    volume = int(volume_var.get())
    speech_rate = speech_rate_var.get()
    alert_sound = alert_sound_var.get()

    # Play alert sound followed by text-to-speech
    text_to_speech_with_audio(text, voice_gender, volume, speech_rate, alert_sound)

# Create the main Tkinter window
root = tk.Tk()
root.title("Audio Alert Simulator")

# Row 1: Voice and Alert Options
row1_frame = ttk.Frame(root, padding="10")
row1_frame.grid(row=0, column=0, sticky="ew")

# Voice Gender
ttk.Label(row1_frame, text="Voice Gender:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
voice_gender_var = tk.StringVar(value="male")
ttk.Combobox(row1_frame, textvariable=voice_gender_var, values=["male", "female"], state="readonly").grid(row=0, column=1, padx=5, pady=5)

# Volume
ttk.Label(row1_frame, text="Volume (1-10):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
volume_var = tk.StringVar(value="5")
ttk.Spinbox(row1_frame, from_=1, to=10, textvariable=volume_var, width=5).grid(row=0, column=3, padx=5, pady=5)

# Speech Rate
ttk.Label(row1_frame, text="Speech Rate:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
speech_rate_var = tk.StringVar(value="normal")
ttk.Combobox(row1_frame, textvariable=speech_rate_var, values=["slow", "normal", "fast"], state="readonly").grid(row=0, column=5, padx=5, pady=5)

# Alert Sound
ttk.Label(row1_frame, text="Alert Sound:").grid(row=0, column=6, padx=5, pady=5, sticky="w")
alert_sound_var = tk.StringVar(value="buzzer")
ttk.Combobox(row1_frame, textvariable=alert_sound_var, values=["buzzer", "alarm", "notification"], state="readonly").grid(row=0, column=7, padx=5, pady=5)

# Row 2: Text Input and Simulate Button
row2_frame = ttk.Frame(root, padding="10")
row2_frame.grid(row=1, column=0, sticky="ew")

# Text Input
ttk.Label(row2_frame, text="Message:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
text_input = tk.Entry(row2_frame, width=50)
text_input.grid(row=0, column=1, padx=5, pady=5)

# Simulate Button
simulate_button = ttk.Button(row2_frame, text="Simulate", command=simulate_alert)
simulate_button.grid(row=0, column=2, padx=5, pady=5)

# Start the Tkinter main loop
root.mainloop()
