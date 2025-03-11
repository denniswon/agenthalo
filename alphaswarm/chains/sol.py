import logging
from typing import Dict, Optional

from eth_typing import ChecksumAddress
from solana.rpc import api
from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey  # type: ignore

from ..config import Config, TokenInfo
from .base import Web3Client

logger = logging.getLogger(__name__)

# Define supported chains
SUPPORTED_CHAINS = {"solana", "solana_devnet"}


class SolanaClient(Web3Client):
    """Client for interacting with Solana chains"""

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._clients: Dict[str, api.Client] = {}  # cache for RPC clients
        logger.info("Initialized SolanaClient")

    def _get_client(self, chain: str) -> api.Client:
        """Get or create RPC client for the chain"""
        if chain not in self._clients:
            rpc_url = self.config.get_chain_config(chain).rpc_url
            self._clients[chain] = api.Client(rpc_url)
        return self._clients[chain]

    def _validate_chain(self, chain: str) -> None:
        """Validate that the chain is supported by SolanaClient"""
        if chain not in SUPPORTED_CHAINS:
            raise ValueError(f"Chain '{chain}' is not supported by SolanaClient. Supported chains: {SUPPORTED_CHAINS}")

    def to_checksum_address(self, address: str, chain: str) -> ChecksumAddress:
        """Convert address to checksum format"""
        self._validate_chain(chain)
        raise NotImplementedError("Checksum address not applicable for Solana")

    def get_token_info(self, token_address: str, chain: str) -> Optional[TokenInfo]:
        """Get token info by token contract address"""
        self._validate_chain(chain)
        raise NotImplementedError("Token info not yet implemented for Solana")

    def get_token_balance(self, token: str, wallet_address: str, chain: str) -> Optional[float]:
        """Get token balance for a wallet address.

        Args:
            token: Token name (resolved via Config) or 'SOL' for native SOL
            wallet_address: The wallet address to check balance for
            chain: The chain to query ('solana' or 'solana_devnet')

        Returns:
            Optional[float]: The token balance in human-readable format, or None if error
        """
        try:
            self._validate_chain(chain)
            client = self._get_client(chain)

            chain_config = self.config.get_chain_config_or_none(chain)
            # Get token info from chain_config section
            if chain_config is None:
                logger.error(f"No token configuration found for chain {chain}")
                return None

            token_info = chain_config.get_token_info_or_none(token)
            if token_info is None:
                logger.error(f"No token configuration found for token {token}")
                return None

            # Handle native SOL balance
            if token.upper() == "SOL":
                pubkey = Pubkey.from_string(wallet_address)
                response = client.get_balance(pubkey)
                if response.value is not None:
                    # Convert lamports to SOL (1 SOL = 10^9 lamports)
                    return float(response.value) / 1_000_000_000
                return None

            token_address = token_info.address
            decimals = token_info.decimals

            # For SPL tokens
            try:
                token_pubkey = Pubkey.from_string(token_address)
                wallet_pubkey = Pubkey.from_string(wallet_address)

                # Get token accounts
                opts = TokenAccountOpts(mint=token_pubkey)
                token_accounts = client.get_token_accounts_by_owner_json_parsed(wallet_pubkey, opts)

                if not token_accounts.value:
                    return 0.0  # No token account found means 0 balance

                # Get balance from account data
                account_data = token_accounts.value[0].account.data.parsed

                # Type checking to prevent issues (and lint errors)
                if not isinstance(account_data, dict):
                    raise ValueError("Unexpected data format: 'parsed' is not a dict")

                info = account_data.get("info")
                if not isinstance(info, dict):
                    raise ValueError("'info' is not a dict")

                token_amount = info.get("tokenAmount")
                if not isinstance(token_amount, dict):
                    raise ValueError("'tokenAmount' is not a dict")

                amount_json = token_amount["amount"]
                if isinstance(amount_json, (str, int, float)):
                    balance = int(amount_json)
                elif amount_json is None:
                    balance = 0  # or handle None how you like
                else:
                    raise TypeError(f"Unexpected type for amount: {type(amount_json)}")

                decimals_json = token_amount["decimals"]
                if isinstance(decimals_json, (str, int, float)):
                    decimals = int(decimals_json)
                elif amount_json is None:
                    decimals = 0  # or handle None how you like
                else:
                    raise TypeError(f"Unexpected type for decimals: {type(decimals)}")

                # Convert to human-readable format
                return float(balance) / (10**decimals)

            except Exception:
                logger.exception("Error getting SPL token balance")
                return None

        except Exception:
            logger.exception("Error in get_token_balance")
            return None
