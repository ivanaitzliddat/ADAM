import os, traceback
import tkinter as tk
import tkinter.messagebox as tk_msgbox
from tkinter import ttk
from datetime import datetime, timedelta

import numpy as np
import cv2
import io
from PIL import Image, ImageTk
from imageio.plugins.deviceslist import DevicesList
from tkcalendar import DateEntry

from config_handler import ConfigHandler
from processed_screenshot import Processed_Screenshot

class AlertsPage(tk.Frame):

    muted_alerts = []

    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a label to display the number of devices
        self.device_count_label = tk.Label(self, text="Connected Devices: Loading...", font=("Arial", 12))
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

        # Load and resize icons
        self.green_icon = self.load_resized_icon(os.path.join(ConfigHandler.dirname, "green_monitor.png"), 50, 50)  # Resize to 50x50 pixels
        self.red_icon = self.load_resized_icon(os.path.join(ConfigHandler.dirname, "red_monitor.png"), 50, 50)  # Resize to 50x50 pixels
        self.grey_icon = self.load_resized_icon(os.path.join(ConfigHandler.dirname, "grey_monitor.png"), 50, 50)  # Resize to 50x50 pixels
        self.unmuted_icon = self.load_resized_icon(os.path.join(ConfigHandler.dirname, "green_unmute.png"), 30, 30)
        self.muted_icon = self.load_resized_icon(os.path.join(ConfigHandler.dirname, "red_mute.png"), 30, 30)

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
        # self.date_filter_entry.pack(side="left", padx=5, pady=5)
        # self.time_filter_entry.pack(side="left", padx=5, pady=5)
        # self.message_filter_entry.pack(side="left", padx=5, pady=5)

        # Apply filter button (using pack inside the filter frame)
        filter_button = tk.Button(self.filter_frame, text="Filter Options", command=self.open_filter_window)
        filter_button.pack(side="left", padx=5, pady=5)

        # Clear filters button (using pack inside the filter frame)
        clear_button = tk.Button(self.filter_frame, text="Clear Filters",
                                 command=lambda: (setattr(self, 'filtered', False), self.filter_params.clear(), self.clear_filters()))
        clear_button.pack(side="left", padx=5, pady=5)

        # Create a Treeview widget with three columns
        self.treeview = ttk.Treeview(self.bottom_frame, columns=("Date & Time", "Device", "Detected with trigger(s)", "Hidden Sentence"), show="tree headings")
        self.treeview.heading("#0", text="Mute Status")
        self.treeview.heading("Date & Time", text="Date & Time", command=lambda: self.sort_column("date_time", False))
        self.treeview.heading("Device", text="Device")
        self.treeview.heading("Detected with trigger(s)", text="Detected with trigger(s)")
        self.treeview.heading("Hidden Sentence", text="Hidden Sentence")
        self.treeview.column("Hidden Sentence", width=0, stretch=False)

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

        # To keep track of filter state (whether filter is active or not)
        self.filtered = False

        # To keep track of date/time column sort state
        self.current_sort_column = "date_time"
        self.current_sort_reverse = True  # True = descending (newest first)

        # To keep track of filter parameters
        self.filter_params = {}

    # Function to load and resize an image to the given width and height
    def load_resized_icon(self, image_path, width, height):
        img = Image.open(image_path)  # Open the image
        img = img.resize((width, height), Image.Resampling.LANCZOS)  # Resize the image
        return ImageTk.PhotoImage(img)  # Convert the resized image to a Tkinter-compatible format
     
    # Update the display of connected devices with the appropriate icons
    def update_device_display(self):
        # Add devices that are not yet added to the UI
        for device in self.starting_device_list:
            custom_name = self.get_custom_name_from_alt_name(device)
            
            if device not in self.device_labels:
                # Decide which icon to show based on device state
                if self.device_states.get(device, False):
                    if self.get_disabled_status(device):
                        icon = self.grey_icon
                    else:
                        icon = self.green_icon
                else:
                    icon = self.red_icon
                device_label = tk.Label(self.top_frame, text=custom_name, image=icon, compound="left", font=("Arial", 12))
                device_label.pack(anchor="w", pady=5)
                self.device_labels[device] = device_label

            device_label = self.device_labels[device]
            if self.device_states.get(device, False):
                if self.get_disabled_status(device):
                    icon = self.grey_icon
                else:
                    icon = self.green_icon
            else:
                icon = self.red_icon
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
        self.device_count_label["text"] = f"Connected Devices: {len(current_device_list)}"

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
        date_time_raw = message[0]
        sentence_list = message[1]
        alt_name = message[2]
        tts_text = message[3]

        date_time = datetime.strptime(date_time_raw, "%Y%m%d %H%M%S")
        date_time_display = date_time.strftime("%Y/%m/%d %H:%M:%S")

        msg_dict = {
            "date_time": date_time,
            "alt_name": alt_name,
            "tts_text": tts_text,
            "date_time_display": date_time_display,
            "sentence_list": sentence_list
        }

        self.all_messages.append(msg_dict)

        icon = self.muted_icon if self.if_muted(alt_name, sentence_list) else self.unmuted_icon
        custom_name = self.get_custom_name_from_alt_name(alt_name)
        values = date_time_display, custom_name, sentence_list, sentence_list
        passes_filter = True

        # Get filter params or defaults
        start = self.filter_params.get("start_date_entry", datetime.min)
        end = self.filter_params.get("end_date_entry", datetime.max)
        alt_name_filter = self.filter_params.get("alt_name_var", "All")
        text_filter = self.filter_params.get("filter_text_entry", "").lower()
        
        # Check if specified date_time is not within start and end date/time
        if not (start <= date_time <= end):
            passes_filter = False

        # Check if specified custom name is not "All"
        if alt_name_filter != "All":
            selected_alt = next(
                (msg["alt_name"] for msg in self.all_messages
                 if self.get_custom_name_from_alt_name(msg["alt_name"]) == alt_name_filter),
                None
            )
            if selected_alt != alt_name:
                passes_filter = False


        # Check if specified text exists, and is not found in sentence_list
        if text_filter and text_filter not in sentence_list.lower():
            passes_filter = False

        insert_index = 0
        visible_items = self.treeview.get_children()

        # Calculate insert_index only among visible items (those matching filter)
        if passes_filter:
            # Determine insert position among visible rows by sorting column
            if self.current_sort_column == "date_time":
                n_visible = len(visible_items)
                for i, item_id in enumerate(visible_items):
                    item_values = self.treeview.item(item_id, "values")
                    existing_dt = datetime.strptime(item_values[0], "%Y/%m/%d %H:%M:%S")

                    if self.current_sort_reverse:
                        if existing_dt < date_time:
                            insert_index = i
                            break
                    else:
                        if existing_dt > date_time:
                            insert_index = i
                            break
                else:
                    insert_index = n_visible
            else:
                insert_index = 0
        else:
            # If filtered out, just insert at the end or top (won't matter as it will be detached)
            insert_index = len(visible_items)

        # Insert the new item into treeview
        item_id = self.treeview.insert("", insert_index, image=icon, values=values)
        msg_dict["item_id"] = item_id

        # Detach if it doesn't pass filter, so it won't show
        if not passes_filter:
            self.treeview.detach(item_id)

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
        '''
        alt_name_options = list(set(msg["alt_name"] for msg in self.all_messages))
        alt_name_options.insert(0, "All")
        alt_name_menu = ttk.Combobox(filter_window, textvariable=alt_name_var, values=alt_name_options, state="readonly")
        '''
        custom_name_map = {
            self.get_custom_name_from_alt_name(msg["alt_name"]): msg["alt_name"]
            for msg in self.all_messages
        }
        custom_name_options = ["All"] + sorted(custom_name_map.keys())
        alt_name_var = tk.StringVar()
        alt_name_menu = ttk.Combobox(filter_window, textvariable=alt_name_var, values=custom_name_options, state="readonly")

        alt_name_menu.current(0)
        alt_name_menu.pack(pady=(0, 10))

        # Search for text message 
        filter_text_label = tk.Label(filter_window, text="Search Text")
        filter_text_label.pack()
        filter_text_entry = tk.Entry(filter_window)
        filter_text_entry.pack()

        apply_button = tk.Button(
            filter_window,
            text="Apply Filters",
            command=lambda: self.apply_filters(start_date_entry, end_date_entry, alt_name_var, filter_text_entry, filter_window)
        )
        apply_button.pack()

    """ Function to apply the filters based on the entries """
    def apply_filters(self, start_date_entry, end_date_entry, alt_name_var, filter_text_entry, filter_window):
        self.filtered = True

        if filter_window == None:
            # If filter_window is None, then it means apply_filters() is being automatically re-run after a new alert appears, so the arguments do not need additional processing.
            start = start_date_entry
            end = end_date_entry
            alt_name = alt_name_var
            text = filter_text_entry
        else:
            # Else, it means that apply_filters() is being manually run by user, so the arguments need some additional processing.
            start = datetime.strptime(start_date_entry.get(), "%Y/%m/%d")
            end = datetime.strptime(end_date_entry.get(), "%Y/%m/%d")
            end = end.replace(hour=23, minute=59, second=59)
            alt_name = alt_name_var.get()
            text = filter_text_entry.get().lower()

        # Set filter_params so that apply_filters() can automatically be called with appropriate arguments from other functions
        self.filter_params = {
            "start_date_entry": start,
            "end_date_entry": end,
            "alt_name_var": alt_name,
            "filter_text_entry": text,
            "filter_window": None
            }
        
        # Detach or reattach treeview entries based on filter result
        for msg in self.all_messages:
            item_id = msg.get("item_id")
            if not item_id:
                continue

            passes_filter = True
            # Check if specified date_time is not within start and end date/time
            if not (start <= msg["date_time"] <= end):
                passes_filter = False

            selected_custom = alt_name_var if isinstance(alt_name_var, str) else alt_name_var.get()
            # Check if specified custom name is not "All"
            if selected_custom != "All":
                selected_alt = next(
                    (msg["alt_name"] for msg in self.all_messages
                     if self.get_custom_name_from_alt_name(msg["alt_name"]) == selected_custom), None
                     )
                if selected_alt != msg["alt_name"]:
                    passes_filter = False
            # Check if specified text exists, and is not found in msg["sentence_list"]
            if text and text not in msg["sentence_list"].lower():
                passes_filter = False
                        
            if passes_filter:
                self.treeview.reattach(item_id, '', 0)
            else:
                self.treeview.detach(item_id)

        # Re-sort visible items after applying filters
        self.sort_column(self.current_sort_column, self.current_sort_reverse)

        if filter_window is not None:
            filter_window.destroy()

    def sharpen_image(image):
        kernel = np.array([[-1, -1, -1],
                        [-1,  9, -1],
                        [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)
    
    def on_row_click(self, event):
        try:
            region = self.treeview.identify_region(event.x, event.y)
            if region == "heading":
                return  # Ignore clicks on the header
            selected_item = self.treeview.selection()[0]
            item_data = self.treeview.item(selected_item)
            column_values = item_data['values']
            date_time_display = column_values[0]
            custom_name = column_values[1]

            alt_name = next(
                (msg["alt_name"] for msg in self.all_messages
                 if self.get_custom_name_from_alt_name(msg["alt_name"]) == custom_name), None
                 )
            if alt_name is None:
                tk_msgbox.showerror("Error", f"No matching device found for custom name '{custom_name}'")
                return
 
            sentence_list = column_values[3]
            alert_options_window = tk.Toplevel(self)
            alert_options_window.title("Alert Options")
            alert_options_window.geometry("400x300")  # width x height in pixels
            view_screenshot = tk.Button(
                alert_options_window,
                text="View Screenshot",
                command=lambda: self.on_message_click(alt_name, date_time_display, sentence_list)
            )
            view_screenshot.pack()
            mute_alerts = tk.Button(
                alert_options_window,
                text="Mute Alerts",
                command=lambda: self.mute_alert(alt_name, date_time_display, sentence_list)
            )
            mute_alerts.pack()
        except IndexError as e:
            #traceback.print_exc()
            pass    # Do nothing as user clicked on an empty area in the treeview
        except Exception:
            traceback.print_exc()

    def on_message_click(self, alt_name, date_time_display, sentence_list):
        with Processed_Screenshot.lock:
            try: 
                date_time_object = datetime.strptime(date_time_display, "%Y/%m/%d %H:%M:%S")
                image_with_boxes = Processed_Screenshot.frames[alt_name][(date_time_object.strftime("%Y%m%d %H%M%S"), sentence_list)]
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
                window = tk.Toplevel(self)
                window.grab_set()
                canvas = tk.Canvas(window, width=tk_image.width(), height=tk_image.height())
                canvas.pack()
                canvas.create_image(0, 0, anchor="nw", image=tk_image)

                # Keep a reference to avoid garbage collection
                window.image = tk_image

                # Deselect the row after opening the image
                self.treeview.selection_remove(self.treeview.selection())
            except KeyError as e:
                tk_msgbox.showinfo("No Screenshot", "The screenshot has expired and is no longer available for viewing.")

    def refresh_mute_icons(self):
        for msg in self.all_messages:
            item_id = msg.get("item_id")
            if item_id and self.treeview.exists(item_id):
                new_icon = self.muted_icon if self.if_muted(msg["alt_name"], msg["sentence_list"]) else self.unmuted_icon
                self.treeview.item(item_id, image=new_icon)

    def mute_alert(self, target_alt_name, date_time_display, sentence_list):
        # Find the matching message
        matching_message = next(
            (msg for msg in self.all_messages
            if msg['alt_name'] == target_alt_name
            and msg['date_time_display'] == date_time_display
            and msg['sentence_list'] == sentence_list), None
            )

        custom_name = self.get_custom_name_from_alt_name(target_alt_name)
        if matching_message:
            sentence_list = matching_message['sentence_list']

            mute_alert_window = tk.Toplevel(self)
            mute_alert_window.title("Mute Options")
            mute_alert_window.geometry("400x300")
            mute_alert_window.grab_set()

            # Main label
            mute_label = tk.Label(
                mute_alert_window,
                text = (
                    f"Muting on: {custom_name}\n"
                    f"Muting sentence: {sentence_list}\n\n"
                    "This will still display the alert, but no sound will be played."
                ),
                wraplength=380,
                justify="left"
            )
            mute_label.pack(pady=10)

            # Frame for "Mute Duration" label + combobox
            duration_frame = tk.Frame(mute_alert_window)
            duration_frame.pack(pady=5)

            tk.Label(duration_frame, text="Mute duration:").pack(side="left", padx=(0, 10))

            duration_options = {
                "1 min": 1,
                "5 mins": 5,
                "15 mins": 15,
                "30 mins": 30,
                "1 hr": 60,
                "2 hrs": 120,
                "3 hrs": 180,
                "6 hrs": 360,
                "1 day": 1440,
            }

            duration_var = tk.StringVar()
            duration_menu = ttk.Combobox(duration_frame, textvariable=duration_var, state="readonly", width=20)
            duration_menu['values'] = list(duration_options.keys())
            duration_menu.current(0)
            duration_menu.pack(side="left")

            # Confirm/Cancel buttons
            button_frame = tk.Frame(mute_alert_window)
            button_frame.pack(pady=20)

            def confirm_mute():
                selected = duration_var.get()
                duration_minutes = duration_options.get(selected)

                if duration_minutes is not None:
                    expiry_time = datetime.now() + timedelta(minutes=duration_minutes)

                    mute_entry = {
                        "alt_name": target_alt_name,
                        "sentence_list": sentence_list,
                        "expiry_time": expiry_time
                    }
                    AlertsPage.muted_alerts.append(mute_entry)

                    # Schedule automatic unmute
                    delay_ms = int(duration_minutes * 60 * 1000)
                    self.master.after(delay_ms, lambda: self.unmute_alert(mute_entry))
                    self.refresh_mute_icons()

                    print(f"Muted {target_alt_name} with sentence {sentence_list} until {expiry_time.strftime('%Y-%m-%d %H:%M:%S')}")
                mute_alert_window.destroy()

            def cancel_mute():
                mute_alert_window.destroy()

            confirm_btn = tk.Button(button_frame, text="Confirm", command=confirm_mute)
            confirm_btn.pack(side="left", padx=10)

            cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_mute)
            cancel_btn.pack(side="left", padx=10)

    def unmute_alert(self, mute_entry):
        try:
            AlertsPage.muted_alerts.remove(mute_entry)
            print(f"Unmuted {mute_entry['alt_name']} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.refresh_mute_icons()
        except ValueError:
            pass  # Entry already removed
    
    # Sort visible messages in all_messages based on column_key, preserving filter state (i.e., detached rows remain detached).
    def sort_column(self, column_key, reverse):
        self.current_sort_column = column_key
        self.current_sort_reverse = reverse

        # Get currently visible item_ids (i.e. item_ids currently 'attached' to treeview)
        visible_items = set(self.treeview.get_children())

        # Extract visible messages from all_messages based on item_id in visible_items
        visible_messages = [msg for msg in self.all_messages if msg.get("item_id") in visible_items]

        # Sort only visible messages
        visible_messages.sort(
            key=lambda x: x[column_key] if column_key != "sentence_list" else x[column_key].lower(),
            reverse=reverse
            )

        # Detach all visible items first (to reorder)
        for msg in visible_messages:
            item_id = msg.get("item_id")
            if item_id:
                self.treeview.detach(item_id)

        # Reattach in sorted order
        for msg in visible_messages:
            item_id = msg.get("item_id")
            if item_id:
                self.treeview.reattach(item_id, '', 'end')

        # Update header command to toggle sort direction next time
        heading_text = {
            "date_time": "Date & Time",
            "alt_name": "Device Name",
            "sentence_list": "Message"
            }.get(column_key, column_key)
        self.treeview.heading(heading_text, command=lambda: self.sort_column(column_key, not reverse))

    def clear_filters(self):
        # Mark filter as cleared
        self.filtered = False
        self.filter_params = {}

        # Determine current sort field and direction
        sort_key = self.current_sort_column if hasattr(self, "current_sort_column") else "date_time"
        reverse = self.current_sort_reverse if hasattr(self, "current_sort_reverse") else True

        # Sort all messages using the current sort settings
        sorted_messages = sorted(
            self.all_messages,
            key=lambda m: m[sort_key] if sort_key != "sentence_list" else m[sort_key].lower(),
            reverse=reverse
        )

        # Reattach or insert all messages
        for msg in sorted_messages:
            item_id = msg.get("item_id")

            icon = self.muted_icon if self.if_muted(msg["alt_name"], msg["sentence_list"]) else self.unmuted_icon
            custom_name = self.get_custom_name_from_alt_name(msg["alt_name"])
            values = msg["date_time_display"], custom_name, msg["sentence_list"]


            if item_id and self.treeview.exists(item_id):
                self.treeview.reattach(item_id, '', 'end')
                self.treeview.item(item_id, image=icon)
            else:
                item_id = self.treeview.insert("", 'end', image=icon, values=values)
                msg["item_id"] = item_id

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

    def if_muted(self, alt_name, sentence_list):
        now = datetime.now()
        is_muted = any(
            mute["alt_name"] == alt_name and
            mute["sentence_list"] == sentence_list and
            mute["expiry_time"] > now
            for mute in AlertsPage.muted_alerts
        )
        return is_muted

    def get_custom_name_from_alt_name(self, alt_name):
        device_dict = ConfigHandler.get_cfg_input_devices(usb_alt_name = alt_name)
        custom_name = ""
        for key, val in device_dict.items():
            custom_name = val["custom_name"]
        return custom_name
    
    def get_disabled_status(self, alt_name):
        return bool(ConfigHandler.get_cfg_disabled_input_devices(usb_alt_name = alt_name))
