import numpy as np
import sounddevice as sd
# pip install numpy sounddevice

def print_sound(indata, outdata, frames, time, status):
    norm = int(np.linalg.norm(indata))
    print(f"IN {norm}: {'|' * norm}")

def interruptable_sleep(duration_ms=-1, poll_time_ms=1000):
    try:
        duration_iter = itertools.count() if duration_ms == -1 else range(duration_ms // poll_time_ms)
        for i in duration_iter:
            print(f"Sleep: {i}, poll_time: {poll_time_ms}")
            sd.sleep(poll_time_ms)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    duration_ms = -1
    with sd.Stream(callback=print_sound): interruptable_sleep(duration_ms)
