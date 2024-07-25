import tkinter as tk
import keyboard
import os

# Track the state of the keys and mode
quickswitch_enabled = False
key_a_pressed = False
key_d_pressed = False

def on_key_event(e):
    global key_a_pressed, key_d_pressed, quickswitch_enabled

    if quickswitch_enabled:
        if e.name == 'a':
            if e.event_type == 'down':
                key_a_pressed = True
                if key_d_pressed:
                    keyboard.block_key('d')
            elif e.event_type == 'up':
                key_a_pressed = False
                keyboard.unblock_key('d')
        
        if e.name == 'd':
            if e.event_type == 'down':
                key_d_pressed = True
                if key_a_pressed:
                    keyboard.block_key('a')
            elif e.event_type == 'up':
                key_d_pressed = False
                keyboard.unblock_key('a')

def update_status():
    status_label.config(text=f"QuickSwitch Mode {'Enabled' if quickswitch_enabled else 'Disabled'}")

def enable_quickswitch():
    global quickswitch_enabled
    quickswitch_enabled = True
    update_status()

def disable_quickswitch():
    global quickswitch_enabled
    quickswitch_enabled = False
    update_status()

def check_root():
    if os.name != 'nt' and os.geteuid() != 0:
        root.destroy()
        raise PermissionError("This script must be run as root on Linux.")

# Create the GUI
root = tk.Tk()
root.title("QuickSwitch Mode")

status_label = tk.Label(root, text="QuickSwitch Mode Disabled", font=("Times New Roman", 14))
status_label.pack(pady=20)

enable_button = tk.Button(root, text="Enable QuickSwitch", command=enable_quickswitch, font=("Times New Roman", 12))
enable_button.pack(pady=10)

disable_button = tk.Button(root, text="Disable QuickSwitch", command=disable_quickswitch, font=("Times New Roman", 12))
disable_button.pack(pady=10)

# Check for root privileges on Linux
check_root()

# Hook the keyboard events
keyboard.hook(on_key_event)

# Run the GUI event loop
root.mainloop()

# Unhook all keyboard events when the GUI is closed
keyboard.unhook_all()
