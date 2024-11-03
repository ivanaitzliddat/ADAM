import tkinter as tk

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)