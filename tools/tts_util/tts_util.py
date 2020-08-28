import pyttsx3
import keyboard
import pyperclip
import os
import time
if os.name == 'posix':
    mouse = lambda: print("Placeholder")
    mouse.click = lambda: print("Dummy click")
else:
    import mouse

start_key = "ctrl+`"
stop_key = "esc"
copy_key = "ctrl+c"
copy_wait = 0.1
rate_factor = 1.20
volume_factor = 5
pattern_replacements = [
    ("\r", ""),
    ("\n", " "),
    ("  ", " "),
    ("∈", "in"),
    ("=", "equals"),
    ("⊂", "proper subset"),
    ("⊆", "subset"),
    ("∩", "intersect"),
    ("∪", "union"),
]

def copy():
    keyboard.press_and_release(copy_key)
    time.sleep(copy_wait)
    contents = pyperclip.paste()
    mouse.click()  # to clear selected region
    return contents

def clean(text):
    for (pattern, replacement) in pattern_replacements:
        text = text.replace(pattern, replacement)
    return text

def speak(text):
    engine = pyttsx3.init()
    scaled_rate = engine.getProperty('rate') * rate_factor
    engine.setProperty('rate', scaled_rate)
    scaled_volume = engine.getProperty('volume') * volume_factor
    engine.setProperty('volume', scaled_volume)
    def onWord(name, location, length):
        # print(f"onWord: {name} | {location} | {length}")
        if keyboard.is_pressed(stop_key):
            engine.stop()
    engine.connect('started-word', onWord)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    del engine

def speak_selected(hotkeys):
    for hotkey in hotkeys.split("+"):
        keyboard.release(hotkey)
    raw_message = copy()
    message = clean(raw_message)
    print(f"Detected: =====\n\n{raw_message}\n\n===============\n\n")
    print(f"Speaking: =====\n\n{message}\n\n===============\n\n")
    speak(message)

def display_vars():
    print("Variables:")
    for (_name, _obj) in globals().items():
        if type(_obj) not in [str, float, int, bool, list] or _name.startswith("_"):
            continue
        print(f"{_name}: {_obj}")

if __name__ == '__main__':
    display_vars()
    keyboard.add_hotkey(start_key, speak_selected, args=[start_key])
    keyboard.wait()
