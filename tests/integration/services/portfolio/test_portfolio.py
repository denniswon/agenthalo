import pytest

from agenthalo.config import ChainConfig, Config, WalletInfo
from agenthalo.services.alchemy import AlchemyClient
from agenthalo.services.chains import EVMClient
from agenthalo.services.portfolio import Portfolio
from agenthalo.services.portfolio.portfolio_evm import PortfolioEvm
from agenthalo.services.portfolio.portfolio_base import PortfolioBase


@pytest.fixture
def eth_sepolia_config(default_config: Config) -> ChainConfig:
    return default_config.get_chain_config("ethereum_sepolia")


@pytest.fixture
def eth_sepolia_portfolio(eth_sepolia_config: ChainConfig, alchemy_client: AlchemyClient) -> PortfolioEvm:
    return PortfolioEvm(WalletInfo.from_chain_config(eth_sepolia_config), EVMClient(eth_sepolia_config), alchemy_client)


@pytest.fixture
def portfolio(chain: str, default_config: Config, alchemy_client: AlchemyClient) -> PortfolioBase:
    chain_config = default_config.get_chain_config(chain)
    return Portfolio.from_chain(chain_config)


@pytest.mark.skip("Need wallet")
def test_portfolio_get_balances(default_config: Config, alchemy_client: AlchemyClient) -> None:
    portfolio = Portfolio.from_config(default_config)
    result = portfolio.get_token_balances()
    assert len(result.get_non_zero_balances()) > 3


chains = ["ethereum", "ethereum_sepolia", "base", "solana"]


@pytest.mark.parametrize("chain", chains)
@pytest.mark.skip("Need wallet")
def test_portfolio_get_swaps(chain: str, portfolio: PortfolioBase, default_config: Config) -> None:
    result = portfolio.get_swaps()
    for item in result:
        print(item.to_short_string())
