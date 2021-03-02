from text_interface import TextInferface
from macro_interface import MacroInterface
from tts import TTS
from pynput import keyboard
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TTSUtil:
    def __init__(self):
        self.activate_hotkey = "`"
        self.deactivate_hotkey = "<esc>"
        self.toggle_highlight_hotkey = "<ctrl>+<f1>"
        self.add_edit_highlight_hotkey = "<ctrl>+<f2>"
        self.text_interface = TextInferface()
        self.macro_interface = MacroInterface()
        self.tts = TTS()
        self.is_active = False

    def _on_activate(self):
        logger.info('attempting: _on_activate')
        if not self.is_active:
            logger.info('executing: _on_activate')
            self.is_active = True
            text = self.text_interface.retrieve_text()
            self.tts.speak(text)
            # Note: you need manually deactivate due to a pyttsx3 bug
            # self.is_active = False

    def _on_deactivate(self):
        logger.info('attempting: _on_deactivate')
        if self.is_active:
            logger.info('executing: _on_deactivate')
            self.tts.stop()
            self.is_active = False

    def start(self):
        logger.info("Starting TTSUtil...")
        hotkeys = {
            self.activate_hotkey: self._on_activate,
            self.deactivate_hotkey: self._on_deactivate,
            self.toggle_highlight_hotkey: self.macro_interface.toggle_highlight,
            self.add_edit_highlight_hotkey: self.macro_interface.add_edit_highlight,
        }
        with keyboard.GlobalHotKeys(hotkeys) as t:
            t.join()


if __name__ == '__main__':
    tts_util = TTSUtil()
    tts_util.start()
