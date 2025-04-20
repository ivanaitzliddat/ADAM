import tkinter as tk
from tkinter import colorchooser
from edit_bg_colour import edit_bg_colour
from config_handler import ConfigHandler


class DeviceSettingsEditor(tk.Tk):
    def __init__(self, device_label, usb_alt_name):
        super().__init__()
        self.usb_alt_name = usb_alt_name
        self.title(f"Editing Trigger Condition(s) for {device_label}")
        self.geometry("900x600")
        self.configure(bg="#DCE0D9")

        self.conditions = []
        self.resizable(False, False)

        # Center the window
        self.center_window()

        # Add New Condition Button
        self.add_button = tk.Button(self, text="Add New Condition", command=self.add_condition)
        self.add_button.pack(pady=10)

        # Canvas and Scrollable Frame
        self.canvas = tk.Canvas(self, bg="#DCE0D9")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#DCE0D9")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", tags="inner_frame")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Adjust the inner frame width on resize
        self.canvas.bind("<Configure>", self.resize_inner_frame)

        # Save & Cancel Buttons
        self.bottom_frame = tk.Frame(self, bg="#DCE0D9")
        self.bottom_frame.pack(pady=10)

        tk.Button(self.bottom_frame, text="Save", width=10, command=self.retrieve_form_data).pack(side="left", padx=10)
        tk.Button(self.bottom_frame, text="Cancel", width=10, command=self.destroy).pack(side="left", padx=10)

        # Auto-populate conditions
        self.populate_conditions()

    def center_window(self):
        """Center the window on the screen."""
        window_width = 900
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def resize_inner_frame(self, event):
        self.canvas.itemconfig("inner_frame", width=event.width)

    def populate_conditions(self):
        """Read conditions from ConfigHandler and populate the condition cards."""
        device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name=self.usb_alt_name)

        for key, val in device_dict.items():
            triggers = val["triggers"] #return a dictionary of triggers
            self.device_custom_name = val["custom_name"] #return device custom name
            usb_alt_name = val["usb_alt_name"] #return device usb alt name
            for condition, trigger_condition in triggers.items():
                condition_seq = condition 
                condition_name = trigger_condition["condition_name"] #return condition name
                #keywords = trigger_condition["keywords"] #return a list of keywords
                #tts_text = trigger_condition["tts_text"] #return tts text
                #bg_colour = trigger_condition["bg_colour"] #return background colour
                
                condition_card = ConditionCard(
                    self.scrollable_frame,
                    self,
                    self.usb_alt_name,
                    condition_seq,
                    trigger_condition
                )
                condition_card.pack(fill="x", expand=True, padx=20, pady=10)
                self.conditions.append(condition_card)

    def add_condition(self):
        """Add a new blank condition card."""
        condition = ConditionCard(self.scrollable_frame, self, self.usb_alt_name)
        condition.pack(fill="x", expand=True, padx=20, pady=10)
        self.conditions.append(condition)

    def retrieve_form_data(self):
        """Retrieve form data for all conditions and process it before saving them"""
        error_dict = {}

        if len(self.conditions) == 0:
            tk.messagebox.showerror("Form Validation Errors", "No conditions to save.")
            return
        
        # Collect all condition data for duplicate checking
        condition_data = []

        for cond in self.conditions:
            condition_seq = cond.condition_seq_label.cget("text")
            condition_name = cond.name_entry.get().strip()
            keywords = cond.keyword_list.get(0, tk.END)
            colour = cond.color_display.cget("text")
            tts_message = cond.tts_entry.get().strip()
            
            errors = []

            #Condition name cannot be empty
            if condition_name == "":
                errors.append("Condition Name is empty")

            #if keywords is empty, colour cannot be None
            if len(keywords) == 0:
                if colour == "None":
                    errors.append("Please assign a colour if no keyword(s) is provided")
            
            #if colour is None, keywords cannot be empty
            if colour == "None":
                if len(keywords) == 0:
                    errors.append("Please assign a keyword if no colour is provided")

            # Check if condition name exists in another condition card
            for existing_condition in condition_data:
                if existing_condition["condition_name"] == condition_name:
                    errors.append(f"Condition Name '{condition_name}' already exists in another condition card.")

            #check if current condition card values already exist in other condition card(s)
            for existing_condition in condition_data:
                if (
                    existing_condition["condition_name"] == condition_name
                    and existing_condition["keywords"] == keywords
                    and existing_condition["colour"] == colour
                    and existing_condition["tts_message"] == tts_message
                ):
                    errors.append("This condition is a duplicate of another condition.")

            # Add the current condition to the list for duplicate checking
            condition_data.append({
                "condition_name": condition_name,
                "keywords": keywords,
                "colour": colour,
                "tts_message": tts_message,
            })

            if errors:
                error_dict[f"{condition_seq}"] = errors

        # If any errors found, format and display
        if error_dict:
            formatted_error = ""
            for cond_key, issues in error_dict.items():
                formatted_error += f"Error(s) found in {cond_key}:\n"
                for issue in issues:
                    formatted_error += f"  - {issue}\n"
                formatted_error += "\n"

            tk.messagebox.showerror("Form Validation Errors", formatted_error)
            return  # stop saving if validation failed
        
        #if no errors, save the config
        self.save_config()

    def save_config(self):
        """Save the configuration to config.ini."""
        device_custom_name = self.device_custom_name
        #to overwrite the existing trigger conditions, we need to remove the existing conditions first
        ConfigHandler.del_input_device(usb_alt_name = self.usb_alt_name)

        #create a new input device with the same usb_alt_name
        ConfigHandler.add_input_device(usb_alt_name = self.usb_alt_name)

        #set the custom name for the input device
        ConfigHandler.set_cfg_input_device(usb_alt_name = self.usb_alt_name, custom_name = device_custom_name)

        #iterate through all each condition card and save them to config.ini
        for cond in self.conditions:
            condition_seq = str(cond.condition_seq_label.cget("text"))
            condition_name = str(cond.name_entry.get().strip())
            keywords = list(cond.keyword_list.get(0, tk.END))
            colour = cond.color_display.cget("text")
            tts_message = str(cond.tts_entry.get().strip())

            if colour == "None":
                colour = ""
            
            if len(self.conditions) == 1:
            #if only one condition card is present, set the condition name to the custom name of the device
                ConfigHandler.set_cfg_input_device(usb_alt_name = self.usb_alt_name, condition = "cond0", condition_name = condition_name, keywords = keywords, bg_colour = colour, tts_text = tts_message)
            else:
                ConfigHandler.set_cfg_input_device(usb_alt_name = self.usb_alt_name, condition = condition_seq, condition_name = condition_name, keywords = keywords, bg_colour = colour, tts_text = tts_message)
        
        ConfigHandler.save_config()
        tk.messagebox.showinfo("Success", "Device settings saved successfully!")
        self.destroy()

        #self.refresh_page()
    
    #keep it for now, not in used
    def refresh_page(self):
        """Refresh the device settings page by reinitializing the editor."""
        self.destroy()  # Destroy the current instance
        new_editor = DeviceSettingsEditor("Device Label", self.usb_alt_name)  # Recreate the editor
        new_editor.mainloop()  # Start the new instance

