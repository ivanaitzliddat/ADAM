import tkinter as tk
from tkinter import messagebox
from tkinter import *
import cv2
from threading import Thread
import time
from PIL import Image, ImageTk 
from tkinter import font as tkFont
import os.path



        #---------------------------------------Start of ADAM App-----------------------------------
class VideoCaptureSetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to ADAM")
        self.root.geometry("1920x1080")
        
        #Create the main frame
        # Main frame
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        #Create 3 rows
        #First row (to store ADAM logo)
        self.first_row = tk.Frame(self.frame) 
        self.first_row.pack(fill="both") 

        # Second row (to store simple guides before user begin using ADAM)
        self.second_row = tk.Frame(self.frame) 
        self.second_row.pack(fill="both") 
        
        # Third row (to store button "begin")
        self.third_row = tk.Frame(self.frame) 
        self.third_row.pack(fill="both") 

        # Logo (placeholder in first row)
        self.logo_label1 = tk.Label(self.first_row , text="ADAM", font=("Malgun Gothic Semilight", 38))
        self.logo_label2= tk.Label(self.first_row , text="Auxillary Dynamic Alert Monitor", font=("Malgun Gothic Semilight", 16))
        self.logo_label1.pack()
        self.logo_label2.pack()

        # Center the window after initializing
        self.root.after(100, self.center_window)

        # 3 frames in second row
        self.left_frame = tk.Frame(self.second_row,highlightbackground="grey",highlightthickness=2)
        self.middle_frame = tk.Frame(self.second_row,highlightbackground="grey",highlightthickness=2)
        self.right_frame = tk.Frame(self.second_row,highlightbackground="grey",highlightthickness=2)

        self.left_frame.pack(side="left", fill="both", expand=True, pady=10, padx=20)
        self.middle_frame.pack(side="left", fill="both", expand=True, pady=10, padx=20)
        self.right_frame.pack(side="left", fill="both", expand=True, pady=10, padx=20)

        # Load images
        self.left_image = ImageTk.PhotoImage(Image.open(r"C:\Users\user\Desktop\ADAM\Testing\GUI testing\images\1.jpg").resize((200, 200)))
        self.middle_image = ImageTk.PhotoImage(Image.open(r"C:\Users\user\Desktop\ADAM\Testing\GUI testing\images\1.jpg").resize((200, 200)))
        self.right_image = ImageTk.PhotoImage(Image.open(r"C:\Users\user\Desktop\ADAM\Testing\GUI testing\images\1.jpg").resize((200, 200)))

        #info in left_frame
        self.second_row_left_header=tk.Label(self.left_frame,
                                        text="STEP 1",
                                        font=("Arial",16,"bold"),
                                        justify="left",
                                        pady=20)

        self.left_image_label = tk.Label(self.left_frame, image=self.left_image)
        

        self.second_row_left_sub_info = tk.Label(self.left_frame, 
                                    text="Please ensure all end device(s) that you want ADAM to monitor is powered on with the neccessary application on and presented in the main screen", 
                                    font=("Arial",10),
                                    wraplength=200,
                                    justify="left"
                                    )
        self.second_row_left_header.pack()
        self.left_image_label.pack(padx=10)
        self.second_row_left_sub_info.pack()
        


        #info in middle_frame
        self.second_row_middle_header=tk.Label(self.middle_frame,
                                        text="STEP 2",
                                        font=("Arial",16,"bold"),
                                        justify="left",
                                        pady=20)

        self.middle_image_label = tk.Label(self.middle_frame, image=self.middle_image)

        self.second_row_middle_sub_info = tk.Label(self.middle_frame,
                                    text="Connect the USB video capture card to the rear of ADAM. Then, ensure the device to be monitored is conneted to the input of the usb video capture device", 
                                    font=("Arial",10),
                                    wraplength=200,
                                    justify="left"
                                    )
        self.second_row_middle_header.pack()
        self.middle_image_label.pack(padx=10)
        self.second_row_middle_sub_info.pack()
    
        #info in right_frame
        self.second_row_right_header=tk.Label(self.right_frame,
                                        text="STEP 3",
                                        font=("Arial",16,"bold"),
                                        justify="left",
                                        pady=20)

        self.right_image_label = tk.Label(self.right_frame, image=self.right_image)


        self.second_row_right_sub_info = tk.Label(self.right_frame,text="Repeat Step 1 and Step 2 until all the desired devices are connected then press Begin button", 
                                    font=("Arial",10),
                                    wraplength=200,
                                    justify="left",
                                    )
                                    
        self.second_row_right_header.pack()
        self.right_image_label.pack(padx=10)
        self.second_row_right_sub_info.pack()

        # Setup button (in third row)
        begin_button_font = tkFont.Font(family='Helvetica', size=26, weight='bold')
        self.setup_button = tk.Button(self.third_row, text="Begin", font=begin_button_font,  command=self.show_loading_screen)
        self.setup_button.pack(pady=10)

        # Initialize device statuses
        self.device_statuses = {}
    def show_loading_screen(self):
        
        # Start the actual setup process in a separate thread
        setup_thread = Thread(target=self.perform_setup)
        setup_thread.start()


    def perform_setup(self):
        # Perform the actual setup logic here
        self.setup_screen()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
