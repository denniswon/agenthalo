from typing import Tuple

from dstack_sdk import AsyncTappdClient, DeriveKeyResponse
from solders.keypair import Keypair
from web3 import Account


def convert_key_to_hex(derive_key_response: DeriveKeyResponse) -> str:
    byte_array = derive_key_response.toBytes(32)
    # Convert each byte to a two-character hex string and join
    hex_string = "".join(f"{b:02x}" for b in byte_array)
    return f"0x{hex_string}"


def tappd_key_to_account_info(key: DeriveKeyResponse, chain: str) -> Tuple[str, str]:
    """Load account info from Tappd derive key response."""
    private_key = convert_key_to_hex(key)
    if chain == "solana":
        keypair = Keypair.from_base58_string(private_key)
        address = str(keypair.pubkey())
    else:
        account = Account.from_key(private_key)
        address = account.address
    return address, private_key


async def chain_account_info(chain: str) -> Tuple[str, str]:
    key = await AsyncTappdClient().derive_key(chain)
    return tappd_key_to_account_info(key, chain)
