from pynput import keyboard as kb

def key_translator(string):
    if len(string) == 1:
        return kb.KeyCode(char=string)
    elif len(string) > 1:
        return kb.Key.__members__.get(string, None)

class HotkeyHandler:
    def __init__(self, raw_combos, debug=False):
        self.combos = {tuple((key_translator(k) for k in key)): val for key, val in raw_combos.items()}
        for (key, val) in self.combos.items(): print(f"Loaded combo: {[str(k) for k in key]} for `{val[0].__name__}` with args {val[1: ]}")
        self.logger = lambda s: print(f"  > {s}") if debug else lambda s: None
        self.pressed_keys = list()
        self.void = (lambda: None, )

    def on_press(self, key):
        if key not in self.pressed_keys:
            self.pressed_keys.append(key)

    def on_release(self, key):
        (callback, *args) = self.combos.get(tuple(self.pressed_keys), self.void)
        self.logger(f"Pressed keys {self.pressed_keys}")
        self.logger(f"Running {callback.__name__}{args}")
        if (callback, *args) == self.void:
            self.pressed_keys = []
        elif key in self.pressed_keys:
            self.pressed_keys.remove(key)
        return callback(*args)

    def start(self):
        with kb.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.logger(f"Joining listener {listener} to main thread")
            listener.join()

