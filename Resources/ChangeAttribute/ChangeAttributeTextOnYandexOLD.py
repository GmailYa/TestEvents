#!/usr/bin/env python3
import json
import requests
import websockets
import asyncio

async def input_text_to_field():
    try:
        # Получаем информацию о вкладках
        response = requests.get('http://localhost:9222/json', timeout=10)
        tabs = response.json()

        if not tabs:
            print("Нет открытых вкладок")
            return

        tab = tabs[0]
        print(f"Работаем с вкладкой: {tab['title']}")
        print(f"URL: {tab['url']}")

        async with websockets.connect(tab['webSocketDebuggerUrl']) as websocket:
            # Текст для ввода
            text_to_input = "TestЗначение1!"

            # Команда для ввода текста в поле
            command = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": f"""
                        (function() {{
                            // Находим поле ввода
                            const inputField = document.querySelector('input#input1');

                            if (!inputField) {{
                                return "Ошибка: Поле input#input1 не найдено";
                            }}

                            // Убедимся, что поле доступно для ввода
                            if (inputField.disabled) {{
                                return "Ошибка: Поле заблокировано";
                            }}

                            if (inputField.readOnly) {{
                                return "Ошибка: Поле только для чтения";
                            }}

                            // Фокусируемся на поле
                            inputField.focus();

                            // Очищаем поле (если нужно)
                            inputField.value = '';

                            // Вводим текст
                            inputField.value = '{text_to_input}';

                            // Триггерим события для обновления состояния
                            inputField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            inputField.dispatchEvent(new Event('change', {{ bubbles: true }}));

                            // Проверяем результат
                            return "Успех: В поле введено: '" + inputField.value + "'";
                        }})()
                    """,
                    "returnByValue": True
                }
            }

            print(f"Пытаюсь ввести текст: {text_to_input}")
            await websocket.send(json.dumps(command))

            # Ждем ответа
            response = await websocket.recv()
            result = json.loads(response)

            if 'result' in result and 'result' in result['result']:
                print("Результат:", result['result']['result']['value'])
            else:
                print("Ошибка выполнения:", result)

    except Exception as e:
        print(f"Ошибка подключения: {e}")
        print("Убедитесь, что браузер запущен с параметром: yandex-browser --remote-debugging-port=9222")

# Запуск
asyncio.run(input_text_to_field())
