""""""

"""
Задание 1 - easy

Напишите функцию get_balance(rpc: str, contract_address: str, user_address: str) -> float, которая принимает на вход
три аргумента:
rpc: str - адрес RPC ноды
contract_address: str - адрес контракта токена ERC20
user_address: str - адрес пользователя

Функция должна вернуть баланс пользователя в токенах ERC20 в человеческом формате.
Функция должна работать во всех EVM сетях со всеми токенами ERC20.

"""
import json

from web3 import Web3

def get_balance(rpc: str, contract_address: str, user_address: str) -> float:
    w3 = Web3(Web3.HTTPProvider(rpc))
    with open('erc20.json') as file:
        abi = json.loads(file.read())
    contract_address = w3.to_checksum_address(contract_address)
    user_address = w3.to_checksum_address(user_address)
    contract = w3.eth.contract(address=contract_address, abi=abi)
    balance_wei = contract.functions.balanceOf(user_address).call()
    decimals = contract.functions.decimals.call()
    return balance_wei / 10 ** decimals

# код пишем тут

"""
Задание 2  - medium
Создайте класс Chain, который будет хранить информацию о сети:
name: str - имя сети
rpc: str - адрес RPC ноды
native_token: str - название нативного токена сети

Создайте класс Chains, который будет хранить информацию о сетях:
Ethereum: Chain - сеть Ethereum
Arbitrum: Chain - сеть Arbitrum
Optimism: Chain - сеть Optimism

Создайте класс Token, который будет хранить информацию о токене ERC20:  
name: str - имя токена
address: str - адрес контракта токена ERC20
chain: Chain - сеть, на которой находится токен
decimals: int - количество знаков после запятой

Создайте класс Tokens, который будет хранить информацию о токенах ERC20:
USDT_Ethereum: Token - токен USDT на сети Ethereum
USDT_Arbitrum: Token - токен USDT на сети Arbitrum
USDT_Optimism: Token - токен USDT на сети Optimism

Создайте функцию get_balance(chain: Chain, token: Token, user_address: str) -> float, 
которая принимает на вход три аргумента:
chain: Chain - сеть
token: Token - токен ERC20
user_address: str - адрес пользователя

Функция должна вернуть баланс пользователя в токенах ERC20 в человеческом формате.
Функция должна работать во всех EVM сетях со всеми токенами ERC20.

Функцию должно быть возможно использовать следующим образом:
get_balance(Chains.Ethereum, Tokens.USDT_Ethereum, '0x624c222fed7f88500afa5021cc760b3106fe34be')
get_balance(Chains.Arbitrum, Tokens.USDT_Arbitrum, '0x624c222fed7f88500afa5021cc760b3106fe34be')
"""

# код пишем тут

class Chain:
    def __init__(self, name: str, rpc: str, native_token: str):
        self.name = name
        self.rpc = rpc
        self.native_token = native_token

class Chains:
    Ethereum = Chain('Ethereum', 'https://1rpc.io/eth', 'ETH')
    Arbitrum = Chain('Arbitrum', 'https://1rpc.io/arb', 'ETH')
    Optimism = Chain('Optimism', 'https://1rpc.io/op', 'ETH')

class Token:
    def __init__(self, name: str, address: str, chain: Chain, decimals: int):
        self.name = name
        self.address = address
        self.chain = chain
        self.decimals = decimals

class Tokens:
    USDT_Ethereum = Token('USDT', '0xdac17f958d2ee523a2206206994597c13d831ec7', Chains.Ethereum, 6)
    USDT_Arbitrum = Token('USDT', '0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9', Chains.Arbitrum, 6)
    USDT_Optimism = Token('USDT', '0x94b008aa00579c1307b0ef2c499ad98a8ce58e58', Chains.Optimism, 6)

def get_balance(chain: Chain, token: Token, user_address: str) -> float:
    w3 = Web3(Web3.HTTPProvider(chain.rpc))
    with open('erc20.json') as file:
        abi = json.loads(file.read())
    contract_address = w3.to_checksum_address(token.address)
    user_address = w3.to_checksum_address(user_address)
    contract = w3.eth.contract(address=contract_address, abi=abi)
    balance_wei = contract.functions.balanceOf(user_address).call()
    return balance_wei / 10 ** token.decimals

"""
Задание 3 - hard

Напишите класс Onchain, который будет принимать на вход private_key: str и chain: Chain. 
В объекте при инициализации должен быть создан объект w3 класса Web3 с адресом RPC ноды chain.rpc,
должен быть извлечен адрес кошелька из приватного ключа.
Реализуйте методы класса Onchain:
get_balance(self, token: Token | None = None, user_address: str | None = None) -> float - 
который возврвщает баланс токена в человеческом формате. 
Если token не передан, то возвращает баланс нативного токена сети (decimals = 18).
Если user_address не передан, то возвращает баланс кошелька инициализированного приватным ключом.
decimals должен извлекаться из атрибута token.decimals, если значение не передано, должно быть запрошено 
из контракта токена.


Пример использования:
onchain = Onchain(Chains.Ethereum, '0x...0') 

# запрос USDT баланса кошелька 0x624c222fed7f88500afa5021cc760b3106fe34be в сети Ethereum
print(onchain.get_balance(Tokens.USDT_Ethereum, '0x624c222fed7f88500afa5021cc760b3106fe34be'))

# запрос баланса нативного токена кошелька из приватного ключа в сети Ethereum
print(onchain.get_balance())

# запрос баланса USDT кошелька из приватного ключа в сети Ethereum
print(onchain.get_balance(Tokens.USDT_Ethereum))

# запрос баланса нативного токена кошелька 0x624c222fed7f88500afa5021cc760b3106fe34be в сети Ethereum
print(onchain.get_balance(user_address='0x624c222fed7f88500afa5021cc760b3106fe34be'))

"""

class Onchain:
    def __init__(self, chain: Chain, private_key: str):
        self.chain = chain
        self.private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider(chain.rpc))
        self.address = self.w3.eth.account.from_key(private_key).address


    def get_balance(self, token: Token = None, user_address: str = None) -> float:

        if not user_address:
            user_address = self.address
        user_address = self.w3.to_checksum_address(user_address)
        if not token:
            return self.w3.eth.get_balance(user_address) / 10 ** 18

        contract_address = self.w3.to_checksum_address(token.address)

        with open('erc20.json') as file:
            abi = json.loads(file.read())

        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        balance_wei = contract.functions.balanceOf(user_address).call()
        if not token.decimals:
            token.decimals = contract.functions.decimals.call()
        return balance_wei / 10 ** token.decimals
# код пишем тут

