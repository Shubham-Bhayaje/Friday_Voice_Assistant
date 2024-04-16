from plyer import notification
import time
import json
import pyttsx3

def read_reminders_from_json():
    with open("C:\\Friday\\reminder.json", "r") as file:
        reminders = json.load(file)
    return reminders

def set_reminder(title, time_str):
    try:
        reminder_time = time.strptime(time_str, "%H:%M")
    except ValueError:
        print("Invalid time format. Please use HH:MM.")
        return

    while True:
        current_time = time.localtime()
        if current_time.tm_hour == reminder_time.tm_hour and current_time.tm_min == reminder_time.tm_min:
            notify(title)
            break
        time.sleep(60)  # Check every minute

def notify(title):
    notification.notify(
        title=title,
        message="REMINDER",
        timeout=10
    )
    
    speak_message("Sir, you have a reminder.")
    time.sleep(1)  # 2 seconds delay
    speak_message(title)

def speak_message(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

if __name__ == "__main__":
    reminders = read_reminders_from_json()

    for reminder in reminders:
        title = reminder.get("title", "")
        time_str = reminder.get("time", "")
        set_reminder(title, time_str)
