from eth_account import Account as EthAccount
from eth_typing import ChecksumAddress
from loguru import logger
from web3 import Web3
from web3.contract import Contract

from chains import Chain
from utils import get_user_agent


class Onchain:
    def __init__(self, private_key: str, chain: Chain):
        self.account = EthAccount.from_key(private_key)
        self.address = self.account.address
        self.chain = chain
        self.w3 = self._prepare_w3(chain)


    def _prepare_w3(self, chain: Chain) -> Web3:
        request_kwargs = {
            'headers': {
                'User-Agent': get_user_agent(),
                "Content-Type": "application/json",
            },
        }
        self.w3 = Web3(Web3.HTTPProvider(chain.rpc, request_kwargs=request_kwargs))
        return self.w3

    def change_chain(self, chain: Chain):
        """
        Изменение сети для работы
        :param chain: объект Chain
        :return: None
        """
        self.chain = chain
        self.w3 = self._prepare_w3(chain)


    def _get_token_params(self, token_address: str | ChecksumAddress) -> tuple[str, int]:
        """
        Получение параметров токена (symbol, decimals) по адресу контракта токена
        :param token_address:  адрес контракта токена
        :return: кортеж (symbol, decimals)
        """
        token_contract_address = to_checksum(token_address)

        if token_contract_address == Tokens.NATIVE_TOKEN.address:
            return self.chain.native_token, Tokens.NATIVE_TOKEN.decimals

        token_contract_raw = ContractRaw(token_contract_address, 'erc20', self.chain)
        token_contract = self._get_contract(token_contract_raw)
        decimals = token_contract.functions.decimals().call()
        symbol = token_contract.functions.symbol().call()
        return symbol, decimals

    def _get_contract(self, contract_raw: ContractRaw) -> Contract:
        """
        Получение инициализированного объекта контракта
        :param contract_raw: объект ContractRaw
        :return: объект контракта
        """
        return self.w3.eth.contract(contract_raw.address, abi=contract_raw.abi)

    def _estimate_gas(self, tx_params: dict) -> dict:
        """
        Оценивает стоимость газа для транзакции и добавляет исходный словарь tx параметр gas
        :param tx: параметры транзакции
        """
        tx_params['gas'] = int(self.w3.eth.estimate_gas(tx_params) * get_multiplayer())
        return tx_params

    def _get_fee(self, tx_params: dict[str, str | int] | None = None) -> dict[str, str | int]:
        """
        Подготовка параметров транзакции с учетом EIP-1559. Берет значение EIP-1559 из self.chain.is_eip1559,
        если не определено, то запрашивает и сохраняет значение на время сессии.
        Если сеть не поддерживает EIP-1559, то устанавливает параметр gasPrice,
        если поддерживает, то устанавливает параметры maxFeePerGas и maxPriorityFeePerGas.
        :param tx_params: параметры транзакции без параметров комиссии либо None, если передан None, то создается новый словарь
        """
        if tx_params is None:
            tx_params = {}

        fee_history = None

        if self.chain.is_eip1559 is None:
            fee_history = self.w3.eth.fee_history(20, 'latest', [40])
            self.chain.is_eip1559 = any(fee_history.get('baseFeePerGas', [0]))

        if self.chain.is_eip1559 is False:
            tx_params['gasPrice'] = self._multiply(self.w3.eth.gas_price)
            return tx_params

        fee_history = fee_history or self.w3.eth.fee_history(20, 'latest', [40])
        base_fee = fee_history.get('baseFeePerGas', [0])[-1]
        priority_fees = [fee[0] for fee in fee_history.get('reward', [[0]]) if fee[0] != 0] or [0]
        median_index = len(priority_fees) // 2
        priority_fees.sort()
        median_priority_fee = priority_fees[median_index]

        priority_fee = self._multiply(median_priority_fee)
        max_fee = self._multiply(base_fee + priority_fee)

        tx_params['type'] = '0x2'
        tx_params['maxFeePerGas'] = max_fee
        tx_params['maxPriorityFeePerGas'] = priority_fee

        return tx_params

    def _multiply(self, value: int, min_mult: float = 1.03, max_mult: float = 1.1) -> int:
        """
        Умножение значения газа на переданный множитель и множитель сети
        :param value: значение
        :return: умноженное значение
        """
        return int(value * get_multiplayer(min_mult, max_mult) * self.chain.multiplier)

    def _get_l1_fee(self, tx_params: dict[str, str | int]) -> Amount:
        """
        Получение комиссии для L1 сети Optimism
        :param tx_params: параметры транзакции
        :return: комиссия
        """
        if self.chain.name != 'op':
            return Amount(0, wei=True)

        abi = [
            {
                "inputs": [{"internalType": "bytes", "name": "_data", "type": "bytes"}],
                "name": "getL1Fee",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        oracle_address = self.w3.to_checksum_address('0x420000000000000000000000000000000000000F')
        contract = self.w3.eth.contract(address=oracle_address, abi=abi)
        tx_params['data'] = tx_params.get('data', '0x')
        l1_fee = contract.functions.getL1Fee(tx_params['data']).call()
        return Amount(l1_fee, wei=True)

    def _prepare_tx(self, value: Optional[Amount] = None,
                    to_address: Optional[str | ChecksumAddress] = None) -> dict:
        """
        Подготовка параметров транзакции
        :param value: сумма перевода ETH, если ETH нужно приложить к транзакции
        :param to_address: адрес получателя транзакции, для перевода нативного токена
        или если НЕ используете build_transaction (он автоматически укажет адрес получателя)
        :return: параметры транзакции
        """
        # получаем параметры комиссии
        tx_params = self._get_fee()

        # добавляем параметры транзакции
        tx_params['from'] = self.account.address
        tx_params['nonce'] = self.w3.eth.get_transaction_count(self.account.address)
        tx_params['chainId'] = self.chain.chain_id

        # если передана сумма перевода, то добавляем ее в транзакцию
        if value:
            tx_params['value'] = value.wei

        # если передан адрес получателя, то добавляем его в транзакцию
        # нужно для отправки нативных токенов на адрес, а не на смарт контракт
        if to_address:
            tx_params['to'] = to_address

        return tx_params

    def _sign_and_send(self, tx: dict) -> str:
        """
        Подпись и отправка транзакции
        :param tx: параметры транзакции
        :return: хэш транзакции
        """
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt['transactionHash'].hex()

    def get_balance(
            self,
            *,
            token: Optional[Token | str | ChecksumAddress] = None,
            address: Optional[str | ChecksumAddress] = None
    ) -> Amount:
        """
        Получение баланса кошелька в нативных или erc20 токенах, в формате Amount.
        :param token: объект Token или адрес смарт контракта токена, если не указан, то нативный баланс
        :param address: адрес кошелька, если не указан, то берется адрес аккаунта
        :return: объект Amount с балансом
        """

        if token is None:
            token = Tokens.NATIVE_TOKEN
            token.chain = self.chain

        # если не указан адрес, то берем адрес аккаунта
        if not address:
            address = self.account.address

        # приводим адрес к формату checksum
        address = to_checksum(address)

        # если передан адрес контракта, то получаем параметры токена и создаем объект Token
        if isinstance(token, str):
            symbol, decimals = self._get_token_params(token)
            token = Token(symbol, token, self.chain, decimals)

        if token.chain != self.chain:
            logger.error(f'Токен на другой сети {token.chain.name} проверяется в {self.chain.name}')
            raise ValueError('Токен на другой сети')

        # если токен не передан или передан нативный токен
        if token.type_token == TokenTypes.NATIVE:
            # получаем баланс нативного токена
            native_balance = self.w3.eth.get_balance(address)
            balance = Amount(native_balance, wei=True)
        else:
            # получаем баланс erc20 токена
            contract = self._get_contract(token)
            erc20_balance_wei = contract.functions.balanceOf(address).call()
            balance = Amount(erc20_balance_wei, decimals=token.decimals, wei=True)
        return balance

    def _validate_native_transfer_value(self, tx_params: dict) -> None:
        """
        Проверка возможности отправки нативного токена и корректировка суммы перевода, если недостаточно средств
        в исходном словаре tx_params
        :param tx_params: параметры транзакции c указанным value
        """
        amount = Amount(tx_params['value'], wei=True)
        l1_fee = self._get_l1_fee(tx_params)
        gues_gas = self.w3.eth.estimate_gas(
            {'from': self.account.address, 'to': self.account.address, 'value': 1})
        gues_gas_price = tx_params.get('maxFeePerGas', tx_params.get('gasPrice'))
        fee_spend = self._multiply(l1_fee.wei + gues_gas * gues_gas_price, 1.1, 1.2)
        balance = self.get_balance()
        if balance.wei - fee_spend - amount.wei >= 0:
            return

        message = f'баланс {self.chain.native_token}: {balance}, сумма: {amount} to {tx_params["to"]}'
        logger.warning(
            f'{self.account.profile_number} Недостаточно средств для отправки транзакции, {message}'
            f'Отправляем все доступные средства')
        tx_params['value'] = int(balance.wei -  self._multiply(fee_spend, 1.1, 1.2))
        if tx_params['value'] > 0:
            return
        logger.error(f'{self.account.profile_number} Недостаточно средств для отправки транзакции')
        raise ValueError('Недостаточно средств для отправки нативного токена')

    def send_token(self,
                   to_address: str | ChecksumAddress,
                   amount: Amount | int | float | None = None,
                   token: Optional[Token | str | ChecksumAddress] = None
                   ) -> str:
        """
        Отправка любых типов токенов, если не указан токен или адрес контракта токена, то отправка нативного токена,
        если при отправке токена не хватает средств, то отправляется все доступное количество.
        Если не передана сумма, отправляются все доступные токены.
        :param amount: сумма перевода, может быть объектом Amount, int, float или None
        :param to_address: адрес получателя
        :param token: объект Token или адрес контракта токена, если оставить пустым будет отправлен нативный токен
        :return: хэш транзакции
        """
        # если не передан токен, то отправляем нативный токен
        if token is None:
            token = Tokens.NATIVE_TOKEN
            token.chain = self.chain
            token.symbol = self.chain.native_token

        if amount is None:
            amount = Amount(self.get_balance(token=token).wei, decimals=token.decimals, wei=True)

        # приводим адрес к формату checksum
        to_address = to_checksum(to_address)

        # если передан адрес контракта, то получаем параметры токена и создаем объект Token
        if isinstance(token, str):
            symbol, decimals = self._get_token_params(token)
            token = Token(symbol, token, self.chain, decimals)

        # если передана сумма в виде числа, то создаем объект Amount
        if not isinstance(amount, Amount):
            amount = Amount(amount, decimals=token.decimals)

        # если передан нативный токен
        if token.type_token == TokenTypes.NATIVE:
            tx_params = self._prepare_tx(amount, to_address)
            self._validate_native_transfer_value(tx_params)
            amount = Amount(tx_params['value'], wei=True)
        else:
            # получаем баланс кошелька
            balance = self.get_balance(token=token)
            # проверка наличия средств на балансе
            if balance.wei < amount.wei:
                # если недостаточно средств, отправляем все доступные
                amount = balance
            # получаем контракт токена
            contract = self._get_contract(token)
            tx_params = self._prepare_tx()
            # создаем транзакцию
            tx_params = contract.functions.transfer(to_address, amount.wei).build_transaction(tx_params)

        self._estimate_gas(tx_params)
        # подписываем и отправляем транзакцию
        tx_hash = self._sign_and_send(tx_params)
        message = f' {amount} {token.symbol} на адрес {to_address} '
        logger.info(f'{self.account.profile_number} Транзакция отправлена [{message}] хэш: {tx_hash}')
        return tx_hash

    def _get_allowance(self, token: Token | str, spender: str | ChecksumAddress | ContractRaw) -> Amount:
        """
        Получение разрешенной суммы токенов на снятие
        :param token: объект Token или адрес контракта токена
        :param spender: адрес контракта, который получил разрешение на снятие токенов
        :return: объект Amount с разрешенной суммой
        """
        if token is None or token.type_token == TokenTypes.NATIVE:
            return Amount(0, wei=True)

        if isinstance(token, str):
            symbol, decimals = self._get_token_params(token)
            token = Token(symbol, token, self.chain, decimals)

        if isinstance(spender, ContractRaw):
            spender = spender.address

        if isinstance(spender, str):
            spender = Web3.to_checksum_address(spender)

        contract = self._get_contract(token)
        allowance = contract.functions.allowance(self.account.address, spender).call()
        return Amount(allowance, decimals=token.decimals, wei=True)

    def approve(self, token: Optional[Token, str], amount: Amount | int | float,
                spender: str | ChecksumAddress | ContractRaw) -> None:
        """
        Одобрение транзакции на снятие токенов
        :param token: токен, который одобряем или адрес контракта токена
        :param amount: сумма одобрения
        :param spender: адрес контракта, который получит разрешение на снятие токенов
        :return: None
        """
        if token is None or token.type_token == TokenTypes.NATIVE:
            return

        if isinstance(token, str):
            symbol, decimals = self._get_token_params(token)
            token = Token(symbol, token, self.chain, decimals)

        if isinstance(amount, (int, float)):
            amount = Amount(amount, decimals=token.decimals)

        allowed = self._get_allowance(token, spender)

        if amount.wei == 0 and allowed.wei == 0:
            return

        if amount.wei != 0 and allowed.wei >= amount.wei:
            return

        if isinstance(spender, ContractRaw):
            spender = spender.address

        contract = self._get_contract(token)
        tx_params = self._prepare_tx()
        tx_params = self._get_fee(tx_params)

        tx_params = contract.functions.approve(spender, amount.wei).build_transaction(tx_params)
        self._estimate_gas(tx_params)
        self._sign_and_send(tx_params)
        message = f'approve {amount} {token.symbol} to {spender}'
        logger.info(f'{self.account.profile_number} Транзакция отправлена {message}')

    def get_gas_price(self, gwei: bool = True) -> int:
        """
        Получение текущей ставки газа
        :return: ставка газа
        """
        gas_price = self.w3.eth.gas_price
        if gwei:
            return gas_price / 10 ** 9
        return gas_price

    def gas_price_wait(self, gas_limit: int = None) -> None:
        """
        Ожидание пока ставка газа не станет меньше лимита, осуществляется запрос каждые 5-10 секунд
        :param gas_limit: лимит ставки газа, если не передан, берется из конфига
        :return:
        """
        if not gas_limit:
            gas_limit = config.gas_price_limit

        while self.get_gas_price() > gas_limit:
            random_sleep(5, 10)

    def get_pk_from_seed(self, seed: str | list) -> str:
        """
        Получение приватного ключа из seed
        :param seed: seed фраза в виде строки или списка слов
        :return: приватный ключ
        """
        EthAccount.enable_unaudited_hdwallet_features()
        if isinstance(seed, list):
            seed = ' '.join(seed)
        return EthAccount.from_mnemonic(seed).key.hex()

    def is_eip_1559(self) -> bool:
        """
        Проверка наличия EIP-1559 на сети. Возвращает True, если EIP-1559 включен.
        :return: bool
        """
        fees_data = self.w3.eth.fee_history(50, 'latest')
        base_fee = fees_data['baseFeePerGas']
        if any(base_fee):
            return True
        return False

    def remove_approves(self):


        if not config.ETHERSCAN_API_KEY:
            logger.error('[onchain.remove_approves] Не указан ключ для etherscan')
            return

        logs = self._get_approval_logs()
        if not logs:
            logger.info('[onchain.remove_approves] Нет логов Approval')
            return

        approved = set()

        tokens_cache = {}

        for log in logs:
            token_address = log.get('address')
            spender_address = '0x' + log.get('topics')[2][26:]  # адрес spender
            approved.add((token_address, spender_address))

        for token_address, spender_address in approved:
            # получаем параметры токена
            token = tokens_cache.get(token_address)
            # кешируем токен для дальнейшего использования
            if not token:
                symbol, decimals = self._get_token_params(token_address)
                token = Token(symbol, token_address, self.chain, decimals)
                tokens_cache[token_address] = token

            self.approve(token, 0, spender_address)



    def _get_approval_logs(self):
        """
        Получение логов Approval(address,address,uint256) по адресу отправителя
        :return: список логов Approval из etherscan по блокчейну Chain
        """
        url = f'https://api.etherscan.io/v2/api'
        params = {
            'chainid': self.chain.chain_id,
            'module': 'logs',
            'action': 'getLogs',
            'fromBlock': 0,
            'toBlock': 'latest',
            'topic0': '0x' + self.w3.keccak(text='Approval(address,address,uint256)').hex(),
            'topic0_1': 'and',
            'topic1': '0x' + self.account.address[2:].rjust(64, '0'),
            'apikey': config.ETHERSCAN_API_KEY,
        }
        response = get_response(url, params)
        return response.get('result', [])



if __name__ == '__main__':
    pass
