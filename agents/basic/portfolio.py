from typing import List

import dotenv
from agenthalo.agent import AgentHaloAgent
from agenthalo.config import Config
from agenthalo.core.tool import AgentHaloToolBase
from agenthalo.tools.portfolio import GetPortfolioBalance

dotenv.load_dotenv()
config = Config()

# Initialize tools
tools: List[AgentHaloToolBase] = [
    GetPortfolioBalance(config),
]

# Get LLM config for Anthropic
llm_config = config.get_default_llm_config("anthropic")
agent = AgentHaloAgent(tools=tools, model_id=llm_config.model_id)

async def _portfolio() -> str:
    response = await agent.process_message("Get portfolio balance on Ethereum Sepolia")
    return response
    