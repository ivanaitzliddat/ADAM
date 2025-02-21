import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from screen_capturer import ScreenCapturer
from config_handler import ConfigHandler
from edit_condition import edit_condition
import Pmw
import time
from imageio.plugins.deviceslist import DevicesList
import imageio.v3 as iio
from PIL import Image, ImageTk
from tkinter import ttk


#o porpose using config ini to store the following theme colours:
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 ="#FF934F"
GRAB_ATTENTION_COLOUR_2 ="#C3423F"

class InitialVideoCaptureSetup:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Capture Card Configuration")
        self.root.geometry("1920x1080")
        self.root.state("zoomed")
        self.root.configure(bg=BG_COLOUR)
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Prevent user from resizing this window
        self.root.resizable(False,False)   

        # Create the main frame
        self.frame = tk.Frame(root, bg=BG_COLOUR)
        self.frame.pack(pady=20)

        # First row (ADAM logo)
        self.first_row = tk.Frame(self.frame, bg=BG_COLOUR)
        self.first_row.pack(fill="both")
        self.logo_label1 = tk.Label(
            self.first_row, text="Video Capture Card Configuration", font=("Malgun Gothic Semilight", 38,), bg=BG_COLOUR
        )
        self.logo_label1.pack()

        # Call the method to detect devices and save them into config.ini
        num_of_devices = self.detect_and_save_devices()

        if num_of_devices == 0:
            messagebox.showinfo("No video inputs detected. Please ensure all the video inputs are connected to the capture card correctly.")
            self.root.destroy()
  
        # Second row (scrollable area)
        self.create_scrollable_second_row()

        # Fourth row (Save button)
        self.fourth_row = tk.Frame(self.frame, bg=BG_COLOUR)
        self.fourth_row.pack(fill="both")
        save_button_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.save_button = tk.Button(self.fourth_row, text="Save Configuration", font=save_button_font, command=self.save)
        self.save_button.pack(pady=20)

        # Center the window
        self.root.after(100,  lambda: self.center_window(self.root))

    def show_loading_popup(self):
        popup = tk.Tk()
        popup.title("Fetching info from connected devices")
        popup.geometry("500x100")
        label = ttk.Label(popup, text="Please wait while ADAM is fetching information from the connected devices")
        label.pack(pady=10)
        
        # Calculate the center position
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        window_width = 500
        window_height = 100
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        #Progress bar with percentage
        progress_bar = ttk.Progressbar(popup, orient="horizontal", length=200, mode="determinate")
        progress_bar.pack(pady=10)
        progress_label = ttk.Label(popup, text="0%")
        progress_label.pack()

        return popup, progress_bar, progress_label
    
    def detect_and_save_devices(self):
        """Detect available video devices and update config."""
        # Get the number of connected devices
        number_of_devices = ScreenCapturer.get_num_of_devices()
        
        # Show loading popup
        popup, progress_bar, progress_label = self.show_loading_popup()
        progress_bar["maximum"] = number_of_devices

        # Wait for DevicesList.device_list to fully populate
        while len(DevicesList.device_list) != number_of_devices:
            if not popup.winfo_exists():  # Ensure the popup is still open
                break

            current_devices = len(DevicesList.device_list)
            progress_bar["value"] = current_devices
            progress_label.config(text=f"{int((current_devices / number_of_devices) * 100)}%")
            popup.update()
            time.sleep(0.1)

        # Close popup once device_list is fully populated
        if popup.winfo_exists():
            popup.destroy()

        # Remove old input devices
        ConfigHandler.del_input_device(usb_alt_name="")

        # Add newly detected devices to Config.ini
        for device in DevicesList.device_list:
            ConfigHandler.add_input_device(usb_alt_name=device)

        # Save the updated config
        ConfigHandler.save_config()

        return len(DevicesList.device_list)

    def save(self):
        proceed_to_save = False
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for button in widget.winfo_children():
                    if isinstance(button, tk.Button) and button.cget("text") == "Trigger Conditions" and button["state"] == "disabled":
                        proceed_to_save = False
                    else:
                        proceed_to_save = True
        if proceed_to_save == False:
            print("hello")
            messagebox.showwarning("Incomplete Configuration", "Please complete the configuration for all devices.")
        else:
            #to be replaced with switching to the alerts_page or the main.py from Actual folder
            self.root.destroy()  # Close the current window
            import main as main
            main.run_ADAM()
            
    def create_scrollable_second_row(self):
        """Create a scrollable second row with detected inputs."""
        self.second_row_frame = tk.Frame(self.frame)
        self.second_row_frame.pack(fill="both", expand=True)

        # Canvas for scrollable area
        self.canvas = tk.Canvas(
            self.second_row_frame, width=1890, height=800, highlightbackground="black", highlightthickness=2 ,bg=FRAME_COLOUR  
        )
        self.scrollbar = tk.Scrollbar(
            self.second_row_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas,bg=FRAME_COLOUR)

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

    def get_one_frame_from_capture_device(self, video_label, index_num):
        device_index = f"<video{index_num}>"
        try:
            frame_count = 0
            for frame in iio.imiter(device_index):
                # Convert the frame to an image
                image = Image.fromarray(frame).resize((430,300))
                image_tk = ImageTk.PhotoImage(image)
                
                video_label.config(image=image_tk)
                video_label.image = image_tk
                
                frame_count += 1
                if frame_count == 1:  # Limit to 1 frame
                    break

        except Exception as e:
            print(f"An error occurred with device {index_num}: {e}")

                # Function to display the frame in a tkinter window

    def populate_video_inputs(self):
        """Populate the scrollable frame with video input elements."""
         
        device_dict = ConfigHandler.get_cfg_input_devices()
        i = 0
        for key, val in device_dict.items():
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
                highlightbackground=GRAB_ATTENTION_COLOUR_1,
                highlightthickness=4,
                width=450,
                height=500
            )

            device_frame.grid_propagate(False)
            device_frame.pack_propagate(False)
            device_frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)

            # Video Frame Placeholder
            video_label = tk.Label(
                device_frame, text=f"Video Frame {i} = to hold 1 frame from each input", bg="black", fg="white", height=300, padx=5
            )
            video_label.pack(fill="x", pady=5)

            self.get_one_frame_from_capture_device(video_label,i)

            # Display the device sequence number
            device_seq_num_frame = tk.Frame(device_frame)
            device_seq_num_frame.pack(fill="x", pady=5)
            device_seq_num_label = tk.Label(
                device_seq_num_frame, text=key, font=("Arial", 10, "bold")
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

            # Trigger Condition Button
            button_frame = tk.Frame(device_frame)
            button_frame.pack(fill="x")
            trig_condition_button = tk.Button(button_frame, text="Trigger Conditions", width=10, height=3, command=lambda usb_alt_name=usb_alt_name: edit_condition(usb_alt_name))
            trig_condition_button.pack(fill="both")
            if custom_name == "":
                trig_condition_button.config(state="disabled") 
                #create a tooltip using balloon widget
                balloon = Pmw.Balloon(self.root)
                #bind the balloon to the button
                balloon.bind(trig_condition_button, "Please rename the device first to enable this button")
            
            rename_button = tk.Button(device_given_name_frame, text="Rename", width=10, command=lambda device_label=device_given_name, usb_alt_name=usb_alt_name, trig_condition_button= trig_condition_button: self.rename_and_update_trigger_condition_button(device_label,usb_alt_name,trig_condition_button))
            rename_button.pack(side="right", padx=5)

            i += 1
    
    def rename_and_update_trigger_condition_button(self, device_label, usb_alt_name,trig_condition_button):
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

        tk.Button(rename_window, text="Save", command=lambda: save_name(device_label, usb_alt_name, trig_condition_button)).pack(side="left", padx=10, pady=20)
        tk.Button(rename_window, text="Cancel", command=rename_window.destroy).pack(side="right", padx=10, pady=20)

        def save_name(device_label, usb_alt_name,trig_condition_button):
            new_name = str(name_entry.get())
            usb_alt_name = str(usb_alt_name)
            if new_name:
                ConfigHandler.set_cfg_input_device(usb_alt_name=usb_alt_name, custom_name=new_name)
                ConfigHandler.save_config()
                device_label.config(text=new_name)  # Update the label with the new name
                messagebox.showinfo("Success", f"Device renamed to '{new_name}'!")
                change_button_state = True
                trig_condition_button.config(state="normal")

                rename_window.destroy()
            else:
                messagebox.showwarning("Warning", "Name cannot be empty!")
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")      

    def start_video_capture_setup():
        root = tk.Tk()
        app = InitialVideoCaptureSetup(root)
        root.mainloop()

    if __name__ == "__main__":
        start_video_capture_setup()
