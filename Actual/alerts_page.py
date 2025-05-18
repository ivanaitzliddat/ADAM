import tkinter as tk
import numpy as np
import cv2
import io
from PIL import Image, ImageTk
from config_handler import ConfigHandler
from processed_screenshot import Processed_Screenshot
from tkinter import ttk
import os
import tkinter.messagebox as tk_msgbox
from imageio.plugins.deviceslist import DevicesList
from datetime import datetime
from tkcalendar import DateEntry

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a label to display the number of devices
        self.device_count_label = tk.Label(self, text="Connected Devices: 0", font=("Arial", 12))
        self.device_count_label.pack(pady=10)

        self.starting_device_list = []
        self.device_states = {}  # Device states (True = connected)Dictionary to track device states (True for connected, False for disconnected)
        self.device_labels = {} # Store references to device labels for updating later

        # Create frames: top_frame for device connection status, filter and bottom_frame for other content
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.filter_frame = tk.Frame(self)
        self.filter_frame.pack(side="top", fill="x", padx=5, pady=5)

        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Load and resize monitor icons
        self.green_icon = self.load_resized_icon(os.path.join(ConfigHandler.dirname, "green_monitor.png"), 50, 50)  # Resize to 50x50 pixels
        self.red_icon = self.load_resized_icon(os.path.join(ConfigHandler.dirname, "red_monitor.png"), 50, 50)  # Resize to 50x50 pixels

        # Start polling for device changes (first call after initialization)
        self.poll_for_device_changes()

        # Initial device connection update
        self.update_device_display()

        # Filter entries inside the filter frame
        self.date_filter_entry = tk.Entry(self.filter_frame, width=30)
        self.date_filter_entry.insert(0, "Enter Date (e.g., 2025-02-16)")  # Default text
        self.date_filter_entry.bind("<FocusIn>", lambda event: self.clear_default_text(event, self.date_filter_entry, "Enter Date (e.g., 2025-02-16)"))
        self.date_filter_entry.bind("<FocusOut>", lambda event: self.restore_default_text(event, self.date_filter_entry, "Enter Date (e.g., 2025-02-16)"))
        self.time_filter_entry = tk.Entry(self.filter_frame, width=30)
        self.time_filter_entry.insert(0, "Enter Time (e.g., 01:05:38)")  # Default text
        self.time_filter_entry.bind("<FocusIn>", lambda event: self.clear_default_text(event, self.time_filter_entry, "Enter Time (e.g., 01:05:38)"))
        self.time_filter_entry.bind("<FocusOut>", lambda event: self.restore_default_text(event, self.time_filter_entry, "Enter Time (e.g., 01:05:38)"))
        self.message_filter_entry = tk.Entry(self.filter_frame, width=30)
        self.message_filter_entry.insert(0, "Enter Message (e.g., Alert: Rahul detected.)")  # Default text
        self.message_filter_entry.bind("<FocusIn>", lambda event: self.clear_default_text(event, self.message_filter_entry, "Enter Message (e.g., Alert: Rahul detected.)"))
        self.message_filter_entry.bind("<FocusOut>", lambda event: self.restore_default_text(event, self.message_filter_entry, "Enter Message (e.g., Alert: Rahul detected.)"))

        # Pack the filter entries in the window (inside the filter frame)
        self.date_filter_entry.pack(side="left", padx=5, pady=5)
        self.time_filter_entry.pack(side="left", padx=5, pady=5)
        self.message_filter_entry.pack(side="left", padx=5, pady=5)

        # Apply filter button (using pack inside the filter frame)
        filter_button = tk.Button(self.filter_frame, text="Filter Options", command=self.open_filter_window)
        filter_button.pack(side="left", padx=5, pady=5)

        # Clear filters button (using pack inside the filter frame)
        clear_button = tk.Button(self.filter_frame, text="Clear Filters", command=self.clear_filters)
        clear_button.pack(side="left", padx=5, pady=5)

        # Create a Treeview widget with three columns
        self.treeview = ttk.Treeview(self.bottom_frame, columns=("Date & Time", "Device", "TTS Message"), show="headings")
        self.treeview.heading("Date & Time", text="Date & Time")
        self.treeview.heading("Device", text="Device")
        self.treeview.heading("TTS Message", text="TTS Message")

        # Add a vertical scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self.bottom_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # Pack the Treeview widget
        self.treeview.pack(fill="both", expand=True)

        # Bind the click event to the Treeview rows
        self.treeview.bind("<ButtonRelease-1>", self.on_row_click)

        # To keep track of all messages passed from the MessageQueue
        self.all_messages = []

        # To keep track of the row_ids that are filtered
        self.detached_rows = []

 ################## Old Code for clickable buttons in list ##############################
        # # Create a canvas to contain the scrollable content
        # self.canvas = tk.Canvas(self.bottom_frame, bg="white", bd=2, relief="solid")
        # self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # # Create a scrollbar and associate it with the canvas
        # self.scrollbar = tk.Scrollbar(self.bottom_frame, orient="vertical", command=self.canvas.yview)
        # self.scrollbar.pack(side="right", fill="y")
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # # Create a frame inside the canvas to hold the messages
        # self.message_frame = tk.Frame(self.canvas)
        # self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

        # Update the scrollable region whenever the frame size changes
        # self.message_frame.bind("<Configure>", self.on_frame_configure)
