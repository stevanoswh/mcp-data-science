import pytest
import pytest_asyncio
from fastmcp import Client
from servers.dataops import app

@pytest_asyncio.fixture
async def client():
    async with Client(app) as c:
        yield c

@pytest.mark.asyncio
async def test_ingest_s3(client):
    result = await client.call_tool("ingest_s3", {"s3_uri": "s3://acme/churn.csv"})
    assert isinstance(result[0].text, str)

@pytest.mark.asyncio
async def test_validate_df(client):
    result = await client.call_tool("validate_df", {"path": "/tmp/churn.csv"})
    assert result == []
