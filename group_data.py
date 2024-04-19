import json
from typing import Union


PairData = tuple[int, int, int]
DayData = tuple[int, PairData, PairData, PairData]
WeekData = list[DayData]
DayDataTeacher = tuple[PairData, PairData, PairData, PairData, PairData, PairData]
WeekDataTeacher = list[DayDataTeacher]
WeekDataWeb = tuple[int, int, DayData, DayData, DayData, DayData, DayData, DayData]


def loadWeek(value:str) -> WeekData:
    return json.loads(value)


def loadWeekWeb(value:str) -> WeekDataWeb:
    return json.loads(value)


def saveWeek(value:WeekData) -> str:
    return json.dumps(value, ensure_ascii=False).replace(" ",  "")

