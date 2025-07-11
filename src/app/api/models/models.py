import datetime
from pydantic import BaseModel, Field


class Date(BaseModel):
    date: datetime.date = datetime.date.today()

class Interval(Date):
    start: datetime.time
    end: datetime.time

class Duration(BaseModel):
    hours: int = Field(ge=0, le=8)
    minutes: int = Field(ge=0, le=59)