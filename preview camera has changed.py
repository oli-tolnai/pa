import PyATEMMax
from pynput.keyboard import Key, Listener, KeyCode
from pynput import keyboard
import win32gui, win32process, os
import sys, time, threading
from colored import fg



atemMini = PyATEMMax.ATEMMax()
atem4K = PyATEMMax.ATEMMax()

PGM = atem4K.previewInput[1].videoSource.value
PVW = atem4K.previewInput[1].videoSource.value

def setPGMandPVWtoCurrent():
    global PGM
    global PVW
    if PVW == 5:
        PVW = atem4K.previewInput[1].videoSource.value + atemMini.programInput[1].videoSource.value
    if PGM == 5:
        PGM = atem4K.programInput[1].videoSource.value + atemMini.programInput[1].videoSource.value

setPGMandPVWtoCurrent()

stop_flag = False
def PGM_and_PVW_has_chaned():
    global PVW
    global PGM
    while not stop_flag:
        last_PGM = atem4K.previewInput[1].videoSource.value
        last_PVW = atem4K.previewInput[1].videoSource.value

        # if last_PGM != PGM:
        #     PGM = last_PGM
        #     setPGMandPVWtoCurrent()
        # if last_PVW != PVW:
        #     PVW = last_PVW
        #     setPGMandPVWtoCurrent()

        if last_PVW != PVW or last_PGM != PGM:
            PVW = last_PVW
            PGM = last_PGM
            setPGMandPVWtoCurrent()
            #consoleText()

        print(11111)
        time.sleep(0.01)


PGM_PVW_Listener = threading.Thread(target=PGM_and_PVW_has_chaned)
PGM_PVW_Listener.start()


for i in range(100):
    print(99999)
    time.sleep(0.01)


stop_flag = True
#PGM_PVW_Listener.join()