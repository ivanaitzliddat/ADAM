import tkinter as tk
from tkinter import messagebox
from tkinter import *
from threading import Thread
from PIL import Image, ImageTk 
from tkinter import font as tkFont
from InitialCamSetupPage import InitialVideoCaptureSetup
from config_handler import ConfigHandler

TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 ="#FF934F"
GRAB_ATTENTION_COLOUR_2 ="#C3423F"

        #---------------------------------------Start of ADAM App-----------------------------------
class welcomeScreen(tk.Frame):
    def __init__(self, parent, topbar, option1):
        super().__init__(parent,bg=BG_COLOUR)
        self.parent = parent  # Store parent reference
        # Create the main frame
        self.frame = tk.Frame(self, bg=BG_COLOUR)
        self.frame.pack(pady=20)
        
        if ConfigHandler.is_fresh_setup():
            for child in topbar.winfo_children():
                child.configure(state='normal')
        else:
            for child in topbar.winfo_children():
                child.configure(state='disable')
            
        #Create 3 rows
        #First row (to store ADAM logo)
        self.first_row = tk.Frame(self.frame, bg=BG_COLOUR) 
        self.first_row.pack(fill="both", expand=0) 

        # Second row (to store simple guides before user begin using ADAM)
        self.second_row = tk.Frame(self.frame, bg=BG_COLOUR) 
        self.second_row.pack(fill="both",expand=0) 
        
        # Third row (to store button "begin")
        self.third_row = tk.Frame(self.frame, bg=BG_COLOUR) 
        self.third_row.pack(fill="both") 

        # Logo (placeholder in first row)
        self.logo_label_header = tk.Label(self.first_row , text="WELCOME TO ADAM", font=("Terminal", 58), bg=BG_COLOUR)
        self.logo_label_subheader= tk.Label(self.first_row , text="Auxillary Dynamic Alert Monitor", font=("Malgun Gothic Semilight", 16), bg=BG_COLOUR)
        self.logo_label_before_you_being = tk.Label(self.first_row, text="Before we begin, please ensure the following steps are done", font=("Malgun Gothic Semilight", 20), bg=BG_COLOUR)
        self.logo_label_header.pack(pady=(200,10))
        self.logo_label_subheader.pack()
        self.logo_label_before_you_being.pack(side="left",padx=(90,0),pady=(50,20))

        # 3 frames in second row
        self.left_frame = tk.Frame(self.second_row, bg=BG_COLOUR)
        self.middle_frame = tk.Frame(self.second_row, bg=BG_COLOUR)
        self.right_frame = tk.Frame(self.second_row, bg=BG_COLOUR)

        self.left_frame.pack(side="left", expand=True, pady=10, padx=(20,10))
        self.middle_frame.pack(side="left", expand=True, pady=10, padx=10)
        self.right_frame.pack(side="left", expand=True, pady=10, padx=(0,20))

        # Load images
        # ConfigHandler.dirname returning "". to address the issue then amend the directory again
        self.left_image = ImageTk.PhotoImage(Image.open(ConfigHandler.dirname+"\\green_monitor.png").resize((200, 200)))
        self.middle_image = ImageTk.PhotoImage(Image.open(ConfigHandler.dirname+"\\green_monitor.png").resize((200, 200)))
        self.right_image = ImageTk.PhotoImage(Image.open(ConfigHandler.dirname+"\\green_monitor.png").resize((200, 200)))

        # self.left_image = ImageTk.PhotoImage(Image.open(r"C:\Users\bai_j\Desktop\ADAM-main\Testing\GUI testing\images\1.jpg").resize((300, 300)))
        # self.middle_image = ImageTk.PhotoImage(Image.open(r"C:\Users\bai_j\Desktop\ADAM-main\Testing\GUI testing\images\1.jpg").resize((300, 300)))
        # self.right_image = ImageTk.PhotoImage(Image.open(r"C:\Users\bai_j\Desktop\ADAM-main\Testing\GUI testing\images\1.jpg").resize((300, 300)))


        #info in left_frame
        self.second_row_left_header=tk.Label(self.left_frame,
                                        text="STEP 1",
                                        font=("Arial",30,"bold"),
                                        justify="left",
                                        fg=TEXT_COLOUR,
                                        bg=BG_COLOUR)


        self.left_image_label = tk.Label(self.left_frame, image=self.left_image, bg=BG_COLOUR)
        

        self.second_row_left_sub_info = tk.Label(self.left_frame, 
                                    text="Please ensure all end device(s) that you want ADAM to monitor is powered on with the neccessary application on and presented in the main screen", 
                                    font=("Arial",20),
                                    wraplength=400,
                                    justify="left",
                                    bg=BG_COLOUR
                                    )
        
        # Use grid to arrange the widgets
        self.second_row_left_header.grid(row=0, column=0, sticky="ew", padx=20,pady=(10,0))
        self.left_image_label.grid(row=1, column=0, sticky="ew",padx=20, pady=(0,10))
        self.second_row_left_sub_info.grid(row=0, column=1, rowspan=2, sticky="ew", padx=20,pady=(10,10))


        #info in middle_frame
        self.second_row_middle_header=tk.Label(self.middle_frame,
                                        text="STEP 2",
                                        font=("Arial",30,"bold"),
                                        justify="left",
                                        fg=TEXT_COLOUR,
                                        bg=BG_COLOUR
                                        )

        self.middle_image_label = tk.Label(self.middle_frame, image=self.middle_image, bg=BG_COLOUR)

        self.second_row_middle_sub_info = tk.Label(self.middle_frame,
                                    text="Connect the USB video capture card to the rear of ADAM. Then, ensure the device to be monitored is conneted to the input of the usb video capture device", 
                                    font=("Arial",20),
                                    wraplength=400,
                                    justify="left",
                                    fg=TEXT_COLOUR,
                                    bg=BG_COLOUR    
                                    )
        self.second_row_middle_header.grid(row=0, column=0, sticky="ew", padx=20,pady=(10,0))
        self.middle_image_label.grid(row=1, column=0, sticky="ew",padx=20, pady=(0,10))
        self.second_row_middle_sub_info.grid(row=0, column=1, rowspan=2, sticky="ew", padx=20,pady=(10,10))
    
        #info in right_frame
        self.second_row_right_header=tk.Label(self.right_frame,
                                        text="STEP 3",
                                        font=("Arial",30,"bold"),
                                        justify="left",
                                        fg=TEXT_COLOUR,
                                        bg=BG_COLOUR
                                        )

        self.right_image_label = tk.Label(self.right_frame, image=self.right_image, bg=BG_COLOUR)


        self.second_row_right_sub_info = tk.Label(self.right_frame,text="Repeat Step 1 and Step 2 till your desired devices are connected to ADAM. Press the Begin button below once you are ready.", 
                                    font=("Arial",20),
                                    wraplength=400,
                                    justify="left",
                                    fg=TEXT_COLOUR,
                                    bg=BG_COLOUR    
                                    )
                                    
        self.second_row_right_header.grid(row=0, column=0, sticky="ew", padx=20,pady=(10,0))
        self.right_image_label.grid(row=1, column=0, sticky="ew",padx=20, pady=(0,10))
        self.second_row_right_sub_info.grid(row=0, column=1, rowspan=2, sticky="ew", padx=20,pady=(10,10))

        # Setup button (in third row)
        begin_button_font = tkFont.Font(family='Helvetica', size=26, weight='bold')
        self.setup_button = tk.Button(self.third_row, text="Begin", font=begin_button_font,  command=option1)
        self.setup_button.pack(pady=60)

if __name__ == "__main__":
    root = tk.Tk()
    app = welcomeScreen(root, lambda page: print(f"switch to {page}"))
    app.pack(fill="both",expand = True)
    root.mainloop()