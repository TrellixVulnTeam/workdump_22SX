import pyttsx3
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TTS:
    def __init__(self):
        self.rate_factor = 1.20
        self.engine = pyttsx3.init()
        self._set_rate()

    def _set_rate(self):
        rate = self.engine.getProperty('rate')
        scaled_rate = rate * self.rate_factor
        self.engine.setProperty('rate', scaled_rate)

    def stop(self):
        logger.info("Stopping engine...")
        self.engine.endLoop()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        logger.info("Finished speaking.")
