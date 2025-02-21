import tkinter as tk
import numpy as np
import cv2
import io
from PIL import Image, ImageTk
from config_handler import ConfigHandler
from processed_screenshot import Processed_Screenshot
from tkinter import ttk
import os
from imageio.plugins.deviceslist import DevicesList

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
        apply_button = tk.Button(self.filter_frame, text="Apply Filters", command=self.apply_filters)
        apply_button.pack(side="left", padx=5, pady=5)

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

        # Message Queue that is tracked on the frontend for filters
        self.frontend_messages_with_index = {}
        self.filtered_frontend_messages_with_index = {}

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
            if device not in self.device_labels:
                # Decide which icon to show based on device state
                icon = self.green_icon if self.device_states.get(device, False) else self.red_icon
                device_label = tk.Label(self.top_frame, text=device, image=icon, compound="left", font=("Arial", 12))
                device_label.pack(anchor="w", pady=5)
                self.device_labels[device] = device_label

            device_label = self.device_labels[device]
            icon = self.green_icon if self.device_states.get(device, False) else self.red_icon
            device_label.config(image=icon)
            device_label.image = icon

        # Remove devices from the UI that are no longer in starting (they are disconnected)
        devices_to_remove = [device for device in self.device_labels if device not in self.starting_device_list]
        for device in devices_to_remove:
            self.device_labels[device].config(image=self.red_icon)  # Set red icon for disconnected devices
            self.device_labels[device].image = self.red_icon  # Update the image reference

    #Fetch device changes and update the display every 5 seconds
    def poll_for_device_changes(self):
        current_device_list = DevicesList.device_list # only contains alt_names

        # Compare the starting device list with the new list
        added_devices = set(current_device_list) - set(self.starting_device_list)
        removed_devices = set(self.starting_device_list) - set(current_device_list)

        # Add new devices to starting_device_list and mark them as connected
        for device in added_devices:
            self.starting_device_list.append(device)
            self.device_states[device] = True  # New device is connected
            # need to add to add to config.ini if it does not exist there

        # Mark removed devices as disconnected (but don't remove them from the list)
        for device in removed_devices:
            self.device_states[device] = False  # Device is disconnected
            self.starting_device_list.remove(device)
            # need to show alert pop-up saying device disconnected 

        # Update the display with the current state of the devices
        self.update_device_display()

        # Schedule the next call to poll_for_device_changes after 5000ms (5 seconds)
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
        date_time, alt_name, tts_text = message
        # Insert the parsed message into the Treeview
        self.treeview.insert("", "end", values=(date_time, alt_name, tts_text))
    
    def apply_filters(self):
        """ Function to apply the filters based on the entries """
        self.filtered_frontend_messages_with_index = []
        for row in self.frontend_messages_with_index:
            # Check each filter independently
            match = True
            
            # Filter by date if it is not empty
            if self.date_filter_entry.get() and self.date_filter_entry.get() != "Enter Date (e.g., 2025-02-16)":
                if self.date_filter_entry.get() not in row[0]:  # Assuming date is in row[0]
                    match = False
            
            # Filter by time if it is not empty
            if self.time_filter_entry.get() and self.time_filter_entry.get() != "Enter Time (e.g., 01:05:38)":
                if self.time_filter_entry.get() not in row[1]:  # Assuming time is in row[1]
                    match = False
            
            # Filter by message if it is not empty
            if self.message_filter_entry.get() and self.message_filter_entry.get() != "Enter Message (e.g., Alert: Rahul detected.)":
                if self.message_filter_entry.get() not in row[2]:  # Assuming message is in row[2]
                    match = False
            
            # If the row matches all non-empty filters, add it to the filtered data list
            if match:
                self.filtered_frontend_messages_with_index.append(row)
    
        self.clear_treeview()
        # Update the Treeview with filtered data
        self.insert_rows(self.filtered_frontend_messages_with_index)
    
    def clear_filters(self):
        """ Function to clear the filters and restore all data """
        # Clear the filter entry fields
        print('clearing filters')
        self.date_filter_entry.delete(0, tk.END)
        self.time_filter_entry.delete(0, tk.END)
        self.message_filter_entry.delete(0, tk.END)

        # Restore all rows from the original data
        self.clear_treeview()
        self.insert_rows(self.frontend_messages_with_index)
    
    def clear_treeview(self):
        """ Helper function to clear all rows in the Treeview """
        for row in self.treeview.get_children():
            self.treeview.delete(row)

    def insert_rows(self, frontend_messages_with_index):
        for item in frontend_messages_with_index:
            print(item)
        """ Helper function to insert rows into the Treeview """
        for index, message in frontend_messages_with_index:
            date, time, message_text = self.process_message(message)
            self.treeview.insert("", "end", values=(date, time, message_text),tags=(index,))

    def sharpen_image(image):
        kernel = np.array([[-1, -1, -1],
                        [-1,  9, -1],
                        [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)
    
    def on_row_click(self, event):
        selected_item = self.treeview.selection()[0]
        item_data = self.treeview.item(selected_item)
        column_values = item_data['values']
        date_time = column_values[0]
        alt_name = column_values[1] 
        tts_message = column_values[2]
        self.on_message_click(alt_name, date_time)

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