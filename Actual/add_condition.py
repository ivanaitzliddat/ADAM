import tkinter as tk
from tkinter import messagebox
from config_handler import ConfigHandler
from screenshots import Screenshot
from PIL import Image, ImageTk

class add_condition_page:
    def __init__(self, root, usb_alt_name, callback):
        self.root = root
        self.root.geometry("900x500")
        self.usb_alt_name = usb_alt_name
        self.callback = callback

        self.root.grab_set()
        self.root.focus_set()

        # Center the window after initializing
        self.root.after(0, self.center_window)
        self.add_condition()

    def add_condition(self):
        device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name=self.usb_alt_name)
        for key, val in device_dict.items():
            usb_alt_name = val["usb_alt_name"]
            custom_name = val["custom_name"]
            triggers = val["triggers"]
            
        #track number of existing trigger conditions
        device_key = next(iter(device_dict))  
        device_info = device_dict[device_key]  

        # Get the "triggers" dictionary
        triggers = device_info.get("triggers", {})

        # Count the number of triggers
        trigger_count = len(triggers) + 2

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
        self.temp_condition = "cond" + str(trigger_count)
        self.temp_condition_name = self.temp_condition
        self.condition_name_frame = tk.Frame(temp_trigger_conditions_frame)
        self.condition_name_frame.pack(fill="x", pady=5)
        self.display_condition_name(self.temp_condition_name)
        
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

    def display_condition_name(self,cond_name):
        for widget in self.condition_name_frame.winfo_children():
            widget.destroy()

        tk.Label(self.condition_name_frame,text=f"Trigger Condition Name: {cond_name}",font=("Arial", 10, "bold"),anchor="w",).pack(fill="x", padx=5, pady=2)

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

    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb
    
    def display_image(self, image):
        """Display the provided image on the canvas."""
        #convert pyimage13 to PIL
        PIL_image = ImageTk.getimage(image).convert("RGB")
        #resized_PIL_image = PIL_image.resize((800, 600))

        #set the canvas size to the image size
        img_width, img_height = PIL_image.size
        self.canvas.config(width=img_width, height=img_height)

        #convert PIL to ImageTk format to display on canvas
        self.image_tk = ImageTk.PhotoImage(PIL_image)
        
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.image = PIL_image  # Store the PIL image for color picking

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

    def display_tts(self):
        for widget in self.tts_frame.winfo_children():
            widget.destroy()

        tk.Label(self.tts_frame, text="Text-to-Speech Message:", font=("Arial", 10)).pack(side="left", padx=5)
        tts_entry = tk.Entry(self.tts_frame, width=50)
        tts_entry.insert(0, self.temp_tts_text)
        tts_entry.config(state='readonly')
        tts_entry.pack(side="left", padx=5)    
            
    def create_buttons(self):
        edit_condition_name = tk.Button(self.buttons_frame, text="Change Condition Name", command=self.change_condition_name)
        edit_condition_name.pack(side="left", padx=5)

        edit_keywords_button = tk.Button(self.buttons_frame, text="Add a keyword", command=self.add_keyword)
        edit_keywords_button.pack(side="left", padx=5)

        edit_color_button = tk.Button(self.buttons_frame, text="Add Colour", command=self.add_color)
        edit_color_button.pack(side="left", padx=5)

        edit_tts_button = tk.Button(self.buttons_frame, text="Add Text-to-Speech Message", command=self.add_tts)
        edit_tts_button.pack(side="left", padx=5)

    def check_dup_cond_name(self,cond_name):
        device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name=self.usb_alt_name)
        existing_cond_names=[]
        for key, val in device_dict.items():
            triggers = val["triggers"]
            
            for condition, trigger in triggers.items():
                existing_cond_names.append(trigger['condition_name'])
        if cond_name in existing_cond_names:
            return True
        else:
            return False

    def change_condition_name(self):
        def on_submit():
            new_cond_name = new_cond_name_entry.get()
            if self.check_dup_cond_name(new_cond_name):
                messagebox.showwarning("Duplicate Condition Name Found", "Duplicate Condition Name found, please enter another condition name.", parent=change_cond_name_window)
            else:
                self.temp_condition_name = new_cond_name
                self.display_condition_name(self.temp_condition_name)
                change_cond_name_window.destroy()

        change_cond_name_window = tk.Toplevel(self.root)
        change_cond_name_window.title("Change Condition Name")
        change_cond_name_window.geometry("300x100")
        change_cond_name_window.transient(self.root)

        tk.Label(change_cond_name_window, text="Enter a new condition name:", font=("Arial", 10)).pack(pady=10)
        new_cond_name_entry = tk.Entry(change_cond_name_window, font=("Arial", 10))
        new_cond_name_entry.pack(pady=5)

        submit_button = tk.Button(change_cond_name_window, text="Submit", command=on_submit)
        submit_button.pack(pady=5)

        change_cond_name_window.after(0, self.center_window)

        # Center the window
        self.center_sub_window(change_cond_name_window)

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
        add_color_window = tk.Toplevel(self.root)
        add_color_window.title("Choose a Color")
        add_color_window.transient(self.root)
        add_color_window.resizable(False, False)

        # Main container frame (ensures everything is structured properly)
        main_frame = tk.Frame(add_color_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header Label
        header_label = tk.Label(main_frame, text="Click on the image below to get the colour code", font=("Arial", 14, "bold"))
        header_label.pack(fill="x", pady=(5, 10))

        # Content Frame (for layout organization)
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        # Left Side: Canvas for Displaying Image
        self.canvas = tk.Canvas(content_frame)
        self.canvas.pack(side="left")
        self.canvas.bind("<Button-1>", self.colorpic)

        # Get the image dynamically from Screenshot.frames
        image_tk = None  # Initialize to avoid NameError
        for item in Screenshot.frames:
            if item['alt_name'] == self.usb_alt_name:
                frame = item["current"]
                image = Image.fromarray(frame)
                image_tk = ImageTk.PhotoImage(image)

        if image_tk:
            self.display_image(image_tk)

        # Right Side: Color Selection & Buttons
        color_frame = tk.Frame(content_frame)
        color_frame.pack(side="left", padx=(20, 0), fill="y")

        self.color_label = tk.Label(color_frame, text="Selected Color:", font=("Arial", 12))
        self.color_label.pack(pady=5)

        self.color_display = tk.Label(color_frame, width=20, height=10, bg="white")
        self.color_display.config(text="None")
        self.color_display.pack(pady=5)

        # Button Frame (organized vertically)
        button_frame = tk.Frame(color_frame)
        button_frame.pack(fill="x", pady=10)

        clear_color_button = tk.Button(button_frame, text="Clear Colour Selection", width=25, command=self.clear_colour)
        clear_color_button.pack(fill="x", pady=5)

        save_button = tk.Button(button_frame, text="Save", width=25, command=lambda: self.save_bg_colour(add_color_window))
        save_button.pack(fill="x", pady=5)

        cancel_button = tk.Button(button_frame, text="Cancel", width=25, command=add_color_window.destroy)
        cancel_button.pack(fill="x", pady=5)

        # Update the window geometry to fit the contents
        add_color_window.update_idletasks()
        width = add_color_window.winfo_width()
        height = add_color_window.winfo_height()
        x = (add_color_window.winfo_screenwidth() // 2) - (width // 2)
        y = (add_color_window.winfo_screenheight() // 2) - (height // 2)
        add_color_window.geometry(f"{width}x{height}+{x}+{y}")

        # Center the window
        self.center_sub_window(add_color_window)

    def clear_colour(self):
        self.color_display.config(text="None", bg="white")

    def save_bg_colour(self, add_color_window):
        self.bg_colour = self.color_display.cget("text")
        if self.bg_colour == "None":
            self.bg_colour = ""
        self.temp_bg_colour = self.bg_colour
        self.display_color()
        add_color_window.destroy()

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
            ConfigHandler.set_cfg_input_device(usb_alt_name = self.usb_alt_name, condition = self.temp_condition, condition_name = self.temp_condition_name, keywords = self.temp_keywords ,tts_text=self.temp_tts_text,bg_colour=self.temp_bg_colour)
            #ConfigHandler.set_cfg_input_device(usb_alt_name = self.usb_alt_name, condition_name=self.temp_condition_name)
            ConfigHandler.save_config()
            self.callback()
            self.root.grab_release()
            self.root.destroy()
 
        else:
            self.root.lift()  # Bring the main window to the front
            self.root.attributes('-topmost', True)  # Keep it on top
            self.root.attributes('-topmost', False)  # Allow other windows to be on top
            messagebox.showwarning("Warning", "Unable to proceed. Condition must have at least 1 keyword!", parent=self.root)

    def cancel(self):
        self.root.grab_release()
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
    root = tk.Toplevel()
    app = add_condition_page(root, alt_name, callback)
    root.transient()
    root.wait_window(root)



    