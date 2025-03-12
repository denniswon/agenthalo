from typing import List

import dotenv
from agenthalo.agent import HaloAgent
from agenthalo.config import Config
from agenthalo.core.tool import AgentHaloToolBase
from agenthalo.tools.portfolio import GetPortfolioBalance

dotenv.load_dotenv()

async def fetch_portfolio(query: str) -> str | None:
    config = Config(network_env="test")
    await config.init()

    # Initialize tools
    tools: List[AgentHaloToolBase] = [
        GetPortfolioBalance(config),
    ]

    # Get LLM config for Anthropic
    llm_config = config.get_default_llm_config("anthropic")
    agent = HaloAgent(tools=tools, model_id=llm_config.model_id)

    response = await agent.process_message(query)
    return response
