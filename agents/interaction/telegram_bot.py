import asyncio
import logging
from typing import List

import dotenv
from agenthalo.agent.agent import AgentHaloAgent
from agenthalo.agent.clients.telegram_bot import TelegramBot
from agenthalo.config import Config
from agenthalo.core.tool import AgentHaloToolBase
from agenthalo.tools.alchemy import GetAlchemyPriceHistoryByAddress, GetAlchemyPriceHistoryBySymbol
from agenthalo.tools.cookie import (
    GetCookieMetricsByContract,
    GetCookieMetricsBySymbol,
    GetCookieMetricsByTwitter,
    GetCookieMetricsPaged,
)
from agenthalo.tools.core import GetTokenAddress, GetUsdPrice
from agenthalo.tools.exchanges import ExecuteTokenSwap, GetTokenPrice

logging.getLogger("smolagents").setLevel(logging.ERROR)


async def main() -> None:
    dotenv.load_dotenv()
    config = Config()

    tools: List[AgentHaloToolBase] = [
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
    agent = AgentHaloAgent(tools=tools, model_id=llm_config.model_id)
    bot_token = config.get("telegram", {}).get("bot_token")
    tg_bot = TelegramBot(bot_token=bot_token, agent=agent)

    await asyncio.gather(
        tg_bot.start(),
    )


if __name__ == "__main__":
    asyncio.run(main())
