from typing import List

import dotenv
from agenthalo.agent import AgentHaloAgent
from agenthalo.config import Config
from agenthalo.core.tool import AgentHaloToolBase
from agenthalo.tools.core import GetTokenAddress
from agenthalo.tools.exchanges import ExecuteTokenSwap, GetTokenPrice
from agenthalo.tools.strategy_analysis import AnalyzeTradingStrategy, Strategy

dotenv.load_dotenv()
config = Config(network_env="test")  # Use a testnet environment (as defined in config/default.yaml)

# Initialize tools
llm_config = config.get_default_llm_config("anthropic")
strategy = Strategy(
    rules="Swap 3 USDC for WETH on Ethereum Sepolia when price below 10_000 USDC per WETH",
    model_id=llm_config.model_id,
)

tools: List[AgentHaloToolBase] = [
    GetTokenAddress(config),  # Get token address from a symbol
    GetTokenPrice(config),  # Get the price of a token pair from available DEXes given addresses
    AnalyzeTradingStrategy(strategy),  # Check a trading strategy
    ExecuteTokenSwap(config),  # Execute a token swap on a supported DEX (Uniswap V2/V3 on Ethereum and Base chains)
]

# Create the agent
agent = AgentHaloAgent(tools=tools, model_id=llm_config.model_id)

# Interact with the agent
async def _strategy_trade(query: str) -> str:
    response = await agent.process_message(query)
    return response

# Interact with the agent
async def main() -> None:
    response = await agent.process_message("Check strategy and initiate a trade if applicable")
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
