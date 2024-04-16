import json
import os
import random
import webbrowser
from bs4 import BeautifulSoup
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import eel
import time

import keyboard

from plyer import notification

def speak(text):
    text =str(text) 
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 140)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

@eel.expose
def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        
        print('Listening.......')
        eel.DisplayMessage('Listening.......')
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source,10,6)

    try:
        print('Recognizing')
        eel.DisplayMessage('Recognizing')
        query = r.recognize_google(audio, language='en-in')
        
        capitalized_query = ' '.join(word.capitalize() for word in query.split())
        print(capitalized_query)
        eel.DisplayMessage(capitalized_query)
        time.sleep(2)
        
    except Exception as e:
        return""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message==1:
        query = takecommand()
        capitalized_query = ' '.join(word.capitalize() for word in query.split())
        print(capitalized_query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)



    try:
        


        
        if "hello" in query:
            speak("Hello , How Can I Help You")
        elif "launch" in query:
            from engine.features import OpenAppCommand
            OpenAppCommand(query)
            # query_lower = query.lower()
            # app = query_lower.replace("launch", "").strip()
            # os.system(f"start {app}://")
            # speak("launch")

        elif "application" in query:
            speak("ok, type application name and command" )
            os.system("python engine\\Custom_app_launch.py")
        
        elif "setting" in query or "settings" in query:
            from engine.features import process_input
            process_input(query)
        # elif "open" in query:
        #     from engine.features import openCommand
        #     openCommand(query)
        elif "internet speed" in query:
            webbrowser.open("https://www.speedtest.net/")
            speak("click go") 

        elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter") 

        

        elif "game" in query:
                    from engine.game import game_play
                    game_play()
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "on chrome" in query or "search" in query:
            from engine.features import search_chrome
            search_chrome(query)
        elif "play" in query and "serial" in query:
            from engine.features import process_user_input
            process_user_input(query)
        elif "find" in query and "word" in query:
            from engine.features import simulate_ctrl_f
            simulate_ctrl_f(query)
        elif "close" in query and "android studio" in query:
            from engine.features import close_android_studio
            close_android_studio()

        elif "stop" in query:
            from engine.features import stop
            stop()

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    message = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query or "call" in query:
                    message = 'call'
                else:
                    message = 'video call'
                    
                whatsApp(contact_no, query, message, name)

        elif"restart" in query:
            from engine.features import  restart_computer
            restart_computer()

        elif"sleep pc"in query or "sleep"in query:
            from engine.features import  sleep_computer
            sleep_computer()


        elif"play" in query or "Stop Playing" in query or "pause" in query:
            from engine.features import media_play
            media_play()
            
        elif "stop playing" in query:
            from engine.features import media_stop
            media_stop()

        elif "set reminder" in query:
            speak("ok")
            speak("Please Enter Title and Time")
            from engine.features import create_reminder_ui
            create_reminder_ui()
            speak("Reminder is set Successfully")

        

        elif "how to add new commands" in query or "how to add new command" in query :
            speak("You can Do that from settings option ")
            speak("or Speak i want to add new cammand")

        elif"create" in query and "command" in query:
            speak("Ok Sir")
            speak("Fill This ,add relaunch Friday ")
            from engine.features import runnnn
            runnnn()
            speak("created successfully")

        elif "volume up" in query:
            from engine.features import volumeup
            speak("Turning volume up,sir")
            volumeup()
        elif "volume down" in query:
            from engine.features import volumedown
            speak("Turning volume down, sir")
            volumedown()

        elif "remember that" in query:
            rememberMessage = query.replace("remember that","")
            rememberMessage = query.replace("Friday","")
            speak("You told me to remember that"+rememberMessage)
            remember = open("engine\\Remember.txt","a")
            remember.write(rememberMessage)
            remember.close()
        elif "what do you remember" in query:
            remember = open("engine\\Remember.txt","r")
            speak("You told me to " + remember.read())

        
        
        

        elif "mute" in query:
            keyboard.press('F1')
            keyboard.release('F1')
            speak("muted")

        elif "tired" in query:
            speak("Playing your favourite songs, sir")
            a = (1,2,3) # You can choose any number of songs (I have only choosen 3)
            b = random.choice(a)
            if b==1:
               webbrowser.open("https://youtu.be/HCWvgoTfUjg?si=YZAuVtUGbXOo4R_5")


            

        # elif "new" in query and "want" in query  and "command" in query or "add new command" in query:
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")
            

        # elif "need" in query and "new" in query and ("command" in query or "add new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")

        # elif "urgent" in query and "new" in query and ("command" in query or "add new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")

        # elif "looking for" in query and "new" in query and ("command" in query or "add new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")

        # elif "looking for" in query and "new" in query and ("command" in query or "add new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")



        # elif "please" in query and "new" in query and ("command" in query or "add new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")


        # elif "excited" in query and "about" in query and ("command" in query or "adding a new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")



        # elif "curious" in query and "about" in query and ("command" in query or "adding a new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")


        # elif "would like" in query and "to" in query and ("request a new command" in query or "add new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")

        
        # elif "wishing for" in query and "new" in query and ("command" in query or "adding a new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")

        
        # elif "if" in query and "you could" in query and ("add" in query or "implement" in query) and "new command" in query:
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")


        # elif "fresh" in query and "command" in query and ("request" in query or "add new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")


        # elif "innovate" in query and "with" in query and ("new" in query and "command" in query or "add new command" in query):
        #     speak("Ok Sir")
        #     speak("Fill This Inputs")
        #     from engine.features import runnnn
        #     runnnn()
        #     speak("Fill This Inputs")
        


        elif "python file" in query or "create new python file" in query or "make new python file" in query or "make new python 5" in query:
            speak("Ok")
            speak("Please Enter File Name")
            os.system("python engine\\Creat_python_file.py")
            speak("Python file Created Successfully")

        elif "temperature" in query:
            search = "temperature in mumbai"
            url = f"https://www.google.com/search?q={search}"
            r  = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            speak(f"current{search} is {temp}")
        elif "weather" in query:
            search = "temperature in mumbai"
            url = f"https://www.google.com/search?q={search}"
            r  = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            speak(f"current{search} is {temp}")

        

        elif "show reminders" in query:
            speak("ok")
            os.system("python engine\\show_remiders.py")

        elif "who" in query or "what" in query or "why" in query or "where" in query or "when" in query or "how" in query or "write" in query or "give" in query or "tell" in query:
            from engine.features import chatBot
            chatBot(query)
            

        elif query:
            from engine.features import find_path_by_name
            find_path_by_name(query)
                

        else:
            speak(f"I did not find any function with the name {capitalized_query} in my system.")
            speak(f"Please provide correct input again.")
            Unknown_input = capitalized_query
            
            
    except:
        speak("error")
        

    
    
    
    
    eel.ShowHood()
    # import keyboard
    # import time
    # keyboard.press_and_release('win+down')

    # # Optional: Add a delay to observe the minimized window
    # time.sleep(2)
    import pyautogui as autogui
    import pygetwindow as gw

    def minimize_window(window_title):
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            if window.isActive:
                autogui.hotkey('winleft', 'down')  # Press Win + Down Arrow to minimize the window
        except IndexError:
            print(f"Window with title '{window_title}' not found.")

    # Example usage:
    minimize_window("F.R.I.D.A.Y")





