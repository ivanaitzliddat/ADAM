import tkinter as tk

def create_settings_frame(parent):
    frame = tk.Frame(parent, bg="lightgreen")
    
    settings_label = tk.Label(frame, text="Settings Section", font=("Arial", 24))
    settings_label.pack(pady=20)

    setting_option = tk.Label(frame, text="Change your settings here.", font=("Arial", 16))
    setting_option.pack(pady=10)

    return frame
