import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import json

def load_reminder_data(file_path="reminder.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def show_reminders(reminder_data):
    root = tk.Tk()
    root.title("Reminders")

    # Create a style to configure vertical and horizontal lines
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"), foreground="white", background="#309f91")
    style.configure("Treeview", font=("Arial", 12), rowheight=25)
    style.configure("Treeview.Heading", borderwidth=2, relief="solid")
    style.configure("Treeview", borderwidth=2, relief="solid")

    tree = ttk.Treeview(root, style="Custom.Treeview")
    tree["columns"] = ("Index", "Time", "Title")
    tree.heading("#0", text="", anchor="w")
    tree.column("#0", anchor="w", width=10)
    tree.heading("Index", text="Index", anchor="center")
    tree.column("Index", anchor="center", width=50)
    tree.heading("Time", text="Time", anchor="center")
    tree.column("Time", anchor="center", width=100)
    tree.heading("Title", text="Title", anchor="w")
    tree.column("Title", anchor="w", width=150)

    # Apply a custom style to set the background color for the title row
    tree.tag_configure("title_row", background="#309f91")

    # Add the title row to the treeview
    tree.insert("", "end", values=("Index", "Time", "Title"), tags="title_row")

    current_time = datetime.now().strftime("%H:%M")

    for idx, reminder in enumerate(reminder_data):
        reminder_title = reminder["title"]
        reminder_time = reminder["time"]

        # Convert reminder time to datetime object for comparison
        reminder_datetime = datetime.strptime(reminder_time, "%H:%M")

        # Check if the reminder time is later than the current time
        if reminder_datetime > datetime.strptime(current_time, "%H:%M"):
            time_difference = reminder_datetime - datetime.strptime(current_time, "%H:%M")
        else:
            # If the time has already passed, calculate the difference for the next day
            time_difference = timedelta(days=1) + (reminder_datetime - datetime.strptime(current_time, "%H:%M"))

        # Schedule a callback to show the reminder after the time difference
        root.after(int(time_difference.total_seconds() * 1000), lambda index=idx, title=reminder_title: show_reminder_popup(index, title))

        # Insert data into the treeview
        tree.insert("", "end", values=(idx + 1, reminder_time, reminder_title))

    # Configure the rows and columns to expand with the window
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Set the window size to be three times larger
    window_width = root.winfo_screenwidth() // 3
    window_height = root.winfo_screenheight() // 3
    root.geometry(f"{window_width}x{window_height}+100+100")  # Adjust the position accordingly

    # Use grid for the Treeview widget
    tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    root.mainloop()

def show_reminder_popup(index, title):
    popup = tk.Toplevel()
    popup.title("Reminder")
    popup.geometry("300x120")

    reminder_label = tk.Label(popup, text=f"Reminder #{index + 1}: {title}", font=("Arial", 16, "bold"), fg="green")
    reminder_label.pack(pady=20)

    close_button = tk.Button(popup, text="Close", command=popup.destroy, font=("Arial", 12, "bold"), bg="lightgray")
    close_button.pack()

if __name__ == "__main__":
    # Load reminder data from the JSON file
    reminder_data = load_reminder_data()

    # Call the function to show reminders
    show_reminders(reminder_data)
