import PyATEMMax
from pynput.keyboard import Key, Listener, KeyCode
from pynput import keyboard
import win32gui, win32process, os
import sys, time, threading
from colored import fg

PVW_color = fg('green_1')
PGM_color = fg('red_1')
sColor = fg('white')

cmd = 'mode 19,7'
os.system(cmd)

atemMini = PyATEMMax.ATEMMax()
atem4K = PyATEMMax.ATEMMax()

import tkinter as tk
from tkinter import messagebox


def exit_application():
    msg_box = tk.messagebox.askquestion('Exit', 'Are you sure you want to exit?',
                                        icon='question')
    if msg_box == 'yes':
        atem4K.disconnect()
        atemMini.disconnect()
        os.system("cls")
        print("Disconnected")
        exit()
        quit()
        return False  # stop listener
    # else:
    #     tk.messagebox.showinfo('Return', 'You will now return to the application screen')


def restart_application():
    global stop_flag
    msg_box = tk.messagebox.askquestion('Restart', 'Are you sure you want to restart the application?',
                                        icon='question')
    if msg_box == 'yes':
        stop_flag = True
        atem4K.disconnect()
        atemMini.disconnect()
        os.startfile(__file__)
        quit()
        # os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
    # else:
    #     atem4K.disconnect()
    #     atemMini.disconnect()
    #     os.system("cls")
    #     print("Disconnected")
    #     exit()
    #     quit()
    #     return False  # stop listener


