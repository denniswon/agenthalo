import asyncio
import json
from typing import List, Mapping

import dotenv
from agenthalo.agent.agent import HaloAgent
from agenthalo.agent.clients import TerminalClient
from agenthalo.config import CONFIG_PATH, Config
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
from agenthalo.tools.portfolio import GetPortfolioBalance
from agenthalo.tools.strategy_analysis.generic import AnalyzeTradingStrategy
from agenthalo.tools.strategy_analysis.strategy import Strategy
from agenthalo.tools.telegram import SendTelegramNotification
from agenthalo.utils import read_text_file_to_string


async def main() -> None:
    dotenv.load_dotenv()
    config = Config()
    await config.init()

    telegram_config = config.get("telegram", {})
    telegram_bot_token = telegram_config.get("bot_token")
    chat_id = int(telegram_config.get("chat_id"))

    strategy = Strategy.from_file(filename=str(CONFIG_PATH / "momentum_strategy_config.md"))

    tools: List[AgentHaloToolBase] = [
        GetUsdPrice(),
        GetTokenAddress(config),
        GetTokenPrice(config),
        GetAlchemyPriceHistoryByAddress(),
        GetAlchemyPriceHistoryBySymbol(),
        AnalyzeTradingStrategy(strategy=strategy),
        GetCookieMetricsByContract(),
        GetCookieMetricsBySymbol(),
        GetCookieMetricsByTwitter(),
        GetCookieMetricsPaged(),
        SendTelegramNotification(telegram_bot_token=telegram_bot_token, chat_id=chat_id),
        ExecuteTokenSwap(config),
        GetPortfolioBalance(config),
    ]  # Add your tools here

    # Optional step to provide a custom system prompt.
    # If no custom system prompt is provided, a default one will be used.
    system_prompt = read_text_file_to_string(CONFIG_PATH / "trading_strategy_agent_system_prompt.txt")

    token_name_to_address: Mapping[str, str] = {
        "AIXBT (base)": "0x4F9Fd6Be4a90f2620860d680c0d4d5Fb53d1A825",
        "VIRTUAL (base)": "0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b",
        "VADER (base)": "0x731814e491571A2e9eE3c5b1F7f3b962eE8f4870",
    }

    system_prompt = system_prompt.replace("{{trading_strategy}}", strategy.rules)
    system_prompt = system_prompt.replace("{{token_name_to_address}}", json.dumps(token_name_to_address))

    # Optional hints
    hints = read_text_file_to_string(CONFIG_PATH / "trading_strategy_agent_hints.txt")

    llm_config = config.get_default_llm_config("anthropic")
    agent = HaloAgent(tools=tools, model_id=llm_config.model_id, system_prompt=system_prompt, hints=hints)

    terminal = TerminalClient("AgentHalo terminal", agent)
    await asyncio.gather(
        terminal.start(),
    )


if __name__ == "__main__":
    asyncio.run(main())
