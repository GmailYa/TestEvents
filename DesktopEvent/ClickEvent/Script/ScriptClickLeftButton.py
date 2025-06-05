from evdev import UInput, ecodes as e
import time

# Создаем виртуальное устройство ввода с поддержкой мыши
capabilities = {
    e.EV_KEY: [e.BTN_LEFT],
    e.EV_REL: [
        e.REL_X,
        e.REL_Y,
    ],
}

with UInput(capabilities, name="test_mouse", version=0x3) as ui:
    time.sleep(5)

    # Нажатие левой кнопки мыши
    ui.write(e.EV_KEY, e.BTN_LEFT, 1)  # 1 - нажатие
    ui.syn()

    time.sleep(0.5)

    # Отпускание левой кнопки мыши
    ui.write(e.EV_KEY, e.BTN_LEFT, 0)  # 0 - отпускание
    ui.syn()
