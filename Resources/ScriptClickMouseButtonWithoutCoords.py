from evdev import UInput, ecodes as e
import time
import argparse

def perform_click(button_type='LeftButton', double_click=False):
    """Выполняет указанный тип клика"""
    button_codes = {
        'LeftButton': e.BTN_LEFT,
        'RightButton': e.BTN_RIGHT,
        'MidButton': e.BTN_MIDDLE
    }

    capabilities = {
        e.EV_KEY: list(button_codes.values()),
        e.EV_REL: [e.REL_X, e.REL_Y],
    }

    with UInput(capabilities, name="smart_mouse", version=0x3) as ui:
        time.sleep(5)

        btn_code = button_codes[button_type]

        if double_click:
            if button_type != 'LeftButton':
                print("Ошибка: двойной клик поддерживается только для LeftButton!")
                return

            # Двойной левый клик
            for _ in range(2):
                ui.write(e.EV_KEY, e.BTN_LEFT, 1)
                ui.syn()
                time.sleep(0.05)
                ui.write(e.EV_KEY, e.BTN_LEFT, 0)
                ui.syn()
                time.sleep(0.1)
        else:
            # Одинарный клик любой кнопкой
            ui.write(e.EV_KEY, btn_code, 1)
            ui.syn()
            time.sleep(0.05)
            ui.write(e.EV_KEY, btn_code, 0)
            ui.syn()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Управление кликами мыши')
    parser.add_argument('--button', type=str, default='LeftButton',
                      choices=['LeftButton', 'RightButton', 'MidButton'],
                      help='Выберите кнопку (LeftButton/RightButton/MidButton)')
    parser.add_argument('--double', action='store_true',
                      help='Левый двойной клик (только для LeftButton)')

    args = parser.parse_args()

    if args.double and args.button != 'LeftButton':
        print("Ошибка: двойной клик работает только с LeftButton!")
        exit(1)

    print(f"Выполняем {'двойной ' if args.double else ''}клик: {args.button}")
    perform_click(args.button, args.double)
