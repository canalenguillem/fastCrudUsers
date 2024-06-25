from web3 import Web3
from sqlalchemy.orm import Session
from app.crud.blockchain import get_blockchain_by_name
from app.crud.erc20_token import get_tokens_by_blockchain_id

from abis.ERC20_token import ERC20_ABI

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

def get_token_balances(db: Session, blockchain_name: str, address: str) -> dict:
    web3 = get_web3_instance(db, blockchain_name)
    blockchain = get_blockchain_by_name(db, blockchain_name)
    tokens = get_tokens_by_blockchain_id(db, blockchain.id)
    balances = {}
    for token in tokens:
        contract = web3.eth.contract(address=Web3.to_checksum_address(token.contract_address), abi=ERC20_ABI)
        balance = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
        balances[token.symbol] = Web3.from_wei(balance, 'ether')
    return balances
