from web3 import Web3
from decouple import config

# Leer la URL del nodo Ethereum desde el archivo .env
ethereum_node_url = config("RPC_PULSE")

# Conectar al nodo Ethereum
web3 = Web3(Web3.HTTPProvider(ethereum_node_url))

# Verificar si estamos conectados
if not web3.is_connected():
    raise ConnectionError("No se puede conectar a la red Ethereum")

# Ejemplo de función para obtener el saldo de una dirección


def get_balance(address: str) -> float:
    balance_wei = web3.eth.get_balance(address)
    balance_eth = web3.from_wei(balance_wei, 'ether')
    return balance_eth
