# Задачи к уроку "Условный оператор и boolean"
## Задача 1 - light
### Условие:

Напишите программу, которая будет запрашивать ввести баланс
кошелька в терминале и выводить сообщение о том, кем является
владелец кошелька с таким балансом:
- менее 0 = трейдер
- 0 = начинающий
- от 1 до 100 = нормис
- от 101 до 1000 = деген
- от 1001 до 10000 = кит
- от 10001 и выше = Илон Маск

## Задача 2 - medium
### Условие:
Напишите программу, которая генерирует цену на газ (от 10 до 100) и начальный баланс кошелька (от 2000 до 10000) при помощи `random.randint()` 

Стоимость операций:

- мост стоит = цена газа * 75
- свап стоит = цена газа * 40
- минт домена стоит = цена газа * 100

Если на кошельке недостаточно средств для операций, программа должна имитировать вывод недостающей суммы с биржи:
- посчитать сумму вывода
- вывести сообщение о выводе
- прибавить сумму вывода к балансу

Дальнейшая логика программы:
- Если цена на газ ниже 25, то программа запускает мост Scroll, расходы должны вычитаться с баланса.
- Если цена на газ ниже 15, то после запуска моста программа должна еще сминтить домен, расходы должны вычитаться с баланса.
- Если цена на газ выше 25, то программа запускает свап, расходы должны вычитаться с баланса.
- Если цена на газ выше 50, то программа ничего не делает и рекомендует поработать в другой раз.
В конце программа выводит сообщение о завершении работы, указывает выполненные операции и оставшийся баланс кошелька.

## Задача 3 - hard
У вас есть 2 переменные с балансами кошелька в токене ETH и USDT.
Еще одна переменная описывает стоимость ETH в USDT.

Напишите программу, которая будет делать обмен из ETH в USDT если баланс USDT нулевой, при этом оставляя 5% токенов ETH на комиссии.

Если баланс USDT не нулевой, то программа должна делать обмен всех токенов USDT в ETH.

Во время обмена должно печататься в терминале какой токен меняется на какой и какая сумма обмена.
По результату обмена программа балансы должны меняться.

Продублируйте логику, чтобы программа делала 5 обменов из ETH в USDT и обратно, сама выбирая когда и какой обмен делать.

В конце работы программа должна выводить сообщение актуальный баланс токенов ETH и USDC.
