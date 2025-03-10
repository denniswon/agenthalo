from dotenv import load_dotenv
from agents.basic.quote import basic_quote
from agents.basic.swap import _swap
from agents.basic.strategy import _strategy_trade
load_dotenv()

from fastapi import FastAPI
from dstack_sdk import AsyncTappdClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tdx_quote")
async def tdx_quote():
    client = AsyncTappdClient()
    result = await client.tdx_quote('test')
    return result

@app.get('/derive_key')
async def derive_key():
    client = AsyncTappdClient()
    result = await client.derive_key('test')
    return result

@app.get('/get_quote')
async def get_quote():
    query = "What's the current price of AIXBT in USDC on Base for Uniswap v3?"
    response = await basic_quote(query)
    return f"Query: {query}\nResponse: {response}"

@app.get('/swap')
async def swap():
    query = "Swap 3 USDC for WETH on Base Sepolia"
    response = await _swap(query)
    return f"Query: {query}\nResponse: {response}"

@app.get('/strategy_trade')
async def strategy_trade():
    query = "Check strategy and initiate a trade if applicable"
    response = await _strategy_trade(query)
    return f"Query: {query}\nResponse: {response}"
