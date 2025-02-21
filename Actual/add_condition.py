import tkinter as tk
from tkinter import messagebox
from config_handler import ConfigHandler

class add_condition_page:
    def __init__(self, root, usb_alt_name, callback):
        self.root = root
        self.root.geometry("900x500")
        self.usb_alt_name = usb_alt_name
        self.callback = callback

        # Center the window after initializing
        self.root.after(0, self.center_window)
        self.add_condition()

    def add_condition(self):
        device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name=self.usb_alt_name)
        for key, val in device_dict.items():
            usb_alt_name = val["usb_alt_name"]
            custom_name = val["custom_name"]
            triggers = val["triggers"]
            #condition = triggers["cond0"]
            #keywords = condition["keywords"]
            #tts_text = condition["tts_text"]
            #g_colour = condition["bg_colour"]
            
        #track number of existing trigger conditions
        last_key = list(triggers.keys())[-1]
        last_trigger_number = last_key[4:]
        
        number_of_trigger_conditions = int(last_trigger_number)

        #temp variables to store the condition details
        self.temp_keywords = []
        self.temp_tts_text = ""
        self.temp_bg_colour = ""

        # Create a new window
        self.root.title(f"Please configure the trigger parameters for the new condition")
        temp_condition_window = tk.Frame(self.root, width=1000, height=700, pady=5)
        temp_condition_window.pack(fill="y", pady=5)
        #trigger_window.grab_set()

        # 1st Row: Title Label with text based on the givenName
        tk.Label(temp_condition_window, text=f"Please configure the trigger parameters for the new condition", font=("Arial", 14, "bold"), pady=10).pack()

        # 2nd Row: Frame for Trigger Conditions
        temp_trigger_conditions_frame = tk.Frame(temp_condition_window)
        temp_trigger_conditions_frame.pack(fill="both", padx=10)

        # 3rd Row: Frame for Save and Cancel Buttons
        save_cancel_button_frame = tk.Frame(temp_condition_window)
        save_cancel_button_frame.pack(fill="x", padx=10, pady=(20,0))

        # Create an inner frame to center the buttons
        inner_button_frame = tk.Frame(save_cancel_button_frame)
        inner_button_frame.pack(expand=True)

        save_button = tk.Button(inner_button_frame, text="Save", font=("Arial", 10), command=self.save_new_condition)
        save_button.pack(side="left",padx=5)
        cancel_button = tk.Button(inner_button_frame, text="Cancel", font=("Arial", 10), command=self.cancel)
        cancel_button.pack(side="left",padx=5)

        #populate temp condition parameters into 2nd row: Frame for Trigger Conditions
        # 1st row: Display the trigger condition text e.g. Trigger Condition: cond0
        self.temp_condition = "cond" + str(number_of_trigger_conditions+1)
        tk.Label(temp_trigger_conditions_frame,text=f"Trigger Condition: {self.temp_condition}",font=("Arial", 10, "bold"),anchor="w",).pack(fill="x", padx=5, pady=2)
        
        # 2nd row: Display sub-heading "List of keyword(s):"
        self.keywords_frame = tk.Frame(temp_trigger_conditions_frame)
        self.keywords_frame.pack(fill="x", pady=5)
        self.display_keywords()

        # 3rd row: Create a frame to store the label and entry for bg_colour
        self.color_frame = tk.Frame(temp_trigger_conditions_frame)
        self.color_frame.pack(fill="x", pady=5)
        self.display_color()

        # 4th row: Create a frame to store the label and entry for tts_text
        self.tts_frame = tk.Frame(temp_trigger_conditions_frame)
        self.tts_frame.pack(fill="x", pady=5)
        self.display_tts()

        #5th row: Create a frame to store the buttons for editing keywords, color, tts message, and delete condition
        self.buttons_frame = tk.Frame(temp_trigger_conditions_frame)
        self.buttons_frame.pack(fill="x", pady=5)
        self.create_buttons()

    def display_keywords(self):
        for widget in self.keywords_frame.winfo_children():
            widget.destroy()

        tk.Label(self.keywords_frame, text="Keywords:", font=("Arial", 10)).pack(side="left", padx=5)
        for keyword in self.temp_keywords:
            tk.Label(self.keywords_frame, text=keyword, font=("Arial", 10)).pack(side="left", padx=5)
        
    def display_color(self):
        for widget in self.color_frame.winfo_children():
            widget.destroy()

        tk.Label(self.color_frame, text="Color Code:", font=("Arial", 10)).pack(side="left", padx=5)
        color_entry = tk.Entry(self.color_frame, width=20)
        color_entry.insert(0, self.temp_bg_colour)
        color_entry.config(state='readonly')
        color_entry.pack(side="left", padx=5)    

    def display_tts(self):
        for widget in self.tts_frame.winfo_children():
            widget.destroy()

        tk.Label(self.tts_frame, text="Text-to-Speech Message:", font=("Arial", 10)).pack(side="left", padx=5)
        tts_entry = tk.Entry(self.tts_frame, width=50)
        tts_entry.insert(0, self.temp_tts_text)
        tts_entry.config(state='readonly')
        tts_entry.pack(side="left", padx=5)    
            
    def create_buttons(self):
        edit_keywords_button = tk.Button(self.buttons_frame, text="Add a keyword", command=self.add_keyword)
        edit_keywords_button.pack(side="left", padx=5)

        edit_color_button = tk.Button(self.buttons_frame, text="Add Colour", command=self.add_color)
        edit_color_button.pack(side="left", padx=5)

        edit_tts_button = tk.Button(self.buttons_frame, text="Add Text-to-Speech Message", command=self.add_tts)
        edit_tts_button.pack(side="left", padx=5)

    def add_keyword(self):
        def on_submit():
            keyword = keyword_entry.get()
            if keyword and isinstance(keyword, str):
                self.temp_keywords.append(keyword)
                self.display_keywords()
                add_a_keyword_window.destroy()
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid keyword (non-empty string).", parent=add_a_keyword_window)

        add_a_keyword_window = tk.Toplevel(self.root)
        add_a_keyword_window.title("Add Keyword")
        add_a_keyword_window.geometry("300x100")
        add_a_keyword_window.transient(self.root)

        tk.Label(add_a_keyword_window, text="Enter Keyword:", font=("Arial", 10)).pack(pady=10)
        keyword_entry = tk.Entry(add_a_keyword_window, font=("Arial", 10))
        keyword_entry.pack(pady=5)

        submit_button = tk.Button(add_a_keyword_window, text="Submit", command=on_submit)
        submit_button.pack(pady=5)

        add_a_keyword_window.after(0, self.center_window)

        # Center the window
        self.center_sub_window(add_a_keyword_window)

    def add_color(self):
        color_window = tk.Toplevel(self.root)
        color_window.title("Choose a Color")
        color_window.geometry("600x800")
        color_window.transient(self.root)

        color_chooser_frame = tk.Frame(color_window, width=1000, pady=5)
        color_chooser_frame.pack(fill="y", pady=5)

        # Center the window
        self.center_sub_window(color_window)

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
        clear_button = tk.Button(color_chooser_frame, text="Clear", command=self.clear_color)
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

        save_button = tk.Button(inner_button_frame, text="Save", command=lambda: self.save_bg_colour(color_window))
        save_button.pack(side="left", padx=20, pady=5)
        cancel_button = tk.Button(inner_button_frame, text="Cancel", command=color_window.destroy)
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

    def save_bg_colour(self, color_window):
        self.bg_colour = self.color_label.cget("text").split(": ")[1]
        if self.bg_colour == "None":
            self.bg_colour = ""
        self.temp_bg_colour = self.bg_colour
        self.display_color()
        color_window.destroy()

    def add_tts(self):
        def on_submit():
            tts_message = tts_entry.get()
            if tts_message and isinstance(tts_message, str):
                self.temp_tts_text = tts_message
                self.display_tts()
                tts_window.destroy()
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid text-to-speech message (non-empty string).", parent=tts_window)

        tts_window = tk.Toplevel(self.root)
        tts_window.title("Edit Text-to-Speech Message")
        tts_window.geometry("400x150")
        tts_window.transient(self.root)
        self.center_sub_window(tts_window)

        tk.Label(tts_window, text="Enter Text-to-Speech Message:", font=("Arial", 10)).pack(pady=10)
        tts_entry = tk.Entry(tts_window, font=("Arial", 10), width=50)
        tts_entry.pack(pady=5)

        submit_button = tk.Button(tts_window, text="Submit", command=on_submit)
        submit_button.pack(pady=5)

    def save_new_condition(self):
        if len(self.temp_keywords)>=1:
            ConfigHandler.set_cfg_input_device(usb_alt_name = self.usb_alt_name, condition = self.temp_condition, keywords = self.temp_keywords ,tts_text=self.temp_tts_text,bg_colour=self.temp_bg_colour)
            ConfigHandler.save_config()
            self.root.destroy()
            self.callback()
        else:
            self.root.lift()  # Bring the main window to the front
            self.root.attributes('-topmost', True)  # Keep it on top
            self.root.attributes('-topmost', False)  # Allow other windows to be on top
            messagebox.showwarning("Warning", "Unable to proceed. Condition must have at least 1 keyword!", parent=self.root)

    def cancel(self):
        self.root.destroy()

    def refresh_trigger_window(self, trigger_window, usb_alt_name):
        trigger_window.destroy()
        self.trigger_condition()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def center_sub_window(self,window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")      

def add_condition(alt_name, callback):
    root = tk.Tk()
    app = add_condition_page(root, alt_name, callback)
    root.mainloop()



    