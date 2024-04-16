import cv2
import face_recognition

# Load images of your face for training
your_image = face_recognition.load_image_file(r"C:\Users\shubham\Pictures\WhatsApp Image 2024-03-30 at 21.22.33_03eef9b6.jpg")
your_encoding = face_recognition.face_encodings(your_image)[0]

# Function to recognize faces and display appropriate message
def recognize_faces_and_greet(frame):
    # Convert frame to RGB (face_recognition library uses RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face found in the frame
    for face_location, face_encoding in zip(face_locations, face_encodings):
        # Compare face encoding with your face encoding
        match = face_recognition.compare_faces([your_encoding], face_encoding)

        # Display appropriate message based on recognition result
        if match[0]:
            cv2.putText(frame, 'Hello', (face_location[3], face_location[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Unwanted', (face_location[3], face_location[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame

# Open a video capture object (you can replace '0' with the path to your video file)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Recognize faces and display appropriate message
    frame_with_message = recognize_faces_and_greet(frame)

    # Display the frame
    cv2.imshow('Face Recognition', frame_with_message)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close all windows
cap.release()
cv2.destroyAllWindows()
