import tkinter as tk
from tkinter import messagebox
from processed_screenshot import Processed_Screenshot
import matplotlib.pyplot as plt

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a Text widget to display messages
        #self.message_display = tk.Text(self, wrap=tk.WORD, height=10, width=50)
        #self.message_display.pack(pady=10)

        # Create a frame to hold the listbox of event messages
        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
        # Add a vertical scrollbar to the listbox
        # scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.event_listbox.yview)
        # scrollbar.pack(side="right", fill="y")
        # self.event_listbox.config(yscrollcommand=scrollbar.set)

    def append_message(self, message, index):
        # Create a label for each message and make it clickable
        clickable_label = tk.Label(self.frame, text=message, fg="blue", cursor="hand2")
        clickable_label.pack(anchor="w", padx=10, pady=5)

        # Bind the label to call on_message_click when clicked
        # clickable_label.bind("<Button-1>", lambda event, msg=message: self.on_message_click(msg))
        clickable_label.bind("<Button-1>", lambda event, idx=index: self.on_message_click(idx))

    def on_message_click(self, image_index):
        with Processed_Screenshot.lock:
            # Convert images to Tkinter-compatible format
            plt.imshow(Processed_Screenshot.frames[image_index])
            plt.axis('off')
            plt.show()


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