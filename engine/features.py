import os
from pipes import quote
import struct
import subprocess
import sys
import time
import urllib.parse
import webbrowser
from anyio import sleep
import pyaudio
import pyautogui
import sqlite3
import sqlite3
import os
import json
import tkinter as tk
from tkinter import simpledialog

from playsound import playsound
import keyboard
import re
from playsound import playsound
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pywhatkit as  kit


from engine.helper import extract_yt_term, remove_words

con = sqlite3.connect("Friday.db")
cursor = con.cursor()



@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\www_assets_audio_start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")



def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)







def load_app_associations():
    try:
        with open('engine\\app_associations.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def OpenAppCommand(query):
    loaded_app_associations = load_app_associations()

    query_lower = query.lower()
    if "launch" in query_lower:
        app_to_open = query_lower.split("launch", 1)[-1].strip()
        app_protocol = loaded_app_associations.get(app_to_open, None)

        if app_protocol:
            os.system(f"start {app_protocol}")
            speak(f"{app_to_open.capitalize()} opend...")
        else:
            speak(f"You Dont Have {app_to_open.capitalize()} App ")
            speak(f"Opening Microsoft Store To Install {app_to_open.capitalize()} App")
            # Open the Microsoft Store
            os.system("start ms-windows-store:")
            time.sleep(2)  # Adjust the delay based on your system's speed

            # Simulate search in Microsoft Store
            pyautogui.hotkey('ctrl', 'e')  # Simulate Ctrl + E to focus the search box
            pyautogui.typewrite(app_to_open, interval=0.1)  # Type the app name with a specified interval
            pyautogui.press('enter')  # Press Enter to perform the search
            print(f"Searching for {app_to_open.capitalize()} in Microsoft Store...")
            time.sleep(3)
            speak(f"hover Mouse on {app_to_open.capitalize()} and Click Get Button")
    else:
        print("Launch command not found in input")





def load_settings_associations():
    try:
        with open('engine\\settings_associations.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

settings_data = load_settings_associations()

def process_input(query_lower):
    # Extracting key phrases from user input
    key_phrases = re.findall(r'\b(\w+)\b', query_lower)
    
    # Filtering out common words like 'open' and 'setting'
    ignore_words = ['open', 'setting']
    key_phrases = [word for word in key_phrases if word.lower() not in ignore_words]
    joined_key_phrases = ' '.join(key_phrases)
    clean_keys = re.sub(r"\W+", '', joined_key_phrases)
    
    # Matching remaining words with keys in the JSON data
    matched_keys = []
    for key in settings_data:
        if any(word in key.lower() for word in key_phrases):
            matched_keys.append(key)
    
    # If a match is found, perform the action
    if matched_keys:
        for matched_key in matched_keys:
            protocol = settings_data[matched_key]['protocol']
            print(f"Opening {matched_key} Setting.")
            clean_key = re.sub(r'\W+', '', matched_key)
            speak(f"Opening {clean_key} Setting") 
            os.system(f"start {protocol}")
    else:
        print("No matching settings found.")
        speak(f"Sorry, I Couldn't Find Any Matching Settings For {clean_keys}.")
        speak(f"If You Want To Add This {clean_keys} Setting In My Fuctions  ")
        speak("You Able To Do That In My Settings")








def extract_search_term(command):
    pattern = r'search\s+(.*?)$'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

def search_chrome(query_lower):
    search_term = extract_search_term(query_lower)
    if search_term:
        search_url = f"https://www.google.com/search?q={search_term}"
        clean_query_lower = re.sub(r'\bsearch\b', '', query_lower, flags=re.IGNORECASE)
        clean_query_lower = clean_query_lower.strip()
        speak(f"Ok Searching For {clean_query_lower}")
        os.system(f"start chrome \"{search_url}\"")
    else:
        print("No valid search term found for Chrome")







def process_user_input(query):
    if "play" in query and "serial" in query:
        name_start_index = query.find("play") + len("play")
        name_end_index = query.find("serial")
        serial_name = query[name_start_index:name_end_index].strip()

        print(f"Searching for '{serial_name}' on Disney+ Hotstar")
        driver = webdriver.Chrome()  
        driver.get('https://www.hotstar.com/in/explore')
        driver.maximize_window()

        try:
            search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchBar')))
            search_bar.click()
            search_bar.send_keys(serial_name)
            time.sleep(2)  
            search_bar.send_keys(Keys.RETURN)

            # Try finding the first element, if not found, attempt the alternate one
            try:
                watch_now = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, '_1CSTLo7uotP5mTlp3jKun7')))
                watch_now.click()
            except TimeoutException:
                print("Alternate element will be clicked.")
                alternate_elements = driver.find_elements(By.CLASS_NAME, '_1zc788KtPN0EmaoSx7RUA_._3jpCHAWW0NRsHATyBme6hh.BODY3_MEDIUM')
                for alternate_element in alternate_elements:
                    span_elements = alternate_element.find_elements(By.TAG_NAME, 'span')
                    for span_element in span_elements:
                        span_element.click()
                # You might want to add further actions after clicking the alternate element

            time.sleep(1500)

        except TimeoutException as te:
            print("Timeout occurred:", te)
        except Exception as e:
            print("Error occurred:", e)
        finally:
            driver.quit()
    else:
        print("Input format not recognized. Please use 'play {name} serial' format.")






