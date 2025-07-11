import datetime
from pydantic import BaseModel

class Date(BaseModel):
    date: datetime.date = datetime.date.today()

class Interval(Date):
    start: datetime.time
    end: datetime.time

class Duration(BaseModel):
    hours: int
    minutes: int