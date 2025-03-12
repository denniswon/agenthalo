from typing import Any, AsyncGenerator, Optional
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from dstack_sdk import AsyncTappdClient

from agents.basic.portfolio import fetch_portfolio
from agents.basic.quote import basic_quote
from agents.basic.strategy import analyze_strategy
from agents.basic.swap import _swap
from agenthalo.services.tappd.keystore import Keystore

load_dotenv()

ks: Keystore

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global ks
    ks = Keystore()
    try:
        await ks.prepare()
        yield
    finally:
        await ks.clean_up()
        ks = None

app = FastAPI(lifespan=lifespan)


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


@app.get("/get_portfolio")
async def get_portfolio(chain: Optional[str] = None) -> Any:
    query = f"What's the portfolio balances on chain {chain}?"
    response = await fetch_portfolio(query)
    return response


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
    response = await analyze_strategy(query)
    return response
