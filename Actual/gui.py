import tkinter as tk
import queue
from tkinter import font
from alerts_page import AlertsPage
from settings_page import SettingsPage
from keyword_page import KeywordPage
from color_picker_page import ColorPage

'''
    Represents a GUI object which allows user to control ADAM.
'''
class ADAM:
    # Class-level variable to keep track of all instances
    instances = []

    def __init__(self, status_queue):
        self.master = tk.Tk()
        self.master.title("ADAM")
        self.master.geometry("1600x900")

        ADAM.instances.append(self)

        # Define a larger font
        self.label_font = font.Font(size=24, weight="bold")

        # Set up the sidebar
        self.sidebar = tk.Frame(self.master, width=150, bg="lightgray")
        self.sidebar.pack(side="left", fill="y")
        
        # Add a label
        self.label = tk.Label(self.master, text="Welcome to ADAM!", font=self.label_font)
        self.label.pack()
        
        # Buttons to switch between pages
        self.alerts_button = tk.Button(self.sidebar, text="Alerts", command=self.show_alerts_page)
        self.alerts_button.pack(fill="x")

        self.settings_button = tk.Button(self.sidebar, text="Settings", command=self.show_settings_page)
        self.settings_button.pack(fill="x")
        
        self.keyword_button = tk.Button(self.sidebar, text="Keyword", command=self.show_keywords_page)
        self.keyword_button.pack(fill="x")
        
        self.color_picker_button = tk.Button(self.sidebar, text="Color Picker", command=self.show_color_picker_page)
        self.color_picker_button.pack(fill="x")

        # Main content area to display the current page
        self.content_frame = tk.Frame(self.master)
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Initialize pages
        self.alerts_page = AlertsPage(self.content_frame)  # Create an instance of AlertsPage
        self.settings_page = SettingsPage(self.content_frame)  # Create an instance of SettingsPage and pass the callback
        self.keyword_page = KeywordPage(self.content_frame) 
        self.color_picker_page = ColorPage(self.content_frame) 
        self.show_alerts_page()  # Start with Alerts page

        # Start the queue checking process
        self.status_queue = status_queue
        self.check_queue()

    '''
        Checks if there are any messages that are sent from the screen capturer.
    '''
    def check_queue(self):
        try:
            while True:
                message = self.status_queue.get_nowait()
                self.alerts_page.append_message(message)
        except queue.Empty:
            pass
        finally:
            # Schedule the next check
            self.master.after(100, self.check_queue)  # Check again after 100ms

    def show_alerts_page(self):
        self.clear_content_frame()
        self.alerts_page.pack(expand=True, fill="both")

    def show_settings_page(self):
        self.clear_content_frame()
        self.settings_page.pack(expand=True, fill="both")
    
    def show_keywords_page(self):
        self.clear_content_frame()
        self.keyword_page.pack(expand=True, fill="both")
        
    def show_color_picker_page(self):
        self.clear_content_frame()
        self.color_picker_page.pack(expand=True, fill="both")

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()

    '''
        Starts the GUI.
    '''
    def run(self):
        self.master.mainloop()

    '''
        Stops all instances of the GUI.
    '''
    @staticmethod
    def close():
        print("Closing all instances of ADAM.")
        # Close all instances and destroy their main windows
        for instance in ADAM.instances:
            instance.master.destroy()
        ADAM.instances.clear()
        print("Closed all instances of ADAM.")