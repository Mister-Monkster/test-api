import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_busy_slots(async_client: AsyncClient):
    response = await async_client.get(
                                '/test-api/busy-slots',
                                    params={
                                        'date': "2025-02-16"
                                            }
                                    )
    correct_response = [{'start': '14:30', 'end': '18:00'}, {'start': '09:30', 'end': '11:00'}]
    assert response.status_code == 200
    assert response.json() == correct_response


@pytest.mark.asyncio
async def test_negative_busy_slots(async_client: AsyncClient):
    response = await async_client.get('/test-api/busy-slots', params={'date': "2025-20-16"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_free_time(async_client: AsyncClient):
    response = await async_client.get('/test-api/free-slots', params={'date': "2025-02-16"})
    correct_response = [
        {'date': '2025-02-16', 'start': '08:00:00', 'end': '09:30:00'},
        {'date': '2025-02-16', 'start': '11:00:00', 'end': '14:30:00'},
        {'date': '2025-02-16', 'start': '18:00:00', 'end': '22:00:00'}
    ]
    assert response.status_code == 200
    assert response.json() == correct_response


@pytest.mark.asyncio
async def test_negative_free_time(async_client: AsyncClient):
    response = await async_client.get('/test-api/free-slots', params={'date': "2025-20-16"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_check_time_false(async_client: AsyncClient):
    response = await async_client.get(
                                '/test-api/check-time',
                                    params={
                                        "date": "2025-02-16",
                                        "start": "14:30",
                                        "end": "15:30"
                                           }
    )
    correct_response = {"is_free": False}
    assert response.status_code == 200
    assert response.json() == correct_response


@pytest.mark.asyncio
async def test_check_time_true(async_client: AsyncClient):
    response = await async_client.get(
                                '/test-api/check-time',
                                    params={
                                        "date": "2025-02-16",
                                        "start": "08:00",
                                        "end": "09:30"
                                            }
                                    )
    correct_response = {"is_free": True}
    assert response.status_code == 200
    assert response.json() == correct_response


@pytest.mark.asyncio
async def test_negative_check_time(async_client: AsyncClient):
    response = await async_client.get(
                                 '/test-api/check-time',
                                      params={
                                          "date": "2025-20-16",
                                          "start": "8:00",
                                          "end": "9:30"
                                            }
                                      )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_is_free_true(async_client: AsyncClient):
    response = await async_client.get(
                                  '/test-api/free-time',
                                      params={
                                            "hours": 1,
                                            "minutes": 30
                                             }
                                      )
    correct_response = {'date': '2025-02-15', 'start': '12:00', 'end': '17:30'}
    assert response.status_code == 200
    assert response.json() == correct_response

@pytest.mark.asyncio
async def test_is_free_false(async_client: AsyncClient):
    response = await async_client.get(
                                  '/test-api/free-time',
                                      params={
                                            "hours": 10,
                                            "minutes": 30
                                             }
                                      )
    correct_response = {'ok': True, 'detail': 'На данный момент нет свободного времени для такой заявки.'}
    assert response.status_code == 200
    assert response.json() == correct_response


@pytest.mark.asyncio
async def test_negative_is_free_false(async_client: AsyncClient):
    response = await async_client.get(
                                  '/test-api/free-time',
                                      params={
                                            "hours": "test",
                                            "minutes": "test"
                                             }
                                      )
    assert response.status_code == 422





