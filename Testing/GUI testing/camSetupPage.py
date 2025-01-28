import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from tkinter import font as tkFont
from PIL import Image, ImageTk
import random
import string


class VideoCaptureSetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to ADAM")
        self.root.geometry("1920x1080")

        self.video_inputs = {}

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
            self.second_row_frame, width=1920, height=1000, highlightbackground="grey", highlightthickness=1
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

        # Generate and populate video inputs
        self.video_inputs = self.generate_video_inputs(7)
        self.populate_video_inputs(self.video_inputs)

    def generate_unique_name(self):
        """Generate a unique 8-character string."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def generate_video_inputs(self,num_devices):
        """Generate and return a dictionary of video inputs."""
        video_inputs = {}
        for i in range(num_devices): #simulate # devices connected
            video_inputs[f"videoinput {i}"] = {
                "uniqueName": self.generate_unique_name(),
                "givenName": f"Video Input Device {i}",  
                "triggerConditions": {
                    "trigger0":{"KEYWORDS":["test1", "testx", "testa"],"COLOR":"color123","MESSAGE":"test message"},
                    "trigger1":{"KEYWORDS":["test2"],"COLOR":"oi2","MESSAGE":"test message2"},
                    "trigger2":{"KEYWORDS":["test3"],"COLOR":"oi3","MESSAGE":"test message3"}
                    }
                }
        return video_inputs

    def populate_video_inputs(self, video_inputs):
        """Populate the scrollable frame with video input elements."""
        for i, (key, video_input) in enumerate(video_inputs.items()):
            # Create a subframe for each video input
            device_frame = tk.Frame(
                self.scrollable_frame,
                highlightbackground="grey",
                highlightthickness=1,
                width=460,
                height=500,
                bg="white",
            )
            #print(video_inputs[key])
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

            # Display the unique device name
            unique_name_label = tk.Label(name_frame, text="Device Default Name: ", font=("Arial", 10, "bold"), height=3)
            unique_name_label.pack(side="left")
            device_label = tk.Label(
                name_frame, text=video_input["uniqueName"], font=("Arial", 10, "bold"), height=3
            )
            device_label.pack(side="left")

            # Desired Device Name Frame
            device_given_name_frame = tk.Frame(device_frame)
            device_given_name_frame.pack(fill="x", pady=5)

            # Display the desired given name (user-defined name)
            device_given_name_label = tk.Label(device_given_name_frame, text="Given Name: ", font=("Arial", 10, "bold"), height=3)
            device_given_name_label.pack(side="left")
            device_given_name = tk.Label(
                device_given_name_frame, text=video_input["givenName"], font=("Arial", 10, "bold"), height=3
            )
            device_given_name.pack(side="left")

            rename_button = tk.Button(device_given_name_frame, text="Rename", width=10, command=lambda video_data=video_inputs[key]: self.rename_device(video_data))
            rename_button.pack(side="right", padx=5)

            # Trigger Condition Button
            button_frame = tk.Frame(device_frame)
            button_frame.pack(fill="x")
            trig_condition_button = tk.Button(
                button_frame, text="Trigger Conditions", width=10, height=3, command=lambda video_data=video_inputs[key]: self.trigger_condition(video_data),
            )
            trig_condition_button.pack(fill="both")

    def rename_device(self, video_data):
        """Prompt the user to rename the device."""
        rename_window = tk.Toplevel(self.root)
        rename_window.title("Rename Device")
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

        tk.Button(rename_window, text="Save", command=lambda: save_name(video_data)).pack(side="left", padx=10, pady=20)
        tk.Button(rename_window, text="Cancel", command=rename_window.destroy).pack(side="right", padx=10, pady=20)
       
        def save_name(video_data):
            new_name = name_entry.get().strip()
            if new_name:
                video_data["givenName"] = new_name
                messagebox.showinfo("Success", f"Device renamed to '{new_name}'!")
                rename_window.destroy()
            else:
                messagebox.showwarning("Warning", "Name cannot be empty!")
      
    def trigger_condition(self, video_data):
        """Display the trigger conditions for the selected device."""
        givenName=video_data["givenName"]
        # Create a new window
        trigger_window = tk.Toplevel(self.root)
        trigger_window.title(f"Configuring alert trigger conditions for {givenName}")
        trigger_window.geometry("1100x600")
        trigger_window.transient(self.root)
        trigger_window.grab_set()

        # 1st Row: Title Label
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
        

        '''test'''

        def delete_condition(condition_frame):
            """Delete a specific condition frame."""
            condition_frame.destroy()

        def delete_keyword(keyword_field, keyword_label):
            """Delete a specific keyword field."""
            keyword_field.destroy()
            keyword_label.destroy()

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

        # If there are existing conditions for the video inputs, auto populate the conditions into the scrollable frame in 2nd row
        if len(video_data) != 0:
            uniqueName=video_data["uniqueName"]  
            
            conditions = video_data["triggerConditions"].keys()
            
            for condition in conditions:
                num_of_conditions=len(video_data)
                num_of_keywords=0
                condition_frame = tk.Frame(scrollable_conditions_frame, pady=5, highlightbackground="grey", highlightthickness=1)
                condition_frame.pack(fill="x", pady=5)
                # 1st row: Display the trigger condition text
                tk.Label(
                    condition_frame,
                    text=f"{condition}",
                    font=("Arial", 10, "bold"),
                    anchor="w",
                ).pack(fill="x", padx=5, pady=2)

                # 2nd row: Button for Keyword
                keyword_button_frame = tk.Frame(condition_frame)
                keyword_button_frame.pack(fill="x", padx=5, pady=2)

                keyword_button = tk.Button(keyword_button_frame, text="Add Keyword", command="")
                keyword_button.pack(side="left", padx=5)

                # 3rd row: Button for Color Picker
                color_picker_button_frame = tk.Frame(condition_frame)
                color_picker_button_frame.pack(fill="x", padx=5, pady=2)

                color_button = tk.Button(color_picker_button_frame, text="Add a Color", command="")
                color_button.pack(side="left", padx=5)

                keywords =  video_data["triggerConditions"][condition]["KEYWORDS"] #returns a list of keywords
                for keyword in keywords:
                    #print(keyword)
                    """Add a keyword input field."""
                    keyword_label = tk.Label(keyword_button_frame, text=f"Keyword {num_of_keywords+1}", font=("Arial", 10))
                    keyword_label.pack(side="left")
                    keyword_entry = tk.Entry(keyword_button_frame,width=20)
                    keyword_entry.insert(0,keyword)
                    keyword_entry.pack(side="left", padx=5)
                    
                    delete_keyword_button = tk.Button(
                    keyword_button_frame,
                    text="X",
                    font=("Arial", 8, "bold"),
                    fg="red",
                    command=lambda e=keyword_entry, l=keyword_label: delete_keyword(e, l))
                    delete_keyword_button.pack(side="left", padx=5)

                    num_of_keywords+=1 #to track number of keyword fields

                

                colorCode = video_data["triggerConditions"][condition]["COLOR"]
                color_label = tk.Label(color_picker_button_frame, text="Color Code:", font=("Arial", 10))
                color_label.pack(side="left", padx=5)
                color_entry = tk.Entry(color_picker_button_frame, width=20)
                color_entry.insert(0,colorCode)
                color_entry.pack(side="left", padx=5)

                TTSmessage = video_data["triggerConditions"][condition]["MESSAGE"]
                custom_message_frame = tk.Frame(condition_frame)
                custom_message_frame.pack(fill="x", padx=5, pady=5)

                TTSmessageLabel = tk.Label(custom_message_frame, text="Custom Message:", font=("Arial", 10))
                TTSmessageLabel.pack(side="left", padx=5)
                TTSmessageEntry = tk.Entry(custom_message_frame, width=50)
                TTSmessageEntry.insert(0,TTSmessage)
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
