import xlrd
from xlrd.sheet import Sheet

import group_data
from group_data import PairData

from fuzzywuzzy.fuzz import ratio

PairDataStr = tuple[str, str, str]

GroupData = tuple[str, group_data.WeekData]


class ParseDataError(Exception):
    def __init__(self, *args):
        super().__init__(args)


def get_start(worksheet: Sheet) -> tuple[int, int]:
    for y in range(worksheet.nrows):
        x = -1
        for cell in worksheet.row(y):
            x += 1
            if "группа" in str(cell.value).lower():
                return x, y


def days_scan(worksheet: Sheet, x: int) -> tuple[list[int], list[int]]:
    datas = []
    lens = []
    for y in range(worksheet.nrows):
        getted = worksheet.cell(y, x).value
        if getted == 1:
            datas.append(y)
            lens.append(0)
        elif getted != "" and len(lens) > 0:
            lens[-1] = int(getted)

    return (datas, lens)


def groups_scan(worksheet: Sheet, y: int) -> list[int]:
    datas = []
    for x in range(worksheet.ncols):
        if "группа" in str(worksheet.cell(y, x).value).lower():
            datas.append(x)
    return datas


def get_pair(worksheet: Sheet, x: int, y: int) -> PairDataStr:

    return (
        str(worksheet.cell(y, x).value),
        str(worksheet.cell(y, x + 1).value),
        str(worksheet.cell(y, x + 2).value)
    )


def get_list_index(value: str, values: list[str]) -> int:
    if len(value) < 3:
        return -1

    best = 0
    bestI = 0
    i = -1
    for v in values:
        i += 1
        rt = ratio(value, v)
        if rt > best:
            best = rt
            bestI = i

    if best > 60:
        return bestI
    raise ParseDataError(f"Не найдено: {value}")


def pair_str_to_normal(value: PairDataStr, pairs: list[str], teachers: list[str]) -> PairData:
    result = [-1, -1, -1]
    p, t, c = value

    с = c.lower()

    result[0] = get_list_index(p, pairs)
    result[1] = get_list_index(t, teachers)

    if c == "":
        result[2] = -1
    elif c.startswith("с"):
        result[2] = 0
    elif c.startswith("б"):
        result[2] = 1
    elif c.count("\\") > 0:
        result[2] = 27
    elif c.endswith(".0"):
        lol = int(float(c))
        if lol < 0:
            result[2] = -1
        else:
            result[2] = lol + 1
    else:
        raise ParseDataError(f"Ожидался кабинет, получено: {c}")

    return result


def try_get_data(file: bytes, pairs: list[str], teachers: list[str]) -> list[GroupData]:

    workbook = xlrd.open_workbook_xls(file_contents=file)
    worksheet = workbook.sheet_by_index(0)

    startX, startY = get_start(worksheet)

    days_indices, days_lens = days_scan(worksheet, startX - 1)
    if len(days_indices) < 6:
        raise ParseDataError("Дней Меньше Шести!")
    groups_indices = groups_scan(worksheet, startY)

    week_datas: list[GroupData] = []

    for g in range(len(groups_indices)):
        week_data = group_data.WeekDataEmpty[:]
        for d in range(6):
            getPairs = []
            for i in range(days_lens[d]):
                pair = pair_str_to_normal(get_pair(worksheet, groups_indices[g], days_indices[d] + i), pairs, teachers)
                if (pair)[0] == -1:
                    week_data[d][0] += 1
                else:
                    getPairs.append(pair)

            if len(getPairs) >= 1: week_data[d][1] = getPairs[0]
            if len(getPairs) >= 2: week_data[d][2] = getPairs[1]
            if len(getPairs) >= 3: week_data[d][3] = getPairs[2]

        week_datas.append((str(worksheet.cell(startY, groups_indices[g]).value), week_data))
    return week_datas