import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from tkinter import font as tkFont
from screen_capturer import ScreenCapturer
from config_handler import ConfigHandler
from edit_keywords import edit_keywords
from edit_bg_colour import edit_bg_colour
from edit_tts_text import edit_tts_text
from add_condition import add_condition
import Pmw

class edit_condition_page:
    def __init__(self, root, usb_alt_name):
        self.root = root
        self.root.geometry("1200x700")
        self.usb_alt_name = usb_alt_name

        # Center the window after initializing
        self.root.after(0, self.center_window)
        self.trigger_condition()

    def trigger_condition(self):
        """Display the trigger conditions for the selected device."""
       
        device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name=self.usb_alt_name) #temp_device_dict use as a temporary dictionary to store the changes made by the user
      
        for key, val in device_dict.items():
            usb_alt_name = val["usb_alt_name"]
            custom_name = val["custom_name"]
            triggers = val["triggers"]
            #condition = triggers["cond0"]
            #keywords = condition["keywords"]
            #tts_text = condition["tts_text"]
            #bg_colour = condition["bg_colour"]

        # Create a new window
        self.root.title(f"Configuring alert trigger conditions for {custom_name}")
        trigger_window = tk.Frame(self.root, width=1000, height=700, pady=5)
        #trigger_window.winfo_toplevel
        trigger_window.pack(fill="y", pady=5)
        #trigger_window.grab_set()

        # 1st Row: Title Label with text based on the givenName
        tk.Label(trigger_window, text=f"Configuring alert trigger conditions for {custom_name}", font=("Arial", 14, "bold"), pady=10).pack()

        # 2nd Row: Frame for Trigger Conditions
        trigger_conditions_frame = tk.Frame(trigger_window)
        trigger_conditions_frame.pack(fill="both", expand=True, padx=10)

        condition_canvas=tk.Canvas(trigger_conditions_frame,width=1000, height=500)
        
        scrollbar = tk.Scrollbar(trigger_conditions_frame, orient="vertical", command=condition_canvas.yview)

        scrollable_conditions_frame = tk.Frame(condition_canvas)
        scrollable_conditions_frame.bind("<Configure>", lambda e: condition_canvas.configure(scrollregion=condition_canvas.bbox("all")))

        condition_canvas.create_window((0,0), window=scrollable_conditions_frame, anchor="nw")
        condition_canvas.configure(yscrollcommand=scrollbar.set)

        # Bind mouse wheel event to canvas
        condition_canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, condition_canvas))

        condition_canvas.pack(side="left", fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")

        # 3rd Row: Frame for Add Condition Button
        add_condition_button_frame = tk.Frame(trigger_window)
        add_condition_button_frame.pack(fill="x", padx=10)
        add_condition_button = tk.Button(add_condition_button_frame, text="Add Condition", font=("Arial", 10), command=lambda a=usb_alt_name, tw=trigger_window: self.open_add_condition(a, tw, lambda: self.refresh_trigger_window(trigger_window, usb_alt_name)))
        add_condition_button.pack(pady=10)

        # 4th Row: Frame for Save and Cancel Buttons
        save_cancel_button_frame = tk.Frame(trigger_window)
        save_cancel_button_frame.pack(fill="x", padx=10, pady=(20,0))

        # Create an inner frame to center the buttons
        inner_button_frame = tk.Frame(save_cancel_button_frame)
        inner_button_frame.pack(expand=True)

        Done_button = tk.Button(inner_button_frame, text="Done", font=("Arial", 10), command=self.done)
        Done_button.pack(side="left",padx=5)

        #auto populate the conditions into the scrollable frame in 2nd row
        for condition, trigger in triggers.items():
    
                condition_frame = tk.Frame(scrollable_conditions_frame, width=900, height=200 , pady=5, highlightbackground="grey", highlightthickness=1)
                condition_frame.pack_propagate(False)
                condition_frame.pack(fill="x", pady=5, padx=8)
                
                # 1st row: Display the trigger condition text e.g. Trigger Condition: cond0
                tk.Label(
                    condition_frame,
                    text=f"Trigger Condition: {condition}",
                    font=("Arial", 10, "bold"),
                    anchor="w",
                ).pack(fill="x", padx=5, pady=2)

                # 2nd row: Display sub-heading "List of keyword(s):"
                keyword_subheading_frame = tk.Frame(condition_frame)
                keyword_subheading_frame.pack(fill="x", padx=5, pady=2)

                keywords_label = tk.Label(keyword_subheading_frame, text="List of keyword(s):", font=("Arial", 10)) 
                keywords_label.pack(side="left", padx=5)

                # 3rd row: Create a Frame to display the array of keywords
                keyword_array_frame = tk.Frame(condition_frame, width=500, highlightbackground="grey", highlightthickness=1)
                keyword_array_frame.pack(fill="x", padx=5, pady=2)

                # Create a Frame to hold the keywords as labels
                keyword_labels_frame = tk.Frame(keyword_array_frame, width=500)
                keyword_labels_frame.pack(fill="x", expand=True)

                # 4th row: Create a frame to store the label and entry for bg_colour
                bg_colour_frame = tk.Frame(condition_frame)
                bg_colour_frame.pack(fill="x", padx=5, pady=2)

                # 5th row: Create a frame to store the label and entry for tts_text
                tts_text_frame = tk.Frame(condition_frame)
                tts_text_frame.pack(fill="x", padx=5, pady=2)

                #6th row: Create a frame to store the buttons for editing keywords, color, tts message, and delete condition
                editing_buttons_frame = tk.Frame(condition_frame)
                editing_buttons_frame.pack(fill="x",padx=5, pady=2)

                
                keywords = trigger["keywords"] #returns a list of keywords
                #for every keyword, create an inner frame "inner_keyword_frame" and pack within keyword_frame
                #inner_keyword_frame contains a keyword label, keyword entry, and keyword_delete_button
                # Insert the keywords into the Frame as Labels in a 4-column layout
                columns = 10
                for index, keyword in enumerate(keywords):
                    row = index // columns
                    col = index % columns
                    keyword_label = tk.Label(keyword_labels_frame, text=keyword, font=("Arial", 10), anchor="w")
                    keyword_label.grid(row=row, column=col, padx=5, pady=2, sticky="w")

                bg_colour = trigger["bg_colour"]
                color_label = tk.Label(bg_colour_frame, text="Color Code:", font=("Arial", 10))
                color_label.pack(side="left", padx=5)
                color_entry = tk.Entry(bg_colour_frame, width=20)
                color_entry.insert(0,bg_colour)
                color_entry.config(state='readonly')
                color_entry.pack(side="left", padx=5)
                
                tts_text = trigger["tts_text"]
                TTSmessageLabel = tk.Label(tts_text_frame, text="Text-to-Speech Message:", font=("Arial", 10))
                TTSmessageLabel.pack(side="left", padx=5)
                TTSmessageEntry = tk.Entry(tts_text_frame, width=50)
                TTSmessageEntry.insert(0,tts_text)
                TTSmessageEntry.config(state='readonly')
                TTSmessageEntry.pack(side="left", padx=5)
                
                #Edit Keywords Button
                edit_keywords_button = tk.Button(editing_buttons_frame, text="Edit Keywords", command=lambda a=usb_alt_name, c=condition, k=keywords, tw=trigger_window, cN=custom_name: self.open_edit_keywords(a, c, k, tw, cN, lambda: self.refresh_trigger_window(trigger_window, usb_alt_name)))
                edit_keywords_button.pack(side="left", padx=5)
                
                #Edit bg_colour Button
                edit_bg_colour_button = tk.Button(editing_buttons_frame, text="Edit Colour", command=lambda a=usb_alt_name, c=condition, bc=bg_colour, tw=trigger_window, cN=custom_name: self.open_edit_bg_colour(a,c,bc,tw,cN, lambda: self.refresh_trigger_window(trigger_window, usb_alt_name)))
                edit_bg_colour_button.pack(side="left", padx=5)
                
                #Edit tts_text Button
                edit_tts_text_button = tk.Button(editing_buttons_frame, text="Edit Text-to-Speech Message", command=lambda a=usb_alt_name, c=condition, tt=tts_text, tw=trigger_window, cN=custom_name: self.open_edit_tts_text(a,c,tt,tw,cN, lambda: self.refresh_trigger_window(trigger_window, usb_alt_name)))
                edit_tts_text_button.pack(side="left", padx=5)

                # Delete Condition Button
                delete_button = tk.Button(editing_buttons_frame, text="Delete Condition", font=("Arial", 10), fg="red", command=lambda cf=condition_frame, c=condition: self.delete_condition(cf,c))
                delete_button.pack(side="right", padx=5)
    
    def _on_mousewheel(self, event,canvas):
        """Scroll the canvas content with the mouse wheel."""
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def done(self):
        self.root.destroy()

    def delete_condition(self, condition_frame, condition):
    
        # Set the window to be always on top
     
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this condition?")
         # Reset the window's 'topmost' attribute after the pop-up
 
        if response:  # If the user clicks "Yes"
            # Proceed to delete the selected condition
            ConfigHandler.set_cfg_input_device(usb_alt_name=self.usb_alt_name, condition=condition, del_condition=True)
            ConfigHandler.save_config()
            # Delete the condition frame from the GUI (not saved until 'Save' is clicked)
            condition_frame.destroy()
    
    def open_add_condition(self, usb_alt_name, trigger_window, callback=None):
        def on_add_condition_complete():
            if callback:
                callback()
            trigger_window.destroy()
        add_condition(usb_alt_name, on_add_condition_complete)

    def open_edit_keywords(self, usb_alt_name, condition, keywords, trigger_window, custom_name, callback=None):
        print(custom_name)
        def on_edit_keywords_complete():
            if callback:
                callback()
            trigger_window.destroy()
        edit_keywords(usb_alt_name, condition, keywords, custom_name, on_edit_keywords_complete)

    def open_edit_bg_colour(self, usb_alt_name, condition, bg_color, trigger_window, custom_name, callback=None):
        def on_edit_bg_colour_complete():
            if callback:
                callback()
            trigger_window.destroy()
        edit_bg_colour(usb_alt_name, condition, bg_color, custom_name, on_edit_bg_colour_complete)

    def open_edit_tts_text(self, usb_alt_name, condition, tts_message, trigger_window, custom_name, callback=None):
        def on_edit_tts_text_complete():
            if callback:
                callback()
            trigger_window.destroy()
        edit_tts_text(usb_alt_name, condition, tts_message, custom_name, on_edit_tts_text_complete)

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
  
def edit_condition(alt_name):
    root = tk.Tk()
    app = edit_condition_page(root,alt_name)
    root.mainloop()