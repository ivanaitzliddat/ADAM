import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from tkinter import font as tkFont
from screen_capturer import ScreenCapturer
from config_handler import ConfigHandler
import time

class VideoCaptureSetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to ADAM")
        #self.root.geometry("1920x1080")

        #Prevent user from resizing this window
        self.root.resizable(False,False)   

        # Create the main frame
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        # First row (ADAM logo)
        self.first_row = tk.Frame(self.frame)
        self.first_row.pack(fill="both")
        self.logo_label1 = tk.Label(
            self.first_row, text="Configuration", font=("Malgun Gothic Semilight", 38)
        )
        self.logo_label1.pack()

        # Second row (scrollable area)
        self.create_scrollable_second_row()

        # Fourth row (Save button)
        self.fourth_row = tk.Frame(self.frame)
        self.fourth_row.pack(fill="both")
        save_button_font = tkFont.Font(family="Helvetica", size=26, weight="bold")
        self.save_button = tk.Button(
            self.fourth_row, text="Save", font=save_button_font
        )
        self.save_button.pack(pady=20)

        # Center the window
        self.root.after(100, self.center_window)

    def create_scrollable_second_row(self):
        """Create a scrollable second row with detected inputs."""
        self.second_row_frame = tk.Frame(self.frame)
        self.second_row_frame.pack(fill="both", expand=True)

        # Canvas for scrollable area
        self.canvas = tk.Canvas(
            self.second_row_frame, width=1890, height=800, highlightbackground="grey", highlightthickness=1
        )
        self.scrollbar = tk.Scrollbar(
            self.second_row_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        # Bind scrollable frame to canvas
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # retrieve the number of devices from config.ini and populate the video_inputs dictionary
        self.populate_video_inputs()

########################################################################################################################################################################
    def populate_video_inputs(self):
        """Populate the scrollable frame with video input elements."""
        
        ConfigHandler.init()
        #ConfigHandler.set_cfg_input_devices(usb_alt_name = "testing aaasdsadsadsaadads name", condition = "cond0", keywords = ["poo", "laaa"])
        #ConfigHandler.save_config()
        device_dict = ConfigHandler.get_cfg_input_devices()
        i = 0
        for key, val in device_dict.items():
            #print(key)
            #print(val)
            #print(val["triggers"]["cond0"]["keywords"])
            usb_alt_name = val["usb_alt_name"]
            custom_name = val["custom_name"]
            triggers = val["triggers"]
            condition = triggers["cond0"]
            keywords = condition["keywords"]
            tts_text = condition["tts_text"]
            bg_colour = condition["bg_colour"]
            
            # Create a subframe for each video input
            device_frame = tk.Frame(
                self.scrollable_frame,
                highlightbackground="grey",
                highlightthickness=1,
                width=450,
                height=500,
                bg="white",
            )

            device_frame.grid_propagate(False)
            device_frame.pack_propagate(False)
            device_frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)

            # Video Frame Placeholder
            video_label = tk.Label(
                device_frame, text=f"Video Frame {i} = to hold 1 frame from each input", bg="black", fg="white", height=20, padx=5
            )
            video_label.pack(fill="x", pady=5)

            # Display the device sequence number
            device_seq_num_frame = tk.Frame(device_frame)
            device_seq_num_frame.pack(fill="x", pady=5)
            device_seq_num_label = tk.Label(
                device_seq_num_frame, text=f"first dictionary key: {key}", font=("Arial", 10, "bold")
            )
            device_seq_num_label.pack()

            # Unique Device Name Frame
            name_frame = tk.Frame(device_frame)
            name_frame.pack(fill="x")

            # Display the alt device name
            unique_name_label = tk.Label(name_frame, text=f"Device Default Name: ", font=("Arial", 10, "bold"), height=3)
            unique_name_label.pack(side="left")
            device_label = tk.Label(
                name_frame, text=usb_alt_name, font=("Arial", 10, "bold"), height=3
            )
            device_label.pack(side="left")

            # Desired Device Name Frame
            device_given_name_frame = tk.Frame(device_frame)
            device_given_name_frame.pack(fill="x", pady=5)

            # Display the desired given name (user-defined name)
            device_given_name_label = tk.Label(device_given_name_frame, text="Given Name: ", font=("Arial", 10, "bold"), height=3)
            device_given_name_label.pack(side="left")
            device_given_name = tk.Label(
                device_given_name_frame, text=custom_name, font=("Arial", 10, "bold"), height=3
            )
            device_given_name.pack(side="left")

            rename_button = tk.Button(device_given_name_frame, text="Rename", width=10, command=lambda device_label=device_given_name, usb_alt_name=usb_alt_name: self.rename_device(device_label,usb_alt_name))
            rename_button.pack(side="right", padx=5)

            # Trigger Condition Button
            button_frame = tk.Frame(device_frame)
            button_frame.pack(fill="x")
            trig_condition_button = tk.Button(button_frame, text="Trigger Conditions", width=10, height=3, command=lambda usb_alt_name=usb_alt_name, custom_name=custom_name, triggers=triggers: self.trigger_condition(usb_alt_name,custom_name,triggers))
            trig_condition_button.pack(fill="both")
            i += 1

    def rename_device(self, device_label, usb_alt_name):
        """Prompt the user to rename the device."""
        rename_window = tk.Toplevel(self.root)
        rename_window.title(f"Rename Device for {usb_alt_name}")
        rename_window.geometry("300x150")
        rename_window.transient(self.root)
        rename_window.grab_set()

        # Center the rename window
        rename_window.update_idletasks()
        width = rename_window.winfo_width()
        height = rename_window.winfo_height()
        x = (rename_window.winfo_screenwidth() // 2) - (width // 2)
        y = (rename_window.winfo_screenheight() // 2) - (height // 2)
        rename_window.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(rename_window, text="Enter a desired name for the device:", pady=10).pack()

        name_entry = tk.Entry(rename_window, width=25)
        name_entry.pack(pady=5)

        def save_name(device_label, usb_alt_name):
            new_name = str(name_entry.get().strip())
            usb_alt_name = str(usb_alt_name)
            if new_name:
                ConfigHandler.set_cfg_input_device(usb_alt_name=usb_alt_name, custom_name=new_name)
                ConfigHandler.save_config()
                device_label.config(text=new_name)  # Update the label with the new name
                messagebox.showinfo("Success", f"Device renamed to '{new_name}'!")
                rename_window.destroy()
            else:
                messagebox.showwarning("Warning", "Name cannot be empty!")

        tk.Button(rename_window, text="Save", command=lambda: save_name(device_label, usb_alt_name)).pack(side="left", padx=10, pady=20)
        tk.Button(rename_window, text="Cancel", command=rename_window.destroy).pack(side="right", padx=10, pady=20)

    def trigger_condition(self, usb_alt_name, custom_name, triggers):
        """Display the trigger conditions for the selected device."""
        
        usb_alt_name = str(usb_alt_name)
        custom_name = str(custom_name)

        temp_device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name=usb_alt_name) #temp_device_dict use as a temporary dictionary to store the changes made by the user

        #to display the window title with the custom name if it exists, else display the usb_alt_name
        if custom_name == "": 
            givenName=usb_alt_name
        else:
            givenName=custom_name

        # Create a new window
        trigger_window = tk.Toplevel(self.root)
        trigger_window.title(f"Configuring alert trigger conditions for {givenName}")
        trigger_window.geometry("1100x600")
        trigger_window.transient(self.root)
        trigger_window.grab_set()

        # 1st Row: Title Label with text based on the givenName
        tk.Label(trigger_window, text=f"Configuring alert trigger conditions for {givenName}", font=("Arial", 14, "bold"), pady=10).pack()

        # 2nd Row: Frame for Trigger Conditions
        trigger_conditions_frame = tk.Frame(trigger_window)
        trigger_conditions_frame.pack(fill="both", expand=True, padx=10)

        condition_canvas=tk.Canvas(trigger_conditions_frame,width=1000, height=300)
        
        scrollbar = tk.Scrollbar(trigger_conditions_frame, orient="vertical", command=condition_canvas.yview)

        scrollable_conditions_frame = tk.Frame(condition_canvas)
        scrollable_conditions_frame.bind("<Configure>", lambda e: condition_canvas.configure(scrollregion=condition_canvas.bbox("all")))

        condition_canvas.create_window((0,0), window=scrollable_conditions_frame, anchor="nw")
        condition_canvas.configure(yscrollcommand=scrollbar.set)

        condition_canvas.pack(side="left", fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")
                
        def delete_condition(condition_frame):
            """Delete an entire specific condition frame."""
            condition_frame.destroy()

        def delete_keyword_inner_frame(inner_keyword_frame, temp_device_dict, condition, keyword_to_be_removed):
            """GUI - inner_keyword_frame will destroy the keyword label, keyword entry, and the keyword delete button."""
            inner_keyword_frame.destroy()

            #remove keyword from the temp_device_dict. Iterate through the dictionary to find the keyword to be removed if the condition matches
            for key, value in temp_device_dict.items():
                value['triggers'][condition]['keywords'].remove(keyword_to_be_removed)
            #print(temp_device_dict)
            return(temp_device_dict) #return the updated temp_device_dict
                
        def add_keyword_field(keyword_button_frame):
            """Add a keyword input field with a delete button."""
            keyword_label = tk.Label(keyword_button_frame, text="Keyword:", font=("Arial", 10))
            keyword_label.pack(side="left")
            keyword_entry = tk.Entry(keyword_button_frame, width=20)
            keyword_entry.pack(side="left", padx=5)
            delete_button = tk.Button(
                keyword_button_frame,
                text="X",
                font=("Arial", 8, "bold"),
                fg="red",
                command=lambda: delete_keyword(keyword_entry, keyword_label),
            )
            delete_button.pack(side="left", padx=5)
        
        '''test'''

        #auto populate the conditions into the scrollable frame in 2nd row
        for condition, trigger in triggers.items():
                
                #to count number of triggers for each device
                num_of_triggers=len(triggers)
                
                keyword_seq=1 #used for the keyword label

                condition_frame = tk.Frame(scrollable_conditions_frame, pady=5, highlightbackground="grey", highlightthickness=1)
                condition_frame.pack(fill="x", pady=5)
                
                # 1st row: Display the trigger condition text e.g. Trigger Condition: cond0
                tk.Label(
                    condition_frame,
                    text=f"Trigger Condition: {condition}",
                    font=("Arial", 10, "bold"),
                    anchor="w",
                ).pack(fill="x", padx=5, pady=2)

                # 2nd row: Button for Keyword
                keyword_frame = tk.Frame(condition_frame)
                keyword_frame.pack(fill="x", padx=5, pady=2)

                keyword_button = tk.Button(keyword_frame, text="Add Keyword", command="") #command=lambda: add_keyword_field(keyword_button_frame) ---> later update
                keyword_button.pack(side="left", padx=5)

                # 3rd row: Button for Color Picker
                color_picker_button_frame = tk.Frame(condition_frame)
                color_picker_button_frame.pack(fill="x", padx=5, pady=2)

                color_button = tk.Button(color_picker_button_frame, text="Add a Color", command="")
                color_button.pack(side="left", padx=5)
                
                keywords = trigger["keywords"] #returns a list of keywords

                for keyword in keywords:
                    #for every keyword, create an inner frame "inner_keyword_frame" and pack within keyword_frame
                    #inner_keyword_frame contains a keyword label, keyword entry, and keyword_delete_button
                    """start create inner_keyword_frame"""
                    inner_keyword_frame = "inner_keyword_frame" + str(keyword_seq)
                    inner_keyword_frame = tk.Frame(keyword_frame)
                    inner_keyword_frame.pack(side="left")

                    """Add a keyword label, keyword entry, keyword delete button into the inner_keyword_frame"""
                    keyword_label = tk.Label(inner_keyword_frame, text=f"Keyword {keyword_seq}", font=("Arial", 10))
                    keyword_label.pack(side="left")

                    #for every keyword, create a keyword_label and pack within the inner_keyword_frame
                    #inner_keyword_frame contains a keyword label, keyword entry, and keyword_delete_button
                    keyword_entry = "keyword_entry" + str(keyword_seq)
                    keyword_entry = tk.Entry(inner_keyword_frame,width=20)
                    keyword_entry.insert(0,keyword)
                    keyword_entry.pack(side="left", padx=5)
                    keyword_in_the_entry = keyword_entry.get()
            
                    delete_inner_keyword_frame_button = tk.Button(
                        inner_keyword_frame,
                        text="X",
                        font=("Arial", 8, "bold"),
                        fg="red",
                        command=lambda f=inner_keyword_frame, t=temp_device_dict, c=condition, w=keyword_in_the_entry: delete_keyword_inner_frame(f,t,c,w))
                    delete_inner_keyword_frame_button.pack(side="left", padx=5)
                    keyword_seq+=1 #so each inner_frame is unqiue by itself and allow delete_inner_keyword_frame_button to delete each individual frame

                bg_colour = trigger["bg_colour"]
                color_label = tk.Label(color_picker_button_frame, text="Color Code:", font=("Arial", 10))
                color_label.pack(side="left", padx=5)
                color_entry = tk.Entry(color_picker_button_frame, width=20)
                color_entry.insert(0,bg_colour)
                color_entry.pack(side="left", padx=5)

                tts_text = trigger["tts_text"]
                custom_message_frame = tk.Frame(condition_frame)
                custom_message_frame.pack(fill="x", padx=5, pady=5)

                TTSmessageLabel = tk.Label(custom_message_frame, text="Custom Message:", font=("Arial", 10))
                TTSmessageLabel.pack(side="left", padx=5)
                TTSmessageEntry = tk.Entry(custom_message_frame, width=50)
                TTSmessageEntry.insert(0,tts_text)
                TTSmessageEntry.pack(side="left", padx=5)

                # Delete Condition Button
                delete_button = tk.Button(
                    condition_frame,
                    text="Delete Condition",
                    font=("Arial", 10),
                    fg="red",
                    command=lambda c=condition_frame: delete_condition(c),
                )
                delete_button.pack(side="right", padx=5)

                def add_keyword_field(num_of_keyword):
                    """Add a keyword input field."""
                    keyword_label = tk.Label(keyword_button_frame, text=f"Keyword {num_of_keyword}:", font=("Arial", 10))
                    keyword_label.pack(side="left")
                    keyword_entry = tk.Entry(keyword_button_frame, width=20)
                    keyword_entry.pack(side="left", padx=5)

                def add_color_field():
                    """Add a color picker input field."""
                    color_label = tk.Label(color_picker_button_frame, text="Color Code:", font=("Arial", 10))
                    color_label.pack(side="left", padx=5)
                    color_entry = tk.Entry(color_picker_button_frame, width=20)
                    color_entry.pack(side="left", padx=5)

        #print(temp_device_dict)

        # Center the window
        trigger_window.update_idletasks()
        width = trigger_window.winfo_width()
        height = trigger_window.winfo_height()
        x = (trigger_window.winfo_screenwidth() // 2) - (width // 2)
        y = (trigger_window.winfo_screenheight() // 2) - (height // 2)
        trigger_window.geometry(f"{width}x{height}+{x}+{y}")

        # Function to create a row for each condition
        def create_condition_row(num_of_conditions):
            trigger_condition_serialNum = num_of_conditions + 1
            num_of_keywords = 1
            num_of_color=0
            #print(trigger_condition_serialNum)

            """Create a row for a single trigger condition."""
            # Parent frame for each condition
            new_condition_frame = tk.Frame(scrollable_conditions_frame, pady=5, highlightbackground="grey", highlightthickness=1)
            new_condition_frame.pack(fill="x", pady=5)

            # 1st row: Display the trigger condition text
            tk.Label(
                new_condition_frame,
                text=f"Trigger Condition: {trigger_condition_serialNum}",
                font=("Arial", 10, "bold"),
                anchor="w",
                ).pack(fill="x", padx=5, pady=2)

            # 2nd row: Button for Keyword
            keyword_button_frame = tk.Frame(new_condition_frame)
            keyword_button_frame.pack(fill="x", padx=5, pady=2)

            # 3rd row: Button for Color Picker
            color_picker_button_frame = tk.Frame(new_condition_frame)
            color_picker_button_frame.pack(fill="x", padx=5, pady=2)

            def add_keyword_field(num_of_keywords):
                """Add a keyword input field."""
                keyword_label = tk.Label(keyword_button_frame, text=f"Keyword {num_of_keywords}:", font=("Arial", 10))
                keyword_label.pack(side="left")
                keyword_entry = tk.Entry(keyword_button_frame, width=20)
                keyword_entry.pack(side="left", padx=5)
                num_of_keywords+=1

            def add_color_field(num_of_color):
                """Add a color picker input field."""
                if num_of_color != 1:
                    color_label = tk.Label(color_picker_button_frame, text="Color Code:", font=("Arial", 10))
                    color_label.pack(side="left", padx=5)
                    color_entry = tk.Entry(color_picker_button_frame, width=20)
                    color_entry.pack(side="left", padx=5)
                    num_of_color+=1

            keyword_button = tk.Button(keyword_button_frame, text="Add Keyword", command=lambda: add_keyword_field(num_of_keywords))
            keyword_button.pack(side="left", padx=5)

            color_button = tk.Button(color_picker_button_frame, text="Color Picker", command=lambda: add_color_field(num_of_color))
            color_button.pack(side="left", padx=5)

            # 3rd row: Custom Message Text Field
            custom_message_frame = tk.Frame(new_condition_frame)
            custom_message_frame.pack(fill="x", padx=5, pady=5)

            tk.Label(custom_message_frame, text="Custom Message:", font=("Arial", 10)).pack(side="left", padx=5)
            tk.Entry(custom_message_frame, width=50).pack(side="left", padx=5)

            # Delete Condition Button
            delete_button = tk.Button(
                new_condition_frame,
                text="Delete Condition",
                font=("Arial", 10),
                fg="red",
                command=lambda c=new_condition_frame: delete_condition(c),
            )
            delete_button.pack(side="right", padx=5)

        add_button = tk.Button(trigger_window, text="Add Condition", command=lambda: create_condition_row(num_of_conditions))
        add_button.pack(pady=10)

        def save_conditions():
            print("save button pressed")
        '''
        def save_conditions():
            """Save updated trigger conditions."""
            updated_conditions = []
            for child in trigger_window.winfo_children():
                if isinstance(child, tk.Frame):
                    # Retrieve Trigger Condition from the first label in the frame
                    trigger_label = child.winfo_children()[0]
                    if isinstance(trigger_label, tk.Label):
                        updated_conditions.append(trigger_label.cget("text").replace("Trigger Condition: ", ""))
            trigger_data["triggerCondition0"] = updated_conditions
            print("Updated Trigger Data:", trigger_data)
            trigger_window.destroy()
'''
        # 4th Row: Save and Cancel Buttons
        button_frame = tk.Frame(trigger_window)
        button_frame.pack(fill="x", pady=10)

        save_button = tk.Button(button_frame, text="Save", command=save_conditions)
        save_button.pack(side="left", padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=trigger_window.destroy)
        cancel_button.pack(side="right", padx=5)
       
        
    
    def center_window(self):
        """Center the application window."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCaptureSetupApp(root)
    root.state("zoomed")
    root.mainloop()
