import tkinter as tk

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a frame to hold the custom list of event messages
        self.list_frame = tk.Frame(self)
        self.list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create header for "Button" and "Description"
        self.create_header()

        # Hardcoded alerts
        self.alerts = [
            "CPU usage exceeded threshold!",
            "Disk space running low.",
            "System running normally.",
            "Network interface down.",
            "Memory usage high."
        ]

        # Add each alert to the list with a sound icon at the start
        for index, alert in enumerate(self.alerts):
            self.add_alert_row(alert, index)

    def create_header(self):
        """Create header row with "Button" and "Description" labels."""
        header_frame = tk.Frame(self.list_frame)
        header_frame.pack(fill="x", pady=5)

        button_label = tk.Label(header_frame, text="Button", font=("Arial", 12, "bold"), width=10)
        button_label.pack(side="left")

        description_label = tk.Label(header_frame, text="Description", font=("Arial", 12, "bold"), width=50, anchor="w")
        description_label.pack(side="left", fill="x")

    def add_alert_row(self, alert_text, index):
        """Adds a row with a sound icon and alert text."""
        # Alternate row colors
        bg_color = "#f0f0f0" if index % 2 == 0 else "#ffffff"
        
        # Create a frame for each row
        row_frame = tk.Frame(self.list_frame, bg=bg_color)
        row_frame.pack(fill="x")

        # Create the sound icon button (instead of text)
        sound_button = tk.Button(row_frame, text="sound", font=("Arial", 12), command=lambda: self.show_sound_popup(alert_text))
        sound_button.pack(side="left", padx=10)

        # Add the alert text (Description)
        alert_label = tk.Label(row_frame, text=alert_text, anchor="w", justify="left", bg=bg_color)
        alert_label.pack(side="left", fill="x", expand=True)

        # Bind the entire row frame to show the alert details pop-up when clicked
        row_frame.bind("<ButtonRelease-1>", lambda e: self.show_alert_popup(alert_text))
        
        # Bind the description label to also trigger the alert pop-up when clicked
        alert_label.bind("<ButtonRelease-1>", lambda e: self.show_alert_popup(alert_text))

    def show_sound_popup(self, alert_text):
        """Display a pop-up window when the sound button is clicked."""
        popup = tk.Toplevel(self)
        popup.title("Sound Alert")
        popup.geometry("300x250")

        # Label to show which alert triggered the sound
        label = tk.Label(popup, text=f"Sound triggered for:\n{alert_text}", font=("Arial", 14), wraplength=250)
        label.pack(pady=10)

        # Create a frame for mute/unmute control
        mute_frame = tk.Frame(popup)
        mute_frame.pack(pady=10)

        mute_var = tk.BooleanVar()  # This variable will track mute state
        mute_checkbox = tk.Checkbutton(mute_frame, text="Mute", variable=mute_var)
        mute_checkbox.pack()

        # Create a frame for time selection (Hours and Minutes)
        time_frame = tk.Frame(popup)
        time_frame.pack(pady=10)

        # Hour and Minute Spinboxes
        hour_label = tk.Label(time_frame, text="Time (hh:mm):")
        hour_label.pack(side="left", padx=5)
        
        # Spinbox for hour (0 to 23)
        hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f")
        hour_spinbox.pack(side="left", padx=5)
        
        # Spinbox for minute (0 to 59)
        minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f")
        minute_spinbox.pack(side="left", padx=5)
        
        # Function to handle the OK button press
        def on_ok():
            hours = int(hour_spinbox.get())  # Get hour value
            minutes = int(minute_spinbox.get())  # Get minute value
            muted = mute_var.get()
            mute_duration = f"{hours} hour(s) and {minutes} minute(s)"
            
            # You can use the mute state and duration for further processing here
            print(f"Muted: {muted}, Duration: {mute_duration}")
            
            popup.destroy()

        # Function to handle the Cancel button press
        def on_cancel():
            popup.destroy()

        # OK and Cancel buttons
        ok_button = tk.Button(popup, text="OK", command=on_ok)
        ok_button.pack(side="left", padx=20, pady=10)

        cancel_button = tk.Button(popup, text="Cancel", command=on_cancel)
        cancel_button.pack(side="right", padx=20, pady=10)

    def show_alert_popup(self, alert_text):
        """Display a pop-up window when the row or description is clicked."""
        popup = tk.Toplevel(self)
        popup.title("Alert Details")
        popup.geometry("300x200")

        label = tk.Label(popup, text=f"Details for alert:\n{alert_text}", font=("Arial", 14), wraplength=250)
        label.pack(pady=20, padx=20)

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)







































# import tkinter as tk

# class AlertsPage(tk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
#         label.pack(pady=20, padx=20)

#         # Create a Text widget to display messages
#         #self.message_display = tk.Text(self, wrap=tk.WORD, height=10, width=50)
#         #self.message_display.pack(pady=10)

#         # Create a frame to hold the listbox of event messages
#         frame = tk.Frame(self)
#         frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

#         # Create a Listbox to display event messages
#         self.event_listbox = tk.Listbox(frame, height=10, width=80, selectmode=tk.SINGLE)
#         self.event_listbox.pack(side="left", fill=tk.BOTH, expand=True)

#         # Add a vertical scrollbar to the listbox
#         scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.event_listbox.yview)
#         scrollbar.pack(side="right", fill="y")
#         self.event_listbox.config(yscrollcommand=scrollbar.set)

#     def append_message(self, message):
#         self.event_listbox.insert(tk.END, message)  # Append message to listbox
#         self.event_listbox.yview(tk.END)  # Automatically scroll to the bottom of the listbox

#         # Function to simulate updating event messages periodically
#     # def update_event_messages(self):
#     #     messages = [
#     #         "CPU usage exceeded threshold!",
#     #         "Disk space running low.",
#     #         "System running normally.",
#     #         "Network interface down.",
#     #         "Memory usage high."
#     #     ]
        
#     #     # Add each event message to the listbox
#     #     for message in messages:
#     #         self.add_event_message(message)
        
#     #     # Call this function again in 5 seconds to simulate new event messages
#     #     self.after(5000, self.update_event_messages)


#     # def append_message(self, message):
#     #     self.message_display.insert(tk.END, message + "\n")
#     #     self.message_display.see(tk.END)  # Scroll to the end of the Text widget