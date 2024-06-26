import json
import os

def load_abi_from_path(abi_path: str) -> dict:
    print(f"in load_abi_from_path")
    if not os.path.exists(abi_path):
        raise FileNotFoundError(f"ABI not found at {abi_path}")
    print(f"is file founde {abi_path}? {os.path.exists(abi_path)}")
    with open(abi_path, 'r') as abi_file:
        return json.load(abi_file)
