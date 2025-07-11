from fastapi import APIRouter, Depends, Query, HTTPException

from app.api.dependencies.depends import ServiceDep
from app.api.models.models import Duration, Interval, Date

router = APIRouter(prefix="/test-api")

@router.get("/busy-slots")
async def get_busy_intervals(
    service: ServiceDep,
    date: Date = Depends()):
    try:
        res = await service.get_busy_intervals(date.date)
        if res:
            return res
        else:
            return {"ok": True, "detail": "Этот день полностью свободен."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении занятых интервалов: {str(e)}"
        )

@router.get("/free-slots")
async def get_free_time(
    service: ServiceDep,
    date: Date = Depends()) -> list[Interval] | dict:
    try:
        res = await service.get_free_intervals(date.date)
        if res:
            return res
        return {'ok': True, 'detail': "В этот день нет свободного времени."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении свободных интервалов: {str(e)}"
        )

@router.get('/check-time')
async def check_time(
    service: ServiceDep,
    interval: Interval = Depends()):
    try:
        res = await service.check_time(interval)
        return {'is_free': res}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при проверке времени: {str(e)}")


@router.get("/free-time")
async def get_free_time(
    service: ServiceDep,
    duration: Duration = Depends()) -> Interval | dict:
    try:
        res = await service.get_free_time(duration)
        if res:
            return res
        return {"ok": True, "detail": "На данный момент нет свободного времени для такой заявки."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при поиске свободного времени: {str(e)}"
        )
