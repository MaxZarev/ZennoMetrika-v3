## Задача 1 - light
### Условие:

Создать функцию которая принимает 1 аргумент gas_limit, в функции в цикле должен генерироваться рандомный газ от 10 до 50, 
Если газ выше чем gas_limit, то функция должна вставать на паузу 0,1 секунду и писать уведомление в терминал,
если сгенерированный газ меньше чем gas_limit, то функция печатает "можно работать" и завершает работу.


## Задача 2 - middle
### Условие:

Создать функцию генератор паролей, которая принимает 4 аргумента: длину пароля, а так же 3 аргумента bool (true/false):
1. использовать ли латинские буквы
2. использовать ли цифры
3. использовать ли спец символы
Функция должна генерировать пароль с использованием выбранных символов и печатать его в терминале.

## Задача 3 - middle
### Условие:
Создать функцию генератор кошельков, которая принимает 1 аргумент, количество кошельков и генерирует список из нужного количества кошельков
в формате "0x" + 40 случайных символов из набора "abcdef0123456789" (16-ричная система исчисления).
Итоговый список должен быть сохранен в через глобальную переменную wallets снаружи функции, чтобы полученный список можно было использовать вне функции.

## Задача 4 - middle
### Условие:
Создать функцию "вывода с биржи", на вход должна получать адрес кошелька и минимальный баланс, внутри должен 
проходить псевдо запрос баланса (генерируем рандомно), 
если баланс ниже минимальной суммы делать вывод на кошелек рандомной суммы и напечатать сообщение об этом.

## Задача 5 - hard
### Условие:

Используя созданные функции создайте программу, которая:
создает список кошельков
Потом в цикле перебирает список кошельков и делает следующее:
Печатает название кошелька.
Генерирует новый пароль при помощи функции и печатает его в терминале.
Ждет когда газ будет меньше 30 и печатает уведомление в терминале.
Проверяет баланс кошелька, если баланс меньше 1000 делает вывод на кошелек рандомной суммы.
Функции должны быть определены в верхней части программы, логика программы и вызов функций в нижней части.