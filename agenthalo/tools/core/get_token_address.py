from typing import Any

from agenthalo.config import Config
from agenthalo.core.tool import AgentHaloToolBase


class GetTokenAddress(AgentHaloToolBase):
    """Get the token address for known token symbols"""

    def __init__(self, config: Config, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._config = config

    def forward(self, token_symbol: str, chain: str) -> str:
        """
        Args:
            token_symbol: The token symbol to get the address for
            chain: The chain to get the address for
        """
        return self._config.get_chain_config(chain).get_token_info(token_symbol).address
