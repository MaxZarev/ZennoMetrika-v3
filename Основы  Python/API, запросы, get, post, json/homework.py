"""API"""

"""
Задание 1 - easy

Напишите функцию для отправки post запросов, на входе принимает:
- url - адрес запроса
- params - параметры запроса (опционально)
- payload - полезная нагрузка (опционально)
- headers - заголовки (опционально)
- proxy - прокси (опционально)
- attempts - количество попыток отправить запрос (опционально, по умолчанию 3)

Функция должна возвращать ответ в виде json (dict или list[dict]) или бросать исключение, если не удалось 
получить ответ за attempts попыток.
"""

# код пишем тут

"""
Задание 2 - medium
Напишите функцию, которая принимает список адресов кошельков, обратно возвращает словарь,
где ключи адреса кошельков, а значения - балансы кошельков:
- Для получения баланса используйте API https://api.etherscan.io/.
- Используйте endpoint для запроса балансов у пачки аккаунтов.
- функция должна запрашивать балансы сразу по 20 адресов (или меньше, если адресов меньше 20)
- балансы должны быть в человекочитаемом виде.
"""



# код пишем тут

"""
Задание 3 - hard
Изучите документацию https://docs.etherscan.io/etherscan-v2/getting-started/v2-quickstart

Доработайте скрипт из задания 2, чтобы балансы проверялись в блокчейнах:
- Ethereum
- Arbitrum
- Linea
- Base

Записывает в словарь суммарный баланс кошелька и балансы по каждому блокчейну.
Балансы должны проверяться пачками по 20 адресов.

Результирующий словарь должен быть в формате:
{'address': {Total: '2.0', 'Ethereum': '0.5', 'Arbitrum': '0.5', 'Linea': '0.5', 'Base': '0.5'}}

"""

# код пишем тут
