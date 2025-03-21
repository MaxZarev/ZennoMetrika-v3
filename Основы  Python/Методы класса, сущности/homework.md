## Задача 1 - light

1. Создайте класс Account, который имеет атрибуты:
- номер профиля
- адрес кошелька
- адрес суб аккаунта
- balance - баланс аккаунта (изначально 1000)
2. Создайте методы:
- init для инициализации атрибутов
- get_balance - возвращает баланс аккаунта, при запуске печатает "Баланс аккаунта {номер профиля}, {адрес кошелька} равен {баланс}"
- send_tx - принимает параметры: адрес кошелька и сумму, уменьшает баланс в атрибуте на сумму отправки, печатает в терминале
  "Транзакция на сумму {сумма} успешно отправлена на адрес {адрес кошелька}, баланс аккаунта {номер профиля}, {адрес кошелька} равен {баланс}"


## Задача 2 - medium

1. Создайте класс Metamask, который имеет атрибуты:
- адрес кошелька 
- пароль кошелька
- сид фраза
2. Создайте методы, которые имитируют реальное поведение Metamask:
- init для инициализации атрибутов, все 3 атрибуты не обязательны
- auth для авторизации пользователя, при запуске печатает "Вы успешно авторизовались с помощью пароля: {пароль}",
  пароль должен браться из атрибута, при этом если пароль не указан, то печатает "Вы не указали пароль"
- create_wallet для создания кошелька, при запуске генерирует сид фразу из 12 слов, адрес кошелька и пароль 
 (если пароль был указан ранее в атрибуте, использует из атрибута, если нет, генерирует случайный пароль), присваивает их
  атрибутам, печатает в терминале "Кошелек успешно создан,   адрес кошелька: {адрес кошелька}, пароль: {пароль}, сид фраза: {сид фраза}"
- import_wallet для импорта кошелька, берет адрес, сид фразу и пароль из атрибутов, если пароль не указан, то генерирует случайный пароль,
  сохраняя его в атрибут, печатает в терминале "Кошелек успешно импортирован, адрес кошелька: {адрес кошелька}, пароль: {пароль}, сид фраза: {сид фраза}"

## Задача 3 - hard 

1. Создайте класс Account, который имеет:
- атрибут номер профиля
- атрибут адрес кошелька
- атрибут адрес суб аккаунта
- атрибут баланс аккаунта (изначально 0)
- метод init для инициализации атрибутов
- метод get_balance для возврата баланса аккаунта из атрибута баланс
- метод send_token для отправки токена, принимает параметры: адрес кошелька и сумму, уменьшает баланс аккаунта на сумму транзакции
- метод withdraw_to_sub для отправки транзакции на указанную сумму на адрес суб аккаунта, для отправки внутри метода используйте метод send_token

2. Создайте класс Exchange, который имеет атрибуты:
- account - объект класса Account
- main_balance - баланс биржи (изначально 10000)
- sub_balance - баланс суб аккаунтов (изначально 0)
3. Создайте методы:
- init для инициализации атрибутов
- withdraw - метод для вывода токена с баланса биржи, принимает сумму вывода, уменьшает баланс биржи на сумму вывода, увеличивает баланс аккаунта на сумму вывода
- popup_sub_balance - метод для пополнения баланса суб аккаунта после вывода токена с кошелька, увеличивает балаанс суб аккаунта на сумму пополнения
- collect_from_sub_to_main - метод для сбора токенов с суб аккаунтов на главный аккаунт, уменьшает баланс суб аккаунтов на сумму сбора, увеличивает баланс биржи на сумму сбора

4. Напишите скрипт, который будет:
- извлекать из 3 текстовых файлов данные с номером профиля, адресом кошелька, адресом суб аккаунта
- создавать список объектов класса Account
- в цикле берет аккаунт из списка, создает объект класса Exchange и передает в него аккаунт
- делает вывод ~90% доступного баланса биржи на баланс аккаунта
- при выводе минусуйте с баланса биржи комиссию 0.1% от суммы вывода
- ждет 2-3 секунды
- делает вывод с кошелька всей суммы с кошелька на суб аккаунт, оставляя на балансе 5-10 токенов
- пополните баланс суб аккаунта на отправленную сумму
- делает сбор с суб аккаунта на баланс биржи
- запускает следующий цикл

- Задача прогнать объем токенов через все аккаунты, оставив на балансе аккаунтов по 5-10 токенов.
- Каждая операция с балансами должна уменьшать и увеличивать соответствующие балансы на указанные суммы.
- В конце необходимо будет посчитать сколько суммарно осталось токенов на балансах аккаунтов запрашивая баланс через метод get_balance
- В конце необходимо будет вывести оставшийся баланс на бирже и суб аккаунте