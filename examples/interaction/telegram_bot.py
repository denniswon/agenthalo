import asyncio
import logging
from typing import List

import dotenv
from newtonswarm.agent.agent import NewtonSwarmAgent
from newtonswarm.agent.clients.telegram_bot import TelegramBot
from newtonswarm.config import Config
from newtonswarm.core.tool import NewtonSwarmToolBase
from newtonswarm.tools.alchemy import GetAlchemyPriceHistoryByAddress, GetAlchemyPriceHistoryBySymbol
from newtonswarm.tools.cookie import (
    GetCookieMetricsByContract,
    GetCookieMetricsBySymbol,
    GetCookieMetricsByTwitter,
    GetCookieMetricsPaged,
)
from newtonswarm.tools.core import GetTokenAddress, GetUsdPrice
from newtonswarm.tools.exchanges import ExecuteTokenSwap, GetTokenPrice

logging.getLogger("smolagents").setLevel(logging.ERROR)


async def main() -> None:
    dotenv.load_dotenv()
    config = Config()

    tools: List[NewtonSwarmToolBase] = [
        GetUsdPrice(),
        GetTokenAddress(config),
        GetTokenPrice(config),
        GetAlchemyPriceHistoryByAddress(),
        GetAlchemyPriceHistoryBySymbol(),
        GetCookieMetricsByContract(),
        GetCookieMetricsBySymbol(),
        GetCookieMetricsByTwitter(),
        GetCookieMetricsPaged(),
        ExecuteTokenSwap(config),
    ]  # Add your tools here

    llm_config = config.get_default_llm_config("anthropic")
    agent = NewtonSwarmAgent(tools=tools, model_id=llm_config.model_id)
    bot_token = config.get("telegram", {}).get("bot_token")
    tg_bot = TelegramBot(bot_token=bot_token, agent=agent)

    await asyncio.gather(
        tg_bot.start(),
    )


if __name__ == "__main__":
    asyncio.run(main())
