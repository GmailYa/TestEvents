from evdev import UInput, ecodes as e
import time
import argparse

def press_keys(keys):
    """
    Нажимает клавиши последовательно, отпускает одновременно
    Поддерживаемые клавиши: 1, 2, 3
    """
    key_mapping = {
        '1': e.KEY_1,
        '2': e.KEY_2,
        '3': e.KEY_3
    }

    if len(keys) > 3:
        print("Ошибка: максимум 3 клавиши!")
        return

    for key in keys:
        if key not in key_mapping:
            print(f"Ошибка: клавиша '{key}' не поддерживается!")
            return

    capabilities = {
        e.EV_KEY: list(key_mapping.values()),
    }

    with UInput(capabilities, name="virtual_keyboard") as ui:
        time.sleep(5)

        # Последовательное нажатие
        for key in keys:
            ui.write(e.EV_KEY, key_mapping[key], 1)  # Нажатие
            ui.syn()
            print(f"Нажата: {key}")
            time.sleep(0.1)  # Интервал между нажатиями

        time.sleep(0.4)  # Удержание

        # Одновременное отпускание
        for key in keys:
            ui.write(e.EV_KEY, key_mapping[key], 0)

        ui.syn()
        print("Все клавиши отпущены")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Нажатие клавиш 1-3')
    parser.add_argument('keys', nargs='+', choices=['1', '2', '3'])
    args = parser.parse_args()

    print(f"Нажимаем: {', '.join(args.keys)}")
    press_keys(args.keys)
