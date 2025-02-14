import tkinter as tk
import numpy as np
import cv2
import io
from PIL import Image, ImageTk
from config_handler import ConfigHandler
from processed_screenshot import Processed_Screenshot
from screen_capturer import ScreenCapturer 
from tkinter import ttk
from tkinter import PhotoImage


class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a label to display the number of devices
        self.device_count_label = tk.Label(self, text="Connected Devices: 0", font=("Arial", 12))
        self.device_count_label.pack(pady=10)

        # Initialize custom_names as an empty list
        #self.custom_names = []
        #self.device_states = {}  # Dictionary to track device states (True for connected, False for disconnected)
        self.custom_names = ["Device 1", "Device 2", "Device 3"]  # Example custom_names list
        self.device_states = {"Device 1": True, "Device 2": True, "Device 3": True}  # Device states (True = connected)
        self.device_labels = {}

        # Create two frames: top_frame for icons and bottom_frame for other content
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Load and resize monitor icons
        self.green_icon = self.load_resized_icon(r"C:\Users\user\Desktop\ADAM\Images\green monitor.png", 50, 50)  # Resize to 50x50 pixels
        self.red_icon = self.load_resized_icon(r"C:\Users\user\Desktop\ADAM\Images\red monitor.png", 50, 50)  # Resize to 50x50 pixels

        # Initialize device display (top_frame) with the initial device states
        # self.device_labels = {}  # Store references to device labels for updating later

        # Start polling for device changes (first call after initialization)
        self.poll_for_device_changes()

        # Initial UI update
        self.update_device_display()

        # Create a Treeview widget with three columns
        self.treeview = ttk.Treeview(self.frame, columns=("Date", "Time", "Message"), show="headings")
        self.treeview.heading("Date", text="Date")
        self.treeview.heading("Time", text="Time")
        self.treeview.heading("Message", text="Message")

        # Add a vertical scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # Pack the Treeview widget
        self.treeview.pack(fill="both", expand=True)

        # Bind the click event to the Treeview rows
        self.treeview.bind("<ButtonRelease-1>", self.on_message_click)

        # # Create a canvas to contain the scrollable content
        # self.canvas = tk.Canvas(self.frame, bg="white", bd=2, relief="solid")
        # self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # # Create a scrollbar and associate it with the canvas
        # self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        # self.scrollbar.pack(side="right", fill="y")
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # # Create a frame inside the canvas to hold the messages
        # self.message_frame = tk.Frame(self.canvas)
        # self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

        # # Update the scrollable region whenever the frame size changes
        # self.message_frame.bind("<Configure>", self.on_frame_configure)

    # Function to load and resize an image to the given width and height
    def load_resized_icon(self, image_path, width, height):
        img = Image.open(image_path)  # Open the image
        img = img.resize((width, height), Image.Resampling.LANCZOS)  # Resize the image
        return ImageTk.PhotoImage(img)  # Convert the resized image to a Tkinter-compatible format
    
    #Update the display of connected devices with the appropriate icons
    # def update_device_display(self):
    #     for device_name in self.custom_names:
    #         # Determine the icon (green for connected, red for disconnected)
    #         if self.device_states.get(device_name, False):  # If connected
    #             icon = self.green_icon
    #         else:  # If disconnected
    #             icon = self.red_icon

    #         # If the device doesn't already have a label, create one
    #         if device_name not in self.device_labels:
    #             device_label = tk.Label(self.top_frame, text=device_name, image=icon, compound="left", font=("Arial", 12))
    #             device_label.pack(anchor="w", pady=5)
    #             self.device_labels[device_name] = device_label  # Save the label reference

    #         # Update the icon (in case it changed from green to red or vice versa)
    #         device_label = self.device_labels[device_name]
    #         device_label.config(image=icon)
    #         device_label.image = icon  # Keep a reference to prevent garbage collection

    # #Fetch device changes and update the display every 5 seconds
    # def poll_for_device_changes(self):
    #     # Fetch the latest custom_names from ConfigHandler
    #     device_details = ConfigHandler.get_cfg_input_devices_temp()
    #     new_custom_names = [device["custom_name"] for device in device_details.values()]

    #     # Compare the old custom_names with the new list
    #     added_devices = set(new_custom_names) - set(self.custom_names)
    #     removed_devices = set(self.custom_names) - set(new_custom_names)

    #     # Add new devices to custom_names and mark them as connected
    #     for device in added_devices:
    #         self.custom_names.append(device)
    #         self.device_states[device] = True  # New device is connected

    #     # Mark removed devices as disconnected (but don't remove them from the list)
    #     for device in removed_devices:
    #         self.device_states[device] = False  # Device is disconnected

    #     # Update the display with the current state of the devices
    #     self.update_device_display()

    #     # Schedule the next call to poll_for_device_changes after 5000ms (5 seconds)
    #     self.after(5000, self.poll_for_device_changes)


    ######################

    def update_device_display(self):
        """Update the display of connected devices with the appropriate icons"""
        # Add devices that are not yet added to the UI
        for device_name in self.custom_names:
            if device_name not in self.device_labels:
                # Decide which icon to show based on device state
                icon = self.green_icon if self.device_states.get(device_name, False) else self.red_icon
                device_label = tk.Label(self.top_frame, text=device_name, image=icon, compound="left", font=("Arial", 12))
                device_label.pack(anchor="w", pady=5)
                self.device_labels[device_name] = device_label

            device_label = self.device_labels[device_name]
            icon = self.green_icon if self.device_states.get(device_name, False) else self.red_icon
            device_label.config(image=icon)
            device_label.image = icon

        # Remove devices from the UI that are no longer in custom_names (they are disconnected)
        devices_to_remove = [device for device in self.device_labels if device not in self.custom_names]
        for device in devices_to_remove:
            self.device_labels[device].config(image=self.red_icon)  # Set red icon for disconnected devices
            self.device_labels[device].image = self.red_icon  # Update the image reference

    def simulate_device_removal(self):
        """Simulate device removal (for testing purposes)"""
        # Simulate the removal of Device 1
        if "Device 1" in self.custom_names:
            self.custom_names.remove("Device 1")  # Remove the device from the list
            # Mark it as disconnected in device states
            self.device_states["Device 1"] = False
            # Manually call the display update to reflect the change
            self.update_device_display()

    def poll_for_device_changes(self):
        """Simulate polling for device changes"""
        # Example: Manually trigger device removal after a delay
        self.after(5000, self.simulate_device_removal)  # Call simulate_device_removal() after 5 seconds


