
# QuickSwitch Mode

QuickSwitch Mode is a Python script that enhances keyboard responsiveness for gaming. It allows for near-instant directional changes. providing a significant advantage in competitive gaming scenarios.

## Features

- **QuickSwitch Mode**: Toggle on/off for fast and responsive directional changes.
- **Customizable Keys**: Easily change the keys used for QuickSwitch.
- **GUI**: Simple GUI to enable/disable QuickSwitch Mode and display the current status.

## Requirements

- Python 3.x
- `pynput` library
- `tkinter` library (included with Python's standard library)

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/).
2. Install the `pynput` library:

```sh
pip install pynput
```

## Usage

1. Clone this repository or download the script.
2. Run the script using Python:

```sh
python quickswitch.py
```

## Script Overview

### Keyboard Listener

The script uses `pynput` to listen for key presses and releases. It toggles QuickSwitch mode when both `Ctrl` and `Shift` are pressed simultaneously.

### GUI with `tkinter`

The GUI provides a simple interface with:
- A status label to display whether QuickSwitch mode is enabled or disabled.
- Buttons to manually enable or disable QuickSwitch mode.

### Customization

- **Custom Keys**: Change the `key1` and `key2` variables to use different keys for QuickSwitch.
- **Toggle Keys**: The script currently uses `Ctrl` and `Shift` to toggle QuickSwitch mode. Modify the `toggle_keys` set if you want to use different keys.

## Code

```python
import tkinter as tk
from pynput import keyboard

# Define the keys for QuickSwitch Mode
key1 = keyboard.KeyCode.from_char('a')
key2 = keyboard.KeyCode.from_char('d')

# Track the state of the keys and mode
key1_pressed = False
key2_pressed = False
quick_switch_enabled = False

# Modifier keys to toggle QuickSwitch Mode
toggle_keys = {keyboard.Key.ctrl, keyboard.Key.shift}
current_keys = set()

def on_press(key):
    global key1_pressed, key2_pressed, quick_switch_enabled

    if key in toggle_keys:
        current_keys.add(key)
        if current_keys == toggle_keys:
            quick_switch_enabled = not quick_switch_enabled
            update_status()

    if quick_switch_enabled:
        if key == key1:
            key1_pressed = True
            key2_pressed = False
            print("Key1 pressed")
        elif key == key2:
            key2_pressed = True
            key1_pressed = False
            print("Key2 pressed")

def on_release(key):
    global key1_pressed, key2_pressed

    if key in toggle_keys:
        current_keys.discard(key)

    if quick_switch_enabled:
        if key == key1:
            key1_pressed = False
        elif key == key2:
            key2_pressed = False

def update_status():
    status_label.config(text=f"QuickSwitch Mode {'Enabled' if quick_switch_enabled else 'Disabled'}")

def enable_quick_switch():
    global quick_switch_enabled
    quick_switch_enabled = True
    update_status()

def disable_quick_switch():
    global quick_switch_enabled
    quick_switch_enabled = False
    update_status()

# Create the GUI
root = tk.Tk()
root.title("QuickSwitch Mode")

status_label = tk.Label(root, text="QuickSwitch Mode Disabled", font=("Times New Roman", 14))
status_label.pack(pady=20)

enable_button = tk.Button(root, text="Enable QuickSwitch", command=enable_quick_switch, font=("Times New Roman", 12))
enable_button.pack(pady=10)

disable_button = tk.Button(root, text="Disable QuickSwitch", command=disable_quick_switch, font=("Times New Roman", 12))
disable_button.pack(pady=10)

# Start the keyboard listener in a separate thread
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Run the GUI event loop
root.mainloop()

# Stop the keyboard listener when the GUI is closed
listener.stop()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Razer's Snap Tap feature for gaming keyboards.
