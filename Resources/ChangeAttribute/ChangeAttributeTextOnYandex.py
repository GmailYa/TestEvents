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

            # Команда для ввода текста в оба поля по name
            command = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": f"""
                        (function() {{
                            const textToInput = '{text_to_input}';
                            const results = [];

                            // Находим поля по атрибуту name
                            const field1 = document.querySelector('input[name="input1"]');
                            const field2 = document.querySelector('input[name="input2"]');

                            const fields = [field1, field2];
                            const names = ['input1', 'input2'];

                            for (let i = 0; i < fields.length; i++) {{
                                const inputField = fields[i];
                                const fieldName = names[i];

                                if (!inputField) {{
                                    results.push("Поле name='" + fieldName + "' не найдено");
                                    continue;
                                }}

                                // Убедимся, что поле доступно для ввода
                                if (inputField.disabled) {{
                                    results.push("Поле name='" + fieldName + "' заблокировано");
                                    continue;
                                }}

                                if (inputField.readOnly) {{
                                    results.push("Поле name='" + fieldName + "' только для чтения");
                                    continue;
                                }}

                                // Фокусируемся на поле
                                inputField.focus();

                                // Очищаем поле
                                inputField.value = '';

                                // Вводим текст
                                inputField.value = textToInput;

                                // Триггерим события
                                inputField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                inputField.dispatchEvent(new Event('change', {{ bubbles: true }}));

                                results.push("Успех: name='" + fieldName + "' введено: '" + inputField.value + "'");
                            }}

                            return results.join('\\\\n');
                        }})()
                    """,
                    "returnByValue": True
                }
            }

            print(f"Пытаюсь ввести текст: {text_to_input} в оба поля")
            await websocket.send(json.dumps(command))

            # Ждем ответа
            response = await websocket.recv()
            result = json.loads(response)

            if 'result' in result and 'result' in result['result']:
                print("Результат:")
                print(result['result']['result']['value'])
            else:
                print("Ошибка выполнения:", result)

    except Exception as e:
        print(f"Ошибка подключения: {e}")
        print("Убедитесь, что браузер запущен с параметром: yandex-browser --remote-debugging-port=9222")

# Запуск
asyncio.run(input_text_to_field())
