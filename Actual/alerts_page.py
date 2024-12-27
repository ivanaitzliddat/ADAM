import tkinter as tk
import numpy as np
import cv2
import io
from PIL import Image, ImageTk
from processed_screenshot import Processed_Screenshot

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a frame to hold the listbox of event messages
        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a canvas to contain the scrollable content
        self.canvas = tk.Canvas(self.frame, bg="white", bd=2, relief="solid")
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Create a scrollbar and associate it with the canvas
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the messages
        self.message_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

        # Update the scrollable region whenever the frame size changes
        self.message_frame.bind("<Configure>", self.on_frame_configure)

    def append_message(self, message, index):
        # Create a label for each message and make it clickable
        clickable_label = tk.Label(self.message_frame, text=message, fg="blue", cursor="hand2", font=("Arial", 12),relief="solid", bd=1, padx=10, pady=5, anchor="w")
        clickable_label.pack(padx=5, pady=5, fill="x")

        # Bind the label to call on_message_click when clicked
        # clickable_label.bind("<Button-1>", lambda event, msg=message: self.on_message_click(msg))
        clickable_label.bind("<Button-1>", lambda event, idx=index: self.on_message_click(idx))

    def sharpen_image(image):
        kernel = np.array([[-1, -1, -1],
                        [-1,  9, -1],
                        [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)

    def on_message_click(self, image_index):
        with Processed_Screenshot.lock:
            image_with_boxes = Processed_Screenshot.frames[image_index]
            sharpened_image = AlertsPage.sharpen_image(image_with_boxes)
            # Convert image to Tkinter-compatible format
            pil_image = Image.fromarray(sharpened_image)

            # Resize the image if it's too large for the screen
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            max_width = screen_width * 0.8  # 80% of the screen width
            max_height = screen_height * 0.8  # 80% of the screen height
            
            image_width, image_height = pil_image.size
            if image_width > max_width or image_height > max_height:
                scaling_factor = min(max_width / image_width, max_height / image_height)
                new_width = int(image_width * scaling_factor)
                new_height = int(image_height * scaling_factor)
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            with io.BytesIO() as buffer:
                pil_image.save(buffer, format="PNG")
                buffer.seek(0)
                tk_image = ImageTk.PhotoImage(Image.open(buffer))

            # Create a new Tkinter window to display the image
            window = tk.Toplevel(self.frame)
            canvas = tk.Canvas(window, width=tk_image.width(), height=tk_image.height())
            canvas.pack()
            canvas.create_image(0, 0, anchor="nw", image=tk_image)

            # Keep a reference to avoid garbage collection
            window.image = tk_image

    def on_frame_configure(self, event):
        """Update the scrollable region when the frame is resized."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))