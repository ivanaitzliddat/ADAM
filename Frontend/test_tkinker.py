# test_tkinter.py
import tkinter as tk

root = tk.Tk()
root.title("Tkinter Test")
root.geometry("200x100")

label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

root.mainloop()
