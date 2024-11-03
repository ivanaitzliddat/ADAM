import tkinter as tk

'''
    Represents a GUI object which allows user to control ADAM.
'''
class ADAM:
    def __init__(self):
        self.master = tk.TK()
        self.master.title("ADAM")

        # Add a label
        self.label = tk.label(self.master, text = "Welcome to ADAM!")
        self.label.pack()

    '''
        Starts the GUI.
    '''
    def run(self):
        self.master.mainloop()