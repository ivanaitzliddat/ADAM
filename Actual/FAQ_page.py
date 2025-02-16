import tkinter as tk

#o request config ini to store the following theme colours:
TEXT_COLOUR = "#000000"
BG_COLOUR = "#DCE0D9"
FRAME_COLOUR = "#508991"
GRAB_ATTENTION_COLOUR_1 ="#FF934F"
GRAB_ATTENTION_COLOUR_2 ="#C3423F"

class FAQPage(tk.Frame):
    def __init__(self, parent):

        super().__init__(parent,bg=BG_COLOUR)
        #ConfigHandler.init() #for testing purposes, to be removed once done

        # Create the main frame
        self.frame = tk.Frame(self, bg=BG_COLOUR)
        self.frame.pack(pady=20)

            # Title
        tk.Label(self.frame, text="Frequently Asked Questions (FAQ)",bg=BG_COLOUR, font=("Arial", 16, "bold"), pady=10).pack()

        # FAQs
        faqs = [
            ("Q1: What is this application used for?", 
            "This application helps you manage and configure alert triggers for USB video capture devices."),
            
            ("Q2: How do I add a new trigger condition?", 
            "Click on 'Add Condition' in the trigger configuration window, then fill out the required fields such as keywords, colors, and custom messages."),
            
            ("Q3: Can I delete a trigger condition?", 
            "Yes, each trigger condition has a 'Delete' button. Click it to remove the condition."),
            
            ("Q4: What type of alerts can I configure?", 
            "You can configure alerts based on keywords and/or colors. Each condition will allow custom messages."),
            
            ("Q5: How do I save my configurations?", 
            "Configurations are saved automatically when you close the settings window or by clicking the 'Save' button (if available)."),
            
            ("Q6: Where can I report issues or suggest features?", 
            "You can contact the The Enablers at your_email@example.com for support, feedback, or suggestions.")
        ]

        # Display FAQs
        for question, answer in faqs:
            # Question
            tk.Label(self.frame, text=question, font=("Arial", 12, "bold"),bg=BG_COLOUR, wraplength=550, anchor="w", pady=5).pack(anchor="w", padx=10)
            # Answer
            tk.Label(self.frame, text=answer, font=("Arial", 11),bg=BG_COLOUR, wraplength=550, anchor="w", pady=2).pack(anchor="w", padx=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = FAQPage(root, lambda page: print(f"switch to {page}"))
    app.pack(fill="both", expand = True)
    root.mainloop()
