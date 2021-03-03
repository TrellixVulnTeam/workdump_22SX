from pynput import keyboard, mouse
import pyperclip
import logging
import time

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TextInferface:
    def __init__(self):
        self.pattern_replacements = [
            ("-\n", ""),
            ("\r", ""),
            ("\n", " "),
            ("  ", " "),
            ("∈", "in"),
            ("=", "equals"),
            ("⊂", "subset"),
            ("⊆", "subset"),
            ("∩", "intersect"),
            ("∪", "union"),
        ]
        self.copy_hotkeys = ["<cmd>+c", "<ctrl>+c"]
        self.copy_wait = 0.10
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()

    def _input_hotkey(self, hotkey):
        for key in keyboard.HotKey.parse(hotkey):
            self.keyboard_controller.press(key)
        for key in keyboard.HotKey.parse(hotkey):
            self.keyboard_controller.release(key)

    def _copy_selected(self):
        for copy_hotkey in self.copy_hotkeys:
            self._input_hotkey(copy_hotkey)
        time.sleep(self.copy_wait)
        contents = pyperclip.paste()
        self.mouse_controller.click(mouse.Button.left)
        logger.info(f"Copied text: {contents}")
        return contents

    def _process_text(self, content):
        if content is None:
            return "None"
        for (pattern, replacement) in self.pattern_replacements:
            content = content.replace(pattern, replacement)
        logger.info(f"Processed text: {content}")
        return content

    def retrieve_text(self):
        content = self._copy_selected()
        text = self._process_text(content)
        return text
