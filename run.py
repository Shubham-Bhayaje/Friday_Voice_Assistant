# To run Jarvis
import threading
from time import sleep
import os

def startJarvis():
    # Code for thread 1
    print("Thread 1 is running.")
    from main import start
    start()

def listenHotword():
    # Code for thread 2
    print("Thread 2 is running.")
    from engine.features import hotword
    hotword()
    

def reminder():
    print("Thread 3 is running.")
    os.system("reminder.py")



if __name__ == '__main__':
    t1 = threading.Thread(target=startJarvis)
    t2 = threading.Thread(target=listenHotword)
    t3 = threading.Thread(target=reminder)
    
    t1.start()
    sleep(1)  # Add a short delay to ensure both threads start properly
    t2.start() 
    sleep(1)
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("System stop")
