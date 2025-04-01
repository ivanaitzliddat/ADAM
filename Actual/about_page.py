import tkinter as tk
from tkinter import ttk, font as tkFont
import pyttsx3
import pygame
from config_handler import ConfigHandler

# o request config ini to store the following theme colours:
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 = "#FF934F"
GRAB_ATTENTION_COLOUR_2 = "#C3423F"


class AboutPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOUR)

        # Create the main frame
        self.frame = tk.Frame(self, bg=BG_COLOUR)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Title
        tk.Label(
            self.frame,
            text="About ADAM",
            bg=BG_COLOUR,
            font=("Arial", 16, "bold"),
            pady=10
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Introduction
        tk.Label(
            self.frame,
            text="Auxillary Dynamic Alert Monitor (ADAM) is a user-customisable alert monitoring system that takes in display inputs from connected systems,\n"
            "analyses their screen content, and alerts the user if configured word triggers are detected. ADAM is designed to function completely offline\n"
            "and to not interact with/control the connected systems in any way (all it does is 'see'). ADAM is useful in environments where Internet connectivity\n"
            "is not available, and where the systems to be monitored are not able to connect to typical monitoring systems and devices.",
            font=("Arial", 12),
            justify="left",
            padx=10,
            bg=BG_COLOUR
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Key Features
        tk.Label(
            self.frame,
            text="Key Features:",
            bg=BG_COLOUR,
            font=("Arial", 12, "bold"),
            pady=5
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=10)

        features = [
            "Detects and lists USB video capture devices.",
            "Configures custom alert trigger conditions.",
            "Supports keyword and color-based configurations.",
            "User-friendly interface for managing alerts."
        ]
        for i, feature in enumerate(features):
            tk.Label(
                self.frame,
                text=f"• {feature}",
                bg=BG_COLOUR,
                font=("Arial", 10),
                anchor="w"
            ).grid(row=3 + i, column=0, columnspan=2, sticky="w", padx=30)

        # Running Version
        tk.Label(
            self.frame,
            text="Version: 1.0.0",
            bg=BG_COLOUR,
            font=("Arial", 12, "bold"),
            pady=5
        ).grid(row=7, column=0, columnspan=2, sticky="w", padx=10)

        # Release Date
        tk.Label(
            self.frame,
            text="Last updated: February 15, 2025",
            bg=BG_COLOUR,
            font=("Arial", 12),
            anchor="w"
        ).grid(row=8, column=0, columnspan=2, sticky="w", padx=10)

        # Developer Information
        tk.Label(
            self.frame,
            text="Developed by the Team: The Enablers",
            bg=BG_COLOUR,
            font=("Arial", 12),
            pady=5
        ).grid(row=9, column=0, columnspan=2, sticky="w", padx=10)

        tk.Label(
            self.frame,
            text="Team Members:",
            font=("Arial", 12),
            bg=BG_COLOUR,
            pady=5
        ).grid(row=10, column=0, columnspan=2, sticky="w", padx=10)

        team_members = ["Rahul", "Ivan Tan", "Bryan", "Kairos", "Russell", "Jun Long", "Cephas"]
        for i, member in enumerate(team_members):
            tk.Label(
                self.frame,
                text=f"• {member}",
                font=("Arial", 10),
                bg=BG_COLOUR,
                anchor="w"
            ).grid(row=11 + i, column=0, columnspan=2, sticky="w", padx=30)

        tk.Label(
            self.frame,
            text="GitHub: https://github.com/ivanaitzliddat/ADAM",
            bg=BG_COLOUR,
            font=("Arial", 12),
            anchor="w"
        ).grid(row=18, column=0, columnspan=2, sticky="w", padx=10)

        tk.Label(
            self.frame,
            text="Contact: insert contact here?",
            bg=BG_COLOUR,
            font=("Arial", 12),
            anchor="w"
        ).grid(row=19, column=0, columnspan=2, sticky="w", padx=10)

        # Acknowledgments
        tk.Label(
            self.frame,
            text="Acknowledgments:",
            bg=BG_COLOUR,
            font=("Arial", 12, "bold"),
            pady=5
        ).grid(row=20, column=0, columnspan=2, sticky="w", padx=10)

        acknowledgments = [
            "Tkinter for GUI development",
            "Other libraries or resources (if applicable)",
            "ChatGPT",
            "YouTube",
            "w3school",
            "GitHub"
        ]
        for i, ack in enumerate(acknowledgments):
            tk.Label(
                self.frame,
                text=f"• {ack}",
                font=("Arial", 10),
                bg=BG_COLOUR,
                anchor="w"
            ).grid(row=21 + i, column=0, columnspan=2, sticky="w", padx=30)

        # License Information
        tk.Label(
            self.frame,
            text="",
            font=("Arial", 12, "italic"),
            bg=BG_COLOUR,
            pady=10
        ).grid(row=27, column=0, columnspan=2, sticky="w")


if __name__ == "__main__":
    root = tk.Tk()
    app = AboutPage(root)
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
