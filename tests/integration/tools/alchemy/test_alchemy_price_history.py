from alphaswarm.services.alchemy import AlchemyClient
from alphaswarm.tools.alchemy.alchemy_price_history import AlchemyPriceHistoryBySymbol, AlchemyPriceHistoryByAddress


def test_get_price_history_by_symbol(alchemy_client: AlchemyClient) -> None:
    tool = AlchemyPriceHistoryBySymbol(alchemy_client)
    result = tool.forward(symbol="USDC", history=1)

    assert result.data[0].value > 0.1


def test_get_price_history_by_address(alchemy_client: AlchemyClient) -> None:
    tool = AlchemyPriceHistoryByAddress(alchemy_client)
    usdc_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    result = tool.forward(address=usdc_address, network="base-mainnet", history=1)
    assert result.data[0].value > 0.1
