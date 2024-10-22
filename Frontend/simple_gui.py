import tkinter as tk

def update_label():
    label.config(text="Button clicked!")

# Create the main window
root = tk.Tk()
root.title("ADAM Dashboard")

# Create a label
label = tk.Label(root, text="Hello, World!")
label.pack(pady=10)

# Create a button
button = tk.Button(root, text="Click Me", command=update_label)
button.pack(pady=10)

# Start the main event loop
root.mainloop()
