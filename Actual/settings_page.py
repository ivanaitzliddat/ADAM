import tkinter as tk

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Settings Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Entry for number of devices
        self.device_count_label = tk.Label(self, text="Enter number of devices connected:")
        self.device_count_label.pack(pady=10)

        self.device_count_entry = tk.Entry(self)
        self.device_count_entry.pack(pady=10)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_device_count)
        self.submit_button.pack(pady=10)

    def submit_device_count(self):
        device_count = self.device_count_entry.get()
        print(f"Number of devices connected: {device_count}")
