from keyring import get_password
from pydantic import SecretStr

class Config:
    """
    Класс для хранения конфигурационных данных
    """
    BINANCE_API_KEY = SecretStr(get_password('binance', 'api_key'))
    BINANCE_SECRET_KEY = SecretStr(get_password('binance', 'secret_key'))
    PROXY = SecretStr('http://' + get_password('proxy', 'exchange_proxy'))
    address = ''
config = Config()