def connectionFailed(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'r':  # restart_application
        restart_application()
        # os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
    if key == keyboard.Key.esc:
        exit_application()


def connectToAtem():
    i = 0
    while not atem4K.connected and not atemMini.connected and i < 1:
        atemMini.connect("192.168.1.223")
        atemMini.waitForConnection(infinite=False)

        atem4K.connect("192.168.1.221")
        atem4K.waitForConnection(infinite=False)
        i += 1


def loadingAnimation(process):
    while process.is_alive():
        chars = ['', '.', '..', '...', '   ']
        for char in chars:
            sys.stdout.write('\r' + 'Connecting' + char)
            time.sleep(.2)
            sys.stdout.flush()


loading_process = threading.Thread(target=connectToAtem)
loading_process.start()

loadingAnimation(loading_process)
loading_process.join()

pressed = False
mode = "8 CAMS"
sugo = "OpenLP"  # OpenLP / M/E 1 PGM #atem4K.auxSource[2].input.value


def consoleText():
    os.system('cls')
    print(f"SÚGÓ: {sugo}")
    print(f"MODE: {mode}")
    print("\n"+PVW_color, end="")
    print(f"PVW: ", end="")
    print(sColor, end="")
    print(f"{PVW}")
    print(PGM_color, end="")
    print(f"PGM: ", end="")
    print(sColor, end="")
    print(f"{PGM}")



def setPGMandPVWtoCurrent():
    global PGM
    global PVW
    # if PVW == 5:
    #     PVW = atem4K.previewInput[1].videoSource.value + atemMini.programInput[1].videoSource.value
    # if PGM == 5:
    #     PGM = atem4K.programInput[1].videoSource.value + atemMini.programInput[1].videoSource.value

stop_flag = False
def PGM_and_PVW_has_chaned():
    global PVW
    global PGM
    while not stop_flag:
        last_PGM = atem4K.programInput[1].videoSource.value
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
            consoleText()

        #print(11111)
        time.sleep(0.01)

PGM_PVW_Listener = threading.Thread(target=PGM_and_PVW_has_chaned)


def on_press(key):
    global stop_flag
    global mode
    global sugo
    global pressed
    global PVW
    global PGM
    focus_window_pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]
    current_process_pid = os.getppid()

    if focus_window_pid == current_process_pid:
        if key == keyboard.Key.esc:
            stop_flag = True
            exit_application()
            # atem4K.disconnect()
            # atemMini.disconnect()
            # os.system("cls")
            # print("Disconnected")
            # return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        if k in ['1', '2', '3', '4'] and k != PVW and k != PGM and pressed == False:  # keys of interest #ATEM4k
            # self.keys.append(k)  # store it in global-like variable
            pressed = True
            kInt = int(k)
            # print(type(kInt))
            atem4K.setPreviewInputVideoSource(1, kInt)  # set PVW on Atem4K M/E 2

            PVW = k
            #PVW = atem4K.previewInput[1].videoSource.value  # k
            consoleText()

        if k in ['5', '6', '7', '8'] and k != PVW and k != PGM and mode == "8 CAMS" and pressed == False:  # ATEMmini

            pressed = True
            kInt = int(k) - 4
            atemMini.setProgramInputVideoSource(0, kInt)  # set PGM on AtemMini M/E 1
            atem4K.setPreviewInputVideoSource(1, 5)  # set PVW on Atem4K M/E 2

            PVW = k

            #PVW = atemMini.previewInput[1].videoSource.value + 4  # k
            consoleText()

        while key == keyboard.Key.space and pressed == False:  ## and PVW != "-1" and PVW != "0": #CUT
            atem4K.execCutME(1)  # Cut on Atem4K M/E 2

            #temp = PGM
            #PGM = PVW
            #PVW = temp

            PGM = atem4K.programInput[1].videoSource.value
            PVW = atem4K.previewInput[1].videoSource.value

            consoleText()


            print("CUT")
            pressed = True
        while key == keyboard.Key.enter and pressed == False:  ## and PVW != "0" and PVW != "-1": #FADE
            atem4K.execAutoME(1)

            # temp = PGM
            # PGM = PVW
            # PVW = temp

            PGM = atem4K.programInput[1].videoSource.value
            PVW = atem4K.previewInput[1].videoSource.value  # "-1" #temp

            consoleText()


            print("FADE")
            pressed = True

        #Mode selector
        if k == 'm' and pressed == False:  # key == Key.page_up and pressed == False:
            if mode == "8 CAMS":
                mode = "4 CAMS"
            else:
                mode = "8 CAMS"

            consoleText()


            pressed = True

        # Súgó
        if key == Key.home and pressed == False:  # k == "s" and pressed == False:
            if sugo == "OpenLP":  # and mode == "Prédikáció":
                sugo = "M/E 1 PGM"
                atem4K.setAuxSourceInput(1, "mE1Prog")
            elif sugo == "M/E 1 PGM":
                sugo = "OpenLP"
                atem4K.setAuxSourceInput(1, "mE3Prog")

            consoleText()


            pressed = True

        if k == 'r':  # restart_application
            restart_application()

        # Fölösleges#
        # if key == Key.page_up: #Preaching mode
        #     mode = "Preaching"
        #     os.system('cls')
        #     print(f"PVW: {PVW}")
        #     print(f"PGM: {PGM}")
        #     print(f"MODE: {mode}")


PVW = atem4K.previewInput[1].videoSource.value  # "-1"
PGM = atem4K.programInput[1].videoSource.value  # "0"


def on_release(key):  # The function that's called when a key is released
    global pressed
    pressed = False


if atem4K.connected or atemMini.connected:
    consoleText()
    PGM_PVW_Listener.start()
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
else:
    os.system('cls')
    print("Connection Failed")
    import ctypes  # An included library with Python install.

    # atem4K.disconnect()
    # atemMini.disconnect()
    # ctypes.windll.user32.MessageBoxW(0, "Failed to connect to Atem", "ERROR", 5)
    with Listener(on_press=connectionFailed, on_release=on_release) as listener:
        listener.join()
    # failedConnectRetry()


# Original
# print(f"MODE: {mode}\n")
# print(f"PVW: {PVW}")
# print(f"PGM: {PGM}")

# listener = keyboard.Listener(on_press=on_press)
# listener.start()  # start to listen on a separate thread
# listener.join()  # remove if main thread is polling self.keys

# Collect events until released
# with Listener(on_press=on_press) as listener:listener.join()

# 1 2 3 4 5 6 7 8 Keys
# 1 2 3 4 5 5 5 5 Atem4K PVW
# x x x x 1 2 3 4 AtemMini PGM
