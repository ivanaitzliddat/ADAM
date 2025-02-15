import tkinter as tk
from config_handler import ConfigHandler

class edit_bg_colour_page:
    def __init__(self, root, usb_alt_name, condition, bg_colour, callback):
        ConfigHandler.init()
        self.root = root
        self.root.geometry("900x700")
        self.usb_alt_name = usb_alt_name
        self.condition = condition
        self.callback = callback
        self.bg_colour = bg_colour

        # Center the window after initializing
        self.root.after(0, self.center_window)
        self.setup_ui()
        self.set_initial_color(bg_colour)

    def setup_ui(self):
        self.root.title(f"Edit colour trigger for {self.usb_alt_name} - {self.condition}")
        color_chooser_frame = tk.Frame(self.root, width=1000, pady=5)
        color_chooser_frame.pack(fill="y", pady=5)
        
        # 1st Row: Header
        header_frame = tk.Frame(color_chooser_frame, pady=5)
        header_frame.pack(fill="x", pady=5)
        header_label = tk.Label(header_frame, text="Edit Background Colour", font=("Arial", 14, "bold"))
        header_label.pack()

        # 2nd Row: Store the color picker
        color_frame = tk.Frame(color_chooser_frame, height=500, highlightbackground="grey", highlightthickness=1)
        color_frame.pack(fill="x", expand=True, padx=5, pady=5)

        self.color_label = tk.Label(color_frame, text="Selected Color: None", font=("Arial", 12))
        self.color_label.pack(pady=20)

        # Add a color display area
        self.color_display = tk.Label(color_frame, text="Color Display", width=20, height=10, bg="white")
        self.color_display.pack(pady=10)

        # Add a clear button to remove selected colour
        clear_button = tk.Button(color_chooser_frame, text="Clear", command=lambda: self.clear_color())
        clear_button.pack(side="left", padx=20, pady=5)

        # Add sliders for RGB values
        self.red_slider = tk.Scale(color_frame, from_=0, to=255, orient="horizontal", label="Red", command=lambda x: self.update_color())
        self.red_slider.pack(fill="x", padx=5, pady=2)
        self.green_slider = tk.Scale(color_frame, from_=0, to=255, orient="horizontal", label="Green", command=lambda x: self.update_color())
        self.green_slider.pack(fill="x", padx=5, pady=2)
        self.blue_slider = tk.Scale(color_frame, from_=0, to=255, orient="horizontal", label="Blue", command=lambda x: self.update_color())
        self.blue_slider.pack(fill="x", padx=5, pady=2)

        # Add a color palette for quick selection
        palette_frame = tk.Frame(color_frame)
        palette_frame.pack(pady=10)

        colors = [
            "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
            "#800000", "#008000", "#000080", "#808000", "#800080", "#008080",
            "#C0C0C0", "#808080", "#999999", "#333333", "#666666", "#000000",
            "#FF6347", "#4682B4", "#DA70D6", "#32CD32", "#FFD700", "#FF4500"
        ]

        # Display colors in a grid with 2 rows
        num_columns = 12  # Number of columns per row
        for index, color in enumerate(colors):
            row = index // num_columns
            col = index % num_columns
            color_button = tk.Button(palette_frame, bg=color, width=2, height=1, command=lambda c=color: self.set_color_from_palette(c))
            color_button.grid(row=row, column=col, padx=2, pady=2)

        # 3rd Row: Save and Cancel buttons below the palette frame
        button_frame = tk.Frame(color_chooser_frame, pady=5)
        button_frame.pack(fill="x", pady=5)

        # Inner frame to centralize buttons
        inner_button_frame = tk.Frame(button_frame)
        inner_button_frame.pack(expand=True)

        save_button = tk.Button(inner_button_frame, text="Save", command=self.save_bg_colour)
        save_button.pack(side="left", padx=20, pady=5)
        cancel_button = tk.Button(inner_button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side="right", padx=20, pady=5)

    def update_color(self):
        r = self.red_slider.get()
        g = self.green_slider.get()
        b = self.blue_slider.get()
        color_code = f'#{r:02x}{g:02x}{b:02x}'
        self.color_label.config(text=f"Selected Color: {color_code}")
        self.color_display.config(text="Color Display", bg=color_code)

    def set_color_from_palette(self, color_code):
        self.color_label.config(text=f"Selected Color: {color_code}", bg=color_code)
        self.color_display.config(bg=color_code)
        r, g, b = int(color_code[1:3], 16), int(color_code[3:5], 16), int(color_code[5:7], 16)
        self.red_slider.set(r)
        self.green_slider.set(g)
        self.blue_slider.set(b)

    def set_initial_color(self, color_code):
        self.color_label.config(text=f"Selected Color: {color_code}")
        self.color_display.config(text="Color Display", bg=color_code)
        r, g, b = int(color_code[1:3], 16), int(color_code[3:5], 16), int(color_code[5:7], 16)
        self.red_slider.set(r)
        self.green_slider.set(g)
        self.blue_slider.set(b)
    
    def clear_color(self):
        self.color_label.config(text="Selected Color: None")
        self.color_display.config(text="No colour selected", bg="#FFFFFF")

    def save_bg_colour(self):
        self.bg_colour = self.color_label.cget("text").split(": ")[1]
        if self.bg_colour == "None":
            self.bg_colour = ""
        ConfigHandler.set_cfg_input_device(usb_alt_name=self.usb_alt_name, condition=self.condition, bg_colour=self.bg_colour)
        ConfigHandler.save_config()
        self.root.destroy()
        self.callback()

    def cancel(self):
        self.root.destroy()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

def edit_bg_colour(alt_name, condition, bg_colour, callback):
    root = tk.Tk()
    app = edit_bg_colour_page(root, alt_name, condition, bg_colour, callback)
    root.mainloop()