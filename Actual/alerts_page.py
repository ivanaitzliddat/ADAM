import tkinter as tk

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a Text widget to display messages
        self.message_display = tk.Text(self, wrap=tk.WORD, height=10, width=50)
        self.message_display.pack(pady=10)

    def append_message(self, message):
        self.message_display.insert(tk.END, message + "\n")
        self.message_display.see(tk.END)  # Scroll to the end of the Text widget