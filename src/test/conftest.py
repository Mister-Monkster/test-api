from typing import AsyncGenerator
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest_asyncio.fixture(scope="function")
async def configured_app() -> AsyncGenerator[FastAPI, None]:
    yield app


@pytest_asyncio.fixture(scope="function")
async def async_client(configured_app: FastAPI):
    BASE_URL = "http://test"
    async with AsyncClient(transport=ASGITransport(app=configured_app), base_url=BASE_URL) as client:
        yield client
