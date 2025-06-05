#!/usr/bin/env python3

from Xlib import X, display
from Xlib.ext import xtest
import time

def simulate_click(x, y):
    # Получаем текущий дисплей
    d = display.Display()

    # Перемещаем курсор (опционально, но полезно для визуализации)
    root = d.screen().root
    root.warp_pointer(x, y)
    d.sync()

    # Имитируем нажатие левой кнопки мыши
    xtest.fake_input(d, X.ButtonPress, 3)  # 1 - левая кнопка мыши
    d.sync()
    time.sleep(0.1)  # небольшая задержка между нажатием и отпусканием
    xtest.fake_input(d, X.ButtonRelease, 3)
    d.sync()

if __name__ == "__main__":
    time.sleep(5)
    target_x = 100  # Замените на нужные координаты X
    target_y = 200  # Замените на нужные координаты Y
    simulate_click(target_x, target_y)
