from typing import List

import dotenv
from agenthalo.agent import AgentHaloAgent
from agenthalo.config import Config
from agenthalo.core.tool import AgentHaloToolBase
from agenthalo.tools.core import GetTokenAddress
from agenthalo.tools.exchanges import ExecuteTokenSwap, GetTokenPrice

dotenv.load_dotenv()
config = Config(network_env="test")  # Use a testnet environment (as defined in config/default.yaml)

# Initialize tools
tools: List[AgentHaloToolBase] = [
    GetTokenAddress(config),  # Get token address from a symbol
    GetTokenPrice(config),  # Get the price of a token pair from available DEXes given addresses
    # GetTokenPrice outputs a quote needed for ExecuteTokenSwap tool
    ExecuteTokenSwap(config),  # Execute a token swap on a supported DEX
]

# Create the agent
llm_config = config.get_default_llm_config("anthropic")
agent = AgentHaloAgent(tools=tools, model_id=llm_config.model_id)

# Interact with the agent
async def _swap(query: str) -> str:
    response = await agent.process_message(query)
    return response

# Interact with the agent
async def main() -> None:
    response = await agent.process_message("Swap 3 USDC for WETH on Ethereum Sepolia")
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
