import tkinter as tk
from tkinter import messagebox
from screen_capturer import ScreenCapturer
from tts_settings_page import TTSSettingsPage

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label = tk.Label(self, text="Settings Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a frame for the left navigation bar
        left_nav_frame = tk.Frame(self, width=200, bg="#f0f0f0", relief="sunken")
        left_nav_frame.pack(side="left", fill="y", padx=10)

        # Buttons for left-side navigation
        tts_button = tk.Button(left_nav_frame, text="TTS Settings", command=self.show_tts_settings)
        tts_button.pack(fill="x", padx=5, pady=5)

        keyword_button = tk.Button(left_nav_frame, text="Keyword Settings", command=self.show_keyword_settings)
        keyword_button.pack(fill="x", padx=5, pady=5)

        device_button = tk.Button(left_nav_frame, text="Device Settings", command=self.show_device_settings)
        device_button.pack(fill="x", padx=5, pady=5)

        # Create a frame for the content area (right side)
        self.content_area = tk.Frame(self, bg="white")
        self.content_area.pack(side="left", fill=tk.BOTH, expand=True)
   
    def show_tts_settings(self):
        """Display the Text-to-Speech settings"""
        self.clear_content_area()
        tts_settings_page = TTSSettingsPage(self.content_area)
        tts_settings_page.pack(fill="both", expand=True)

    def show_keyword_settings(self):
        # to change to put keyword settings page here
        """Display network settings page content"""
        self.clear_content_area()
        network_label = tk.Label(self.content_area, text="Network Settings", font=("Arial", 18))
        network_label.pack(pady=20)
        network_info = tk.Label(self.content_area, text="Configure your network settings here.", font=("Arial", 14))
        network_info.pack(pady=10)
    
    def show_device_settings(self):
        # to change to put keyword settings page here
        """Display network settings page content"""
        self.clear_content_area()
        self.device_count_entry = None

        # Entry for number of devices
        self.device_count_label = tk.Label(self.content_area, text="Enter number of devices connected:")
        self.device_count_label.pack(pady=10)

        self.device_count_entry = tk.Entry(self.content_area)
        self.device_count_entry.pack(pady=10)

        self.submit_button = tk.Button(self.content_area, text="Update", command=self.update_count)
        self.submit_button.pack(pady=10)

    def clear_content_area(self):
        """Clear the content area where dynamic content is displayed"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def update_count(self):
        try:
            new_count = int(self.device_count_entry.get())
            device = ScreenCapturer.update_available_devices(new_count)
            if device == -1:
                # Clear the entry field
                self.device_count_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", f"Device {device + 1} is not detected.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
