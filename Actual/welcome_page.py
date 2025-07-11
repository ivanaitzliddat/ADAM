import tkinter as tk
from tkinter import messagebox
from tkinter import *
from threading import Thread
from PIL import Image, ImageTk 
from tkinter import font as tkFont
from config_handler import ConfigHandler

TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 ="#FF934F"
GRAB_ATTENTION_COLOUR_2 ="#C3423F"

class welcomeScreen(tk.Frame):
    def __init__(self, parent, topbar, option1, is_fresh_setup):
        super().__init__(parent, bg=BG_COLOUR)
        self.parent = parent

        # Configure grid layout for 3 columns
        self.grid_columnconfigure(0, weight=2)  # Left spacer
        self.grid_columnconfigure(1, weight=5)  # Content column
        self.grid_columnconfigure(2, weight=2)  # Right spacer

        if is_fresh_setup:
            for child in topbar.winfo_children():
                child.configure(state='normal')
        else:
            for child in topbar.winfo_children():
                child.configure(state='disable')

        # Scrollable Canvas
        self.canvas = tk.Canvas(self, bg=BG_COLOUR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOUR)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=1, column=1, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="nes")

        # Configure row weights for resizing
        self.grid_rowconfigure(1, weight=1)

        # Mouse Wheel Binding for Scroll
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        # Responsive Resizing
        self.parent.bind("<Configure>", self.on_resize)

        # Title Labels
        self.logo_label_header = tk.Label(self.scrollable_frame, text="WELCOME TO ADAM", bg=BG_COLOUR)
        self.logo_label_subheader = tk.Label(self.scrollable_frame, text="Auxiliary Dynamic Alert Monitor", bg=BG_COLOUR)
        self.logo_label_before_you_begin = tk.Label(self.scrollable_frame, text="Before we begin, please ensure the following steps are done", bg=BG_COLOUR)

        self.logo_label_header.pack(pady=(0,10))  # Reduced top padding
        self.logo_label_subheader.pack()
        self.logo_label_before_you_begin.pack(pady=(10, 10))  # Reduced padding

        # Steps Frame
        self.steps_frame = tk.Frame(self.scrollable_frame, bg=BG_COLOUR)
        self.steps_frame.pack()

        # Load images dynamically
        self.images = []
        for _ in range(3):
            img = Image.open(ConfigHandler.dirname + "/green_monitor.png")
            self.images.append(img)

        # Steps Information
        self.step_labels = []
        self.step_images = []
        self.step_texts = []
        steps = [
            ("STEP 1", "Ensure all devices are powered on and displayed on the main screen."),
            ("STEP 2", "Connect the USB video capture card to the ADAM unit and ensure the input device is connected."),
            ("STEP 3", "Repeat Step 1 and Step 2 for all desired devices. Click Begin when ready.")
        ]

        for i, (step, text) in enumerate(steps):
            frame = tk.Frame(self.steps_frame, bg=BG_COLOUR)
            frame.pack(pady=10, padx=20, fill="both", expand=True)  # Reduced padding

            header = tk.Label(frame, text=step, bg=BG_COLOUR)
            header.pack()
            self.step_labels.append(header)

            img_label = tk.Label(frame, bg=BG_COLOUR)
            img_label.pack(pady=5)  # Reduced padding
            self.step_images.append(img_label)

            desc = tk.Label(frame, text=text, wraplength=500, bg=BG_COLOUR)
            desc.pack()
            self.step_texts.append(desc)

        # Begin Button
        self.setup_button = tk.Button(self.scrollable_frame, text="Begin", command=option1)
        self.setup_button.pack(pady=20)  # Reduced padding
        
        self.on_resize()
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        """Dynamically adjust the layout and font sizes based on window size."""
        width = max(self.parent.winfo_width(), 1)
        height = max(self.parent.winfo_height(), 1)
        min_dimension = max(min(width, height), 1)
        header_font_size = max(10, min(58, min_dimension // 30))
        subheader_font_size = max(10, min(20, min_dimension // 50))
        step_font_size = max(10, min(30, min_dimension // 40))
        button_font_size = max(10, min(26, min_dimension // 40))
        image_size = max(50, min(200, min_dimension // 10))

        self.logo_label_header.config(font=("Terminal", header_font_size))
        self.logo_label_subheader.config(font=("Malgun Gothic Semilight", subheader_font_size))
        self.logo_label_before_you_begin.config(font=("Malgun Gothic Semilight", subheader_font_size))
        self.logo_label_before_you_begin.config(wraplength=width // 2)

        min_width = 900 # Minimum width for resizing
        min_height = 800  # Minimum height for resizing

        # Get the root window (Tk instance)
        root = self.winfo_toplevel()

        # Set the minimum size for the window
        root.wm_minsize(min_width, min_height)

        for label in self.step_labels:
            label.config(font=("Arial", step_font_size, "bold"))
        for text in self.step_texts:
            text.config(font=("Arial", subheader_font_size), wraplength=width // 2)
        for i, img_label in enumerate(self.step_images):
            resized_img = self.images[i].resize((image_size, image_size))
            img_label.image = ImageTk.PhotoImage(resized_img)
            img_label.config(image=img_label.image)

        self.setup_button.config(font=("Helvetica", button_font_size, "bold"))

    # Mouse Wheel Scroll Handler
    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")

if __name__ == "__main__":
    root = tk.Tk()
    app = welcomeScreen(root, None, lambda: print("Begin clicked"))
    app.pack(fill="both", expand=True)
    root.mainloop()