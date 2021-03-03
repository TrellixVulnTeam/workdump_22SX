from InputMacro import InputMacro
from TTSMacro import TTSMacro
from pynput import keyboard
import json
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def start():
    input_macro = InputMacro()
    tts_macro = TTSMacro()
    hotkeys = {
        **input_macro.hotkeys,
        **tts_macro.hotkeys,
    }
    hotkey_dict = {hk: fnc.__qualname__ for (hk, fnc) in hotkeys.items()}
    print("hotkeys:\n{}".format(json.dumps(hotkey_dict, indent=4)))
    with keyboard.GlobalHotKeys(hotkeys) as t:
        logger.info("Started tts_util.")
        t.join()


if __name__ == '__main__':
    start()
