import tkinter as tk
import os
import pyttsx3

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 140)
    engine.say(text)
    engine.runAndWait()

def open_file():
    file_name = entry.get()
    if file_name:
        os.system(f"code {file_name}.py")
        # speak(f"File Created with Name{file_name}")

        root.destroy()  # Close the input window after opening the file
    else:
        result_label.config(text="Please enter a valid file name", fg="red")

def handle_enter_key(event):
    open_file()

# Create the main window
root = tk.Tk()
root.title("File Opener")

# Set window size and center it on the screen
window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Configure window background color
root.configure(bg="#f0f0f0")

# Create and place widgets
label = tk.Label(root, text="Enter file name:", font=("Helvetica", 12), bg="#f0f0f0")
label.pack(pady=10)

entry = tk.Entry(root, width=30, font=("Helvetica", 12))
entry.pack(pady=10)
entry.bind("<Return>", handle_enter_key)

open_button = tk.Button(root, text="Open File", command=open_file, font=("Helvetica", 12))
open_button.pack(pady=10)

# Bind the <Return> key to the open_file function when the "Open File" button has focus
open_button.bind("<Return>", lambda event=None: open_file())

result_label = tk.Label(root, text="", font=("Helvetica", 10), fg="red", bg="#f0f0f0")
result_label.pack(pady=10)

# Set focus to the entry widget
entry.focus_set()

# Run the Tkinter main loop
root.mainloop()
