import json
import time

import requests
from eth_typing import ChecksumAddress
from web3 import Web3

from amount import Amount
from tokens import Token


def get_tx_params(w3: Web3, to: str | ChecksumAddress | None = None, value: int | None = None, data: str | None = None) -> dict:
    tx_params = {
        'chainId': w3.eth.chain_id,
        'from': w3.eth.default_account,
        'nonce': w3.eth.get_transaction_count(w3.eth.default_account),
    }
    if to:
        tx_params['to'] = to
    if value:
        tx_params['value'] = value
    if data:
        tx_params['data'] = data

    return tx_params


def get_fee(w3: Web3) -> dict:
    tx_params = dict()
    fee_history = w3.eth.fee_history(20, 'latest', [20])
    base_fee = fee_history['baseFeePerGas'][-1]
    priority_fees = [fee[0] for fee in fee_history.get('reward', [0])] or [0]
    max_priority_fee = max(priority_fees)
    max_fee = (base_fee + max_priority_fee) * 1.1

    tx_params['maxPriorityFeePerGas'] = int(max_priority_fee)
    tx_params['maxFeePerGas'] = int(max_fee)

    return tx_params

def sing_send_tx(w3: Web3, tx_params: dict, private_key: str) -> str:
    """
    Подписываем транзакцию
    :param w3: объект web3
    :param tx_params: параметры транзакции
    :param private_key: приватный ключ
    :return: хеш транзакции
    """
    signed_tx = w3.eth.account.sign_transaction(tx_params, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return '0x' + tx_hash.hex()

def get_token_price_from_binance(token_symbol: str) -> float:
    """
    Получаем цену токена с Binance
    :param token: название токена (тикер)
    :return: цена токена
    """
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={token_symbol}USDT'
    response = requests.get(url)
    data = response.json()
    return float(data['price']) if 'price' in data else 0.0

def get_abi(abi_name:str) -> dict:
    """
    Получаем ABI контракта
    :param abi_name: название ABI
    :return: ABI контракта
    """
    if not abi_name.endswith('.json'):
        abi_name += '.json'
    with open(f'abis/{abi_name}') as file:
        return json.loads(file.read())


def approve(w3: Web3, token: Token, spender: str, amount: Amount, private_key: str, is_max: bool = False) -> None:
    """
    Проверяет имеется ли у контракта разрешение на списывание токена и, если нет, то дает его
    на переданную сумму
    """
    token_contract = w3.eth.contract(address=token.address, abi=get_abi('erc20'))
    spender = w3.to_checksum_address(spender)
    allowance = token_contract.functions.allowance(w3.eth.default_account, spender).call()
    if allowance < amount.wei:
        amount = amount.wei if not is_max else 2**256 - 1
        tx_params = token_contract.functions.approve(spender, amount).build_transaction(get_tx_params(w3))
        sing_send_tx(w3, tx_params, private_key)
        time.sleep(5)


def to_amount(amount: float | Amount, token: Token | None) -> Amount:
    """
    Приводит сумму к типу Amount
    :param amount: сумма
    :param token: токен
    :return: сумма в wei
    """
    if isinstance(amount, float):
        if token:
            amount = Amount(amount, token.decimals)
        else:
            amount = Amount(amount, 18)
    return amount


def to_checksum(address: str | ChecksumAddress) -> ChecksumAddress:
    """
    Преобразует адрес в checksum формат
    :param address: адрес
    :return: адрес в checksum формате
    """
    if address and isinstance(address, str):
        address = Web3.to_checksum_address(address)
    return address


def get_list_from_file(path: str) -> list[str]:
    """
    Получаем список из файла
    :param path: путь к файлу
    :return: список строк
    """
    with open(path) as file:
        return file.read().splitlines()
