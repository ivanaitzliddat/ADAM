import tkinter as tk

# Theme colors
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 = "#FF934F"
GRAB_ATTENTION_COLOUR_2 = "#C3423F"


class FAQPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOUR)
        self.parent = parent

        # Configure grid layout for 3 columns
        self.grid_columnconfigure(0, weight=2)  # Left spacer
        self.grid_columnconfigure(1, weight=3)  # Content column
        self.grid_columnconfigure(2, weight=2)  # Right spacer

        # Title (outside the scrollable frame)
        self.title_label = tk.Label(
            self,
            text="Frequently Asked Questions (FAQ)",
            bg=BG_COLOUR,
            font=("Arial", 16, "bold"),
            pady=10
        )
        self.title_label.grid(row=0, column=1, sticky="nsew", pady=(10, 10))

        # Scrollable Canvas
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

        # FAQs
        faqs = [
            ("Q1: What is this application used for?",
             "This application helps you manage and configure alert triggers for USB video capture devices."),

            ("Q2: How do I add/delete a new trigger condition?",
             "Click on 'Add Condition' in the trigger configuration window, then fill out the required fields such as keywords, colors, and custom messages. Each trigger condition has a 'Delete' button, click it to remove the condition."),

            ("Q3: What type of alerts can I configure?",
             "You can configure alerts based on keywords and/or colors. Each condition will allow custom messages."),

            ("Q4: How do I save my configurations?",
             "Configurations are saved automatically when you close the settings window or by clicking the 'Save' button (if available)."),

            ("Q5: Where can I report issues or suggest features?",
             "As with most open source projects, it is recommended to report issues or suggest features in the Issues section of the project's Github repository."),

            ("Q6: Does the application record and store the video input?",
             "This application does not record or store the video input. All inputs are processed in real-time and deleted after it is processed. Once the application is closed, no video input is preserved."),

            ("Q7: What is the maximum number of video inputs that can be connected?",
             "The max number is dependent on the hardware that is used to run this application. Some limiting factors include but are not limited to: CPU used, RAM available, and number of video input ports on motherboard.")
        ]
        
        # Display FAQs
        self.dynamic_labels = []
        for i, (question, answer) in enumerate(faqs):
            # Question
            question_label = tk.Label(
                self.scrollable_frame,
                text=question,
                font=("Arial", 12, "bold"),
                bg=BG_COLOUR,
                anchor="w",
                justify="left",
                pady=5
            )
            question_label.pack(anchor="w", padx=10)
            self.dynamic_labels.append(question_label)

            # Answer
            answer_label = tk.Label(
                self.scrollable_frame,
                text=answer + "\n",
                font=("Arial", 11),
                bg=BG_COLOUR,
                anchor="w",
                justify="left",
                pady=2
            )
            answer_label.pack(anchor="w", padx=20,fill="x")
            self.dynamic_labels.append(answer_label)

        # Bind resize event to dynamically adjust wraplength
        self.on_resize()
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        """Dynamically resize fonts and wraplength based on column 1 width."""
        width = max(self.parent.winfo_width(), 1)
        height = max(self.parent.winfo_height(), 1)
        min_dimension = max(min(width, height), 1)

        # Get the width of column 1
        column1_width = self.grid_slaves(row=0, column=1)[0].winfo_width()

        # Dynamically adjust font sizes
        header_font_size = max(10, min(58, min_dimension // 40))
        subheader_font_size = max(10, min(20, min_dimension // 50))
        body_font_size = max(10, min(14, min_dimension // 60))

        # Update title font
        self.title_label.config(font=("Arial", header_font_size, "bold"))

        min_width = 500 # Minimum width for resizing
        min_height = 800  # Minimum height for resizing

        # Get the root window (Tk instance)
        root = self.winfo_toplevel()

        # Set the minimum size for the window
        root.wm_minsize(min_width, min_height)

        # Update dynamic labels with calculated wraplength
        for label in self.dynamic_labels:
            if "bold" in label.cget("font"):
                label.config(font=("Arial", subheader_font_size, "bold"), wraplength=column1_width-100)
            else:
                label.config(font=("Arial", body_font_size), wraplength=column1_width-100)

    def _on_mousewheel(self, event):
        """Scroll the canvas content with the mouse wheel."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == "__main__":
    root = tk.Tk()
    app = FAQPage(root)
    app.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()