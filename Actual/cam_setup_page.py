import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from tkinter import ttk
from config_handler import ConfigHandler
from edit_condition import edit_condition
from imageio.plugins.deviceslist import DevicesList
import time
import Pmw
import imageio.v3 as iio
from PIL import Image, ImageTk
from screenshots import Screenshot
import numpy as np
import threading


#o request config ini to store the following theme colours:
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 ="#FF934F"
GRAB_ATTENTION_COLOUR_2 ="#C3423F"


class VideoCaptureSetupApp(tk.Frame):
    def __init__(self, parent, topbar, fresh_setup_status, proceed_to_alerts_page):
        super().__init__(parent, bg=BG_COLOUR)

        # Create the main frame
        self.frame = tk.Frame(self, bg=BG_COLOUR)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.topbar = topbar
        self.proceed_to_alerts_page = proceed_to_alerts_page

        # First row (ADAM logo)
        self.first_row = tk.Frame(self.frame, bg=BG_COLOUR)
        self.first_row.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 50))
        self.page_header = tk.Label(
            self.first_row, text="Video Capture Card Configuration", font=("Malgun Gothic Semilight", 38), bg=BG_COLOUR
        )
        self.page_header.grid(row=0, column=0, pady=(0, 5))

        if fresh_setup_status:
            # Call the method to detect devices and save them into config.ini
            self.detect_and_save_devices()
            for child in topbar.winfo_children():
                child.configure(state="disable")
        else:
            for child in topbar.winfo_children():
                child.configure(state="normal")

        # Second row (scrollable area)
        self.create_scrollable_second_row()

        # Fourth row (Save button)
        self.fourth_row = tk.Frame(self.frame, bg=BG_COLOUR)
        self.fourth_row.grid(row=2, column=0, columnspan=2, sticky="ew", pady=20)
        proceed_button = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.proceed_button = tk.Button(self.fourth_row, text="Proceed to Alerts Page", font=proceed_button, command=lambda: self.reset_topbar(topbar))
        self.proceed_button.grid(row=0, column=0, pady=20)

        if not fresh_setup_status:
            self.proceed_button.grid_remove()

        self.refresh_video_frames()

    def refresh_video_frames(self):
        """Refresh the video frames every 5 seconds."""
        def refresh():
            for i, video_label in enumerate(self.video_labels):
                usb_alt_name = video_label.usb_alt_name
                self.get_one_frame_from_capture_device(video_label, i, usb_alt_name)
            self.after(5000, self.refresh_video_frames)
        threading.Thread(target=refresh).start()


    def reset_topbar(self,topbar):
        response = messagebox.askyesno("Proceed to Alerts Page?", "Have you completed the configuration for your video input(s) and wish to proceed to Alerts Page?")
        if response:
            for child in topbar.winfo_children():
                child.configure(state="normal")
            self.proceed_to_alerts_page()
            self.proceed_button.grid_remove()

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
        number_of_devices = len(DevicesList.device_list)
        
        # Wait for device_list to populate... Should add in a pop up if after a few loops still no device, for user to check if any device is even plugged in.
        counter = 0
        while number_of_devices == 0:
            if counter >= 5:
                if messagebox.askretrycancel("Unable to detect any USB capture cards",  "Ensure your USB capture cards are connected and try again. "
                                          +"You may need to restart your computer after plugging it in for the first time."):
                    counter = 0
                else:
                    raise RuntimeError
            else:
                print("Currently still 0, so waiting for awhile...")
                time.sleep(3)
                number_of_devices = len(DevicesList.device_list)
                counter += 1
        
        # Show loading popup
        popup, progress_bar, progress_label = self.show_loading_popup()
        progress_bar["maximum"] = number_of_devices

        # Wait for DevicesList.device_list to fully populate
        while len(Screenshot.frames) < number_of_devices:
            if not popup.winfo_exists():  # Ensure the popup is still open
                break

            current_devices = len(Screenshot.frames)
            progress_bar["value"] = current_devices
            progress_label.config(text=f"{int((current_devices / number_of_devices) * 100)}%")
            popup.update()
            time.sleep(0.1)

        # Close popup once device_list is fully populated
        if popup.winfo_exists():
            popup.destroy()

        # Remove old input devices
        ConfigHandler.del_input_device(usb_alt_name="")
        counter = 1
        # Add newly detected devices to Config.ini
        for device in DevicesList.device_list:
            default_custom_name = "Input Device " + str(counter)
            default_condition_name = "Default Condition Name " + str(counter)
            ConfigHandler.add_input_device(usb_alt_name=device)
            ConfigHandler.save_config()
            ConfigHandler.set_cfg_input_device(usb_alt_name=device, custom_name=default_custom_name)
            ConfigHandler.set_cfg_input_device(usb_alt_name=device, condition = "cond0", condition_name = default_condition_name)
            counter+=1
        # Save the updated config
        ConfigHandler.save_config()

    def create_scrollable_second_row(self):
        """Create a scrollable second row with detected inputs."""
        self.second_row_frame = tk.Frame(self.frame, bg=FRAME_COLOUR)
        self.second_row_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

        # Canvas for scrollable area
        self.canvas = tk.Canvas(
            self.second_row_frame, width=1900, height=900, highlightbackground="black", highlightthickness=2, bg=FRAME_COLOUR
            #self.second_row_frame, highlightbackground="black", highlightthickness=2, bg=FRAME_COLOUR
        )
        self.scrollbar = tk.Scrollbar(
            self.second_row_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg=FRAME_COLOUR)

        # Bind scrollable frame to canvas
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind mouse wheel event to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Add canvas and scrollbar to the grid
        self.canvas.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.scrollbar.grid(row=0, column=4, sticky="ns")

        # Retrieve the number of devices from config.ini and populate the video_inputs dictionary
        self.populate_video_inputs()

    def get_one_frame_from_capture_device(self, video_label, index_num, usb_alt_name):
        black_pixel_percentage = 0.95  # Define the percentage of black pixels needed to classify the frame as mostly black
        iio_prep_end = time.time() + 2.5    # Let imageio prep for 2.5s from current time.
        #device_index = f"<video0>"
        try:
            # Let imageio prep for 2.5s from current time.
            while time.time() < iio_prep_end:
                time.sleep(0.1)  # Sleep for a short duration to allow imageio to prepare
                    
            #get the image based on usb_alt_name
            for item in Screenshot.frames:
                if item['alt_name'] == usb_alt_name:
                    frame = item["current"]
                    # Convert the frame to an image
                    image = Image.fromarray(frame).resize((430,300))
                    image_tk = ImageTk.PhotoImage(image)
                
                    frame_colour_sum = np.sum(image_tk, axis=-1)  # Sum over the last axis in the Shape frame, which is the colour channel (R, G, B)

                    # Identify pure black pixels (where RGB sum is exactly 0)
                    black_pixels = frame_colour_sum == 0  # True if the pixel is exactly black
                    black_pixel_count = np.sum(black_pixels)  # Count the number of black pixels

                    # Calculate the total number of pixels in the frame
                    total_pixels = frame.shape[0] * frame.shape[1]  # Height * Width
                       
                    # Calculate the percentage of black pixels
                    black_pixel_ratio = black_pixel_count / total_pixels

                    # Check if the majority of the frame is black
                    if black_pixel_ratio > black_pixel_percentage:
                        # Display "No signal" text instead of the image
                        video_label.config(text="No signal", image='', bg="black", fg="white")
                        # Change this to handle the black screen       
                        print("Black frame detected!!")
                        print(f"Frame {index_num}: black pixel ratio = {black_pixel_ratio:.4f}")
                    else:
                        video_label.config(image=image_tk)
                        video_label.image = image_tk
                else:
                    video_label.config(text="No signal", image='', bg="black", fg="white")

        except Exception as e:
            print(f"An error occurred with device {index_num}: {e}")
            video_label.config(text="No signal", image='', bg="black", fg="white")

    def _on_mousewheel(self, event):
        """Scroll the canvas content with the mouse wheel."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def populate_video_inputs(self):
        """Populate the scrollable frame with video input elements."""
        self.video_labels = []  # Store video labels for refreshing 
        device_dict = ConfigHandler.get_cfg_input_devices()
        i = 0
        for key, val in device_dict.items():
            usb_alt_name = val["usb_alt_name"]
            custom_name = val["custom_name"]
            device_status = val["device_enabled"]

            # Create a subframe for each video input
            device_frame = tk.Frame(
                self.scrollable_frame,
                highlightbackground=GRAB_ATTENTION_COLOUR_1,
                highlightthickness=4,
                width=430,
                height=530
            )
            # Store the device status in the device_frame
            device_frame.device_status = device_status

            device_frame.grid_propagate(False)
            device_frame.pack_propagate(False)
            device_frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)

            video_label = tk.Label(
                device_frame, text=f"No Signal in Video Frame {i}", bg="black", fg="white", height=300, padx=5
            )
            video_label.pack(fill="x",pady=(0,5))

            # Store the usb_alt_name in the video_label object
            video_label.usb_alt_name = usb_alt_name
            self.video_labels.append(video_label)
            
            self.get_one_frame_from_capture_device(video_label,i,usb_alt_name)

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
            trig_condition_button = tk.Button(button_frame, text="Edit Trigger Conditions", width=10, command=lambda usb_alt_name=usb_alt_name: edit_condition(usb_alt_name))
            trig_condition_button.pack(fill="both")
            if custom_name == "":
                trig_condition_button.config(state="disabled") 
                #create a tooltip using balloon widget
                balloon = Pmw.Balloon()
                #bind the balloon to the button
                balloon.bind(trig_condition_button, "Please rename the device first to enable this button")
            
            rename_button = tk.Button(device_given_name_frame, text="Rename", width=10, command=lambda device_label=device_given_name, usb_alt_name=usb_alt_name, trig_condition_button= trig_condition_button: self.rename_and_update_trigger_condition_button(device_label,usb_alt_name,trig_condition_button))
            rename_button.pack(side="right", padx=5)

            # Create the Enable/Disable button
            enable_disable_button = tk.Button(button_frame, text="Enable/Disable")
            enable_disable_button.pack(fill="both")

            # Update the button's command after it is created
            enable_disable_button.config(command=lambda device_frame=device_frame, enable_disable_button=enable_disable_button, usb_alt_name=usb_alt_name: self.enable_disable_device(device_frame, enable_disable_button, usb_alt_name))

            if device_status == True: 
                device_frame.config(highlightbackground="#6bc33f")
                enable_disable_button.config(text="Disable Device")
            else:
                device_frame.config(highlightbackground="RED")
                enable_disable_button.config(text="Enable Device")

            i += 1

    def enable_disable_device(self, device_frame, enable_disable_button, usb_alt_name):
        device_status = device_frame.device_status
        if device_status == True:
            response = messagebox.askyesnocancel("Disable Device", "Are you sure you want to disable this device?\nThis will stop the video feed from this device.")
        else:
            response = messagebox.askyesnocancel("Enable Device", "Are you sure you want to enable this device?\nThis will start the video feed from this device.")
        
        """Once user clicks on yes, it will always change the device status to the opposite of what it is now and change the colour."""
        if response:
            device_status = not device_status
            device_frame.device_status = device_status
            ConfigHandler.set_cfg_input_device(usb_alt_name=usb_alt_name, device_enabled=device_status)
            if device_status == True:
                device_frame.config(highlightbackground="#6bc33f")
                enable_disable_button.config(text="Disable Device")
            else:
                device_frame.config(highlightbackground="RED")
                enable_disable_button.config(text="Enable Device")
            ConfigHandler.save_config()

    def rename_and_update_trigger_condition_button(self, device_label, usb_alt_name,trig_condition_button):
        """Prompt the user to rename the device."""
        rename_window = tk.Toplevel(self)
        rename_window.title(f"Rename Device for {usb_alt_name}")
        rename_window.geometry("300x150")
        rename_window.transient(self)
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
                #change_button_state = True
                trig_condition_button.config(state="normal")

                rename_window.destroy()
            else:
                messagebox.showwarning("Warning", "Name cannot be empty!")
 
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCaptureSetupApp(root, lambda page: print(f"switch to {page}"))
    app.pack(fill="both",expand = True)
    root.mainloop()
