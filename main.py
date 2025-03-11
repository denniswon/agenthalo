from typing import Any

from agents.basic.portfolio import _portfolio
from agents.basic.quote import basic_quote
from agents.basic.strategy import _strategy_trade
from agents.basic.swap import _swap
from dotenv import load_dotenv
from dstack_sdk import AsyncTappdClient
from fastapi import FastAPI

load_dotenv()

app = FastAPI()


@app.get("/")
async def read_root() -> Any:
    return {"Hello": "World"}


@app.get("/tdx_quote")
async def tdx_quote() -> Any:
    client = AsyncTappdClient()
    result = await client.tdx_quote("test")
    return result


@app.get("/derive_key")
async def derive_key() -> Any:
    client = AsyncTappdClient()
    result = await client.derive_key("test")
    return result


@app.get("/portfolio")
async def portfolio() -> Any:
    portfolio = await _portfolio()
    return portfolio


@app.get("/get_quote")
async def get_quote() -> Any:
    query = "What's the current price of AIXBT in USDC on Base for Uniswap v3?"
    response = await basic_quote(query)
    return response


@app.get("/swap")
async def swap() -> Any:
    query = "Swap 3 USDC for WETH on Ethereum Sepolia"
    response = await _swap(query)
    return response


@app.get("/strategy_trade")
async def strategy_trade() -> Any:
    query = "Check strategy and initiate a trade if applicable"
    response = await _strategy_trade(query)
    return response
