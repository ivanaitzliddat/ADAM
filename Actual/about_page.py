import tkinter as tk
from tkinter import ttk, font as tkFont
from PIL import Image, ImageTk

# Theme colors
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 = "#FF934F"
GRAB_ATTENTION_COLOUR_2 = "#C3423F"


class AboutPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOUR)
        self.parent = parent

        # Store references to labels for resizing
        self.dynamic_labels = []

        # Title (outside the scrollable frame)
        self.title_label = tk.Label(
            self,
            text="About ADAM",
            bg=BG_COLOUR,
            font=("Arial", 16, "bold"),
            pady=10
        )
        self.title_label.pack(side="top", fill="x", pady=(10, 10))

        # Scrollable Canvas
        self.canvas_frame = tk.Frame(self, bg=BG_COLOUR)  # Container for canvas and scrollbar
        self.canvas_frame.pack(side="top", fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg=BG_COLOUR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOUR)

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar inside the container frame
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y",padx=(10,0))

        # Create a window inside the canvas for the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind the scrollable frame to the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Responsive Resizing
        self.parent.bind("<Configure>", self.on_resize)

        # Introduction
        self.intro_label = tk.Label(
            self.scrollable_frame,
            text="Auxillary Dynamic Alert Monitor (ADAM) is a user-customisable alert monitoring system that takes in display inputs from connected systems,"
            "analyses their screen content, and alerts the user if configured word triggers are detected. \n\nADAM is designed to function completely offline"
            "and to not interact with/control the connected systems in any way (all it does is 'see'). \n\nADAM is useful in environments where Internet connectivity"
            "is not available, and where the systems to be monitored are not able to connect to typical monitoring systems and devices.",
            font=("Arial", 12),
            justify="left",
            padx=10,
            bg=BG_COLOUR
        )
        self.intro_label.pack(anchor="w", pady=(0, 10), padx=(0,10))
        self.dynamic_labels.append(self.intro_label)

        # Key Features
        key_features_label = tk.Label(
            self.scrollable_frame,
            text="Key Features:",
            bg=BG_COLOUR,
            font=("Arial", 12, "bold"),
            pady=5
        )
        key_features_label.pack(anchor="w", padx=10)
        self.dynamic_labels.append(key_features_label)

        features = [
            "Detects and lists USB video capture devices.",
            "Configures custom alert trigger conditions.",
            "Supports keyword and color-based configurations.",
            "User-friendly interface for managing alerts."
        ]
        for feature in features:
            feature_label = tk.Label(
                self.scrollable_frame,
                text=f"• {feature}",
                bg=BG_COLOUR,
                font=("Arial", 10),
                anchor="w"
            )
            feature_label.pack(anchor="w", padx=30)
            self.dynamic_labels.append(feature_label)

        # Running Version
        version_label = tk.Label(
            self.scrollable_frame,
            text="Version: 1.0.0",
            bg=BG_COLOUR,
            font=("Arial", 12, "bold"),
            pady=5
        )
        version_label.pack(anchor="w", padx=10)
        self.dynamic_labels.append(version_label)

        # Release Date
        release_date_label = tk.Label(
            self.scrollable_frame,
            text="Last updated: February 15, 2025",
            bg=BG_COLOUR,
            font=("Arial", 12),
            anchor="w"
        )
        release_date_label.pack(anchor="w", padx=10)
        self.dynamic_labels.append(release_date_label)

        # Developer Information
        developer_label = tk.Label(
            self.scrollable_frame,
            text="Developed by the Team: The Enablers",
            bg=BG_COLOUR,
            font=("Arial", 12),
            pady=5
        )
        developer_label.pack(anchor="w", padx=10)
        self.dynamic_labels.append(developer_label)

        team_members_label = tk.Label(
            self.scrollable_frame,
            text="Team Members:",
            font=("Arial", 12),
            bg=BG_COLOUR,
            pady=5
        )
        team_members_label.pack(anchor="w", padx=10)
        self.dynamic_labels.append(team_members_label)

        team_members = ["Rahul", "Ivan Tan", "Bryan", "Kairos", "Russell", "Jun Long", "Cephas"]
        for member in team_members:
            member_label = tk.Label(
                self.scrollable_frame,
                text=f"• {member}",
                font=("Arial", 10),
                bg=BG_COLOUR,
                anchor="w"
            )
            member_label.pack(anchor="w", padx=30)
            self.dynamic_labels.append(member_label)

        github_label = tk.Label(
            self.scrollable_frame,
            text="GitHub: https://github.com/ivanaitzliddat/ADAM",
            bg=BG_COLOUR,
            font=("Arial", 12),
            anchor="w"
        )
        github_label.pack(anchor="w", padx=10)
        self.dynamic_labels.append(github_label)

        contact_label = tk.Label(
            self.scrollable_frame,
            text="Contact: insert contact here?",
            bg=BG_COLOUR,
            font=("Arial", 12),
            anchor="w"
        )
        contact_label.pack(anchor="w", padx=10)
        self.dynamic_labels.append(contact_label)

        # Acknowledgments
        acknowledgments_label = tk.Label(
            self.scrollable_frame,
            text="Acknowledgments:",
            bg=BG_COLOUR,
            font=("Arial", 12, "bold"),
            pady=5
        )
        acknowledgments_label.pack(anchor="w", padx=10)
        self.dynamic_labels.append(acknowledgments_label)

        acknowledgments = [
            "Tkinter for GUI development",
            "Other libraries or resources (if applicable)",
            "ChatGPT",
            "YouTube",
            "w3school",
            "GitHub"
        ]
        for ack in acknowledgments:
            ack_label = tk.Label(
                self.scrollable_frame,
                text=f"• {ack}",
                font=("Arial", 10),
                bg=BG_COLOUR,
                anchor="w"
            )
            ack_label.pack(anchor="w", padx=30)
            self.dynamic_labels.append(ack_label)

    def on_resize(self, event=None):
        """Dynamically resize fonts based on window size."""
        width = max(self.parent.winfo_width(), 1)
        height = max(self.parent.winfo_height(), 1)
        min_dimension = max(min(width, height), 1)

        scrollbar_width = self.scrollbar.winfo_width()

        # Dynamically adjust font sizes
        header_font_size = max(10, min(58, min_dimension // 20))
        subheader_font_size = max(10, min(20, min_dimension // 50))
        body_font_size = max(10, min(14, min_dimension // 60))

        # Update title font
        self.title_label.config(font=("Arial", header_font_size, "bold"))
        self.intro_label.config(wraplength=self.parent.winfo_width() - scrollbar_width - 10)

        # Update dynamic labels
        for label in self.dynamic_labels:
            if "bold" in label.cget("font"):
                label.config(font=("Arial", subheader_font_size, "bold"))
            else:
                label.config(font=("Arial", body_font_size))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = AboutPage(root)
    app.pack(fill="both", expand=True)
    root.mainloop()