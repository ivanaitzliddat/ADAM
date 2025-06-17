import queue
import tkinter as tk
from tkinter import font
from tkinter import messagebox

from cam_setup_page import VideoCaptureSetupApp
from tts_settings_page import TTS_setup_page
from alerts_page import AlertsPage
from about_page import AboutPage
from FAQ_page import FAQPage
from welcome_page import welcomeScreen
from config_handler import ConfigHandler
from messages import MessageQueue
from TTS import TTS
from datetime import datetime

'''
    Represents a GUI object which allows user to control ADAM.
'''
class ADAM:
    # Class-level variable to keep track of all instances
    instances = []

    def __init__(self):
        BG_COLOUR = "#DCE0D9"

        self.master = tk.Tk()
        self.master.title("ADAM")
        #self.master.geometry("1980x1080")
        self.master.state("zoomed")
        self.master.config(bg=BG_COLOUR)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        ADAM.instances.append(self)

        # Define a larger font
        self.label_font = font.Font(size=24, weight="bold")

        # Set up the topbar
        self.topbar = tk.Frame(self.master, height=50, bg=BG_COLOUR)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Buttons to switch between pages
        self.alerts_button = tk.Button(self.topbar, text="Alerts", command=self.open_alerts_page)
        self.alerts_button.grid(row=0, column=0, padx=10, pady=5)

        # Create a settings button and when clicked, a drop-down menu will appear
        self.settings_button = tk.Button(self.topbar, text="Settings", command=self.show_settings_menu)
        self.settings_button.grid(row=0, column=1, padx=10, pady=5)

        # Add options to the drop-down menu when settings button is clicked
        # Create the settings menu
        self.settings_menu = tk.Menu(self.master, tearoff=0)
        self.settings_menu.add_command(label="Video Capture Cards", command=self.option1)
        self.settings_menu.add_command(label="Text-to-Speech", command=self.option2)

        # Button for About page
        self.about_button = tk.Button(self.topbar, text="About ADAM", command=self.show_about_page)
        self.about_button.grid(row=0, column=2, padx=10, pady=5)

        # Button for FAQ page
        self.FAQ_button = tk.Button(self.topbar, text="FAQ", command=self.show_FAQ_page)
        self.FAQ_button.grid(row=0, column=3, padx=10, pady=5)

        # Loading frame to show loading message
        screen_width = self.master.winfo_screenwidth() # Get the screen width
        screen_height = self.master.winfo_screenheight() # Get the screen height

        self.loading_frame_width = int(screen_width)
        self.loading_frame_height = int(screen_height)

        # Center the loading frame
        x = int((screen_width - self.loading_frame_width) // 2)
        y = int((screen_height - self.loading_frame_height) // 2)

        # Create a loading frame and centering it using relx and rely. The frame will cover up the whole window and will destroy once page is loaded
        self.loading_frame = tk.Frame(self.master, bg=BG_COLOUR, width=self.loading_frame_width, height=self.loading_frame_height)
        self.loading_frame.place(x=x, y=y)
        self.loading_label = tk.Label(self.loading_frame, text="Please wait while ADAM is loading...", font=("Arial", 32), bg=BG_COLOUR)
        self.loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Main content area to display the current page
        self.content_frame = tk.Frame(self.master, bg=BG_COLOUR)
        self.content_frame.grid(row=1, column=0, sticky="nsew")

        # Set up 3 columns
        self.content_frame.grid_columnconfigure(0, weight=1)  # Left Spacer
        self.content_frame.grid_columnconfigure(1, weight=10) # Center Column (Main Content)
        self.content_frame.grid_columnconfigure(2, weight=1)  # Right Spacer

        # Ensure content fills the space and resizes properly
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.current_page = None

        fresh_setup_status = ConfigHandler.is_fresh_setup()

        # Initialize pages
        self.pages = {
            "welcome_page": welcomeScreen(self.content_frame, self.topbar, self.option1, fresh_setup_status),
            "cam_setup_page": VideoCaptureSetupApp(self.content_frame, self.topbar, fresh_setup_status, self.open_alerts_page),
            "tts_setup_page": TTS_setup_page(self.content_frame),
            "FAQ_page": FAQPage(self.content_frame),
            "About_page": AboutPage(self.content_frame),
            "alerts_page": AlertsPage(self.content_frame),
        }

        # Show the initial page
        if fresh_setup_status:
            self.show_page("welcome_page")
        else:
            self.show_page("alerts_page")


        # Configure grid weights for resizing
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Start the queue checking process
        self.check_queue()

    '''
        Checks if there are any messages that are sent from the screen capturer.
    '''
    def check_queue(self):
        try:
            while True:
                message = MessageQueue.status_queue.get_nowait()
                self.pages["alerts_page"].append_message(message)
                
                with TTS.lock:
                    #Skip if alert is muted and not expired
                    muted = False
                    now = datetime.now()
                    timestamp = message[0]
                    sentence = message[1]
                    alt_name = message[2]
                    tts_alert = message[3]
                    for mute_entry in self.pages["alerts_page"].muted_alerts:
                        if (
                            mute_entry["alt_name"] == alt_name and
                            mute_entry["sentence_list"] == sentence and
                            mute_entry["expiry_time"] > now
                        ):
                            muted = True
                            break

                    if not muted:
                        if not tts_alert == '':
                            TTS.alert_queue.put(tts_alert)
                        else: 
                            TTS.alert_queue.put(sentence)
        except queue.Empty:
            pass
        finally:
            # Schedule the next check
            self.master.after(1000, self.check_queue)  # Check again after 1000ms

    def show_settings_menu(self, event=None):
        # Display the settings menu
        self.settings_menu.post(self.settings_button.winfo_rootx(), self.settings_button.winfo_rooty() + self.settings_button.winfo_height())

    def option1(self):
        self.show_page("cam_setup_page")

    def option2(self):
        self.show_page("tts_setup_page")

    def open_alerts_page(self):
        self.show_page("alerts_page")

    def show_about_page(self):
        self.show_page("About_page")
    
    def show_FAQ_page(self):
        self.show_page("FAQ_page")

    '''
        Checks if there are any messages that are sent from the screen capturer.
    '''
              
    def show_page(self, page_name):
        """Switches to the specified page."""
        self.loading_frame.destroy()  # Remove the loading frame
        # Hide the current page if there is one
        if self.current_page:
            self.pages[self.current_page].grid_forget()

        # Show the new page
        self.current_page = page_name
        self.pages[page_name].grid(row=0, column=1, sticky="nsew")

        # Force the GUI to redraw
        self.master.update_idletasks()

        # Resize the new page based on its own on_resize method
        if page_name == "welcome_page":
            self.pages[page_name].on_resize()
            
        if page_name == "about_page":
            self.pages[page_name].on_resize()
            
        if page_name == "FAQ_page":
            self.pages[page_name].on_resize()

        if page_name == "cam_setup_page":
            self.pages[page_name].on_resize()

        if page_name == "tts_setup_page":
            self.pages[page_name].on_resize()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()
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


        ##If want to change to menu bar instead of frame in the future
        # menubar = Menu(self.master)

        # filemenu = Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Exit", command=self.master.quit)
        # menubar.add_cascade(label="File", menu=filemenu, command=self.master.quit)

        # settingsmenu = Menu(menubar, tearoff=0)
        # settingsmenu.add_command(label="TTS Settings", command=lambda: self.show_page(""))
        # settingsmenu.add_command(label="Keywords & Colour Settings", command=lambda: self.show_page("keywords"))
        # settingsmenu.add_command(label="LLM Settings", command=lambda: self.show_page(""))
        # menubar.add_cascade(label="Settings", menu=settingsmenu)

        # self.master.config(menu=menubar)
#if __name__ == "__main__":
#    app = ADAM()
#    app.run()