import tkinter as tk
from tkinter import ttk, font as tkFont

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

        # Configure grid layout for 3 columns
        self.grid_columnconfigure(0, weight=2)  # Left spacer
        self.grid_columnconfigure(1, weight=3)  # Content column
        self.grid_columnconfigure(2, weight=2)  # Right spacer

        # Store references to labels for resizing
        self.dynamic_labels = []

        # Title (placed in column 1)
        self.title_label = tk.Label(
            self,
            text="About ADAM",
            bg=BG_COLOUR,
            font=("Arial", 16, "bold"),
            pady=10
        )
        self.title_label.grid(row=0, column=1, sticky="nsew", pady=(10, 10))

        # Scrollable Canvas (placed in column 1)
        self.canvas = tk.Canvas(self, bg=BG_COLOUR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOUR)

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a window inside the canvas for the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind the scrollable frame to the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Place the canvas and scrollbar in column 1
        self.canvas.grid(row=1, column=1, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="nes")

        # Configure row weights for resizing
        self.grid_rowconfigure(1, weight=1)

        # Introduction
        self.intro_label = tk.Label(
            self.scrollable_frame,
            text="Auxillary Dynamic Alert Monitor (ADAM) is a user-customisable alert monitoring system that takes in display inputs from connected systems,"
            "analyses their screen content, and alerts the user if configured word triggers are detected. ADAM is designed to function completely offline"
            "and to not interact with/control the connected systems in any way (all it does is 'see'). ADAM is useful in environments where Internet connectivity"
            "is not available, and where the systems to be monitored are not able to connect to typical monitoring systems and devices.",
            font=("Arial", 12),
            justify="left",
            anchor="w",
            bg=BG_COLOUR
        )
        self.intro_label.pack(anchor="w", padx=10)
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
            text="Version: Unreleased - Development Phase",
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

        team_members_label = tk.Label(
            self.scrollable_frame,
            text="Development Team:",
            font=("Arial", 12, "bold"),
            bg=BG_COLOUR,
            pady=5
        )
        team_members_label.pack(anchor="w", padx=10)
        self.dynamic_labels.append(team_members_label)

        team_members = ["Rahul", "Ivan", "Kairos", "Russell", "Jun Long", "Cephas"]
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

        # Bind resize event to dynamically adjust wraplength
        self.on_resize()
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        """Dynamically resize fonts and wraplength based on column 1 width."""
        # Calculate the width of column 1 (content column)
        total_width = self.winfo_width()
        column1_width = total_width * 3 / 7  # Column 1 has weight 3 out of total weight 7
        #print(column1_width)

        # Dynamically adjust font sizes
        header_font_size = max(10, min(58, int(column1_width // 20)))
        subheader_font_size = max(10, min(20, int(column1_width // 50)))
        body_font_size = max(10, min(14, int(column1_width // 60)))

        # Update title font
        self.title_label.config(font=("Arial", header_font_size, "bold"))

        min_width = 500 # Minimum width for resizing
        min_height = 800  # Minimum height for resizing

        # Get the root window (Tk instance)
        root = self.winfo_toplevel()

        # Set the minimum size for the window
        root.wm_minsize(min_width, min_height)

        # Update dynamic labels
        for label in self.dynamic_labels:
            if "bold" in label.cget("font"):
                label.config(font=("Arial", subheader_font_size, "bold"), wraplength=int(column1_width+150))
            else:
                label.config(font=("Arial", body_font_size), wraplength=int(column1_width+150))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = AboutPage(root)
    app.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()
