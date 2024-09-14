import json
from typing import Union


PairData = list[int, int, int]
DayData = list[int, PairData, PairData, PairData]
TimeData = str
WeekData = list[DayData | TimeData]
DayDataTeacher = list[PairData, PairData, PairData, PairData, PairData, PairData]
WeekDataTeacher = list[DayDataTeacher]
WeekDataWeb = tuple[
    int, int,
    DayData, DayData, DayData, DayData, DayData, DayData,
    TimeData, TimeData, TimeData, TimeData, TimeData, TimeData
]
Settings = tuple[
    int,            # Id
    int | bool,     # Send Every Day
    int | bool,     # Send Every Week
    bool,           # Send Updates
    bool,           # Enable Time In Schedule
]

WeekDataEmpty: WeekData = [[0, [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]] for i in range(6)]


def loadWeek(value:str) -> WeekData:
    return json.loads(value)


def loadWeekWeb(value:str) -> WeekDataWeb:
    return json.loads(value)


def saveWeek(value:WeekData) -> str:
    return json.dumps(value, ensure_ascii=False).replace(" ",  "")

