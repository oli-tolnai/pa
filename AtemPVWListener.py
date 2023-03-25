import PyATEMMax
from pynput.keyboard import Key, Listener, KeyCode
from pynput import keyboard
import win32gui, win32process, os
import sys, time, threading
from colored import fg

def jani():
    global name
    name = "jani"
    while True:
        if name == "jani":
            name = "pista"
            time.sleep(.01)
            name = "jani"
            time.sleep(2)
        print(name)

def pista(process):
    while process.is_alive():
        if name == "pista":
            print("Csá")
            time.sleep(.01)

loading_process = threading.Thread(target=jani)
loading_process.start()

pista(loading_process)
loading_process.join()