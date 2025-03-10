import asyncio
from typing import List

import dotenv
from newtonswarm.agent.agent import NewtonSwarmAgent
from newtonswarm.agent.clients import TerminalClient
from newtonswarm.config import Config
from newtonswarm.core.tool import NewtonSwarmToolBase
from newtonswarm.tools.alchemy import GetAlchemyPriceHistoryBySymbol
from newtonswarm.tools.cookie.cookie_metrics import GetCookieMetricsBySymbol, GetCookieMetricsPaged
from newtonswarm.tools.forecasting import ForecastTokenPrice


class ForecastingAgent(NewtonSwarmAgent):
    """
    This example demonstrates a forecasting agent that uses the `ForecastTokenPrice` to forecast the price of a token.
    The agent and the tool are both experimental. Neither have been validated for accuracy -- these are meant to serve
    as examples of more innovative ways to use LLMs and agents in DeFi use cases such as trading.

    Example prompts:
    > What do you think the price of VIRTUAL will be in 6 hours?
    > Predict the price of AIXBT over the next hour in 5-minute increments.
    """

    def __init__(self, model_id: str) -> None:
        tools: List[NewtonSwarmToolBase] = [
            GetAlchemyPriceHistoryBySymbol(),
            GetCookieMetricsBySymbol(),
            GetCookieMetricsPaged(),
            ForecastTokenPrice(),
        ]

        hints = """P.S. Here are some hints to help you succeed:
        - Use the `GetAlchemyPriceHistoryBySymbol` tool to get the historical price data for the token
        - Use the `GetCookieMetricsBySymbol` tool to get metrics about the subject token
        - Use the `GetCookieMetricsPaged` tool to get a broader market overview of related AI agent tokens
        - Use the `ForecastTokenPrice` once you have gathered the necessary data to produce a forecast
        - Please respond with the output of the `ForecastTokenPrice` directly -- we don't need to reformat it.
        """

        super().__init__(tools=tools, model_id=model_id, hints=hints)


async def main() -> None:
    dotenv.load_dotenv()
    config = Config()
    llm_config = config.get_default_llm_config("anthropic")

    agent = ForecastingAgent(model_id=llm_config.model_id)

    terminal = TerminalClient("NewtonSwarm terminal", agent)
    await asyncio.gather(
        terminal.start(),
    )


if __name__ == "__main__":
    asyncio.run(main())
