from evdev import UInput, ecodes as e
import time
import subprocess
import argparse

def get_current_cursor_position():
    """Получаем текущие координаты курсора через xdotool"""
    try:
        pos = subprocess.check_output(['xdotool', 'getmouselocation']).decode()
        x = int(pos.split()[0].split(':')[1])
        y = int(pos.split()[1].split(':')[1])
        return x, y
    except:
        return 0, 0

def move_and_click(target_x, target_y, button, double_click=False):
    """Перемещает курсор и выполняет указанное действие"""
    current_x, current_y = get_current_cursor_position()
    rel_x = target_x - current_x
    rel_y = target_y - current_y

    # Определяем кнопку
    btn_code = {
        'LeftButton': e.BTN_LEFT,
        'RightButton': e.BTN_RIGHT,
        'MidButton': e.BTN_MIDDLE
    }.get(button, e.BTN_LEFT)  # По умолчанию левая кнопка

    capabilities = {
        e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT, e.BTN_MIDDLE],
        e.EV_REL: [e.REL_X, e.REL_Y],
    }

    with UInput(capabilities, name="test_mouse") as ui:
        time.sleep(5)

        # Перемещаем курсор
        if rel_x != 0:
            ui.write(e.EV_REL, e.REL_X, rel_x)
        if rel_y != 0:
            ui.write(e.EV_REL, e.REL_Y, rel_y)
        ui.syn()

        # Выполняем клик
        if double_click:
            for _ in range(2):
                ui.write(e.EV_KEY, btn_code, 1)
                ui.syn()
                time.sleep(0.05)
                ui.write(e.EV_KEY, btn_code, 0)
                ui.syn()
                time.sleep(0.1)
        else:
            ui.write(e.EV_KEY, btn_code, 1)
            ui.syn()
            time.sleep(0.05)
            ui.write(e.EV_KEY, btn_code, 0)
            ui.syn()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Клик мышью по указанным координатам')
    parser.add_argument('x', type=int, help='X-координата')
    parser.add_argument('y', type=int, help='Y-координата')
    parser.add_argument('--button', type=str, default='LeftButton',
                      choices=['LeftButton', 'RightButton', 'MidButton'],
                      help='Тип кнопки (LeftButton/RightButton/MidButton)')
    parser.add_argument('--double', action='store_true',
                      help='Двойной клик (только для LeftButton)')

    args = parser.parse_args()

    if args.double and args.button != 'LeftButton':
        print("Предупреждение: двойной клик поддерживается только для LeftButton")
        args.double = False

    print(f"Кликаем в ({args.x}, {args.y}) кнопкой: {args.button}{' (двойной)' if args.double else ''}")
    move_and_click(args.x, args.y, args.button, args.double)
