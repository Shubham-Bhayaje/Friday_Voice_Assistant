import pyttsx3

def speak(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

speak("shubham")
