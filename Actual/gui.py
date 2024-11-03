import tkinter as tk

'''
    Represents a GUI object which allows user to control ADAM.
'''
class ADAM:
    def __init__(self, master):
        self.master = master
        self.master.title("ADAM")

        # Add a label
        self.label = tk.label(master, text = "Welcome to ADAM!")
        self.label.pack()