def simulate_ctrl_f(query):
    # List of words to remove from the query
    words_to_remove = ['find', 'for', 'word']

    # Remove specified words from the query
    for word in words_to_remove:
        query = query.replace(word, '')

    # Simulate pressing Ctrl + F
    keyboard.press_and_release('ctrl+f')
    time.sleep(0.5)  # Adjust the sleep duration if needed

    # Simulate typing the modified query
    keyboard.write(query)

import pyautogui as autogui
import pygetwindow as gw  

def maximize_window(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        if window.isActive:
            return  # The window is already active and should already be maximized
        window.activate()
        autogui.hotkey('winleft', 'up')  # Press Win + Up Arrow to maximize the window
    except IndexError:
        speak(f"Window with title '{window_title}' not found.")


import speech_recognition as sr

def hotword():
    def execute_command():
        autogui.keyDown("win")
        autogui.press("j")
        time.sleep(2)
        autogui.keyUp("win")
        # Alternatively, you can use keyboard module:
        # keyboard.press_and_release('win+j')
        print("Command executed!")

    def detect_hotword(input_text, hotword):
        return hotword.lower() in input_text.lower()

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Processing...")
            input_text = recognizer.recognize_google(audio)
            print("Heard:", input_text)
            if detect_hotword(input_text, "Friday"):
                maximize_window("F.R.I.D.A.Y")   
                execute_command()
                
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    # porcupine=None
    # paud=None
    # audio_stream=None
    # try:
       
    #     # pre trained keywords    
    #     porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
    #     paud=pyaudio.PyAudio()
    #     audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
    #     # loop for streaming
    #     while True:
    #         keyword=audio_stream.read(porcupine.frame_length)
    #         keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

    #         # processing keyword comes from mic 
    #         keyword_index=porcupine.process(keyword)

    #         # checking first keyword detetcted for not
    #         if keyword_index>=0:
    #             print("hotword detected")
    #             maximize_window("F.R.I.D.A.Y")
                

    #             # pressing shorcut key win+j
    #             import pyautogui as autogui
    #             import pygetwindow as gw
    #             autogui.keyDown("win")
    #             autogui.press("j")
    #             time.sleep(2)
    #             autogui.keyUp("win")
    #             # keyboard.press_and_release('win+j')
                
    # except:
    #     if porcupine is not None:
    #         porcupine.delete()
    #     if audio_stream is not None:
    #         audio_stream.close()
    #     if paud is not None:
    #         paud.terminate()


def close_android_studio():
    # Specify the path to studio64.exe
    android_studio_path = r"C:\Program Files\Android\Android Studio\bin\studio64.exe"

    # Construct the command to close Android Studio
    command = f'taskkill /IM {os.path.basename(android_studio_path)} /F'

    # Run the command using os.system
    os.system(command)


def stop():
    keyboard.press_and_release('f4')



################whatapp#########################################

def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('Not Exist In Contacts')
        return 0, 0
    




def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)



