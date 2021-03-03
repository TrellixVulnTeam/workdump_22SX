from Macro import Macro
from TextInterface import TextInferface
import pyttsx3
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TTSMacro(Macro):
    def __init__(self):
        self.speak_hotkey = "`"
        self.stop_speaking_hotkey = "<esc>"
        self.rate_factor = 1.33
        self.engine = pyttsx3.init()
        self._set_rate()
        self.is_speaking = False
        self.text_interface = TextInferface()

    @property
    def hotkeys(self):
        return {
            self.speak_hotkey: self.speak,
            self.stop_speaking_hotkey: self.stop_speaking,
        }

    def _set_rate(self):
        rate = self.engine.getProperty('rate')
        scaled_rate = rate * self.rate_factor
        self.engine.setProperty('rate', scaled_rate)

    def stop_speaking(self):
        logger.info("Running: stop_speaking.")
        if self.is_speaking:
            logger.info("Stop speaking...")
            self.engine.endLoop()
            self.is_speaking = False

    def speak(self):
        logger.info("Running: speak.")
        if not self.is_speaking:
            logger.info("Speaking...")
            self.is_speaking = True
            text = self.text_interface.retrieve_text()
            # Note: you need manually deactivate due to a pyttsx3 bug
            # self.is_speaking = False
            self.engine.say(text)
            self.engine.runAndWait()
