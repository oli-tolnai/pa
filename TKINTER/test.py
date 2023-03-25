import tkinter as tk
from pynput import keyboard

# Create a Tkinter window
root = tk.Tk()
root.title("Keyboard Listener")
root.geometry("300x50")

# Create a label widget to display the pressed key
key_label = tk.Label(root, text="Press a key...")
key_label.pack(padx=10, pady=10)

# Define a function to update the label with the pressed key
def on_press(key):
    try:
        key_label.config(text=f"Key pressed: {key.char}")
    except AttributeError:
        key_label.config(text=f"Key pressed: {key.name}")

# Define functions to create and destroy the keyboard listener
def create_listener():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

def destroy_listener():
    listener.stop()

# Bind the listener creation and destruction to window events
root.bind("<FocusIn>", lambda event: create_listener())
root.bind("<FocusOut>", lambda event: destroy_listener())

# Start the Tkinter event loop
root.mainloop()
