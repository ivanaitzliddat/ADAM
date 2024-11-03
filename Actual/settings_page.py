import tkinter as tk

class SettingsPage(tk.Frame):
    def __init__(self, parent, update_device_count_callback):
        super().__init__(parent)
        self.update_device_count_callback = update_device_count_callback
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
            self.update_device_count_callback(new_count)
        except ValueError:
            print("Please enter a valid number.")
