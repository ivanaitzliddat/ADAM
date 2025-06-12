import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from tkinter import ttk
from config_handler import ConfigHandler
from imageio.plugins.deviceslist import DevicesList
import time
import Pmw
import imageio.v3 as iio
from PIL import Image, ImageTk
from screenshots import Screenshot
import numpy as np
import threading

from edit_device_settings import DeviceSettingsEditor

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
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.topbar = topbar
        self.proceed_to_alerts_page = proceed_to_alerts_page

        # First row (ADAM logo)
        self.first_row = tk.Frame(self.frame, bg=BG_COLOUR)
        self.first_row.pack(fill="x", pady=(10, 50))

        # Centered Page Header
        self.page_header = tk.Label(
            self.first_row,
            text="Video Capture Card Configuration",
            font=("Arial", 38),
            bg=BG_COLOUR
        )
        self.page_header.pack(pady=(0, 5))

        if fresh_setup_status:
            # Call the method to detect devices and save them into config.ini
            #self.detect_and_save_devices()
            for child in topbar.winfo_children():
                child.configure(state="disable")
        else:
            for child in topbar.winfo_children():
                child.configure(state="normal")

        # Second row (scrollable area)
        self.create_scrollable_second_row()

        # Fourth row (Save button)
        self.fourth_row = tk.Frame(self.frame, bg=BG_COLOUR)
        self.fourth_row.pack(fill="x", pady=20)
        proceed_button_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.proceed_button = tk.Button(
            self.fourth_row,
            text="Proceed to Alerts Page",
            font=proceed_button_font,
            command=lambda: self.reset_topbar(topbar)
        )
        self.proceed_button.pack(pady=20)

        if not fresh_setup_status:
            self.proceed_button.pack_forget()

        self.update_device_status()
        
        # Bind the on_resize function to the <Configure> event
        self.bind("<Configure>", self.on_resize)

        self.bind_mousewheel()
        self.refresh_video_frames()

    #to call this function when widget is destroyed so mousewheel can be used on the canvas
    def bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    #to call this function when edit_condition button is clicked so mousewheel cannot be used on canvas
    def unbind_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")

    #when edit_condition button is clicked, this function will be called
    def open_device_settings_editor(self, device_label, usb_alt_name):
        self.unbind_mousewheel() #unbind the mousewheel on canvas
        editor = DeviceSettingsEditor(device_label, usb_alt_name) #open the edit_conditino
        editor.protocol("WM_DELETE_WINDOW", lambda: (editor.destroy(), self.bind_mousewheel()))
        editor.wait_window() #when edit_condition window closed, bind mousewheel again for canvas
        self.bind_mousewheel()

    def refresh_video_frames(self):
        """Refresh the video frames every 5 seconds."""
        def refresh():
            for i, video_label in enumerate(self.video_labels):
                usb_alt_name = video_label.usb_alt_name
                self.get_one_frame_from_capture_device(video_label, i, usb_alt_name)
            self.after(5000, self.refresh_video_frames)  # Call refresh again after 5 seconds
        threading.Thread(target=refresh).start()
        #to add refresh on reading from config.ini and update the device frame again

    def reset_topbar(self,topbar):
        response = messagebox.askyesno("Proceed to Alerts Page?", "Have you completed the configuration for your video input(s) and wish to proceed to Alerts Page?")
        if response:
            for child in topbar.winfo_children():
                child.configure(state="normal")
            self.proceed_to_alerts_page()
            self.proceed_button.pack_forget()   

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
    
    def create_scrollable_second_row(self):
        """Create a scrollable second row with detected inputs."""
        self.second_row_frame = tk.Frame(self.frame, bg=FRAME_COLOUR)
        self.second_row_frame.pack(fill="both", expand=True)

        # Canvas for scrollable area
        self.canvas = tk.Canvas(
            self.second_row_frame, highlightbackground="black", highlightthickness=2, bg=FRAME_COLOUR
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

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Retrieve the number of devices from config.ini and populate the video_inputs dictionary
        self.populate_video_inputs()

    def on_resize(self, event=None):
        """Dynamically adjust the layout and font sizes based on window size."""
        # Ensure the window width is not smaller than the size of a single device_frame
        min_width = 550  # Minimum width for to display at least one device_frame
        min_height = 800  # Minimum height for one device_frame plus the button below (for first setup)
        min_dimension = max(min(min_width, min_height), 1)

        # Get the root window (Tk instance)
        root = self.winfo_toplevel()

        # Set the minimum size for the window
        root.wm_minsize(min_width, min_height)

        # Calculate the actual dimensions of the window
        current_width = max(self.winfo_width(), min_width)
        current_height = max(self.winfo_height(), min_height)

        # Adjust the page header font size dynamically
        header_font_size = max(10, min(58, current_width // 30))
        self.page_header.config(font=("Arial", header_font_size, "bold"))

        # Adjust the layout of device frames
        available_width = self.canvas.winfo_width()
        num_columns = max(1, available_width // 430)  # Calculate how many device_frames fit in a row
        for i, device_frame in enumerate(self.scrollable_frame.winfo_children()):
            row = i // num_columns
            column = i % num_columns
            device_frame.grid(row=row, column=column, padx=10, pady=10)

    def get_one_frame_from_capture_device(self, video_label, index_num, usb_alt_name):       
        iio_prep_end = time.time() + 2.5    # Let imageio prep for 2.5s from current time.
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
                
                    video_label.config(image=image_tk, width=430, height=300)
                    video_label.image = image_tk
        except Exception as e:
            print(f"An error has occurred with device {index_num}: {e}")

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
            device_monitoring_status = val["device_enabled"]
            device_connection_status = ""

            # first check if the device in config.ini is connected
            current_device_list = DevicesList.device_list
            if usb_alt_name in current_device_list:
                device_connection_status = True
            else:
                device_connection_status = False

            # Create a subframe for each video input
            device_frame = tk.Frame(
                self.scrollable_frame,
                highlightbackground=GRAB_ATTENTION_COLOUR_1,
                highlightthickness=4,
                width=430,
                height=530
            )

            device_frame.grid_propagate(False)
            device_frame.pack_propagate(False)
            device_frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)

            video_label = tk.Label(
                device_frame, text=f"", bg="black", fg="white", height=20, padx=5
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
            unique_name_label = tk.Label(name_frame, text=f"Device Default Name: ", font=("Arial", 10, "bold"), height=2)
            unique_name_label.pack(side="left")
            device_label = tk.Label(
                name_frame, text=usb_alt_name, font=("Arial", 10, "bold"), height=2
            )
            device_label.pack(side="left")

            #device connection status
            device_connection_status_frame = tk.Frame(device_frame)
            device_connection_status_frame.pack(fill="x")
            device_connection_status_label = tk.Label(device_connection_status_frame, text="Connection Status: ", font=("Arial", 10, "bold"), height=2)
            device_connection_status_label.pack(side="left")
            device_connection_status_entry = tk.Label(
                device_connection_status_frame, text="", font=("Arial", 10, "bold"), height=2
            )
            device_connection_status_entry.pack(side="left")

            #device monitoring status
            device_monitoring_status_frame = tk.Frame(device_frame)
            device_monitoring_status_frame.pack(fill="x")
            device_monitoring_status_label = tk.Label(device_monitoring_status_frame, text="Monitoring Status: ", font=("Arial", 10, "bold"), height=2)
            device_monitoring_status_label.pack(side="left")
            device_monitoring_status_entry = tk.Label(
                device_monitoring_status_frame, text="", font=("Arial", 10, "bold"), height=2
            )
            device_monitoring_status_entry.pack(side="left")

            # Create the Enable/Disable button
            enable_disable_monitoring_button = tk.Button(device_monitoring_status_frame, text="Enable/Disable")
            enable_disable_monitoring_button.pack(side="right",padx=5)

            # Desired Device Name Frame
            device_given_name_frame = tk.Frame(device_frame)
            device_given_name_frame.pack(fill="x")

            # Display the desired given name (user-defined name)
            device_given_name_label = tk.Label(device_given_name_frame, text="Given Name: ", font=("Arial", 10, "bold"), height=2)
            device_given_name_label.pack(side="left")
            device_given_name = tk.Label(
                device_given_name_frame, text=custom_name, font=("Arial", 10, "bold"), height=2
            )
            device_given_name.pack(side="left")

            # Frame to store the buttons below the video frame
            button_frame = tk.Frame(device_frame)
            button_frame.pack(fill="x")

            # Create the Edit Trigger Condition button
            device_trigger_condition_setting_button = tk.Button(button_frame, text="Edit Trigger Condition(s)", width=10,command=lambda device_label=device_given_name.cget("text"), usb_alt_name=usb_alt_name: self.open_device_settings_editor(device_label, usb_alt_name))
            device_trigger_condition_setting_button.pack(fill="both")
            if custom_name == "":
                device_trigger_condition_setting_button.config(state="disabled") 
                #create a tooltip using balloon widget
                balloon = Pmw.Balloon()
                #bind the balloon to the button
                balloon.bind(device_trigger_condition_setting_button, "Please rename the device first to enable this button")
            
            rename_button = tk.Button(device_given_name_frame, text="Rename", width=10, command=lambda device_label=device_given_name, usb_alt_name=usb_alt_name, trig_condition_button= device_trigger_condition_setting_button: self.rename_and_update_trigger_condition_button(device_label,usb_alt_name,trig_condition_button))
            rename_button.pack(side="right", padx=5)

            # Display the device connection status
            if device_connection_status == True: 
                device_connection_status_entry.config(text="Connected", fg="#6bc33f")
                #device_monitoring_status.config(text="Enabled", fg="#6bc33f")
                enable_disable_monitoring_button.config(state="normal")
            else:
                device_connection_status_entry.config(text="Disconnected", fg="RED")
                #device_monitoring_status.config(text="Disabled", fg="RED")
                enable_disable_monitoring_button.config(state="disabled")

            # Display the device monitoring status
            if device_monitoring_status == True: 
                device_monitoring_status_entry.config(text="Enabled", fg="#6bc33f")
                enable_disable_monitoring_button.config(text="Disable Monitoring")
            else:
                device_monitoring_status_entry.config(text="Disabled", fg="RED")
                enable_disable_monitoring_button.config(text="Enable Monitoring")

            # Store the usb_alt_name in the device_frame object
            device_frame.usb_alt_name = usb_alt_name
            # Store the connection status in the device_frame object
            device_frame.device_connection_status = device_connection_status
            # store the connection status entry in the device_frame object
            device_frame.device_connection_status_entry = device_connection_status_entry

            # Store the device monitoring status in the device_frame object
            device_frame.device_monitoring_status = device_monitoring_status
            # Store the device monitoring status entry in the device_frame object
            device_frame.device_monitoring_status_entry = device_monitoring_status_entry
            # Store the device monitoring status button in the device_frame object
            device_frame.enable_disable_monitoring_button = enable_disable_monitoring_button

            # Update the button's command after it is created
            enable_disable_monitoring_button.config(command=lambda device_frame=device_frame, usb_alt_name=usb_alt_name: self.enable_disable_device(device_frame, usb_alt_name))

            i += 1

    def enable_disable_device(self, device_frame, usb_alt_name):
        device_monitoring_status = device_frame.device_monitoring_status
        if device_monitoring_status == True:
            response = messagebox.askyesnocancel("Disable monitoring on this device", "Are you sure you want to disable monitoring on this device?\nThis will stop the video feed from this device.")
        else:
            response = messagebox.askyesnocancel("Enable monitoring on this device", "Are you sure you want to enable monitoring on this device?\nThis will start the video feed from this device.")
        
        """Once user clicks on yes, it will always change the device status to the opposite of what it is now and change the colour."""
        if response:
            device_monitoring_status = not device_monitoring_status
            device_frame.device_monitoring_status = device_monitoring_status
            ConfigHandler.set_cfg_input_device(usb_alt_name=usb_alt_name, device_enabled=device_monitoring_status)
            if device_monitoring_status == True:
                device_frame.device_monitoring_status_entry.config(text="Enabled", fg="#6bc33f")
                device_frame.enable_disable_monitoring_button.config(text="Disable Monitoring")
            else:
                device_frame.device_monitoring_status_entry.config(text="Disabled", fg="RED")
                device_frame.enable_disable_monitoring_button.config(text="Enable Monitoring")
            ConfigHandler.save_config()
    
    def update_device_status(self):
        """Update the device status based on the current device list."""
        #get the current device list from DevicesList
        device_list = DevicesList.device_list

        #get the current devices populated in the scrollable frame
        existing_device_list = []

        #loop through the populated device frames and check if the usb_alt_name is in the current device list
        for device_frame in self.scrollable_frame.winfo_children():
            if hasattr(device_frame, 'usb_alt_name'):
                usb_alt_name = device_frame.usb_alt_name
                existing_device_list.append(usb_alt_name)
                if usb_alt_name in device_list:
                    #print(f"Device {device_alt_name} is connected")
                    # Update the device connection status
                    device_frame.device_connection_status = True
                    device_frame.device_connection_status_entry.config(text="Connected", fg="#6bc33f")
                    device_frame.enable_disable_monitoring_button.config(state="normal")
                else:
                    #print(f"Device {device_alt_name} is disconnected")
                    # Update the device connection status
                    device_frame.device_connection_status = False
                    device_frame.device_connection_status_entry.config(text="Disconnected", fg="RED")
                    device_frame.enable_disable_monitoring_button.config(state="disabled")
                    device_frame.device_monitoring_status = False
                    device_frame.enable_disable_monitoring_button.config(text="Enable Monitoring")
                    device_frame.device_monitoring_status_entry.config(text="Disabled", fg="RED")
                    #if disconnected, set the monitoring status to false
                    ConfigHandler.set_cfg_input_device(usb_alt_name=usb_alt_name, device_enabled=False)
                    ConfigHandler.save_config()
            self.update_monitoring_status(device_frame,usb_alt_name)
        
        self.check_for_new_device(device_list,existing_device_list)

        # Schedule the next call to poll_for_device_changes after 5000ms (5 seconds)
        self.after(5000, self.update_device_status)

    def check_for_new_device(self,current_device_list,existing_device_list):
        """Check for new devices and update the UI accordingly."""
        # Check if any new devices are connected
        for device in current_device_list:
            if device not in existing_device_list:
                # New device detected, prompt the user of the new device, click on Ok and refresh the cam_setup_page
                # Show a message box with the new device information
                response = messagebox.showinfo("New Device Detected", f"New device detected")
                if response:
                    self.refresh_cam_setup_page()
                break

    def update_monitoring_status(self, device_frame, usb_alt_name):
        """Update the monitoring status of the device."""
        device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name = usb_alt_name)
        for key, val in device_dict.items():
            usb_alt_name = val["usb_alt_name"]
            custom_name = val["custom_name"]
            device_monitoring_status = val["device_enabled"]
            if device_monitoring_status == False:
                device_frame.enable_disable_monitoring_button.config(text="Enable Monitoring")
                device_frame.device_monitoring_status_entry.config(text="Disabled", fg="RED")
            else:
                device_frame.enable_disable_monitoring_button.config(text="Disable Monitoring")
                device_frame.device_monitoring_status_entry.config(text="Enabled", fg="#6bc33f")

    def refresh_cam_setup_page(self):
        """Refresh the camera setup page."""
        # Destroy the current scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Repopulate the scrollable frame with updated video input
        self.populate_video_inputs()

        # Update the device status
        self.update_device_status()

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
