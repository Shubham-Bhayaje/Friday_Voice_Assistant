import tkinter as tk
from tkinter import messagebox
import json


import pyttsx3

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 140)
    engine.say(text)
    engine.runAndWait()

def add_to_app_associate():
    app_name = app_name_entry.get()
    app_protocol = app_protocol_entry.get()

    if app_name.strip() == "" or app_protocol.strip() == "":
        messagebox.showerror("Error", "Please fill in both fields.")
        return

    file_path = "C:\\Friday\\engine\\app_associations.json"
    try:
        with open(file_path, "r") as file:
            app_associate = json.load(file)
    except FileNotFoundError:
        app_associate = {}
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"File '{file_path}' is not in valid JSON format.")
        return

    if app_name in app_associate:
        messagebox.showinfo("Info", f"Application '{app_name}' already exists in the file.")
        return

    app_associate[app_name] = app_protocol

    with open(file_path, "w") as file:
        json.dump(app_associate, file, indent=4)
        root.destroy()

    messagebox.showinfo("Success", f"Application '{app_name}' successfully.")
    

# Create GUI
root = tk.Tk()
root.title("Add Application to app_associate.json")

# Calculate the position to center the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 300  # Set your desired window width
window_height = 200  # Set your desired window height
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

app_name_label = tk.Label(root, text="Application Name:")
app_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

app_name_entry = tk.Entry(root)
app_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

app_protocol_label = tk.Label(root, text="Application Protocol:")
app_protocol_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

app_protocol_entry = tk.Entry(root)
app_protocol_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

add_button = tk.Button(root, text="Add Application", command=add_to_app_associate)
add_button.grid(row=2, columnspan=2, padx=5, pady=5)

root.mainloop()
