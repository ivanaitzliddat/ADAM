import tkinter as tk
from sidebar import create_sidebar
from alerts import create_alerts_frame
from user_info import create_user_info_frame
from settings import create_settings_frame

# Function to hide all frames
def hide_all_frames():
    for frame in frames:
        frame.pack_forget()

# Functions to show each tab
def show_alerts():
    hide_all_frames()
    alerts_frame.pack(fill="both", expand=1)

def show_user_info():
    hide_all_frames()
    user_info_frame.pack(fill="both", expand=1)

def show_settings():
    hide_all_frames()
    settings_frame.pack(fill="both", expand=1)

# Initialize the main window (Dashboard)
root = tk.Tk()
root.title("Dashboard with Sidebar and Tabs")
root.geometry("800x600")

# Create the sidebar
create_sidebar(root, show_alerts, show_user_info, show_settings)

# Create a frame for the main content area
main_frame = tk.Frame(root, width=600, height=600)
main_frame.pack(side="right", fill="both", expand=1)

# Create frames for each tab
alerts_frame = create_alerts_frame(main_frame)
user_info_frame = create_user_info_frame(main_frame)
settings_frame = create_settings_frame(main_frame)

# Store frames in a list for easy management
frames = [alerts_frame, user_info_frame, settings_frame]

# Show the first tab by default (Alerts)
show_alerts()

# Run the tkinter main loop
root.mainloop()
