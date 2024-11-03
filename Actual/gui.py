import tkinter as tk
from tkinter import font

'''
    Represents a GUI object which allows user to control ADAM.
'''
class ADAM:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("ADAM")
        self.master.geometry("1600x900")

        # Define a larger font
        self.label_font = font.Font(size=24, weight="bold")

        # Add a label
        self.label = tk.Label(self.master, text = "Welcome to ADAM!", font=self.label_font)
        self.label.pack()

        # Set up the sidebar
        self.sidebar = tk.Frame(self.master, width=150, bg="lightgray")
        self.sidebar.pack(side="left", fill="y")

        # Buttons to switch between pages
        self.alerts_button = tk.Button(self.sidebar, text="Alerts", command=self.show_alerts_page)
        self.alerts_button.pack(fill="x")

        self.settings_button = tk.Button(self.sidebar, text="Settings", command=self.show_settings_page)
        self.settings_button.pack(fill="x")

        # Main content area to display the current page
        self.content_frame = tk.Frame(self.master)
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Initialize pages
        self.alerts_page = None
        self.settings_page = None
        self.show_alerts_page()  # Start with Alerts page

    def show_alerts_page(self):
        # Clear the content frame and display the alerts page
        self.clear_content_frame()

        # Create the alerts page
        self.alerts_page = tk.Label(self.content_frame, text="Alerts Page Content")
        self.alerts_page.pack(pady=20, padx=20)

    def show_settings_page(self):
        # Clear the content frame and display the settings page
        self.clear_content_frame()

        # Create the settings page
        self.settings_page = tk.Label(self.content_frame, text="Settings Page Content")
        self.settings_page.pack(pady=20, padx=20)

    def clear_content_frame(self):
        # Destroy all widgets in the content frame to refresh the page
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    '''
        Starts the GUI.
    '''
    def run(self):
        self.master.mainloop()