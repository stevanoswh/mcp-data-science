import pytest
import pytest_asyncio
import json
from fastmcp import Client
from servers.deployer import app

@pytest_asyncio.fixture
async def client():
    async with Client(app) as c:
        yield c

@pytest.mark.asyncio
async def test_push_k8s(client):
    result = await client.call_tool("push_k8s", {"model_path": "/tmp/model.joblib"})
    assert isinstance(result[0].text, str)

@pytest.mark.asyncio
async def test_monitor_drift(client):
    result = await client.call_tool("monitor_drift", {"deployment": "v1.0.0"})
    assert isinstance(json.loads(result[0].text), dict)

@pytest.mark.asyncio
async def test_rollback(client):
    result = await client.call_tool("rollback", {"deployment": "v1.0.0", "tag": "v0.9.0"})
    assert isinstance(result[0].text, str)