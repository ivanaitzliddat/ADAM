import tkinter as tk
from tkinter import messagebox

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title label
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Frame to hold clickable messages
        self.messages_frame = tk.Frame(self)  # Ensure it's created here
        self.messages_frame.pack(pady=10, fill="both", expand=True)  # Make sure the frame is packed

    def append_message(self, message):
        # Create a label for each message and make it clickable
        clickable_label = tk.Label(self.messages_frame, text=message, fg="blue", cursor="hand2")
        clickable_label.pack(anchor="w", padx=10, pady=5)

        # Bind the label to call on_message_click when clicked
        clickable_label.bind("<Button-1>", lambda event, msg=message: self.on_message_click(msg))

    def on_message_click(self, message):
        # Display a pop-up when a message is clicked
        messagebox.showinfo("Message Details", f"You clicked on: {message}")

# Example usage of AlertsPage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Alerts Page")
    root.geometry("400x300")

    # Initialize the AlertsPage
    alerts_page = AlertsPage(root)
    alerts_page.pack(fill="both", expand=True)

    # Add some messages to demonstrate
    alerts_page.append_message("Message 1: Alert!")
    alerts_page.append_message("Message 2: Another alert.")
    alerts_page.append_message("Message 3: Click here for more info.")

    # Start the Tkinter event loop
    root.mainloop()