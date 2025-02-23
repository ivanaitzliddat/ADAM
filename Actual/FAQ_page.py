import tkinter as tk

# o request config ini to store the following theme colours:
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 = "#FF934F"
GRAB_ATTENTION_COLOUR_2 = "#C3423F"


class FAQPage(tk.Frame):
    def __init__(self, parent):

        super().__init__(parent, bg=BG_COLOUR)
        # ConfigHandler.init() #for testing purposes, to be removed once done

        # Create the main frame
        self.frame = tk.Frame(self, bg=BG_COLOUR)
        self.frame.pack(pady=20)

        # Title
        tk.Label(self.frame, text="Frequently Asked Questions (FAQ)",
                 bg=BG_COLOUR, font=("Arial", 16, "bold"), pady=10).pack()

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
        for question, answer in faqs:
            # Question
            tk.Label(self.frame, text=question, font=("Arial", 12, "bold"), bg=BG_COLOUR,
                     wraplength=550, anchor="w", pady=5).pack(anchor="w", padx=10)
            # Answer
            tk.Label(self.frame, text=answer, font=("Arial", 11), bg=BG_COLOUR,
                     wraplength=550, anchor="w", pady=2).pack(anchor="w", padx=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = FAQPage(root, lambda page: print(f"switch to {page}"))
    app.pack(fill="both", expand=True)
    root.mainloop()
