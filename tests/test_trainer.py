import pytest
import pytest_asyncio
import json
from fastmcp import Client
from servers.trainer import app

@pytest_asyncio.fixture
async def client():
    async with Client(app) as c:
        yield c

@pytest.mark.asyncio
async def test_train(client):
    result = await client.call_tool("train", {"path": "/tmp/churn.csv", "target": "churn"})
    assert isinstance(result[0].text, str)

@pytest.mark.asyncio
async def test_evaluate(client):
    result = await client.call_tool("evaluate", {"model_path": "/tmp/model.joblib"})
    assert isinstance(json.loads(result[0].text), dict)
