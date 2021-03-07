from Macro import Macro
from pynput import keyboard, mouse
from time import sleep
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class InputMacro(Macro):
    def __init__(self):
        self.toggle_highlight_hotkey = "<shift>+!"
        self.add_edit_highlight_hotkey = "<shift>+@"
        self.input_wait = 0.01
        self.load_wait = 0.5
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()

    @property
    def hotkeys(self):
        return {
            self.toggle_highlight_hotkey: self.toggle_highlight,
            self.add_edit_highlight_hotkey: self.add_edit_highlight,
        }

    def _clear_hotkey(self, hotkey):
        keys = keyboard.HotKey.parse(hotkey)
        for key in keys:
            self.keyboard_controller.release(key)

    def _wait(self, duration=None):
        duration = self.input_wait if duration is None else duration
        sleep(duration)

    def _click(self, button, count=1):
        for _ in range(count):
            self.mouse_controller.click(button)
            self._wait()

    def _press(self, key, count=1):
        for _ in range(count):
            self.keyboard_controller.press(key)
            self._wait()

    def _edit_highlight(self):
        self._click(mouse.Button.right)
        self._press(keyboard.Key.down, 8)
        self._press(keyboard.Key.enter)
        self._press(keyboard.Key.down)
        self._press(keyboard.Key.enter)

    def toggle_highlight(self):
        logger.info("attempting: toggle_highlight")
        self._click(mouse.Button.right)
        self._press(keyboard.Key.down, 9)
        self._press(keyboard.Key.enter)
        self._clear_hotkey(self.toggle_highlight_hotkey)

    def add_edit_highlight(self):
        logger.info("attempting: add_edit_highlight")
        self.toggle_highlight()
        self._wait(self.load_wait)
        self._edit_highlight()
        self._clear_hotkey(self.add_edit_highlight_hotkey)
