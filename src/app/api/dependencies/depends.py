from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient

from src.app.api.services.service import GraphicService


async def get_graphic():
    url = "https://ofc-test-01.tspb.su/test-task/"
    async with AsyncClient() as client:
        response = await client.get(url)
        return response.json()

GraphicDep = Annotated[dict, Depends(get_graphic)]


async def get_service(graphic: GraphicDep) -> GraphicService:
    return  GraphicService(graphic)


ServiceDep = Annotated[GraphicService, Depends(get_service)]