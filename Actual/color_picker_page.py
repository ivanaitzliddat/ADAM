# color_page.py

import tkinter as tk
from tkinter import colorchooser, messagebox, simpledialog
from tkinter import ttk

class ColorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.colors = []  # List to store colors in hex format

        # Section for adding colors
        self.add_color_frame = tk.Frame(self)
        self.add_color_frame.pack(pady=10)

        # Label and Entry for hex color code
        self.color_label = tk.Label(self.add_color_frame, text="Enter Hex Color Code:")
        self.color_label.pack(side=tk.LEFT, padx=5)

        self.color_entry = tk.Entry(self.add_color_frame, width=10)
        self.color_entry.pack(side=tk.LEFT, padx=5)

        # Add color button
        self.add_button = tk.Button(self.add_color_frame, text="Add Color", command=self.add_color)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Color picker button
        self.color_picker_button = tk.Button(self.add_color_frame, text="Pick Color", command=self.pick_color)
        self.color_picker_button.pack(side=tk.LEFT, padx=5)

        # Color preview box
        self.color_preview = tk.Label(self.add_color_frame, text="    ", bg="white", relief="solid", width=5)
        self.color_preview.pack(side=tk.LEFT, padx=5)

        # Treeview for viewing all colors with a color cell
        self.color_tree = ttk.Treeview(self, columns=("Color", "Hex"), show="headings", height=10)
        self.color_tree.heading("Color", text="Color")
        self.color_tree.heading("Hex", text="Hex Code")
        self.color_tree.column("Color", width=50)
        self.color_tree.column("Hex", width=100)
        self.color_tree.pack(pady=10)

        # Buttons for managing colors
        self.edit_button = tk.Button(self, text="Edit Color", command=self.edit_color)
        self.edit_button.pack(pady=5)
        
        self.delete_button = tk.Button(self, text="Delete Color", command=self.delete_color)
        self.delete_button.pack(pady=5)

    def add_color(self):
        """Adds a new color based on hex input or chosen color."""
        color_code = self.color_entry.get().strip()
        if color_code and self.is_valid_hex(color_code):
            self.colors.append(color_code)
            self.update_color_tree()
            self.color_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Invalid Input", "Please enter a valid hex color code (e.g., #RRGGBB).")

    def pick_color(self):
        """Opens a color picker dialog and sets the preview and entry fields."""
        color_code = colorchooser.askcolor(title="Choose Color")[1]  # Returns (RGB, hex)
        if color_code:  # User picked a color
            self.color_preview.config(bg=color_code)
            self.color_entry.delete(0, tk.END)
            self.color_entry.insert(0, color_code)

    def update_color_tree(self):
        """Updates the Treeview with all colors and their previews."""
        self.color_tree.delete(*self.color_tree.get_children())
        for color in self.colors:
            # Insert color row with hex code; 'tags' allow custom styling for rows
            self.color_tree.insert("", tk.END, values=("", color), tags=(color,))
            self.color_tree.tag_configure(color, background=color)  # Set background color

    def edit_color(self):
        """Allows the user to edit a selected color."""
        selected_item = self.color_tree.selection()
        if selected_item:
            selected_color = self.color_tree.item(selected_item)["values"][1]
            new_color = simpledialog.askstring("Edit Color", f"Edit color '{selected_color}':", initialvalue=selected_color)
            
            if new_color is not None and self.is_valid_hex(new_color):
                index = self.colors.index(selected_color)
                self.colors[index] = new_color
                self.update_color_tree()
            elif new_color is not None:
                messagebox.showwarning("Invalid Input", "Please enter a valid hex color code.")
                
        else:
            messagebox.showwarning("Selection Error", "Please select a color to edit.")

    def delete_color(self):
        """Deletes the selected color after confirmation."""
        selected_item = self.color_tree.selection()
        if selected_item:
            selected_color = self.color_tree.item(selected_item)["values"][1]
            
            # Prompt user for confirmation before deleting
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_color}'?")
            if confirm:  # Only delete if user clicks "Yes"
                self.colors.remove(selected_color)
                self.update_color_tree()
        else:
            messagebox.showwarning("Selection Error", "Please select a color to delete.")

    def is_valid_hex(self, color_code):
        """Validates if the input is a valid hex color code."""
        if color_code.startswith("#") and len(color_code) == 7:
            try:
                int(color_code[1:], 16)
                return True
            except ValueError:
                return False
        return False
