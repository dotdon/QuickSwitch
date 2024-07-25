import tkinter as tk
from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq
import threading

# Track the state of the keys and mode
quickswitch_enabled = False
key_a_pressed = False
key_d_pressed = False

# X11 display and context
local_dpy = display.Display()
record_dpy = display.Display()

def lookup_keysym(keysym):
    return XK.keysym_to_string(keysym)

def key_press_handler(event):
    global key_a_pressed, key_d_pressed, quickswitch_enabled

    if event.type == X.KeyPress:
        keysym = local_dpy.keycode_to_keysym(event.detail, 0)
        key = lookup_keysym(keysym)

        if quickswitch_enabled:
            if key == 'a':
                key_a_pressed = True
                key_d_pressed = False
                print("Key 'a' pressed")
            elif key == 'd':
                key_d_pressed = True
                key_a_pressed = False
                print("Key 'd' pressed")

def key_release_handler(event):
    global key_a_pressed, key_d_pressed

    if event.type == X.KeyRelease:
        keysym = local_dpy.keycode_to_keysym(event.detail, 0)
        key = lookup_keysym(keysym)

        if quickswitch_enabled:
            if key == 'a':
                key_a_pressed = False
                print("Key 'a' released")
            elif key == 'd':
                key_d_pressed = False
                print("Key 'd' released")

def record_callback(reply):
    if reply.category != record.FromServer:
        return
    if reply.client_swapped:
        return
    if not len(reply.data) or reply.data[0] < 2:
        return

    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)
        if event.type == X.KeyPress:
            key_press_handler(event)
        elif event.type == X.KeyRelease:
            key_release_handler(event)

def enable_quickswitch():
    global quickswitch_enabled
    quickswitch_enabled = True
    update_status()

def disable_quickswitch():
    global quickswitch_enabled
    quickswitch_enabled = False
    update_status()

def update_status():
    status_label.config(text=f"QuickSwitch Mode {'Enabled' if quickswitch_enabled else 'Disabled'}")

def create_record_context():
    ctx = record_dpy.record_create_context(
        0,
        [record.AllClients],
        [{
            'core_requests': (0, 0),
            'core_replies': (0, 0),
            'ext_requests': (0, 0, 0, 0),
            'ext_replies': (0, 0, 0, 0),
            'delivered_events': (0, 0),
            'device_events': (X.KeyPress, X.KeyRelease),
            'errors': (0, 0),
            'client_started': False,
            'client_died': False,
        }]
    )
    return ctx

def listen_to_events():
    ctx = create_record_context()
    record_dpy.record_enable_context(ctx, record_callback)
    record_dpy.record_free_context(ctx)

# Create the GUI
root = tk.Tk()
root.title("QuickSwitch Mode")

status_label = tk.Label(root, text="QuickSwitch Mode Disabled", font=("Times New Roman", 14))
status_label.pack(pady=20)

enable_button = tk.Button(root, text="Enable QuickSwitch", command=enable_quickswitch, font=("Times New Roman", 12))
enable_button.pack(pady=10)

disable_button = tk.Button(root, text="Disable QuickSwitch", command=disable_quickswitch, font=("Times New Roman", 12))
disable_button.pack(pady=10)

# Start listening to the input events in a separate thread
event_listener_thread = threading.Thread(target=listen_to_events, daemon=True)
event_listener_thread.start()

# Run the GUI event loop
root.mainloop()
