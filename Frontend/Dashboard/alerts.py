import tkinter as tk

def create_alerts_frame(parent):
    frame = tk.Frame(parent, bg="lightyellow")
    
    alerts_label = tk.Label(frame, text="Alerts Section", font=("Arial", 24))
    alerts_label.pack(pady=20)

    alert_message = tk.Label(frame, text="You have no new alerts!", font=("Arial", 16))
    alert_message.pack(pady=10)
    
    return frame
