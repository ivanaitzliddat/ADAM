import tkinter as tk
from config_handler import ConfigHandler
from screenshots import Screenshot
from PIL import Image, ImageTk

class edit_bg_colour_page:
    def __init__(self, root, usb_alt_name, callback):
        self.root = root
        #self.root.geometry("900x1000")
        self.usb_alt_name = usb_alt_name
        self.callback = callback
        self.root.grab_set()
        self.root.focus_set()

        self.root.resizable(False, False)
        
        self.bg_colour = ""  # Initialize bg_colour to an empty string

        # Center the window after initializing
        self.root.after(0, self.center_window)
        self.setup_ui()

        #get the image based on usb_alt_name
        for item in Screenshot.frames:
            if item['alt_name'] == usb_alt_name:
                frame = item["current"]
                # Convert the frame to an image
                image = Image.fromarray(frame)
                image_tk = ImageTk.PhotoImage(image)
        self.display_image(image_tk)

    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb
    
    def setup_ui(self):
        self.root.title("Choose your triggered colour")
        # Main container frame to hold everything
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 1st Row: Header
        header_label = tk.Label(main_frame, text="Click on the image below to get the colour code", font=("Arial", 14, "bold"))
        header_label.pack(fill="x", pady=(2,0))

        # 2nd Row: Content Frame (for left-aligned layout)
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        # Left Side: Canvas for Displaying Image
        self.canvas = tk.Canvas(content_frame)
        self.canvas.pack(side="left")
        self.canvas.bind("<Button-1>", self.colorpic)

        # Right Side: Selected colour and Buttons
        color_frame = tk.Frame(content_frame)
        color_frame.pack(side="left", padx=(10,0))

        self.color_label = tk.Label(color_frame, text="Selected Color:", font=("Arial", 12))
        self.color_label.pack()

        self.color_display = tk.Label(color_frame, width=20, height=10, bg="white")
        if self.bg_colour == "":
            self.color_display.config(text="None")
        else:
            self.color_display.config(text=self.bg_colour)
            self.color_display.config(bg=self.bg_colour)
        self.color_display.pack()

        button_frame = tk.Frame(color_frame)
        button_frame.pack(side="left")

        clear_colour_button = tk.Button(button_frame, text="Clear Colour Selection", width=20, command=self.clear_colour)
        clear_colour_button.pack(fill="x", pady=(5,0))

        save_button = tk.Button(button_frame, text="Save",width=20, command=self.save_bg_colour)
        save_button.pack(fill="x", pady=(5,0))

        cancel_button = tk.Button(button_frame, text="Cancel",width=20, command=self.cancel)
        cancel_button.pack(fill="x", pady=(5,0))

    def display_image(self, image):
        """Display the provided image on the canvas."""
        #convert pyimage13 to PIL
        PIL_image = ImageTk.getimage(image).convert("RGB")
        resized_PIL_image = PIL_image.resize((800, 600))

        #set the canvas size to the image size
        img_width, img_height = resized_PIL_image.size
        self.canvas.config(width=img_width, height=img_height)

        #convert PIL to ImageTk format to display on canvas
        self.image_tk = ImageTk.PhotoImage(resized_PIL_image)
        
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.image = resized_PIL_image  # Store the PIL image for color picking

    def colorpic(self, event):
        if not hasattr(self, 'image'):
            return
        x, y = event.x, event.y
        # Convert canvas coordinates to image coordinates
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_x = int(x * self.image.width / canvas_width)
        img_y = int(y * self.image.height / canvas_height)
        rgb = self.image.getpixel((img_x, img_y))
        color_code = self._from_rgb(rgb)
        self.color_display.config(text=f"{color_code}")
        self.color_display.config(bg=color_code)

    def save_bg_colour(self):
        #self.bg_colour = self.color_label.cget("text").split(": ")[1]
        self.bg_colour = self.color_display.cget("text")
        if self.bg_colour == "None":
            self.bg_colour = ""
        self.callback(self.bg_colour)

    def clear_colour(self):
        self.color_display.config(text=f"None")
        self.color_display.config(bg="white")

    def cancel(self):
        self.image = None
        self.root.grab_release()
        self.root.destroy()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

def edit_bg_colour(alt_name, callback):
    root = tk.Toplevel()

    def wrapped_callback(colour):
        callback(colour)
        root.destroy()

    app = edit_bg_colour_page(root, alt_name, wrapped_callback)
    root.transient()
    root.grab_set()
    root.wait_window(root)