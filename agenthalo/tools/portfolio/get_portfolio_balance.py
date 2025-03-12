from typing import Any, List, Optional

from agenthalo.config import Config
from agenthalo.core.token import TokenAmount
from agenthalo.core.tool import AgentHaloToolBase
from agenthalo.services.portfolio import Portfolio


class GetPortfolioBalance(AgentHaloToolBase):
    """List all the tokens owned by the user"""

    output_type = list  # TODO: not fetched automatically at a time

    def __init__(self, config: Config, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._portfolio = Portfolio.from_config(config)

    def forward(self, chain: Optional[str]) -> List[TokenAmount]:
        """
        Args:
            chain: Filter result for that chain if provided. Otherwise, execute for all chains
        """
        return ', '.join([str(token) for token in self._portfolio.get_token_balances(chain).get_all_balances()])
