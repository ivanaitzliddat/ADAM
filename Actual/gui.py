import tkinter as tk
import queue
from tkinter import font
from alerts_page import AlertsPage
from settings_page import SettingsPage
from keyword_page import KeywordPage
from color_picker_page import ColorPage
from messages import MessageQueue

'''
    Represents a GUI object which allows user to control ADAM.
'''
class ADAM:
    # Class-level variable to keep track of all instances
    instances = []

    def __init__(self):
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
        self.alerts_button = tk.Button(self.sidebar, text="Alerts", command=lambda: self.show_page("alerts"))
        self.alerts_button.pack(fill="x")

        # self.settings_button = tk.Button(self.sidebar, text="Settings", command=self.show_settings_page)
        # self.settings_button.pack(fill="x")
        
        self.keyword_button = tk.Button(self.sidebar, text="Keyword", command=lambda: self.show_page("keywords"))
        self.keyword_button.pack(fill="x")
        
        self.color_picker_button = tk.Button(self.sidebar, text="Color Picker", command=lambda: self.show_page("color_picker"))
        self.color_picker_button.pack(fill="x")

        # Main content area to display the current page
        self.content_frame = tk.Frame(self.master)
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Initialize pages
        self.pages = {
            "alerts": AlertsPage(self.content_frame),
            # "settings": SettingsPage(self.content_frame),  # Uncomment if needed
            "keywords": KeywordPage(self.content_frame),
            "color_picker": ColorPage(self.content_frame)
        }
        
        # Show the initial page
        self.current_page = None
        self.show_page("alerts")

        # Start the queue checking process
        self.check_queue()

    '''
        Checks if there are any messages that are sent from the screen capturer.
    '''
    def check_queue(self):
        try:
            while True:
                message = MessageQueue.status_queue.get_nowait()
                self.alerts_page.append_message(message)
        except queue.Empty:
            pass
        finally:
            # Schedule the next check
            self.master.after(100, self.check_queue)  # Check again after 100ms
            
    def show_page(self, page_name):
        """Switches to the specified page."""
        # Hide the current page if there is one
        if self.current_page:
            self.pages[self.current_page].pack_forget()

        # Show the new page
        self.current_page = page_name
        self.pages[page_name].pack(expand=True, fill="both")

        # Force the GUI to redraw
        self.master.update_idletasks()


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