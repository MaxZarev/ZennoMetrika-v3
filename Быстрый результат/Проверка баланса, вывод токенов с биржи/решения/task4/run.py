import datetime
import random
import time

from eth_account import Account
from loguru import logger

from config import config, Chains, Tokens
from core.bot import Bot
from core.onchain import Onchain
from core.excel import Excel
from utils.logging import init_logger
from utils.utils import random_sleep, get_accounts, generate_password


def main():
    """ Основная функция """
    # Инициализация консоли и логгера
    init_logger()
    # Получаем список аккаунтов из файлов
    accounts = get_accounts()

    for i in range(config.cycle):
        # Перебираем аккаунты
        for account in accounts:
            # передаем аккаунт в функцию worker
            # здесь можно добавить логику получения данных из Excel и пропуска профиля, если он уже был обработан
            worker(account)

    logger.success("Все аккаунты обработаны")


def worker(account: Account) -> None:
    """
    Функция для работы с аккаунтом, создает бота и передает его в функцию activity
    :param account: аккаунт
    :return: None
    """

    # if not schedule(account):
    #     return

    # Создаем бота
    with Bot(account) as bot:
        # Вызываем функцию activity и передаем в нее бота
        activity(bot)

    random_sleep(*config.pause_between_profile)


def schedule(account: Account) -> bool:
    """
    Функция для работы с аккаунтом, создает бота и передает его в функцию activity
    :param account: аккаунт
    :return: None
    """
    excel = Excel(account)
    date = excel.get_date('Активность 1')
    if date < datetime.datetime.now() - datetime.timedelta(days=5):
        return True
    return False


def activity(bot: Bot):
    """
    Функция для работы с ботом, описываем логику активности бота.
    :param bot: бот
    :return: None
    """
    chains = [Chains.ETHEREUM, Chains.BSC, Chains.POLYGON, Chains.AVALANCHE, Chains.ZKSYNC, Chains.ARBITRUM_ONE, Chains.OP]

    for chain in chains:
        # создаем объект Onchain с нужной сетью
        onchain = Onchain(bot.account, chain)
        # получаем баланс токена нативного токена
        balance = onchain.get_balance()
        # записываем баланс в Excel
        bot.excel.set_cell(f'{bot.chain.name}-{chain.native_token}', balance.ether_float)



if __name__ == '__main__':
    main()
