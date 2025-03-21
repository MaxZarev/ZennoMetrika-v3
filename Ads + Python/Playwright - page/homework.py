""""""
from typing import Optional

"""
Задание 1 - easy

Напишите функцию open_url, которая принимает на вход URL и объект page из Playwright 
и открывает переданный URL в переданном объекте page, если URL равен уже открытому URL на странице,
то функция ничего не делает.

 
"""

# код пишем тут


"""
Задание 2  - medium
Напишите функцию page_catcher, которая принимает на вход объект BrowserContext из Playwright и
объект Locator из Playwright, который содержит в себе локатор элемента на странице.
Функция должна поймать открывающуюся страницу, при нажатии на переданный элемент и вернуть объект
page новой страницы.
"""

# код пишем тут

"""
Задание 3 - hard
Напишите класс ADS, который будет принимать на вход номер профиля и иметь следующие аттрибуты:
- profile_number - номер профиля
- _profile_id - защищенный аттрибут, который будет хранить id профиля, изначально None
- _pw - объект Playwright
- _browser - объект браузера из Playwright
- context - объект контекста из Playwright
- page - объект страницы из Playwright

Класс должен иметь следующие методы:
- _run_browser - открывает браузер, с номером профиля в аттрибуте profile_number,
 при помощи методов open_browser и check_browser
- _check_browser - проверяет статус профиля из атрибута profile_number, возвращает данные для подключения к браузеру
- _open_browser - открывает браузер из атрибута profile_number, возвращает данные для подключения к браузеру
- метод prepare_browser - при запуске метода, должны закрыться все открытые вкладки, кроме той, которая лежит
в атрибуте page. (будьте осторожны с системными вкладками расширений) 
- _get_profile_id - запрашивает id профиля из ADS по номеру профиля
- геттер profile_id - возвращает id профиля из атрибута _profile_id, если он есть,
иначе запускает метод _get_profile_id, записывает id профиля в атрибут _profile_id и возвращает его
- магический метод __enter__ - запускает метод _run_browser, кладет объект браузера в аттрибут browser,
объект контекста в аттрибут context, создает новую страницу и кладет ее в аттрибут page, печатает в терминале
информацию о запуске профиля с указанием номера и возвращает объект класса.
- магический метод __exit__ - корректно закрывает браузер, печатает в терминале информацию о закрытии профиля
с указанием номера.
- метод open_url - открывает переданный URL в объекте page, если URL уже открыт, то ничего не делает
- метод page_catcher - принимает объект Locator из Playwright, который содержит в себе локатор элемента на странице,
метод должен поймать открывающуюся страницу, при нажатии на переданный элемент и вернуть объект page новой страницы.
- метод reload_context - открывает новую страницу и сразу же закрывает её, тем самым принудительно обновляя
список открытых вкладок в контексте браузера.
- метод find_page - находит страницу по тексту в URL в контексте браузера, если страница не найдена, возвращает None
"""

# код пишем тут