#######################################################################################

    # Function to load and resize an image to the given width and height
    def load_resized_icon(self, image_path, width, height):
        img = Image.open(image_path)  # Open the image
        img = img.resize((width, height), Image.Resampling.LANCZOS)  # Resize the image
        return ImageTk.PhotoImage(img)  # Convert the resized image to a Tkinter-compatible format
     
    # "Update the display of connected devices with the appropriate icons
    def update_device_display(self):
        # Add devices that are not yet added to the UI
        for device in self.starting_device_list:
            custom_name = self.get_custom_name_from_alt_name(device)
            
            if device not in self.device_labels:
                # Decide which icon to show based on device state
                icon = self.green_icon if self.device_states.get(device, False) else self.red_icon
                device_label = tk.Label(self.top_frame, text=custom_name, image=icon, compound="left", font=("Arial", 12))
                device_label.pack(anchor="w", pady=5)
                self.device_labels[device] = device_label

            device_label = self.device_labels[device]
            icon = self.green_icon if self.device_states.get(device, False) else self.red_icon
            device_label.config(image=icon)
            device_label.config(text=custom_name)
            device_label.image = icon

        # Remove devices from the UI that are no longer in starting (they are disconnected)
        devices_to_remove = [device for device in self.device_labels if device not in self.starting_device_list]
        for device in devices_to_remove:
            self.device_labels[device].config(image=self.red_icon)  # Set red icon for disconnected devices
            self.device_labels[device].image = self.red_icon  # Update the image reference

    #Fetch device changes and update the display every 3 seconds
    def poll_for_device_changes(self):
        current_device_list = DevicesList.device_list # only contains alt_names

        # Compare the starting device list with the new list
        added_devices = set(current_device_list) - set(self.starting_device_list)
        removed_devices = set(self.starting_device_list) - set(current_device_list)

        # Add new devices to starting_device_list and mark them as connected
        for device in added_devices:
            self.starting_device_list.append(device)
            self.device_states[device] = True  # New device is connected

        # Mark removed devices as disconnected (but don't remove them from the list)
        for device in removed_devices:
            self.device_states[device] = False  # Device is disconnected
            self.starting_device_list.remove(device)
            custom_name = self.get_custom_name_from_alt_name(device)
            tk_msgbox.showinfo("Device Removed", f"This device: [{custom_name}] was removed.") # show popup for removed device

        # Update the display with the current state of the devices
        self.update_device_display()

        # Schedule the next call to poll_for_device_changes after 3000ms (3 seconds)
        self.after(3000, self.poll_for_device_changes)

    def append_message(self, message):
################### Old Code for clickable events in list #######################################
        # # Create a label for each message and make it clickable
        # clickable_label = tk.Label(self.message_frame, text=message, fg="blue", cursor="hand2", font=("Arial", 12),relief="solid", bd=1, padx=10, pady=5, anchor="w")
        # clickable_label.pack(padx=5, pady=5, fill="x")

        # # Bind the label to call on_message_click when clicked
        # # clickable_label.bind("<Button-1>", lambda event, msg=message: self.on_message_click(msg))
        # clickable_label.bind("<Button-1>", lambda event, idx=index: self.on_message_click(idx))
