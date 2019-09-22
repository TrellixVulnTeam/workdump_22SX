from time import sleep
import os, sys

import pyautogui as pg
from pynput import keyboard as kb

from hotkey_handler import HotkeyHandler

# https://pyautogui.readthedocs.io/en/latest/install.html#

def stop():
    print("Sending stop signal to listener")
    return False

def show_px(duration):
    for _ in range(duration):
        sleep(1)
        print(pg.position())

def find_all(c1, c2, s):
    pg.hotkey('ctrl', 'f')
    pg.typewrite(s)
    pg.click(*c1)
    pg.click(*c2)


if __name__ == '__main__':
    combos = {
        (kb.Key.esc, ): (stop, ),
        (kb.Key.ctrl_l, kb.KeyCode(char='0')): (show_px, 5),
        (kb.Key.ctrl_l, kb.KeyCode(char='1')): (find_all, (207, 975), (1813, 982), "$"),
    }
    for (key, val) in combos.items():
        print(f"Loaded combo: {[str(k) for k in key]} for `{val[0].__name__}` with args {val[1: ]}")
    hotkey_handler = HotkeyHandler(combos, debug=False)
    hotkey_handler.start()
    input("Press [Enter] to restart and [Ctrl+C] to stop")
    os.execl(sys.executable, sys.executable, *sys.argv)
