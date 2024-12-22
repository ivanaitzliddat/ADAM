import tkinter as tk

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a Text widget to display messages
        #self.message_display = tk.Text(self, wrap=tk.WORD, height=10, width=50)
        #self.message_display.pack(pady=10)

        # Create a frame to hold the listbox of event messages
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a Listbox to display event messages
        self.event_listbox = tk.Listbox(frame, height=10, width=80, selectmode=tk.SINGLE)
        self.event_listbox.pack(side="left", fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar to the listbox
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.event_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.event_listbox.config(yscrollcommand=scrollbar.set)

    def append_message(self, message):
        self.event_listbox.insert(tk.END, message)  # Append message to listbox
        self.event_listbox.yview(tk.END)  # Automatically scroll to the bottom of the listbox

        # Function to simulate updating event messages periodically
    # def update_event_messages(self):
    #     messages = [
    #         "CPU usage exceeded threshold!",
    #         "Disk space running low.",
    #         "System running normally.",
    #         "Network interface down.",
    #         "Memory usage high."
    #     ]
        
    #     # Add each event message to the listbox
    #     for message in messages:
    #         self.add_event_message(message)
        
    #     # Call this function again in 5 seconds to simulate new event messages
    #     self.after(5000, self.update_event_messages)


    # def append_message(self, message):
    #     self.message_display.insert(tk.END, message + "\n")
    #     self.message_display.see(tk.END)  # Scroll to the end of the Text widget