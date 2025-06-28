import pytest
import pytest_asyncio
from fastmcp import Client
from servers.feature import app

@pytest_asyncio.fixture
async def client():
    async with Client(app) as c:
        yield c

@pytest.mark.asyncio
async def test_encode_cat(client):
    result = await client.call_tool("encode_cat", {"path": "/tmp/churn.csv"})
    assert isinstance(result[0].text, str)

@pytest.mark.asyncio
async def test_impute_null(client):
    result = await client.call_tool("impute_null", {"path": "/tmp/churn.csv"})
    assert isinstance(result[0].text, str)
