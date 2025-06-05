#!/usr/bin/env python3
import time
import uinput

# Настройка виртуального устройства мыши
device = uinput.Device([
    uinput.BTN_LEFT,      # Левая кнопка
    uinput.BTN_RIGHT,     # Правая кнопка
    uinput.REL_X,         # Ось X (для движения)
    uinput.REL_Y,         # Ось Y (для движения)
])

# Координаты (опционально, если нужно движение)
# device.emit(uinput.REL_X, 100, syn=False)
# device.emit(uinput.REL_Y, 200, syn=False)

# Правый клик: нажатие + отпускание
device.emit(uinput.BTN_RIGHT, 1)  # Нажатие
time.sleep(0.1)                   # Задержка
device.emit(uinput.BTN_RIGHT, 0)  # Отпускание

print("Правый клик выполнен!")
