import tkinter as tk
from tkinter import ttk
import numpy as np
import cv2
import io
from PIL import Image, ImageTk
import imageio_ffmpeg as ffmpeg
from threading import Thread
from processed_screenshot import Processed_Screenshot
import random
from datetime import datetime, timedelta

class AlertsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Alerts Page Content", font=("Arial", 20))
        label.pack(pady=20, padx=20)

        # Create a frame to hold the listbox of event messages
        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
       
        # Create a canvas to contain the scrollable content
        self.canvas = tk.Canvas(self.frame, bg="white", bd=2, relief="solid")
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Create a scrollbar and associate it with the canvas
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the messages
        self.message_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

        # Create Treeview widget
        self.tree = ttk.Treeview(self.message_frame, columns=("Date", "Time", "Message"), show="headings")
        self.tree.heading("Date", text="Date", command=lambda: self.sort_messages("date"))
        self.tree.heading("Time", text="Time", command=lambda: self.sort_messages("time"))
        self.tree.heading("Message", text="Message")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configure column widths
        self.tree.column("Date", width=100, anchor="w")
        self.tree.column("Time", width=100, anchor="w")
        self.tree.column("Message", width=300, anchor="w")

        # Bind click event to messages
        self.tree.bind("<ButtonRelease-1>", self.on_message_click)

        # Store messages for sorting
        self.messages = []

        # Track sorting order
        self.sort_order = {"date": False, "time": False}

        # Generate fake messages for testing
        self.generate_messages()

    def append_message(self, date, time, message, index):
        self.messages.append((date, time, message, index))
        self.display_messages()

    def display_messages(self):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert messages into the treeview
        for date, time, message, index in self.messages:
            self.tree.insert("", "end", values=(date, time, message), tags=(index,))

    def sort_messages(self, key):
        self.sort_order[key] = not self.sort_order[key]
        reverse = self.sort_order[key]
        if key == "date":
            self.messages.sort(key=lambda x: x[0], reverse=reverse)
        elif key == "time":
            self.messages.sort(key=lambda x: x[1], reverse=reverse)
        self.display_messages()

    def sharpen_image(image):
        kernel = np.array([[-1, -1, -1],
                        [-1,  9, -1],
                        [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)

    def test_on_message_click(self, index):
        message = next((msg for msg in self.messages if msg[3] == index), None)
        if message:
            print(f"Message clicked: {message[2]} (Index: {index})")

    def on_message_click(self, event):
        selected_item = self.tree.selection()[0]
        index = int(self.tree.item(selected_item, "tags")[0])
        self.test_on_message_click(index)

    def on_frame_configure(self, event):
        """Update the scrollable region when the frame is resized."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def generate_messages(self):
        for i in range(10):
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            time = (datetime.now() - timedelta(minutes=random.randint(0, 1440))).strftime("%H:%M:%S")
            message = f"Test message {i+1}"
            self.append_message(date, time, message, i)