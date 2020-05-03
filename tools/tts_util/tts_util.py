import pyttsx3
import keyboard
import mouse
import pyperclip

import time

start_key = "ctrl+`"
stop_key = "esc"
copy_key = "ctrl+c"
copy_wait = 0.1
rate_factor = 1.25
volume_factor = 5

def copy():
    keyboard.press_and_release(copy_key)
    time.sleep(copy_wait)
    contents = pyperclip.paste()
    mouse.click()  # to clear selected region
    return contents

def clean(text):
    cleaned_text = text.replace("\r", "").replace("\n", " ").replace("  ", " ")
    return cleaned_text

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
    print(f"Speaking: =====\n\n{message}\n\n===============\n\n")
    speak(message)

def display_vars():
    print("Variables:")
    for (_name, _obj) in globals().items():
        if type(_obj) not in [str, float, int, bool] or _name.startswith("_"):
            continue
        print(f"{_name}: {_obj}")

if __name__ == '__main__':
    display_vars()
    keyboard.add_hotkey(start_key, speak_selected, args=[start_key])
    keyboard.wait()
