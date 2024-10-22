import tkinter as tk

def create_user_info_frame(parent):
    frame = tk.Frame(parent, bg="lightblue")
    
    user_info_label = tk.Label(frame, text="User Info Section", font=("Arial", 24))
    user_info_label.pack(pady=20)

    label_name = tk.Label(frame, text="Name:", font=("Arial", 14))
    label_name.pack(pady=5)

    entry_name = tk.Entry(frame, width=40)
    entry_name.pack(pady=5)

    label_age = tk.Label(frame, text="Age:", font=("Arial", 14))
    label_age.pack(pady=5)

    entry_age = tk.Entry(frame, width=40)
    entry_age.pack(pady=5)

    return frame
