import logging
from web3 import Web3
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.crud.blockchain import get_blockchain_by_name
from app.crud.erc20_token import get_token_by_id
from app.crud.blockchain import get_blockchain_by_id

from app.crud.dex import get_dex_by_id
from app.utils.load_abi import load_abi_from_path



from abis.ERC20_token import ERC20_ABI

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

def get_last_transactions(db: Session, dex_id: int, num_transactions: int = 10):
    try:
        todie=1000
        print("in get_last_transaction")
        dex = get_dex_by_id(db, dex_id)
        if not dex:
            raise ValueError(f"No DEX found with id {dex_id}")
        print(f"dex found {dex}")

        blockchain = get_blockchain_by_id(db, dex.blockchain_id)
        if not blockchain:
            raise ValueError(f"No blockchain found with id {dex.blockchain_id}")
        print(f"blockchainfound {blockchain}")

        web3 = get_web3_instance(blockchain.node_url)
        print(f"web 3 {web3.is_connected()}")
        factory_abi = load_abi_from_path(dex.factory_abi_path)
        print(f"factory_abi ")
        factory_contract = web3.eth.contract(
            address=Web3.to_checksum_address(dex.factory_address), abi=factory_abi)

        latest_block = web3.eth.block_number
        print(f"lates_block {latest_block}")
        transactions = []

        while len(transactions) < num_transactions and latest_block >= 0 and todie>0:
            todie=todie-1
            block = web3.eth.get_block(latest_block, full_transactions=True)
            print(f"block: {block}")
            for tx in block.transactions:
                if tx.to and tx.to.lower() == dex.factory_address.lower():
                    transactions.append(tx)
                    if len(transactions) == num_transactions:
                        break
            latest_block -= 1

        return transactions
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

def get_liquidity_amounts(db: Session, dex_id: int, token0_address: str, token1_address: str):
    dex = get_dex_by_id(db, dex_id)
    if not dex:
        raise ValueError(f"No DEX found with id {dex_id}")

    blockchain = get_blockchain_by_id(db, dex.blockchain_id)
    if not blockchain:
        raise ValueError(f"No blockchain found with id {dex.blockchain_id}")

    web3 = get_web3_instance(blockchain.node_url)
    factory_contract = web3.eth.contract(address=Web3.to_checksum_address(dex.factory_address), abi=load_abi_from_path(dex.factory_abi_path))
    router_contract = web3.eth.contract(address=Web3.to_checksum_address(dex.router_address), abi=load_abi_from_path(dex.router_abi_path))

    pair_address = factory_contract.functions.getPair(token0_address, token1_address).call()
    print(f"pair address {pair_address}")
    if pair_address == Web3.to_checksum_address("0x0000000000000000000000000000000000000000"):
        raise ValueError(f"No liquidity pair found for tokens {token0_address} and {token1_address}")

    pair_contract = web3.eth.contract(address=pair_address, abi=load_abi_from_path("abis/pair.json"))  # Replace with actual path to Pair ABI
    reserves = pair_contract.functions.getReserves().call()

    # Assuming token0 is the first token in the pair
    token0_amount = reserves[0]
    token1_amount = reserves[1]

    return {
        "token0": Web3.from_wei(token0_amount, 'ether'),
        "token1": Web3.from_wei(token1_amount, 'ether')
    }
#inc 0x2fa878Ab3F87CC1C9737Fc071108F904c0B0C95d
#edai 0xefD766cCb38EaF1dfd701853BFCe31359239F305
#plsx 0x95B303987A60C71504D99Aa1b13B4DA07b0790ab

def get_token_price(db: Session, dex_id: int, token0_address: str, token1_address: str) -> float:
    amounts = get_liquidity_amounts(db, dex_id, token0_address, token1_address)
    token0_amount = float(amounts['token0'])
    token1_amount = float(amounts['token1'])
    if token0_amount == 0:
        raise ValueError("Token0 amount is zero, cannot calculate price")
    price = token1_amount / token0_amount
    return price