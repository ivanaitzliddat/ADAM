# keyword_manager.py

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


class KeywordPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Title Label
        label = tk.Label(self, text="Keyword Page", font=("Arial", 20))
        label.pack(pady=20, padx=20)
        
        self.keywords = []  # Stores all keywords

        # Section for adding keywords
        self.add_keyword_frame = tk.Frame(self)
        self.add_keyword_frame.pack(pady=10)
        
        self.keyword_label = tk.Label(self.add_keyword_frame, text="Enter Keyword:")
        self.keyword_label.pack(side=tk.LEFT, padx=5)

        self.keyword_entry = tk.Entry(self.add_keyword_frame, width=20)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)
        
        self.add_button = tk.Button(self.add_keyword_frame, text="Add", command=self.add_keyword)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Section for viewing all keywords
        self.keyword_listbox = tk.Listbox(self, width=50, height=10)
        self.keyword_listbox.pack(pady=10)

        # Section for editing and deleting keywords
        self.edit_delete_frame = tk.Frame(self)
        self.edit_delete_frame.pack(pady=5)

        self.edit_button = tk.Button(self.edit_delete_frame, text="Edit", command=self.edit_keyword)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.edit_delete_frame, text="Delete", command=self.delete_keyword)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Section for searching keywords
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(pady=10)
        
        self.search_label = tk.Label(self.search_frame, text="Search Keyword:")
        self.search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(self.search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_keyword)
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        # Button to clear search results and show all keywords
        self.show_all_button = tk.Button(self, text="Show All Keywords", command=self.show_all_keywords)
        self.show_all_button.pack(pady=5)

    def add_keyword(self):
        """Adds a new keyword to the listbox and keyword list."""
        keyword = self.keyword_entry.get().strip()
        if keyword:
            self.keywords.append(keyword)
            self.update_keyword_listbox()
            self.keyword_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid keyword.")

    def update_keyword_listbox(self):
        """Updates the listbox with all keywords."""
        self.keyword_listbox.delete(0, tk.END)
        for keyword in self.keywords:
            self.keyword_listbox.insert(tk.END, keyword)

    def edit_keyword(self):
        """Allows the user to edit a selected keyword."""
        try:
            selected_index = self.keyword_listbox.curselection()[0]
            selected_keyword = self.keywords[selected_index]

            # Pop up an entry box to edit the keyword
            new_keyword = simpledialog.askstring("Edit Keyword", f"Edit keyword '{selected_keyword}':")
            
            # Check if the user clicked "Cancel" (new_keyword is None)
            if new_keyword is not None:
                new_keyword = new_keyword.strip()
                if new_keyword:  # Only update if new_keyword is not empty
                    self.keywords[selected_index] = new_keyword
                    self.update_keyword_listbox()
                else:
                    messagebox.showwarning("Edit Error", "Please enter a valid keyword.")
            # If new_keyword is None (user clicked "Cancel"), do nothing

        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a keyword to edit.")

    def delete_keyword(self):
        """Deletes a selected keyword from the list."""
        try:
            selected_index = self.keyword_listbox.curselection()[0]
            selected_keyword = self.keywords[selected_index]

            # Confirm deletion
            confirm = messagebox.askyesno("Delete Keyword", f"Are you sure you want to delete '{selected_keyword}'?")
            if confirm:
                del self.keywords[selected_index]
                self.update_keyword_listbox()
                
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a keyword to delete.")

    def search_keyword(self):
        """Searches for keywords that match the search term."""
        search_term = self.search_entry.get().strip().lower()
        if search_term:
            matching_keywords = [kw for kw in self.keywords if search_term in kw.lower()]
            self.keyword_listbox.delete(0, tk.END)
            for keyword in matching_keywords:
                self.keyword_listbox.insert(tk.END, keyword)
        else:
            messagebox.showinfo("Search Error", "Please enter a search term.")

    def show_all_keywords(self):
        """Shows all keywords in the listbox."""
        self.update_keyword_listbox()
        self.search_entry.delete(0, tk.END)
