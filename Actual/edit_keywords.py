import tkinter as tk
from tkinter import messagebox
from config_handler import ConfigHandler

class EditKeywordsPage:
    def __init__(self, root, usb_alt_name, condition, keywords, callback):
        self.root = root
        self.root.geometry("1000x500")
        self.usb_alt_name = usb_alt_name
        self.condition = condition
        self.callback = callback

        #a temp list to store the keywords independently of the actual keywords list
        self.temp_keywords = keywords.copy()

        #actual keywords list
        self.keywords = keywords
     
        # Center the window after initializing
        self.root.after(0, self.center_window)
        self.setup_ui()

    def setup_ui(self):
        self.root.title(f"Edit Keywords for {self.usb_alt_name} - {self.condition}")
        condition_frame = tk.Frame(self.root, width=1000, pady=5, highlightbackground="grey", highlightthickness=1)
        condition_frame.pack(fill="y", pady=5)

        self.keyword_array_frame = tk.Frame(condition_frame, width=1000)
        self.keyword_array_frame.pack(fill="x", padx=5, pady=2)

        self.keyword_labels_frame = tk.Frame(self.keyword_array_frame, width=1000)
        self.keyword_labels_frame.pack(fill="x", expand=True)

        self.display_keywords()

        add_keyword_button = tk.Button(self.keyword_array_frame, text="Add Keyword", command=self.add_keyword_entry)
        add_keyword_button.pack(pady=5)

        save_button = tk.Button(self.keyword_array_frame, text="Save", command=self.save_keywords)
        save_button.pack(side="left", padx=5, pady=5)

        cancel_button = tk.Button(self.keyword_array_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side="right", padx=5, pady=5)

    def display_keywords(self):
        for widget in self.keyword_labels_frame.winfo_children():
            widget.destroy()

        columns = 4
        for index, keyword in enumerate(self.temp_keywords):
            
            row = index // columns
            col = index % columns
            keyword_entry = tk.Entry(self.keyword_labels_frame, font=("Arial", 10))
            keyword_entry.insert(0, keyword)
            keyword_entry.grid(row=row, column=col*6,padx=(20, 0), pady=2, sticky="w")
            keyword_entry.config(state='readonly')
            delete_button = tk.Button(self.keyword_labels_frame, text="X", font=("Arial", 8, "bold"), fg="red",
                                      command=lambda idx=index: self.delete_keyword(idx))
            delete_button.grid(row=row, column=col*6+1, sticky="w")
            edit_keyword_button = tk.Button(self.keyword_labels_frame, text="Edit", font=("Arial", 8, "bold"), fg="blue", 
                                            command=lambda idx=index: self.edit_single_keyword(idx))
            edit_keyword_button.grid(row=row, column=col*6+2, padx=(0, 20),sticky="w")

    def add_keyword_entry(self):
        def on_submit():
            keyword = keyword_entry.get()
            if keyword and isinstance(keyword, str):
                self.temp_keywords.append(keyword)
                self.display_keywords()
                add_keyword_window.destroy()
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid keyword (non-empty string).", parent=add_keyword_window)

        add_keyword_window = tk.Toplevel(self.root)
        add_keyword_window.title("Add Keyword")
        add_keyword_window.geometry("300x100")
        add_keyword_window.transient(self.root)

        # Center the window
        add_keyword_window.update_idletasks()
        width = add_keyword_window.winfo_width()
        height = add_keyword_window.winfo_height()
        x = (add_keyword_window.winfo_screenwidth() // 2) - (width // 2)
        y = (add_keyword_window.winfo_screenheight() // 2) - (height // 2)
        add_keyword_window.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(add_keyword_window, text="Enter Keyword:", font=("Arial", 10)).pack(pady=10)
        keyword_entry = tk.Entry(add_keyword_window, font=("Arial", 10))
        keyword_entry.pack(pady=5)

        submit_button = tk.Button(add_keyword_window, text="Submit", command=on_submit)
        submit_button.pack(pady=5)

    def edit_single_keyword(self, index):
        def on_submit():
            keyword = keyword_entry.get()
            if keyword and isinstance(keyword, str):
                self.temp_keywords[index] = keyword
                self.display_keywords()
                edit_single_keyword_window.destroy()
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid keyword (non-empty string).", parent=edit_single_keyword_window)

        edit_single_keyword_window = tk.Toplevel(self.root)
        edit_single_keyword_window.title("Edit Keyword")
        edit_single_keyword_window.geometry("300x100")
        edit_single_keyword_window.transient(self.root)

        # Center the window
        edit_single_keyword_window.update_idletasks()
        width = edit_single_keyword_window.winfo_width()
        height = edit_single_keyword_window.winfo_height()
        x = (edit_single_keyword_window.winfo_screenwidth() // 2) - (width // 2)
        y = (edit_single_keyword_window.winfo_screenheight() // 2) - (height // 2)
        edit_single_keyword_window.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(edit_single_keyword_window, text="Edit Keyword:", font=("Arial", 10)).pack(pady=10)
        keyword_entry = tk.Entry(edit_single_keyword_window, font=("Arial", 10))
        keyword_entry.insert(0, self.temp_keywords[index])
        keyword_entry.pack(pady=5)

        submit_button = tk.Button(edit_single_keyword_window, text="Submit", command=on_submit)
        submit_button.pack(pady=5)

    def delete_keyword(self, index):
        del self.temp_keywords[index]
        self.display_keywords()

    def save_keywords(self):
        #create a temporary list to store the keywords
        temp_array = []
        empty_keyword_found = False  # Initialize the flag
        #iterate through the keyword_labels_frame
        for widget in self.keyword_labels_frame.winfo_children():
            #check if the widget is an Entry widget
            if isinstance(widget, tk.Entry):
                #check if the entry is not empty
                if widget.get() != "":
                    #append the keyword to the temporary list
                    temp_array.append(widget.get())
                else:
                    self.root.lift()  # Bring the main window to the front
                    self.root.attributes('-topmost', True)  # Keep it on top
                    self.root.attributes('-topmost', False)  # Allow other windows to be on top
                    messagebox.showwarning("Warning", "Empty keyword(s) found! Please fill in all keywords.", parent=self.root)
                    empty_keyword_found = True
                    break

        if not empty_keyword_found:
            if len(temp_array) == 0:
                self.root.lift()  # Bring the main window to the front
                self.root.attributes('-topmost', True)  # Keep it on top
                self.root.attributes('-topmost', False)  # Allow other windows to be on top
                messagebox.showwarning("Warning", "Condition must have at least 1 keyword!", parent=self.root)
            else:
                self.keywords = temp_array
                ConfigHandler.set_cfg_input_device(usb_alt_name = self.usb_alt_name, condition = self.condition, keywords = self.keywords)
                ConfigHandler.save_config()
                self.root.destroy()
                self.callback()
                return True
            
    def cancel(self):
        self.root.destroy()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}") 

def edit_keywords(alt_name, condition, keywords, callback):
    root = tk.Tk()
    app = EditKeywordsPage(root, alt_name, condition, keywords, callback)
    root.mainloop()