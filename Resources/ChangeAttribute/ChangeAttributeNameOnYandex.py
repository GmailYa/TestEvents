#!/usr/bin/env python3
import json
import requests
import websockets
import asyncio

async def change_attribute():
    try:
        response = requests.get('http://localhost:9222/json', timeout=10)
        tabs = response.json()

        if not tabs:
            print("Нет открытых вкладок")
            return

        tab = tabs[0]
        print(f"Работаем с вкладкой: {tab['title']}")

        async with websockets.connect(tab['webSocketDebuggerUrl']) as websocket:
            # Сначала проверим, есть ли элемент на странице
            check_command = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": """
                        (function() {
                            // Простой поиск
                            const element = document.querySelector('input#input1');
                            if (element) {
                                return 'Элемент найден: ' + element.outerHTML;
                            }

                            // Поиск по ID
                            const byId = document.getElementById('input1');
                            if (byId) {
                                return 'Элемент найден по ID: ' + byId.outerHTML;
                            }

                            // Поиск всех input элементов
                            const allInputs = document.querySelectorAll('input');
                            let inputsInfo = 'Все input элементы: ';
                            allInputs.forEach((input, index) => {
                                inputsInfo += `[${index}] id:${input.id} name:${input.name} type:${input.type}; `;
                            });

                            return 'Элемент не найден. ' + inputsInfo;
                        })()
                    """,
                    "returnByValue": True
                }
            }

            print("Поиск элемента...")
            await websocket.send(json.dumps(check_command))
            response = await websocket.recv()
            result = json.loads(response)

            if 'result' in result and 'result' in result['result']:
                print("Результат поиска:", result['result']['result']['value'])

            # Теперь попробуем изменить атрибут
            change_command = {
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": """
                        (function() {
                            // Несколько способов найти элемент
                            let element = document.querySelector('input#input1');
                            if (!element) {
                                element = document.getElementById('input1');
                            }
                            if (!element) {
                                // Поиск по атрибуту name
                                element = document.querySelector('input[name=\"input1\"]');
                            }
                            if (!element) {
                                // Поиск среди всех input элементов
                                const inputs = document.getElementsByTagName('input');
                                for (let i = 0; i < inputs.length; i++) {
                                    if (inputs[i].id === 'input1' || inputs[i].name === 'input1') {
                                        element = inputs[i];
                                        break;
                                    }
                                }
                            }

                            if (element) {
                                const oldName = element.getAttribute('name');
                                element.setAttribute('name', 'new-input-name');
                                return 'Успех: Атрибут name изменен с \"' + oldName + '\" на \"' + element.getAttribute('name') + '\"';
                            } else {
                                return 'Ошибка: Элемент input#input1 не найден на странице';
                            }
                        })()
                    """,
                    "returnByValue": True
                }
            }

            print("Попытка изменения атрибута...")
            await websocket.send(json.dumps(change_command))
            response = await websocket.recv()
            result = json.loads(response)

            if 'result' in result and 'result' in result['result']:
                print("Результат изменения:", result['result']['result']['value'])
            else:
                print("Ошибка:", result)

    except Exception as e:
        print(f"Ошибка подключения: {e}")

asyncio.run(change_attribute())
