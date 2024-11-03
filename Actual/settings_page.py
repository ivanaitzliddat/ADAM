import tkinter as tk
from tkinter import messagebox
from screen_capturer import ScreenCapturer

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.device_count_entry = None
        label = tk.Label(self, text="Settings Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Entry for number of devices
        self.device_count_label = tk.Label(self, text="Enter number of devices connected:")
        self.device_count_label.pack(pady=10)

        self.device_count_entry = tk.Entry(self)
        self.device_count_entry.pack(pady=10)

        self.submit_button = tk.Button(self, text="Update", command=self.update_count)
        self.submit_button.pack(pady=10)

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
            messagebox.showerror("Please enter a valid number.")
