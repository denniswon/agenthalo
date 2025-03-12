from typing import List

import dotenv
from agenthalo.agent import HaloAgent
from agenthalo.config import Config
from agenthalo.core.tool import AgentHaloToolBase
from agenthalo.tools.core import GetTokenAddress
from agenthalo.tools.exchanges import GetTokenPrice

dotenv.load_dotenv()
config = Config()

# Initialize tools
tools: List[AgentHaloToolBase] = [
    GetTokenAddress(config),  # Get token address from a symbol
    GetTokenPrice(config),  # Get the price of a token pair from available DEXes given addresses
]

# Get LLM config for Anthropic
llm_config = config.get_default_llm_config("anthropic")
agent = HaloAgent(tools=tools, model_id=llm_config.model_id)

async def basic_quote(query: str) -> str | None:
    response = await agent.process_message(query)
    return response
