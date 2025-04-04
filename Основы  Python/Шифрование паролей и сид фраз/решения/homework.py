""""""

"""
Задание 1 - easy

Напишите функцию на Python, которая генерирует случайный симметричный ключ 
для шифрования и расшифрования данных и печатает в терминале. Используйте библиотеку cryptography.

"""
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    print(f"Generated Key: {key}")
"""
Задание 2  - medium

Напишите функцию на Python, которая шифрует переданные ей данные и возвращает
зашифрованную строку. Используйте библиотеку cryptography.
Функция принимает:
- строку для шифрования
- ключ для шифрования
Возвращает зашифрованную строку.

"""

def encrypt_data(data: str, key: bytes) -> str:
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data.decode()

"""
Задание 3 - medium

Напишите функцию на Python, которая дешифрует переданные ей данные и возвращает
зашифрованную строку. Используйте библиотеку cryptography.
Функция принимает:
- строку для дешифрования
- ключ для дешифрования
Возвращает расшифрованную строку.
"""

def decrypt_data(data: str, key: bytes) -> str:
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data.encode())
    return decrypted_data.decode()

"""
Задание 4 - hard

Напишите скрипт, который берет из текстового файла список паролей и шифрует их при помощи библиотеки cryptography.
Ключ должен браться из связки ключей системы с помощью библиотеки keyring.
Зашифрованные пароли должны записываться в новый файл.
"""

import keyring
from cryptography.fernet import Fernet

with open("passwords.txt", "r") as file:
    passwords = file.read().splitlines()

key = keyring.get_password("system", "key")
cipher_suite = Fernet(key)

with open("passwords_encrypted.txt", "w") as file:
    for password in passwords:
        encrypted_password = cipher_suite.encrypt(password.encode())
        file.write(encrypted_password.decode() + "\n")


# код пишем тут

