import PyATEMMax
from pynput.keyboard import Key, Listener, KeyCode
from pynput import keyboard
import win32gui, win32process, os
import sys, time, threading
from colored import fg

PVW_color = fg('green_1')
PGM_color = fg('red_1')
sColor = fg('white')


cmd = 'mode 25,6' #16,6
os.system(cmd)

atemMini = PyATEMMax.ATEMMax()
atem4K = PyATEMMax.ATEMMax()

def main():
    os.system('cls')
    def connectToAtem():
        i = 0
        while not atem4K.connected and not atemMini.connected and i < 2:
            atemMini.connect("192.168.1.223")
            atemMini.waitForConnection(infinite=False)

            atem4K.connect("192.168.1.221")
            atem4K.waitForConnection(infinite=False)
            i += 1


    def loadingAnimation(process) :
        while process.is_alive():
            chars = ['', '.', '..', '...', '   ']
            for char in chars:
                sys.stdout.write('\r'+'Connecting'+char)
                time.sleep(.2)
                sys.stdout.flush()

    loading_process = threading.Thread(target=connectToAtem)
    loading_process.start()

    loadingAnimation(loading_process)
    loading_process.join()


    pressed = False
    mode = "Praising"

    def on_press(key):
        global mode
        global pressed
        global PVW
        global PGM
        focus_window_pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]
        current_process_pid = os.getppid()

        if focus_window_pid == current_process_pid:
            if key == keyboard.Key.esc:
                atem4K.disconnect()
                atemMini.disconnect()
                os.system("cls")
                print("Disconnected")
                return False  # stop listener
            try:
                k = key.char  # single-char keys
            except:
                k = key.name  # other keys
            if k in ['1', '2', '3', '4'] and k != PVW and k != PGM:  # keys of interest #ATEM4k
                # self.keys.append(k)  # store it in global-like variable
                PVW = k
                os.system('cls')
                print(f"MODE: {mode}\n")
                print(PVW_color, end="")
                print(f"PVW: ", end="")
                print(sColor, end="")
                print(PVW)
                print(PGM_color, end="")
                print(f"PGM: ", end="")
                print(sColor, end="")
                print(PGM)

                kInt = int(k)
                # print(type(kInt))
                atem4K.setPreviewInputVideoSource(1, kInt) # set PVW on Atem4K M/E 2
            if k in ['5', '6', '7', '8'] and k != PVW and k != PGM and mode == "Praising": #ATEMmini
                PVW = k # k
                os.system('cls')
                kInt = int(k)-4
                print(f"MODE: {mode}\n")
                print(PVW_color, end="")
                print(f"PVW: ", end="")
                print(sColor, end="")
                print(PVW)
                print(PGM_color, end="")
                print(f"PGM: ", end="")
                print(sColor, end="")
                print(PGM)

                atemMini.setProgramInputVideoSource(0, kInt) # set PGM on AtemMini M/E 1
                atem4K.setPreviewInputVideoSource(1, 5) # set PVW on Atem4K M/E 2
            while key == keyboard.Key.space and pressed == False: ## and PVW != "-1" and PVW != "0": #CUT
                temp = PGM
                PGM = PVW
                PVW = temp
                os.system('cls')
                print(f"MODE: {mode}\n")
                print(PVW_color, end="")
                print(f"PVW: ", end="")
                print(sColor, end="")
                print(PVW)
                print(PGM_color, end="")
                print(f"PGM: ", end="")
                print(sColor, end="")
                print(PGM)

                print("CUT")
                atem4K.execCutME(1) #Cut on Atem4K M/E 2
                pressed = True
            while key == keyboard.Key.enter and pressed == False: ## and PVW != "0" and PVW != "-1": #FADE
                atem4K.execAutoME(1)
                temp = PGM
                PGM = PVW
                PVW = temp
                os.system('cls')
                print(f"MODE: {mode}\n")
                print(PVW_color, end="")
                print(f"PVW: ", end="")
                print(sColor, end="")
                print(PVW)
                print(PGM_color, end="")
                print(f"PGM: ", end="")
                print(sColor, end="")
                print(PGM)

                print("FADE")
                pressed = True

            if k == 'm' and pressed == False: #Mode selector
                if mode == "Praising":
                    mode = "Preaching"
                else:
                    mode = "Praising"
                os.system('cls')
                print(f"MODE: {mode}\n")
                print(PVW_color, end="")
                print(f"PVW: ", end="")
                print(sColor, end="")
                print(PVW)
                print(PGM_color, end="")
                print(f"PGM: ", end="")
                print(sColor, end="")
                print(PGM)

                pressed = True

            #Fölösleges#
            # if key == Key.page_up: #Preaching mode
            #     mode = "Preaching"
            #     os.system('cls')
            #     print(f"PVW: {PVW}")
            #     print(f"PGM: {PGM}")
            #     print(f"MODE: {mode}")


    PVW = atem4K.previewInput[1].videoSource.value #"-1"
    PGM = atem4K.programInput[1].videoSource.value #"0"

    def on_release(key):  # The function that's called when a key is released
        global pressed
        pressed = False

    def restart():
        import sys
        print("argv was", sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")

        import os
        os.execv(sys.executable, ['python'] + sys.argv)


    def Timeout(key):
        if key == keyboard.Key.esc:
            atem4K.disconnect()
            atemMini.disconnect()
            os.system("cls")
            print("Disconnected")
            quit()
            exit()
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        if k == 'r' and pressed == False:
            #atem4K.disconnect()
            #atemMini.disconnect()
            restart()



    if atem4K.connected and atemMini.connected:
        os.system('cls')
        print(f"MODE: {mode}\n")
        print(PVW_color, end="")
        print(f"PVW: ", end="")
        print(sColor, end="")
        print(PVW)
        print(PGM_color, end="")
        print(f"PGM: ", end="")
        print(sColor, end="")
        print(PGM)
        with Listener(on_press=on_press, on_release=on_release) as listener: listener.join()
    else:
        os.system('cls')
        print("Connection Failed")
        print("Press 'r' to try again.\nor 'Esc' to exit")
        #atem4K.disconnect()
        #atemMini.disconnect()
        with Listener(on_press=Timeout, on_release=on_release) as listener:
            listener.join()



main()



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