def restart_computer():
    try:
        os.system("shutdown /r /t 1")
    except Exception as e:
        print(f"Error: {e}")




def sleep_computer():
    try:
        os.system("powercfg -change -standby-timeout-ac 0")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    except Exception as e:
        print(f"Error: {e}")




import pyautogui
import time

def media_play():
    pyautogui.press('playpause')

# def media_pause():
#     pyautogui.press('playpause')

# def media_skip():
#     pyautogui.press('nexttrack')

def media_stop():
    pyautogui.press('stop')

# Example: Play media
# media_play()

# # Example: Pause media
# time.sleep(2)  # Sleep for 2 seconds before pausing (adjust as needed)
# media_pause()

# # Example: Skip to the next track
# time.sleep(2)  # Sleep for 2 seconds before skipping (adjust as needed)
# media_skip()

# # Example: Stop media playback
# time.sleep(2)  # Sleep for 2 seconds before stopping (adjust as needed)
# media_stop()






import json
import tkinter as tk
from tkinter import Label, Entry, Button

def save_reminder():
    title = title_entry.get()
    time = time_entry.get()

    try:
        with open('reminder.json', 'r') as file:
            reminders = json.load(file)
    except FileNotFoundError:
        reminders = []

    # Add the new reminder
    reminders.append({"title": title, "time": time})

    with open('reminder.json', 'w') as file:
        json.dump(reminders, file, indent=4)

    reminder_window.destroy()

def create_reminder_ui():
    
    global reminder_window, title_entry, time_entry

    # Create the main window
    reminder_window = tk.Tk()
    reminder_window.title("Reminder App")

    # Set the size of the window
    reminder_window.geometry("300x200")  # Width x Height

    # Create and pack widgets
    title_label = Label(reminder_window, text="Title:")
    title_label.pack()

    title_entry = Entry(reminder_window)
    title_entry.pack()

    time_label = Label(reminder_window, text="Time (HH:MM):")
    time_label.pack()

    time_entry = Entry(reminder_window)
    time_entry.pack()

    save_button = Button(reminder_window, text="Save Reminder", command=save_reminder)
    save_button.pack()

    # Run the main loop
    reminder_window.mainloop()



def simulate_typing(query):
    # Execute the first command
    os.system("ollama run mistral")

    # Sleep for 20 seconds (or any desired duration)
    sleep(20)

    # Simulate typing the provided query
    pyautogui.typewrite(query)

@eel.expose
def runnnn():
    os.system("python C:\\Friday\\engine\\Add.py")

@eel.expose
def Register():
    os.system("python C:\\Friday\\capture.py")




import os
import sqlite3

def find_path_by_name(name):
    con = sqlite3.connect("Friday.db")
    cursor = con.cursor()

    # Assuming your table already exists, you should not create it again
    # query = "CREATE TABLE IF NOT EXISTS users_custom_commands (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
    # cursor.execute(query)

    # Check if the name exists in the database
    queryy = "SELECT path FROM users_cuostom_commands WHERE name = ?"
    cursor.execute(queryy, (name,))
    result = cursor.fetchone()

    if result:
        # If the name is found, execute the corresponding path as a Python script
        
        os.system(f"python {result[0]}")
        speak("Command Executed")
    else:
        speak(f"Not found any command with {name} keyword")

    con.close()




import openai

# Set your API key
openai.api_key = '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'  # Replace with your actual API key
def get_gpt_response(message, max_tokens=200):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                  {"role": "user", "content": message}],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


def open_ai(query):

    response = get_gpt_response(query)
    speak(response)




from hugchat import hugchat

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response  = chatbot.chat(user_input)
    speak(response)
    return response



from pynput.keyboard import Key,Controller

from time import sleep

keyboard = Controller()

def volumeup():
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)
def volumedown():
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)