'''

        #---------------------------------------Displays the detected device and asks for alternate name----------------------------------

    def setup_screen(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Detect and configure alternate name for video capture device(s)").grid(row=0, columnspan=3, pady=5)

        self.capture_devices = self.detect_usb_devices()
        
        self.entries = []

        # Create table headers
        tk.Label(self.frame, text="Device Number", width=15).grid(row=3, column=0)
        tk.Label(self.frame, text="Default Name", width=20).grid(row=3, column=1)
        tk.Label(self.frame, text="Alternate Name", width=20).grid(row=3, column=2)

        # Populate the table with device info
        for index, name in enumerate(self.capture_devices):
            tk.Label(self.frame, text=f"{index+1}", width=15).grid(row=index+4, column=0)
            tk.Label(self.frame, text=name, width=20).grid(row=index+4, column=1)
            entry = tk.Entry(self.frame, width=20)
            entry.grid(row=index+4, column=2)
            self.entries.append(entry)

        tk.Button(self.frame, text="Save", command=self.save_names).grid(row=len(self.capture_devices)+4, columnspan=3, pady=10)

    
    def detect_usb_devices(self):
        # Create a StringVar to hold the dynamic text
        self.status_text = tk.StringVar()
        self.status_text.set("Please wait while ADAM search for devices")
        
         # Create the Label using the StringVar
        tk.Label(self.frame, textvariable=self.status_text).grid(row=1, columnspan=3, pady=5)

        #tk.Label(self.frame,text="Please wait while ADAM search for devices").grid(row=1,columnspan=3,pady=5)   
        # Update the status text (example: simulating a search)
        def update_status(count):
            self.status_text.set(f"Searching for devices{'.' * count}")
   
        devices = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                devices.append(f"USB Video Device {i}")
                cap.release()
            self.status_text.set(f"Search complete! Total number of device(s) detected: {len(devices)}") 
        return devices

    def save_names(self):
        self.renamed_devices = [entry.get() for entry in self.entries]
        print("Renamed Devices:", self.renamed_devices)
        messagebox.showinfo("Success", "Device names saved successfully!")
        self.main_page()


        #---------------------------------------ADAM MAIN PAGE-----------------------------------
    #ADAM main page
    def main_page(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        #Arrange the window into 3 rows. 3 frames in 2nd row

        #Create 3 rows
        #First row (to store ADAM logo)
        self.first_row = tk.Frame(self.frame, bg="lightgray") 
        self.first_row.pack(fill="both") 

        # Second row (to store detected device list, ADAM alert, buttons)
        self.second_row = tk.Frame(self.frame, bg="green") 
        self.second_row.pack(fill="both") 
        
        # Third row (to store ADAM running version, ADAM system uptime")
        self.third_row = tk.Frame(self.frame, bg="blue") 
        self.third_row.pack(fill="both") 

        #split 3 frames in 2nd row
        self.sec_row_left_frame = tk.Frame(self.second_row)
        self.sec_row_middle_frame = tk.Frame(self.second_row)
        self.sec_row_right_frame = tk.Frame(self.second_row)

        self.sec_row_left_frame.pack(side="left", fill="both", expand=True)
        self.sec_row_middle_frame.pack(side="left", fill="both", expand=True)
        self.sec_row_right_frame.pack(side="left", fill="both", expand=True)

        #Start populating items into the arrangements

        # Logo (placeholder in first row)
        self.logo_label = tk.Label(self.first_row , text="[Application Logo Here]", font=("Arial", 16),padx=10,pady=10)
        self.logo_label.pack()

        #second_row_left_frame - contains the device list info
        self.device_frame = tk.Frame(self.sec_row_left_frame,padx=10,pady=10)
        self.device_frame.pack(side="left", fill="both", expand=True)
        tk.Label(self.device_frame, text="Connected Devices").grid(row=0, column=0, columnspan=2)
        tk.Label(self.device_frame, text="Device Name").grid(row=1, column=0)
        tk.Label(self.device_frame, text="Connection Status").grid(row=1, column=1)

        # Display the renamed devices with connection status
        for index, name in enumerate(self.renamed_devices):
            tk.Label(self.device_frame, text=name).grid(row=index+2, column=0)
            status_label = tk.Label(self.device_frame, text="🔴", fg="red")
            status_label.grid(row=index+2, column=1)
            self.device_statuses[name] = False

        # Start the connection checking thread
        self.connection_check_thread = Thread(target=self.check_connections)
        self.connection_check_thread.daemon = True  # Daemon thread will exit when the main thread exits
        self.connection_check_thread.start()

        #second_row_middle_frame - contains the ADAM Alerts
        self.alert_frame = tk.Frame(self.sec_row_middle_frame, bg="lightgray") 
        self.alert_frame.pack(side="left", fill="both") 

        #tkLabel in third_row_left_frame
        self.header_label=tk.Label(self.alert_frame,
                                        text="ADAM KEYWORD ALERT",
                                        font=("Arial",8),
                                        justify="left",
                                        pady=20)

        self.header_label.pack()

        #second_row_third_frame - to store the buttons
        button_frame = tk.Frame(self.sec_row_right_frame, bg="lightblue") 
        button_frame.pack(side="top", fill="y",padx=10) 

        # Settings button
        self.settings_button = tk.Button(button_frame, text="Settings", command=self.settings_screen, anchor="center")
        self.settings_button.pack(side="top",fill="x") 

        # Color Picker button
        self.color_picker_button = tk.Button(button_frame, text="Color Picker", command=self.color_picker_screen, anchor="center") 
        self.color_picker_button.pack(side="top",fill="x") 

        # Keyword button
        self.keyword_button = tk.Button(button_frame, text="Keyword", command=self.keyword_screen, anchor="center")
        self.keyword_button.pack(side="top",fill="x") 

        # FAQ button
        self.faq_button = tk.Button(button_frame, text="FAQ", command=self.faq_screen, anchor="center")
        self.faq_button.pack(side="top",fill="x") 

        #Third row - to contain 2 frames (left and right); 1 for ADAM running version and 2nd frame for ADAM uptime

        #third_row_left_frame
        self.running_ver_frame = tk.Frame(self.third_row, bg="green",padx=10,pady=10) 
        self.running_ver_frame.pack(side="left",fill="both",expand=True)

        #tkLabel in third_row_left_frame
        self.version_label=tk.Label(self.running_ver_frame,
                                        text="Display ADAM running version",
                                        font=("Arial",8),
                                        justify="left",
                                        pady=20)

        self.version_label.pack()
        #third_row_right_frame
        self.uptime_frame = tk.Frame(self.third_row, bg="lightgreen",padx=10,pady=10) 
        self.uptime_frame.pack(side="left",fill="both",expand=True)

        #tkLabel in third_row_right_frame
        self.running_time_label=tk.Label(self.uptime_frame,
                                        text="Display ADAM running time",
                                        font=("Arial",8),
                                        justify="right",
                                        pady=20)

        self.running_time_label.pack()
        


        # TTS Controls
        
        tts_frame = tk.Frame(section_1)
        tts_frame.pack(pady=50)
        
        tk.Label(tts_frame, text="Text-to-Speech Settings").pack()
        tk.Label(tts_frame, text="Voice:").pack()
        self.voice_var = tk.StringVar(value="Male")
        tk.OptionMenu(tts_frame, self.voice_var, "Male", "Female").pack()
        tk.Label(tts_frame, text="Speech Rate:").pack()
        self.rate_var = tk.StringVar(value="Normal")
        tk.OptionMenu(tts_frame, self.rate_var, "Slow", "Normal", "Fast").pack()
        tk.Label(tts_frame, text="Volume:").pack()
        self.volume_slider = tk.Scale(tts_frame, from_=0, to=100, orient="horizontal")
        self.volume_slider.pack()
        
    def check_connections(self):
        while True:
            for name in self.renamed_devices:
                cap = cv2.VideoCapture(self.renamed_devices.index(name))
                if cap.isOpened():
                    self.device_statuses[name] = True
                    self.update_status_label(name, "🟢", "green")
                else:
                    self.device_statuses[name] = False
                    self.update_status_label(name, "🔴", "red")
                cap.release()
            self.root.after(1000)  # Check every second

    def update_status_label(self, device_name, color, fg_color):
        for row in range(2, len(self.renamed_devices) + 2):
            device_label = self.device_frame.grid_slaves(row=row, column=0)[0]
            if device_label["text"] == device_name:
                status_label = self.device_frame.grid_slaves(row=row, column=1)[0]
                status_label.config(text=color, fg=fg_color)
                break

    def settings_screen(self):
        # Implement the logic for the settings screen here
        print("Settings screen displayed!")  # Placeholder for now

    def color_picker_screen(self):
        # Implement the logic for the settings screen here
        print("color_picker_screen displayed!")  # Placeholder for now

    def keyword_screen(self):
        # Implement the logic for the settings screen here
        print("keyword_screen displayed!")  # Placeholder for now    

    def faq_screen(self):
        # Implement the logic for the settings screen here
        print("faq_screen displayed!")  # Placeholder for now
'''
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCaptureSetupApp(root)
    root.mainloop()

