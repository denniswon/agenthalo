from typing import List

import dotenv
from newtonswarm.agent import NewtonSwarmAgent
from newtonswarm.config import Config
from newtonswarm.core.tool import NewtonSwarmToolBase
from newtonswarm.tools.portfolio import GetPortfolioBalance

dotenv.load_dotenv()
config = Config()

# Initialize tools
tools: List[NewtonSwarmToolBase] = [
    GetPortfolioBalance(config),
]

# Get LLM config for Anthropic
llm_config = config.get_default_llm_config("anthropic")
agent = NewtonSwarmAgent(tools=tools, model_id=llm_config.model_id)

async def _portfolio() -> str:
    response = await agent.process_message("Get portfolio balance on Ethereum Sepolia")
    return response
    