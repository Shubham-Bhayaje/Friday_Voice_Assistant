import tkinter as tk
from tkinter import Label, Entry, Button
from tkinter import Tk, filedialog
import sqlite3
import time
import os
import shutil

import pyttsx3


def speak_message(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()


def move_file(file_path, destination_folder):
    try:
        # Move the file to the destination folder
        shutil.move(file_path, destination_folder)
        print(f"File moved successfully to {destination_folder}")
    except Exception as e:
        print(f"Error: {e}")

def get_file_path():
    root = Tk()
    root.withdraw()  # Hide the main window

    # Specify the file types to be selected (only Python files in this case)
    file_path = filedialog.askopenfilename(title="Select a Python file",
                                           filetypes=[("Python files", "*.py")])

    return file_path

def insert_data():
    keyword = keyword_entry.get()

    # Check if keyword already exists
    cursor.execute("SELECT * FROM users_cuostom_commands WHERE name = ?", (keyword,))
    existing_command = cursor.fetchone()

    if existing_command:
        
        status_label.config(text="Keyword Already Exists.Please Choose A Different Keyword.", fg="red")
        speak_message("Keyword Already Exists. Please Choose A Different Keyword.")
        return 

    # Get file path from user using a file dialog
    file_path = get_file_path()

    # Check if a file is selected
    if not file_path:
        status_label.config(text="Please select a Python file.", fg="red")
        return

    # Specify the destination folder
    destination_folder = "C:\\Friday\\engine\\Custom_Commands"

    # Move the file
    move_file(file_path, destination_folder)

    # Extract the file name
    file_name = os.path.basename(file_path)

    # Define the new prefix
    new_prefix = "C:\\Friday\\engine\\Custom_Commands"

    # Create the new path
    new_path = os.path.join(new_prefix, file_name)

    # Insert data into the database
    if keyword:
        query = "INSERT INTO users_cuostom_commands VALUES (null, ?, ?)"
        cursor.execute(query, (keyword, new_path))
        con.commit()
        status_label.config(text="New Command Created Successfully!", fg="green")
    else:
        status_label.config(text="Please enter a keyword.", fg="red")


    from pymongo import MongoClient
    from urllib.parse import quote_plus

    # Encode the username and password
    username = 'shubhambhayaje913'
    password = 'n8GGzx5C0KJ35vDG'
    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)

    # Construct the connection URI with encoded username and password
    connection_uri = f'mongodb+srv://{encoded_username}:{encoded_password}@cluster0.pbpp7vk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

    client = MongoClient(connection_uri)

    # The rest of your code remains the same
    db = client['create_custom_commands']
    collection = db['create_custom_commandss']
    document = {"command":keyword, "path": file_path}
    insert_doc = collection.insert_one(document)
    print(f"Inserted Doc id: {insert_doc.inserted_id}")

    client.close()


    # Insert data into the database
    if keyword:
        query = f"INSERT INTO users_cuostom_commands VALUES (null, '{keyword}', '{new_path}')"
        cursor.execute(query)
        con.commit()
        status_label.config(text="New Command Created Successfully!", fg="green")
        window.update_idletasks()  # Update the Tkinter window
        time.sleep(2)  # Sleep for 2 seconds
        window.destroy()  # Close the Tkinter window after 2 seconds
    else:
        status_label.config(text="Please enter a keyword.", fg="red")

# Create SQLite connection and cursor
con = sqlite3.connect("Friday.db")
cursor = con.cursor()

# Create Tkinter window
window = tk.Tk()
window.title("Custom Commands Database")

# Set the window dimensions
window.geometry("500x200")  # Adjust the width and height as needed

# Create and place labels, entry widgets, and button
Label(window, text="Keyword:", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10)

keyword_entry = Entry(window, font=('Arial', 12))
keyword_entry.grid(row=0, column=1, padx=10, pady=10)

insert_button = Button(window, text="Select Python file", command=insert_data, background="#007BFF", foreground="white")
insert_button.grid(row=2, column=0, columnspan=2, pady=10)

status_label = Label(window, text="", font=('Arial', 12))
status_label.grid(row=3, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
window.mainloop()
