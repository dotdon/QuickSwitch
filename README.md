# QuickSwitch Mode

QuickSwitch Mode is a Python script that enhances keyboard responsiveness for gaming. It allows for near-instant directional changes without needing to lift the initial key pressed, providing a significant advantage in competitive gaming scenarios. Specifically, it prevents both 'a' and 'd' keys from being pressed simultaneously.

## Features

- **QuickSwitch Mode**: Toggle on/off for fast and responsive directional changes.
- **Customizable Keys**: Easily change the keys used for QuickSwitch.
- **GUI**: Simple GUI to enable/disable QuickSwitch Mode and display the current status.

## Requirements

- Python 3.x
- `pynput` library
- `tkinter` library (included with Python's standard library)
- `keyboard` library

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/).
2. Install the required libraries:

```sh
pip install pynput keyboard
```

## Usage

1. Clone this repository or download the script.
2. Run the script using Python:

```sh
python quickswitch.py
```

## Script Overview

### Keyboard Listener

The script uses `pynput` and `keyboard` to listen for key presses and releases. It toggles QuickSwitch mode when both `Ctrl` and `Shift` are pressed simultaneously.

### GUI with `tkinter`

The GUI provides a simple interface with:
- A status label to display whether QuickSwitch mode is enabled or disabled.
- Buttons to manually enable or disable QuickSwitch mode.

### Customization

- **Custom Keys**: Change the `key_a` and `key_d` variables to use different keys for QuickSwitch.
- **Toggle Keys**: The script currently uses `Ctrl` and `Shift` to toggle QuickSwitch mode. Modify the `toggle_keys` set if you want to use different keys.

## Code

```python
import tkinter as tk
import keyboard

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

# Create the GUI
root = tk.Tk()
root.title("QuickSwitch Mode")

status_label = tk.Label(root, text="QuickSwitch Mode Disabled", font=("Times New Roman", 14))
status_label.pack(pady=20)

enable_button = tk.Button(root, text="Enable QuickSwitch", command=enable_quickswitch, font=("Times New Roman", 12))
enable_button.pack(pady=10)

disable_button = tk.Button(root, text="Disable QuickSwitch", command=disable_quickswitch, font=("Times New Roman", 12))
disable_button.pack(pady=10)

# Hook the keyboard events
keyboard.hook(on_key_event)

# Run the GUI event loop
root.mainloop()

# Unhook all keyboard events when the GUI is closed
keyboard.unhook_all()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the concept of "Nullbind" behavior for gaming keyboards.
