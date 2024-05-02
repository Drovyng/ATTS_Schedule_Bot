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

    to_return = (
        str(worksheet.cell(y, x).value),
        str(worksheet.cell(y, x + 1).value),
        str(worksheet.cell(y, x + 2).value)
    )

    return to_return


def get_list_index(value: str, values: list[str]) -> int:
    if len(value) < 3:
        return -1
    if value.count("\n") > 0 or value.count("   ") > 0:
        value = "Несколько"

    best = 0
    bestI = 0
    i = -1
    for v in values:
        i += 1
        rt = ratio(value.lower(), v.lower())
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
    elif c.count("к") > 0 and c.count("м") > 0 and c.index("к")+3 > c.index("м"):
        result[2] = 27
    elif c.count("к") > 0 and c.count("с") > 0 and c.index("к")+3 > c.index("с"):
        result[2] = 28
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

    gi = -1
    for g in groups_indices:
        gi += 1
        week_data = [[0, [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]][:] for i in range(6)]
        for d in range(6):
            hell = 0
            offs = 0
            for i in range(days_lens[d]):
                pair = pair_str_to_normal(get_pair(worksheet, g, days_indices[d] + i), pairs, teachers)
                if hell < 3:
                    if pair[0] == -1:
                        offs += 1
                    else:
                        hell += 1
                        week_data[d][hell] = pair
                week_data[d][0] = min(offs, hell)

        week_datas.append((str(worksheet.cell(startY, g).value), week_data))

    return week_datas

#
# from PIL import Image
# import imaginazer
#
# with open("C:\\Users\\информатика\\Desktop\\test.xls", "rb") as file:
#     pairs = ['Информатика', 'Математика', 'Физика', 'Русский язык', 'Литература', 'Химия', 'Основы Безопасности Жизнедеятельности', 'Обществознание', 'История', 'Иностранный язык', 'Физическая культура', 'Биология', 'География', 'Экономика', 'Основы микробиологии, физиологии питания, санитарии и гигиены', 'Техническое оснащение и организация рабочего места', 'МДК.01.01', 'Охрана труда', 'Основы товароведения продовольственных товаров', 'Технология слесарных работ', 'Допуски и технические измерения', 'Основы электротехники', 'Индивидуальный проект', 'Производственная практика', 'Учебная практика', 'Рисунок и живопись', 'Безопасность жизнедеятельности', 'МДК.02.02', 'Художественная резка овощей и фруктов', 'Организация обслуживания', 'Астрономия', 'Метрология и стандартизация', 'Автоматизация технологических процессов', 'Правовые основы профессиональной деятельности', 'МДК.01.02', 'Психология общения', 'Социальная адаптация и основы социально-правовых знаний', 'Основы технической графики', 'Основы материаловедения', 'Экономические и правовые основы производственной деятельности', 'МДК.03.01', 'Основы предпринимательской деятельности', 'Несколько']
#     teachers = ['Быленко М.И.', 'Борисова И.В.', 'Пасмурнова Е.М.', 'Плешкова О.Г.', 'Алексеева М.В.', 'Горелова Е.Н.', 'Комина Н.С.', 'Шумков М.А.', 'Аулова А.А.', 'Слюнякова И.В.', 'Якубовская Е.В.', 'Вертикова А.А.', 'Федорова Е.С.', 'Лукьянченко А.Е.', 'Воропаева М.В.', 'Миляева Ю.А.', 'Хитрова С.В.', 'Бекетов С.И.', 'Крышталева М.М.', 'Баранцова Ю.А.', 'Ковалева Н.Ю.', 'Такмазян В.П.', 'Согомонян А.А.', 'Шушарина В.В.', 'Бадоева Ю.А.', 'Агамирзоева В.А.', 'Шамота А.С.', 'Зайцева Г.Н.', 'Ашева Н.А.', 'Ломакина М.А.', 'Квочка В.В.', 'Матвеева Е.В.', 'Оленец Н.А.', 'Чикова А.Б.', 'Водинов К.Н.', 'Махова М.А.', 'Тороп И.А.', 'Несколько', 'Володько Е.В.', 'Костенко В.В.']
#     name, data = try_get_data(file.read(), pairs, teachers)[0]
#     print(data)
#     img = imaginazer.toImage(data, pairs, teachers)
#     Image.open(img).show("ljfsgsd")
