from pynput import keyboard, mouse
from time import sleep
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MacroInterface:
    def __init__(self):
        self.input_wait = 0.02
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()
        self.wait = lambda: sleep(self.input_wait)

    def _click(self, button, count=1):
        for _ in range(count):
            self.mouse_controller.click(button)
            self.wait()

    def _press(self, key, count=1):
        for _ in range(count):
            self.keyboard_controller.press(key)
            self.wait()

    def add_highlight(self):
        logger.info("attempting: add_highlight")
        self._click(mouse.Button.right)
        self._press(keyboard.Key.down, 7)
        self._press(keyboard.Key.enter)

    def add_edit_highlight(self):
        logger.info("attempting: add_edit_highlight")
        self.add_highlight()
        self._click(mouse.Button.right)
        self._press(keyboard.Key.down, 6)
        self._press(keyboard.Key.enter)
        self._press(keyboard.Key.down)
        self._press(keyboard.Key.enter)

    def toggle_highlight(self):
        logger.info("attempting: toggle_highlight")
        self._click(mouse.Button.right)
        self._press(keyboard.Key.down, 7)
        self._press(keyboard.Key.enter)
