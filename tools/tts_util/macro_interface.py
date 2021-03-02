from pynput import keyboard, mouse
from time import sleep
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MacroInterface:
    def __init__(self):
        self.input_wait = 0.01
        self.load_wait = 0.5
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()


    def wait(self, duration=None):
        duration = self.input_wait if duration is None else duration
        sleep(duration)

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

    def edit_highlight(self):
        logger.info("attempting: edit_highlight")
        self._click(mouse.Button.right)
        self._press(keyboard.Key.down, 6)
        self._press(keyboard.Key.enter)
        self._press(keyboard.Key.down)
        self._press(keyboard.Key.enter)

    def add_edit_highlight(self):
        logger.info("attempting: add_edit_highlight")
        self.add_highlight()
        self.wait(self.load_wait)
        self.edit_highlight()

    def toggle_highlight(self):
        logger.info("attempting: toggle_highlight")
        self._click(mouse.Button.right)
        self._press(keyboard.Key.down, 7)
        self._press(keyboard.Key.enter)
