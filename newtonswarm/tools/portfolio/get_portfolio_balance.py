from typing import Any, List, Optional

from newtonswarm.config import Config
from newtonswarm.core.token import TokenAmount
from newtonswarm.core.tool import NewtonSwarmToolBase
from newtonswarm.services.portfolio import Portfolio


class GetPortfolioBalance(NewtonSwarmToolBase):
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
        return self._portfolio.get_token_balances(chain).get_all_balances()
