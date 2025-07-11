import datetime

from src.app.api.models.models import Duration, Interval, Date


class GraphicService:
    def __init__(self, graphic: dict):
        self.days = graphic['days']
        self.timeslots = graphic['timeslots']

    async def get_day_by_date(self, date: datetime.date):
        for day in self.days:
            if day['date'] == str(date):
                return day
        return None

    async def get_intervals_by_day_id(self, day_id: int):
        res = []
        for slot in self.timeslots:
            if slot['day_id'] == day_id:
                res.append({"start": slot['start'], "end": slot["end"]})
        return res

    async def get_busy_intervals(self, date: datetime.date):
        day = await self.get_day_by_date(date)
        if day:
            return await self.get_intervals_by_day_id(day['id'])
        return []

    async def get_free_intervals(self, date: datetime.date):
        day = await self.get_day_by_date(date)
        if not day:
            return []
        busy_intervals = await self.get_busy_intervals(date)
        if busy_intervals:
            busy_intervals.sort(key=lambda x: x['start'])
        free_intervals = []
        if not busy_intervals:
            return [{'date': date, "start": day["start"], "end": day["end"]}]

        if busy_intervals[0]["start"] > day["start"]:
            free_intervals.append({
                "date": date,
                "start": day["start"],
                "end": busy_intervals[0]["start"]
            })
        for i in range(len(busy_intervals) - 1):
            current_end = busy_intervals[i]["end"]
            next_start = busy_intervals[i + 1]["start"]

            if current_end < next_start:
                free_intervals.append({
                    'date': date,
                    "start": current_end,
                    "end": next_start
                })
        last_interval = busy_intervals[-1]
        if last_interval["end"] < day["end"]:
            free_intervals.append({
                "date": date,
                "start": last_interval["end"],
                "end": day["end"]
            })

        return free_intervals

    async def check_time(self, interval: Interval):
        free_intervals = await self.get_free_intervals(interval.date)
        if not free_intervals:
            return False
        start_str = interval.start.strftime("%H:%M")
        end_str = interval.end.strftime("%H:%M")

        for interval in free_intervals:
            if start_str >= interval['start'] and end_str <= interval['end']:
                return True
        return False

    async def get_free_time(self, duration: Duration):
        duration_td = datetime.timedelta(
            hours=duration.hours,
            minutes=duration.minutes
        )

        all_free_intervals = []
        for day in self.days:
            date = datetime.datetime.strptime(day['date'], '%Y-%m-%d').date()
            free_intervals = await self.get_free_intervals(date)
            all_free_intervals.extend(free_intervals)

        for interval in all_free_intervals:
            start_time = datetime.datetime.strptime(interval['start'], '%H:%M')
            end_time = datetime.datetime.strptime(interval['end'], '%H:%M')

            if (start_time + duration_td) <= end_time:
                return {
                    "date": interval.get('date', ''),
                    "start": interval['start'],
                    "end": interval['end']
                }

        return None