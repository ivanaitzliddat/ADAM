import tkinter as tk
from tkinter import messagebox
from processed_screenshot import Processed_Screenshot
import matplotlib.pyplot as plt

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a frame to hold the listbox of event messages
        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def append_message(self, message, index):
        # Create a label for each message and make it clickable
        clickable_label = tk.Label(self.frame, text=message, fg="blue", cursor="hand2")
        clickable_label.pack(anchor="w", padx=10, pady=5)

        # Bind the label to call on_message_click when clicked
        # clickable_label.bind("<Button-1>", lambda event, msg=message: self.on_message_click(msg))
        clickable_label.bind("<Button-1>", lambda event, idx=index: self.on_message_click(idx))

    def on_message_click(self, image_index):
        with Processed_Screenshot.lock:
            tk_image = Processed_Screenshot.frames[image_index]
            # Create a new Tkinter window to display the image
            window = tk.Toplevel(self.frame)  # Assuming `self.root` is your main Tkinter window
            canvas = tk.Canvas(window, width=tk_image.width(), height=tk_image.height())
            canvas.pack()
            canvas.create_image(0, 0, anchor="nw", image=tk_image)

            # Keep a reference to avoid garbage collection
            window.image = tk_image