class ConditionCard(tk.Frame):
    # Create a condition card for each trigger.
    # This will allow the user to add keywords, set a custom TTS message, and set a background color for the trigger.
    def __init__(self, parent, controller, usb_alt_name, condition_seq=None, trigger_condition=None):
        super().__init__(parent, bd=2, relief="groove", bg="white")
        self.controller = controller
        self.usb_alt_name = usb_alt_name

        # Use the provided condition_seq or generate a new one
        if condition_seq == None:
            last_seq_number_of_conditions = len(self.controller.conditions)
            self.condition_seq = "cond" + str(last_seq_number_of_conditions)
        else:
            self.condition_seq = condition_seq
        
        if trigger_condition: #if a trigger condition is provided, use it to populate the card
            self.condition_name = str(trigger_condition["condition_name"]) #return condition name
            self.bg_colour = trigger_condition["bg_colour"] #return background colour
            self.keywords = trigger_condition["keywords"] #return a list of keywords
            self.tts_text = str(trigger_condition["tts_text"]) #return tts text
        else: #if no trigger condition is provided, create a new one
            self.condition_name = ""
            self.bg_colour = ""  # Default to empty string if not provided
            self.keywords = []  # Default to empty list if not provided
            self.tts_text = ""  # Default to empty string if not provided      

        #print(f"ConditionCard initialized with condition_name: {self.condition_name}, bg_colour: {self.bg_colour}, keywords: {self.keywords}, tts_text: {self.tts_text}")
        # Condition Sequence
        tk.Label(self, text="Condition Sequence:", bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.condition_seq_label = tk.Label(self, text=self.condition_seq, bg="white")
        self.condition_seq_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Condition Name
        tk.Label(self, text="Condition Name:", bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, str(self.condition_name))
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Trigger Color
        tk.Label(self, text="Trigger Color:", bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        if self.bg_colour != "":
            self.color_display = tk.Label(self, bg=self.bg_colour, text=self.bg_colour, fg="black", width=20, relief="sunken")
        else:
            self.color_display = tk.Label(self, bg="#FFFFFF", text="None", fg="black", width=20, relief="sunken")
        self.color_display.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=5)

        tk.Button(self, text="Pick Color", command=self.pick_color).grid(row=2, column=2, padx=10, pady=5)

        # Keywords
        tk.Label(self, text="Keywords", bg="white").grid(row=3, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 0))
        self.keyword_entry = tk.Entry(self)
        self.keyword_entry.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.keyword_list = tk.Listbox(self, height=4)
        self.keyword_list.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10)

        # Populate keywords if available
        if len(self.keywords) > 0:
            for keyword in self.keywords:
                self.keyword_list.insert(tk.END, keyword)

        tk.Button(self, text="Add", command=self.add_keyword, width=8).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        tk.Button(self, text="Delete", command=self.delete_keyword, width=8).grid(row=6, column=1, pady=5, sticky="w")

        # Custom TTS
        tk.Label(self, text="Custom TTS Message:", bg="white").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.tts_entry = tk.Entry(self)
        self.tts_entry.insert(0, str(self.tts_text))
        self.tts_entry.grid(row=7, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

        # Delete Condition Button
        tk.Button(self, text="Delete This Condition", command=self.delete_card, bg="#C3423F", fg="white").grid(
            row=8, column=0, columnspan=3, pady=10
        )

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

    def pick_color(self):
        edit_bg_colour(alt_name=self.usb_alt_name, callback=self.set_colour_from_picker)

    def set_colour_from_picker(self, colour_code):
        if not colour_code or colour_code == "":
            self.color = "#FFFFFF"
            self.color_display.config(bg=self.color, text="None")
        else:
            self.color = colour_code
            self.color_display.config(bg=colour_code, text=colour_code)

    def add_keyword(self):
        keyword = self.keyword_entry.get()
        if keyword == "":
            tk.messagebox.showwarning("Warning", "Keyword cannot be empty.")
            return
        if keyword:
            self.keyword_list.insert(tk.END, keyword)
            self.keyword_entry.delete(0, tk.END)

    def delete_keyword(self):
        selected = self.keyword_list.curselection()
        for index in selected[::-1]:
            self.keyword_list.delete(index)

    def delete_card(self):
        self.controller.conditions.remove(self)
        self.destroy()

if __name__ == "__main__":
    # Example usage
    app = DeviceSettingsEditor("Example Device", "example_usb_alt_name")
    app.mainloop()