import cv2
import face_recognition
import os
import time
import pyttsx3
import tkinter as tk
from PIL import Image, ImageTk

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 140)
    engine.say(text)
    engine.runAndWait()

# Load images of users for training
users_folder = r"engine\Users_photos"
known_encodings = []
known_names = []

for filename in os.listdir(users_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(users_folder, filename)
        name = os.path.splitext(filename)[0]
        user_image = face_recognition.load_image_file(image_path)
        user_encoding = face_recognition.face_encodings(user_image)[0]
        known_encodings.append(user_encoding)
        known_names.append(name)

# Function to start face recognition
def start_recognition():
    # Open a video capture object
    cap = cv2.VideoCapture(0)

    # Set desired frame width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Set desired frame rate
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Face Recognition")
    root.geometry("800x600")  # Set initial window size

    # Customize window background color to black
    root.configure(bg="#000000")  # Set background color to black

    # Create a label to display the video feed
    label = tk.Label(root)
    label.pack(pady=20)  # Add some padding

    # Flag to indicate whether face detection should be active
    face_detection_active = False

    # Function to recognize faces and display appropriate message
    def recognize_faces_and_greet(frame):
        nonlocal face_detection_active

        # Convert frame to RGB (face_recognition library uses RGB images)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to ImageTk format
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        label.imgtk = imgtk
        label.configure(image=imgtk)

        # Continue face detection loop if not started yet
        if not face_detection_active:
            return True

        # Loop through each face found in the frame for recognition
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare face encoding with known face encodings
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            # Check if any match is found
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            # Display appropriate message based on recognition result
            if name != "Unknown":
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                speak(f"Hello {name}")
                # Sleep for 3 seconds
                time.sleep(1)
                # Release the capture object
                cap.release()
                root.destroy()  # Close the Tkinter window
                # Run system command if user's face is detected
                os.system(r"C:\Friday\run.py")
                return False  # Stop face detection loop
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Red rectangle for unknown face
                speak("Sorry, I don't recognize you.")  # Speak message for unknown face
                speak("If you are new, you need to register first.")

        return True  # Continue face detection loop

    # Function to handle button click for recognition
    def on_recognition_button_click():
        nonlocal face_detection_active
        face_detection_active = True

    # Function to handle button click for registration
    def on_register_button_click():
        # Add your registration logic here
        pass

    # Create a button for starting recognition
    button_recognition = tk.Button(root, text="Start Recognition", command=on_recognition_button_click, bg="#4CAF50", fg="white", font=("Arial", 14))
    button_recognition.pack(side=tk.LEFT, padx=10, pady=10)  # Add some padding and position it to the left

    # Start face detection
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Recognize faces and display appropriate message
        continue_detection = recognize_faces_and_greet(frame)

        # Update the Tkinter window
        root.update()

        # Break the loop if system command was executed or 'q' is pressed
        if not continue_detection or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Start the face recognition process
start_recognition()
