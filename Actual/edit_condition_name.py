import tkinter as tk
from tkinter import messagebox
from config_handler import ConfigHandler
import pyttsx3
import pygame

class edit_condition_name_page:
    def __init__(self, root, usb_alt_name, condition, condition_name, callback):
        self.root = root
        self.root.geometry("900x500")
        self.usb_alt_name = usb_alt_name
        self.callback = callback
        self.condition = condition
        self.current_condition_name = condition_name

        self.root.grab_set()
        self.root.focus_set()

        # Center the window after initializing
        self.root.after(0, self.center_window)
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title(f"Change the Condition Name for {self.current_condition_name}")
        configure_condition_name_frame = tk.Frame(self.root, width=1000, pady=5)
        configure_condition_name_frame.pack(fill="y", pady=5)
        
        # 1st Row: Header
        header_frame = tk.Frame(configure_condition_name_frame, pady=5)
        header_frame.pack(fill="x", pady=5)
        header_label = tk.Label(header_frame, text="Please enter a desired name for this condition", font=("Arial", 14, "bold"))
        sub_header_label = tk.Label(header_frame, text="The desired name for this condition cannot be repeatitive", font=("Arial", 7))
        header_label.pack()
        sub_header_label.pack()

        # 2nd Row: TTS Label and TTS Entry
        condition_name_label = tk.Label(configure_condition_name_frame, text="Condition Name:")
        condition_name_label.pack(fill="x", expand=True, padx=5, pady=5)

        self.desired_condition_name_entry = tk.Entry(configure_condition_name_frame, width=100)
        self.desired_condition_name_entry.insert(0, self.current_condition_name)
        self.desired_condition_name_entry.pack(fill="x", expand=True, padx=5, pady=5)

        #ConfigHandler.set_cfg_input_device(usb_alt_name = "aaa", condition = "cond0", custom_name = "this is a custom name :)", keywords = ["word1", "word2"], bg_colour = "black")

        # 4th Row: Frame for Save and Cancel buttons
        button_frame = tk.Frame(configure_condition_name_frame, pady=5)
        button_frame.pack(fill="x", pady=5)

        # Inner frame to centralize buttons
        inner_button_frame = tk.Frame(button_frame)
        inner_button_frame.pack(expand=True)

        save_button = tk.Button(inner_button_frame, text="Save", command=lambda: self.save_new_condition_name())
        save_button.pack(side="left", padx=20, pady=5)

        cancel_button = tk.Button(inner_button_frame, text="Cancel", command=lambda: self.cancel())
        cancel_button.pack(side="right", padx=20, pady=5)
    
    def save_new_condition_name(self):
        self.desired_condition_name = self.desired_condition_name_entry.get().strip()
        
        if not self.desired_condition_name:
            messagebox.showwarning("Invalid Input", "Condition name cannot be empty")
        
        #retrieve all existing conditions
        device_data = ConfigHandler.get_cfg_input_devices(usb_alt_name = self.usb_alt_name)
        existing_condition_names = set(device_data.keys())
        
        #check if desired condition name exists
        if self.desired_condition_name in existing_condition_names:
            messagebox.showwarning("Invalid Name", "This condition name already exists. Please choose another name")
        else:
            ConfigHandler.set_cfg_input_device(usb_alt_name = self.usb_alt_name, condition = self.condition, condition_name=self.desired_condition_name)
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

def edit_condition_name(alt_name, condition, condition_name, callback):
    root = tk.Toplevel()
    app = edit_condition_name_page(root, alt_name, condition, condition_name, callback)
    root.transient()
    root.wait_window(root)