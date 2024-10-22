import tkinter as tk

def create_sidebar(parent, show_alerts, show_user_info, show_settings):
    sidebar_frame = tk.Frame(parent, bg="gray", width=200, height=600)
    sidebar_frame.pack(side="left", fill="y")

    alerts_button = tk.Button(sidebar_frame, text="Alerts", font=("Arial", 14), command=show_alerts)
    alerts_button.pack(pady=20)

    user_info_button = tk.Button(sidebar_frame, text="User Info", font=("Arial", 14), command=show_user_info)
    user_info_button.pack(pady=20)

    settings_button = tk.Button(sidebar_frame, text="Settings", font=("Arial", 14), command=show_settings)
    settings_button.pack(pady=20)
