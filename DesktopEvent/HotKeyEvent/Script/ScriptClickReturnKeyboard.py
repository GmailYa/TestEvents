from evdev import UInput, ecodes as e
import time

with UInput(name="test_keyboard") as ui:
    time.sleep(5)
    ui.write(e.EV_KEY, e.KEY_ENTER, 1)

    ui.syn()

    time.sleep(0.5)

    ui.write(e.EV_KEY, e.KEY_ENTER, 0)

    ui.syn()
