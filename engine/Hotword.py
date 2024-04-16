import time
import pyttsx3
import speech_recognition 
import pyautogui as autogui

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)

    try:
        print("Understanding..")
        query  = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
        return query.lower()
    except Exception as e:
        print("Say that again")
        return "None"

def manageAI():
    while True:
        query = takeCommand()
        if "wake up" in query:
            from engine.features import hotword
            hotword()
            while True:
                query = takeCommand()
                if "go to sleep" in query:
                    speak("Ok sir, you can call me anytime.")
                    print("Going to sleep...")
                    return


