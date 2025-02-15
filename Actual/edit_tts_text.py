import tkinter as tk
from tkinter import messagebox
from config_handler import ConfigHandler
import pyttsx3
import pygame

class Edit_TTS_Text_Page:
    def __init__(self, root, usb_alt_name, condition, tts_message, callback):
        self.root = root
        self.root.geometry("900x500")
        self.usb_alt_name = usb_alt_name
        self.condition = condition
        self.callback = callback
        self.tts_message = tts_message
        # Center the window after initializing
        self.root.after(0, self.center_window)
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title(f"Edit Text-to-Speech Message for {self.usb_alt_name} - {self.condition}")
        configure_TTS_frame = tk.Frame(self.root, width=1000, pady=5)
        configure_TTS_frame.pack(fill="y", pady=5)
        
        # 1st Row: Header
        header_frame = tk.Frame(configure_TTS_frame, pady=5)
        header_frame.pack(fill="x", pady=5)
        header_label = tk.Label(header_frame, text="Configure Text-to-Speech Message", font=("Arial", 14, "bold"))
        sub_header_label = tk.Label(header_frame, text="Message you want ADAM to read out when the trigger condition hits", font=("Arial", 7))
        header_label.pack()
        sub_header_label.pack()

        # 2nd Row: TTS Label and TTS Entry
        tts_label = tk.Label(configure_TTS_frame, text="TTS Message:")
        tts_label.pack(fill="x", expand=True, padx=5, pady=5)

        self.tts_entry = tk.Entry(configure_TTS_frame, width=100)
        self.tts_entry.insert(0, self.tts_message)
        self.tts_entry.pack(fill="x", expand=True, padx=5, pady=5)

        #retrieve the TTS settings from the config file
        tts_settings = ConfigHandler.get_cfg_tts()

        voice_gender = tts_settings['gender']
        speech_rate = tts_settings['rate']
        volume = tts_settings['volume']

        # 3rd Row: To store the button to test TTS readout
        test_tts_button = tk.Button(configure_TTS_frame, text="Readout the message", command=lambda: self.test_tts(voice_gender,speech_rate,volume))
        test_tts_button.pack(fill="x", expand=True, padx=5, pady=5)

        # 4th Row: Frame for Save and Cancel buttons
        button_frame = tk.Frame(configure_TTS_frame, pady=5)
        button_frame.pack(fill="x", pady=5)

        # Inner frame to centralize buttons
        inner_button_frame = tk.Frame(button_frame)
        inner_button_frame.pack(expand=True)

        save_button = tk.Button(inner_button_frame, text="Save", command=lambda: self.save_tts_text())
        save_button.pack(side="left", padx=20, pady=5)

        cancel_button = tk.Button(inner_button_frame, text="Cancel", command=lambda: self.cancel())
        cancel_button.pack(side="right", padx=20, pady=5)
    
    def save_tts_text(self):
        self.tts_text = self.tts_entry.get().strip()
        print(self.tts_text)
        ConfigHandler.set_cfg_input_device(usb_alt_name=self.usb_alt_name, condition=self.condition, tts_text=self.tts_text)
        ConfigHandler.save_config()
        self.root.destroy()
        self.callback()
   

    def cancel(self):
        self.root.destroy()

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
    
    def test_tts(self, voice_gender,speech_rate,volume, alert_sound="buzzer"):
        text_message = self.tts_entry.get().strip() or "No custom message set. ADAM will read out default message."
        #alert_sounds = {
        #    "buzzer": r"C:\Users\\bai_j\Desktop\\ADAM-main\\Testing\\GUI testing\\sound\\alarm.mp3",
        #    "alarm": r"C:\Users\\bai_j\Desktop\\ADAM-main\\Testing\\GUI testing\\sound\\alarm.mp3",
        #    "notification": r"C:\Users\\bai_j\Desktop\\ADAM-main\\Testing\\GUI testing\\sound\\alarm.mp3"}
        alert_sounds = {
            "buzzer": ConfigHandler.dirname()+'\\Testing\\GUI testing\\sound\\buzzer.mp3',
            "alarm": ConfigHandler.dirname()+"\\Testing\\GUI testing\\sound\\alarm.mp3",
            "notification": ConfigHandler.dirname()+"\\Testing\\GUI testing\\sound\\notification.mp3",
        }
        
        sound_file = alert_sounds.get(alert_sound)
        self.play_audio_alert(sound_file)

        engine = pyttsx3.init()
        voices = engine.getProperty("voices")

        engine.setProperty("voice", voices[0].id if voice_gender == "male" else voices[1].id)
        engine.setProperty("volume", volume)
        engine.setProperty("rate", speech_rate)

        engine.say(text_message)
        engine.runAndWait()

def edit_tts_text(alt_name, condition, tts_message, callback):
    root = tk.Tk()
    app = Edit_TTS_Text_Page(root, alt_name, condition, tts_message, callback)
    root.mainloop()