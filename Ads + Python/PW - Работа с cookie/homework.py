""""""
import time
from playwright.sync_api import Page

"""
Задание 1 - medium

Напишите функцию auth_x, которая принимает на вход 2 аргумента:
1. page: Page - объект страницы
2. token: str - токен для авторизации

Функция должна, добавлять куки авторизации для сайта x.com в контекст браузера,
со сроком жизни 1 год.

"""

# напишите ваш код ниже