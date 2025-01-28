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

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCaptureSetupApp(root)
    root.mainloop()