import os
import cv2
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import json

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Define custom colors
        self.bg_color = "#e3e3e3"  # Light gray
        self.btn_bg_color = "#4caf50"  # Green
        self.btn_fg_color = "white"  # White

        # OpenCV video capture
        self.cap = cv2.VideoCapture(0)
        
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT), bg=self.bg_color)
        self.canvas.pack(pady=10)
        
        # Capture button
        self.capture_btn = tk.Button(window, text="Capture", command=self.capture, bg=self.btn_bg_color, fg=self.btn_fg_color)
        self.capture_btn.pack(fill="both", padx=20, pady=5)
        
        self.delay = 10
        self.update()

        # Bind window closing event to close_window method
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.window.mainloop()
    
    def update(self):
        # Get a frame from the video source
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)
    
    def capture(self):
        # Prompt user to enter name
        user_name = simpledialog.askstring("Input", "Enter your name:", parent=self.window)
        if user_name:
            # Get a frame from the video source
            ret, frame = self.cap.read()
            if ret:
                # Specify the folder path
                folder_path = "engine/Users_photos"
                # Create the folder if it doesn't exist
                os.makedirs(folder_path, exist_ok=True)
                # Generate filename with user's name
                file_name = f"{user_name}.jpg"
                file_path = os.path.join(folder_path, file_name)
                # Save the captured frame with the filename
                cv2.imwrite(file_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                print(f"Photo captured and saved in {file_path}")
                # Save user name along with photo details in a JSON file
                self.save_photo_details(user_name, file_path)
                self.show_message("Photo captured and saved!")
                # Close the window after capturing the photo
                self.close_window()
            else:
                self.show_message("Failed to capture photo.")
        else:
            self.show_message("Please enter your name.")

    def save_photo_details(self, user_name, file_path):
        data = {
            "user_name": user_name,
            "file_path": file_path,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Specify the JSON file path
        json_file_path = "photo_details.json"
        # Append photo details to the JSON file
        with open(json_file_path, 'a') as json_file:
            json.dump(data, json_file)
            json_file.write('\n')

    def close_window(self):
        self.window.destroy()

    def show_message(self, message):
        messagebox.showinfo("Information", message)

# Create a window and pass it to the CameraApp class
root = tk.Tk()

app = CameraApp(root, "Camera App")