#########################

    def append_message(self, message, index):
        # # Create a label for each message and make it clickable
        # clickable_label = tk.Label(self.message_frame, text=message, fg="blue", cursor="hand2", font=("Arial", 12),relief="solid", bd=1, padx=10, pady=5, anchor="w")
        # clickable_label.pack(padx=5, pady=5, fill="x")

        # # Bind the label to call on_message_click when clicked
        # # clickable_label.bind("<Button-1>", lambda event, msg=message: self.on_message_click(msg))
        # clickable_label.bind("<Button-1>", lambda event, idx=index: self.on_message_click(idx))
        # Parse the message into date, time, and remaining text
        message = message.strip('[]')  # Remove the square bracketss
        date, time_text, text = message.split(' ', 2)  # Split date, time, and the remaining text
        
        # Insert the parsed message into the Treeview
        self.treeview.insert("", "end", values=(date, time_text, text))
        # Insert the parsed data into the Treeview and tag each row
        item_id = self.treeview.insert("", "end", values=(date, time_text, text))
        
        # Now bind a custom tag or function to handle the row click
        self.treeview.tag_bind(item_id, "<ButtonRelease-1>", lambda event, item_id=item_id, index=index: self.on_row_click(event, item_id, index))

    def sharpen_image(image):
        kernel = np.array([[-1, -1, -1],
                        [-1,  9, -1],
                        [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)
    
    def on_row_click(self, event, item_id, index):
        # Get the values of the clicked row based on item_id
        item_values = self.treeview.item(item_id)["values"]
        date, time, message = item_values

        # Handle the click: You can now access the date, time, and message of the clicked row
        print(f"Clicked on: Date: {date}, Time: {time}, Message: {message}")
        
        # Trigger some action, like showing an image or processing the message
        self.on_message_click(index)

    def on_message_click(self, image_index):
        with Processed_Screenshot.lock:
            image_with_boxes = Processed_Screenshot.frames[image_index]
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