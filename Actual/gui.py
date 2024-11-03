import tkinter as tk

class CaptureApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ADAM")

        # Add a label
        self.label = tk.label(master, text = "Welcome to ADAM")
        self.label.pack()