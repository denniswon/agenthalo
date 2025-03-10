from dotenv import load_dotenv
from examples.basic.quote import basic_quote
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
    response = await basic_quote("What's the current price of AIXBT in USDC on Base for Uniswap v3?")
    return response
