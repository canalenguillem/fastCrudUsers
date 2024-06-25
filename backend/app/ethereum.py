from web3 import Web3
from app.crud.blockchain import get_blockchain_by_name
from sqlalchemy.orm import Session


def get_web3_instance(db: Session, blockchain_name: str) -> Web3:
    blockchain = get_blockchain_by_name(db, blockchain_name)
    if not blockchain:
        raise ValueError(f"No blockchain found with name {blockchain_name}")

    web3 = Web3(Web3.HTTPProvider(blockchain.node_url))
    if not web3.is_connected():
        raise ConnectionError(f"Cannot connect to {blockchain_name} node")
    return web3


def get_balance(db: Session, blockchain_name: str, address: str) -> float:
    web3 = get_web3_instance(db, blockchain_name)
    balance_wei = web3.eth.get_balance(address)
    balance_eth = Web3.from_wei(balance_wei, 'ether')
    return balance_eth
