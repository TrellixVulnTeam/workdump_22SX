from pynput import keyboard as kb

class HotkeyHandler:
    def __init__(self, combos, debug=False):
        self.pressed_keys = list()
        self.combos = combos
        self.logger = lambda s: print(f"  > {s}") if debug else lambda s: None
        self.void = (lambda: self.logger(f"Combination not found {self.pressed_keys}"), )

    def on_press(self, key):
        if key not in self.pressed_keys:
            self.pressed_keys.append(key)

    def on_release(self, key):
        (callback, *args) = self.combos.get(tuple(self.pressed_keys), self.void)
        self.logger(f"Pressed keys {self.pressed_keys}")
        self.logger(f"Running {callback.__name__}{args}")
        self.pressed_keys.remove(key)
        return callback(*args)

    def start(self):
        with kb.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.logger(f"Joining listener {listener} to main thread")
            listener.join()
