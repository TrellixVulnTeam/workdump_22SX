#!/usr/bin/env python3
import os, sys

import pyautogui as pg
from pynput import keyboard as kb
from hotkey_handler import HotkeyHandler


def restart():
    print("Restarting script...")
    os.execl(sys.executable, sys.executable, *sys.argv)

def stop():
    print("Sending stop signal to listener...")
    return False

def show_px():
    print(pg.position())

def find_all(clear_keys, c1, s, buffer=0.5):
    for k in clear_keys: pg.keyUp(k)
    pg.keyDown('shift')
    pg.click(interval=buffer)
    pg.keyUp('shift')
    pg.hotkey('ctrl', 'f')
    pg.typewrite(s, interval=buffer)
    pg.click(*c1, interval=buffer)
    pg.hotkey('alt', 'enter')


if __name__ == '__main__':
    combos = {
        ('shift', 'f12'): (restart, ),
        ('shift', 'f10'): (stop, ),
        ('shift', 'f9'): (show_px, ),
        ('shift', 'f4'): (find_all, ('shift', 'f4'), (199, 973), "\\$"),
        ('shift', 'f2'): (find_all, ('shift', 'f2'), (167, 876), "\\$"),  # office
        ('shift', 'f1'): (find_all, ('shift', 'f1'), (164, 876), "\\$"),
    }
    hotkey_handler = HotkeyHandler(combos, debug=False)
    hotkey_handler.start()
