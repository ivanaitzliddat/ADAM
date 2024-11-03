import tkinter as tk
from tkinter import font

'''
    Represents a GUI object which allows user to control ADAM.
'''
class ADAM:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("ADAM")
        self.master.geometry("1600x900")

        # Define a larger font
        self.label_font = font.Font(size=24, weight="bold")

        # Add a label
        self.label = tk.Label(self.master, text = "Welcome to ADAM!", font=self.label_font)
        self.label.pack()

    '''
        Starts the GUI.
    '''
    def run(self):
        self.master.mainloop()