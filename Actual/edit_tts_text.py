import os, threading, traceback
import tkinter as tk
from tkinter import messagebox

import pyttsx3
import pygame
from config_handler import ConfigHandler
from TTS import TTS


class Edit_TTS_Text_Page:
    def __init__(self, root, usb_alt_name, condition, tts_message, custom_name, callback):
        self.root = root
        self.root.geometry("900x500")
        self.usb_alt_name = usb_alt_name
        self.condition = condition
        self.callback = callback
        self.tts_message = tts_message
        self.custom_name = custom_name

        self.root.grab_set()
        self.root.focus_set()

        # Center the window after initializing
        self.root.after(0, self.center_window)
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title(f"Edit Text-to-Speech Message for {self.custom_name} - {self.condition}")
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
        test_tts_button = tk.Button(configure_TTS_frame, text="Readout the message", command=lambda: self.test_tts_alert(voice_gender,speech_rate,volume))
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
        self.root.grab_release()
        self.root.destroy()
        self.callback()

    def cancel(self):
        self.root.grab_release()
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
    
    ''' #TODO: This function may not be needed anymore as the audio is now riding on the existing TTS thread to prevent sound clip and TTS inconsistencies.
    def test_tts(self,voice_gender,speech_rate,volume, alert_sound="buzzer"):
        # Run text-to-speech and audio alert in a separate thread
        thread = threading.Thread(target=self._test_tts_alert_thread, args=(voice_gender,speech_rate,volume, alert_sound))
        thread.start()
    '''

    def test_tts_alert(self, voice_gender,speech_rate,volume, alert_sound="buzzer"):
        text_message = self.tts_entry.get().strip() or "No custom message set. ADAM will read out default message."
        #alert_sounds = {
        #    "buzzer": r"C:\Users\\bai_j\Desktop\\ADAM-main\\Testing\\GUI testing\\sound\\alarm.mp3",
        #    "alarm": r"C:\Users\\bai_j\Desktop\\ADAM-main\\Testing\\GUI testing\\sound\\alarm.mp3",
        #    "notification": r"C:\Users\\bai_j\Desktop\\ADAM-main\\Testing\\GUI testing\\sound\\alarm.mp3"}
        alert_sounds = {
            "buzzer": os.path.join(ConfigHandler.dirname, "Sound/buzzer.mp3"),
            "alarm": os.path.join(ConfigHandler.dirname, "Sound/alarm.mp3"),
            "notification": os.path.join(ConfigHandler.dirname, "Sound/notification.mp3"),
        }
        ''' #TODO: This commented-out code may not be needed anymore as the audio settings are using those specified in TTS.py class.
        sound_file = alert_sounds.get(alert_sound)
        self.play_audio_alert(sound_file)

        engine = pyttsx3.init()
        voices = engine.getProperty("voices")

        engine.setProperty("voice", voices[0].id if voice_gender == "male" else voices[1].id)
        engine.setProperty("volume", volume)
        engine.setProperty("rate", speech_rate)
        '''
        with TTS.lock:
            # Insert text_message to start of TTS.alert_queue so it will play immediately after currently-played audio is done
            TTS.alert_queue.queue.insert(0, "This is a test message: "+text_message)

def edit_tts_text(alt_name, condition, tts_message, custom_name, callback):
    root = tk.Toplevel()
    app = Edit_TTS_Text_Page(root, alt_name, condition, tts_message, custom_name, callback)
    root.transient()
    root.wait_window(root)