#################################################################################################
        # Using new treeview, above code is for older listbox

        # To format the datetime
        date_time_raw, alt_name, tts_text = message
        date_time = datetime.strptime(date_time_raw, "%Y%m%d %H%M%S") # formatting the string into a datetime object
        date_time_display = date_time.strftime("%Y/%m/%d %H:%MH") # what will be showed in the treeview

        self.all_messages.append({
            "date_time": date_time,
            "alt_name": alt_name,
            "tts_text": tts_text,
            "date_time_display": date_time_display
        })
        # Insert the parsed message into the Treeview
        self.treeview.insert("", 0, values=(date_time_display, alt_name, tts_text))


    def open_filter_window(self):
        filter_window = tk.Toplevel(self)
        filter_window.title("Filter Options")
        filter_window.geometry("400x300")  # width x height in pixels
        filter_window.grab_set()  # Modal behavior

        # Create a horizontal container
        date_frame = tk.Frame(filter_window)
        date_frame.pack(pady=10)

        # Start Date
        start_label = tk.Label(date_frame, text="Start Date:")
        start_label.pack(side="left", padx=(0, 5))
        start_date_entry = DateEntry(date_frame, date_pattern="yyyy/mm/dd", width=12)
        start_date_entry.pack(side="left", padx=(0, 20))

        # End Date
        end_label = tk.Label(date_frame, text="End Date:")
        end_label.pack(side="left", padx=(0, 5))
        end_date_entry = DateEntry(date_frame, date_pattern="yyyy/mm/dd", width=12)
        end_date_entry.pack(side="left")

        # Label above the dropdown
        alt_name_label = tk.Label(filter_window, text="Select Device (alt_name):")
        alt_name_label.pack(pady=(10, 0))

        # Dropdown
        alt_name_var = tk.StringVar()
        alt_name_options = list(set(msg["alt_name"] for msg in self.all_messages))
        alt_name_menu = ttk.Combobox(filter_window, textvariable=alt_name_var, values=alt_name_options, state="readonly")
        alt_name_menu.set("Choose a device")
        alt_name_menu.pack(pady=(0, 10))

        # Search for text message 
        tts_label = tk.Label(filter_window, text="Search Text")
        tts_label.pack()
        tts_entry = tk.Entry(filter_window)
        tts_entry.pack()

        apply_button = tk.Button(
            filter_window,
            text="Apply Filters",
            command=lambda: self.apply_filters(start_date_entry, end_date_entry, alt_name_var, tts_entry, filter_window)
        )
        apply_button.pack()


    def apply_filters(self, start_date_entry, end_date_entry, alt_name_var, tts_entry, filter_window):
        """ Function to apply the filters based on the entries """
        start = datetime.strptime(start_date_entry.get(), "%Y/%m/%d")
        end = datetime.strptime(end_date_entry.get(), "%Y/%m/%d")
        alt_name = alt_name_var.get()
        text = tts_entry.get()

        # Clear Treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Filter logic
        for msg in self.all_messages:
            if not (start <= msg["date_time"] <= end):
                continue
            if alt_name != "Select alt_name" and msg["alt_name"] != alt_name:
                continue
            if text and text not in msg["tts_text"].lower():
                continue

            self.treeview.insert("", "end", values=(msg["date_time_display"], msg["alt_name"], msg["tts_text"]))

        filter_window.destroy()  # Close popup        
            
    def clear_filters(self):
        """ Function to clear the filters and restore all data """
        # Clear the filter entry fields ## need it for clearing fields within the window
        # self.date_filter_entry.delete(0, tk.END)
        # self.time_filter_entry.delete(0, tk.END)
        # self.message_filter_entry.delete(0, tk.END)
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        for msg in self.all_messages:
            self.treeview.insert("", "end", values=(msg["date_time_display"], msg["alt_name"], msg["tts_text"]))

    def sharpen_image(image):
        kernel = np.array([[-1, -1, -1],
                        [-1,  9, -1],
                        [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)
    
    def on_row_click(self, event):
        try: 
            selected_item = self.treeview.selection()[0]
            item_data = self.treeview.item(selected_item)
            column_values = item_data['values']
            date_time = column_values[0]
            alt_name = column_values[1] 
            tts_message = column_values[2]
            self.on_message_click(alt_name, date_time)
        except Exception as e:
            tk_msgbox.showinfo("Error: Clicked on an invalid row. Please try to click again on the specific alert.")

    def on_message_click(self, alt_name, date_time):
        with Processed_Screenshot.lock:
            image_with_boxes = Processed_Screenshot.frames[alt_name][date_time]
            sharpened_image = AlertsPage.sharpen_image(image_with_boxes)
            # Convert image to Tkinter-compatible format
            pil_image = Image.fromarray(sharpened_image)

            # Resize the image if it's too large for the screen
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            max_width = screen_width * 0.8  # 80% of the screen width
            max_height = screen_height * 0.8  # 80% of the screen height
            
            image_width, image_height = pil_image.size
            if image_width > max_width or image_height > max_height:
                scaling_factor = min(max_width / image_width, max_height / image_height)
                new_width = int(image_width * scaling_factor)
                new_height = int(image_height * scaling_factor)
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            with io.BytesIO() as buffer:
                pil_image.save(buffer, format="PNG")
                buffer.seek(0)
                tk_image = ImageTk.PhotoImage(Image.open(buffer))

            # Create a new Tkinter window to display the image
            window = tk.Toplevel(self.frame)
            canvas = tk.Canvas(window, width=tk_image.width(), height=tk_image.height())
            canvas.pack()
            canvas.create_image(0, 0, anchor="nw", image=tk_image)

            # Keep a reference to avoid garbage collection
            window.image = tk_image

    def on_frame_configure(self, event):
        """Update the scrollable region when the frame is resized."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Helper function for the default text in filter
    def clear_default_text(self, event, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, tk.END)

    # Helper function for the default text in filter
    def restore_default_text(self, event, entry, default_text):
        if entry.get() == "":
            entry.insert(0, default_text)

    def get_custom_name_from_alt_name(self, alt_name):
        device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name = alt_name)
        custom_name = ""
        for key, val in device_dict.items():
            custom_name = val["custom_name"]
        return custom_name