from typing import Tuple
import base58
import asyncio

from dstack_sdk import AsyncTappdClient, DeriveKeyResponse
from solders.keypair import Keypair
from web3 import Account

def byte_array_to_base58(byte_array: bytes) -> str:
    """
    Convert a byte array to a base58 encoded string.
    
    Args:
        byte_array (bytes or bytearray): The bytes to encode
        
    Returns:
        str: The base58 encoded string
    """
    # Encode the byte array to base58
    base58_string = base58.b58encode(byte_array)
    
    # Convert from bytes to string if needed
    if isinstance(base58_string, bytes):
        base58_string = base58_string.decode('utf-8')
        
    return base58_string

def derive_key_to_private_key(derive_key_response: DeriveKeyResponse, chain: str) -> str:
    if chain == "solana":
        return derive_key_response.toBytes(32)
    else:
        byte_array = derive_key_response.toBytes(32)
        # Convert each byte to a two-character hex string and join
        hex_string = "".join(f"{b:02x}" for b in byte_array)
        return f"0x{hex_string}"


def tappd_key_to_account_info(key: DeriveKeyResponse, chain: str) -> Tuple[str, str]:
    """Load account info from Tappd derive key response."""
    if chain == "solana":
        keypair = Keypair.from_seed(key.toBytes(32))
        # Encode the private key bytes to base58
        private_key = base58.b58encode(bytes(keypair)).decode()
        address = str(keypair.pubkey())
    else:
        private_key = derive_key_to_private_key(key, chain)
        account = Account.from_key(private_key)
        address = account.address
    return address, private_key


async def chain_account_info(chain: str) -> Tuple[str, str]:
    key = await AsyncTappdClient().derive_key(chain)
    return tappd_key_to_account_info(key, chain)

class Keystore:
    def __init__(self) -> None:
        self.data = {}
        self.initialized = False
        self._lock = asyncio.Lock()

    async def prepare(self) -> None:
        async with self._lock:
            self.data["ethereum"] = await AsyncTappdClient().derive_key("ethereum")
            self.data["ethereum_sepolia"] = await AsyncTappdClient().derive_key("ethereum_sepolia")
            self.data["base"] = await AsyncTappdClient().derive_key("base")
            self.data["base_sepolia"] = await AsyncTappdClient().derive_key("base_sepolia")
            self.data["solana"] = await AsyncTappdClient().derive_key("solana")
            self.initialized = True

    async def clean_up(self) -> None:
        async with self._lock:
            self.data = {}
            self.initialized = False
    
    def get(self, chain: str) -> str:
        return self.data[chain]

    def get_account_info(self, chain: str) -> Tuple[str, str]:
        return tappd_key_to_account_info(self.get(chain), chain)
