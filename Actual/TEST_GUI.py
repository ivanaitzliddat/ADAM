import tkinter as tk
import queue
from tkinter import font
from tkinter import font as tkFont
from TEST_camSetupPage import VideoCaptureSetupApp
from TEST_TTS_settings_page import TTS_setup_page
from TEST_alerts_page import AlertsPage
from TEST_about_page import about_page
from TEST_FAQ_page import FAQ_page
#from TEST_InitialWelcomeScreen import welcomeScreen
#from alerts_page import AlertsPage
#from settings_page import SettingsPage
#from keyword_page import KeywordPage
#from color_picker_page import ColorPage
from messages import MessageQueue

#TEST_GUI.py is copied from gui.py in Actual folder


'''
    Represents a GUI object which allows user to control ADAM.
'''
class ADAM:
    # Class-level variable to keep track of all instances
    instances = []

    def __init__(self):
        TEXT_COLOUR = "#000000"
        BG_COLOUR = "#DCE0D9"
        FRAME_COLOUR = "#508991"
        GRAB_ATTENTION_COLOUR_1 ="#FF934F"
        GRAB_ATTENTION_COLOUR_2 ="#C3423F"

        self.master = tk.Tk()
        self.master.title("ADAM")
        self.master.geometry("1980x1080")
        self.master.state("zoomed")
        self.master.config(bg=BG_COLOUR)

        ADAM.instances.append(self)

        # Define a larger font
        self.label_font = font.Font(size=24, weight="bold")

        # Set up the topbar
        self.topbar = tk.Frame(self.master, height=50, bg=BG_COLOUR)
        self.topbar.pack(side="top", fill="x")
            
        # Buttons to switch between pages
        self.alerts_button = tk.Button(self.topbar, text="Alerts", command=self.open_alerts_page)
        self.alerts_button.pack(side="left", padx=10)

        #create a settings button and when clicked, a drop down menu will appear
        self.settings_button = tk.Button(self.topbar, text="Settings", command=self.show_settings_menu)
        self.settings_button.pack(side="left", padx=10)

        #add options to the drop down menu when settings button is clicked
        # Create the settings menu
        self.settings_menu = tk.Menu(self.master, tearoff=0)
        self.settings_menu.add_command(label="Video Capture Cards", command=self.option1)
        self.settings_menu.add_command(label="Text-to-Speech", command=self.option2)
        self.settings_menu.add_command(label="Option 3", command=self.option3)
  
        # button for About page
        self.about_button = tk.Button(self.topbar, text="About ADAM", command=self.show_about_page)
        self.about_button.pack(side="left", padx=10)
        
        # button for FAQ page
        self.FAQ_button = tk.Button(self.topbar, text="FAQ", command=self.show_FAQ_page)
        self.FAQ_button.pack(side="left", padx=10)

        # Main content area to display the current page
        self.content_frame = tk.Frame(self.master)
        self.content_frame.pack(side="right", expand=True, fill="both")
        self.current_page = None

        # Initialize pages
        self.pages = {
            "cam_setup_page": VideoCaptureSetupApp(self.content_frame),
            "tts_setup_page": TTS_setup_page(self.content_frame), 
            "alerts_page": AlertsPage(self.content_frame),
            "FAQ_page":FAQ_page(self.content_frame),
            "About_page":about_page(self.content_frame)
        }
        
        # Show the initial page

        self.show_page("alerts_page")

    def show_settings_menu(self, event=None):
        # Display the settings menu
        self.settings_menu.post(self.settings_button.winfo_rootx(), self.settings_button.winfo_rooty() + self.settings_button.winfo_height())

    def option1(self):
        self.show_page("cam_setup_page")

    def option2(self):
        self.show_page("tts_setup_page")

    def option3(self):
        print("Option 3 selected")

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