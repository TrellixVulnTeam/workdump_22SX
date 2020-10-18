from pynput import keyboard, mouse
import pyperclip
import logging
import time
import os

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TextInferface:
    def __init__(self):
        self.pattern_replacements = [
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
        self.copy_hotkey = "<cmd>+c" if os.name == 'posix' else "<ctrl>+c"
        self.copy_wait = 0.10
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()

    def _copy_selected(self):
        for key in keyboard.HotKey.parse(self.copy_hotkey):
            self.keyboard_controller.press(key)
        for key in keyboard.HotKey.parse(self.copy_hotkey):
            self.keyboard_controller.release(key)
        time.sleep(self.copy_wait)
        contents = pyperclip.paste()
        self.mouse_controller.click(mouse.Button.left)
        logger.info(f"Copied text: {contents}")
        return contents

    def _process_text(self, content):
        for (pattern, replacement) in self.pattern_replacements:
            content = content.replace(pattern, replacement)
        logger.info(f"Processed text: {content}")
        return content

    def retrieve_text(self):
        content = self._copy_selected()
        text = self._process_text(content)
        return text
