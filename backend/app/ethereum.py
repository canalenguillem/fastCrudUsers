from web3 import Web3
from sqlalchemy.orm import Session
from app.crud.blockchain import get_blockchain_by_name
from app.crud.erc20_token import get_token_by_id
from app.crud.blockchain import get_blockchain_by_id



from abis.ERC20_token import ERC20_ABI

def get_web3_instance(node_url: str) -> Web3:
    web3 = Web3(Web3.HTTPProvider(node_url))
    if not web3.is_connected():
        raise ConnectionError(f"Cannot connect to node at {node_url}")
    return web3

def get_balance(db: Session, blockchain_name: str, address: str) -> float:
    web3 = get_web3_instance(db, blockchain_name)
    balance_wei = web3.eth.get_balance(address)
    balance_eth = Web3.from_wei(balance_wei, 'ether')
    return balance_eth

def get_token_balance(db: Session, address: str, token_id: int) -> float:
    token = get_token_by_id(db, token_id)
    if not token:
        raise ValueError(f"No token found with id {token_id}")

    blockchain = get_blockchain_by_id(db, token.blockchain_id)
    if not blockchain:
        raise ValueError(f"No blockchain found with id {token.blockchain_id}")

    web3 = get_web3_instance(blockchain.node_url)
    contract = web3.eth.contract(address=Web3.to_checksum_address(token.contract_address), abi=ERC20_ABI)
    balance = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
    return Web3.from_wei(balance, 'ether')