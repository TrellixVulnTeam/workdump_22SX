from text_interface import TextInferface
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
        self.text_interface = TextInferface()
        self.tts = TTS()
        self.is_active = False

    def _on_activate(self):
        if not self.is_active:
            logger.info('on_activate')
            self.is_active = True
            text = self.text_interface.retrieve_text()
            self.tts.speak(text)
            # Note: you need manually deactivate due to a pyttsx3 bug
            self.is_active = False

    def _on_deactivate(self):
        if self.is_active:
            logger.info('on_deactivate')
            self.tts.stop()
            self.is_active = False

    def start(self):
        logger.info("Starting TTSUtil...")
        hotkeys = {
            self.activate_hotkey: self._on_activate,
            self.deactivate_hotkey: self._on_deactivate,
        }
        with keyboard.GlobalHotKeys(hotkeys) as t:
            t.join()


if __name__ == '__main__':
    tts_util = TTSUtil()
    tts_util.start()
