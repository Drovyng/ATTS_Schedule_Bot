from typing import Union

import config
import group_data, sheets, json
import imaginazer

KeyboardButtonsOld: list[str] = [
    "Выбрать Группу 🗒",
    "Админ 🔧",

    "Загрузить Расписание ✏️",
    "Меню 📋",

    "Выйти ❌",
    "Расписание 📄",         # 5 index
    "Расписание (День) 📄",  # 6 index

    "Добавить Группу",
    "Удалить Группу",
    "Добавить Пару",
    "Удалить Пару",
    "Добавить Преподавателя",
    "Удалить Преподавателя",

    "Перезагрузить бота 🔄",
    "Обновить файл",
    #"Консоль",
    #"Команда",

    "Уведомления 🔔",
    "Назад ◀️",
    "Выбрать Роль ⚡️",
    "Выбрать ФИО 🔆",
    "Сменить Роль ⚡️",
    "Редактор 🧷",               # 22 index
    "Статистика",
    "Список",

    "Список 📋",                 # 25 index
    "Обратная связь 📝",         # 26 index
    "Расписание (След.) 📄"      # 27 index
]

AllButtonsDict: list[tuple[str, str]] = [                  # TODO
    ("mm_group",    "Группа ⚡️"),        # 0
    ("mm_fio",      "ФИО ⚡️"),           # 1
    ("mm_rl",      "Роль 🔆"),           # 2
    ("back_menu",  "Назад ◀️"),          # 3
    ("mg_change",   "Сменить ✏️"),       # 4
    ("mf_change",   "Сменить ✏️"),       # 5

    ("mm_schedule", "Расписание 📄"),     # 6
    ("sh_week_cur", "Эта неделя"),        # 7
    ("sh_week_next", "След. неделя"),     # 8
    ("sh_week_day", "Выбрать один день"), # 9

    ("nm_rl", "Выбрать роль 🔆"),        # 10
    ("feedback", "Обратная связь 💬"),   # 11

    ("rl_student", "Студент 🙋🏻"),        # 12
    ("rl_teacher", "Преподаватель 🏫"),  # 13

    ("sh_day_0", "Понедельник"),    # 14
    ("sh_day_1", "Вторник"),        # 15
    ("sh_day_2", "Среда"),          # 16
    ("sh_day_3", "Четверг"),        # 17
    ("sh_day_4", "Пятница"),        # 18
    ("sh_day_5", "Суббота"),        # 19
    ("sh_day_cur", "Сегодня"),      # 20
    ("sh_day_next", "Завтра"),      # 21
    ("sh_day_back", "Назад ◀️"),    # 22

    ("mm_admin", "Админ 🔧"),       # 23

    ("fb_question", "Вопрос ❓"),    # 24
    ("fb_error", "Ошибка 🚫"),      # 25
    ("fb_offer", "Предложение 🤔"), # 26
    ("fb_other", "Другое 🌐"),      # 27

    ("feedback", "Назад ◀️"),       # 28

    ("an_shedule", "Изменить/Загрузить расписание ✏️"),  # 29

    ("sh_time_toggle_on", "Показывать время? (сейчас ВЫКЛ)"),    # 30
    ("sh_time_toggle_off", "Показывать время? (сейчас ВКЛ)"),    # 31
]
AllButtons: list[str] = []
AllButtonsIds: list[str] = []

for data in AllButtonsDict:
    value, name = data
    AllButtons.append(name)
    AllButtonsIds.append(value)

NotifyButtons: list[str] = [
    "На след. день",
    "На след. неделю",
    "Измен. расписания",
    KeyboardButtonsOld[3]
]
NotifyButtonsSelect: list[str] = [
    "Изменить ✏️",
    "Включить ✅",
    "Выключить ❌",
    KeyboardButtonsOld[3]
]
NotifyButtonsTimes: list[str] = [
    "15:00",
    "18:00",
    "19:00",
    "20:00",
    "22:00",
    "4:00",
    "5:00",
    "6:00",
    "7:00",
    KeyboardButtonsOld[3]
]
NotifyButtonsTimesInt: list[int] = [
    15,
    18,
    19,
    20,
    22,
    4,
    5,
    6,
    7
]
SelectGroupButtons = [
    KeyboardButtonsOld[4],
    "⏪",
    "⏩",
    KeyboardButtonsOld[3]
]
WorkModeButtons = [
    "Студент 🙋🏻",
    "Преподаватель 🔆",
    KeyboardButtonsOld[3]
]
FeedbackButtons = [
    KeyboardButtonsOld[3],
    "Вопрос ❓",
    "Ошибка 🚫",
    "Предложение 🤔",
    "Другое 🌐"
]
truefalseEmoji = ["❌", "✅"]
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "/menu", "Сегодня", "Завтра"]

modes = ["Студент 🙋🏻", "Преподаватель ⭐️"]

startText = "Привет! Я создан для того, чтобы студенты и преподаватели <b>Армавирского Техникума Технологии и Сервиса</b> могли узнать расписание в любое время!"

import datetime

class UpdatedData():
    def __init__(self):
        self.admins: list[str] = []
        self.editors: list[str] = []
        self.teachers: list[str] = []
        self.pairs: list[str] = []
        self.groups: list[str] = []
        self.students: list[str] = []
        self.groups_data_cur: list[str] = []
        self.groups_data_next: list[str] = []
        self.groups_week: int = 0

        self.saveTimer = 150

        self.settings: list[str] = []

        self.onSaveAll = None

        self.resize()

        self.reloadAll()

    def resize(self):

        self.adminsCount = len(self.admins)
        self.editorsCount = len(self.editors)
        self.teachersCount = len(self.teachers)
        self.pairsCount = len(self.pairs)
        self.groupsCount = len(self.groups)
        self.studentsCount = len(self.students)
        self.settingsCount = len(self.settings)

    def reloadAll(self):
        self.adminsCount = int(sheets.getRange("A2")[0][0])
        if self.adminsCount > 0:
            self.devs = sheets.getRange(f"A3:A{2 + self.adminsCount}")[0]

        self.editorsCount = int(sheets.getRange("G2")[0][0])
        if self.editorsCount > 0:
            self.devs = sheets.getRange(f"G3:G{2 + self.editorsCount}")[0]

        self.teachersCount = int(sheets.getRange("B2")[0][0])
        self.teachers = sheets.getRange(f"B3:B{2 + self.teachersCount}")[0]

        self.pairsCount = int(sheets.getRange("C2")[0][0])
        self.pairs = sheets.getRange(f"C3:C{2 + self.pairsCount}")[0]

        self.groupsCount = int(sheets.getRange("D2")[0][0])
        self.groups_week = int(sheets.getRange(f"H2")[0][0])
        if self.groupsCount > 0:
            self.groups = sheets.getRange(f"D3:D{2 + self.groupsCount}")[0]
            self.groups_data_cur = sheets.getRange(f"H3:H{2 + self.groupsCount}")[0]
            self.groups_data_next = sheets.getRange(f"I3:I{2 + self.groupsCount}")[0]

        self.studentsCount = int(sheets.getRange("E2")[0][0])
        if self.studentsCount > 0:
            self.students = sheets.getRange(f"E3:E{2 + self.studentsCount}")[0]

        self.settingsCount = int(sheets.getRange("F2")[0][0])
        if self.settingsCount > 0:
            self.settings = sheets.getRange(f"F3:F{2 + self.settingsCount}")[0]

        self.check()

    def save_groups(self):
        sheets.setRange("D2", [[str(len(self.groups))]])
        sendGroups = self.groups[:]
        sendGroups_data_cur = self.groups_data_cur[:]
        sendGroups_data_next = self.groups_data_next[:]
        while len(sendGroups) < self.groupsCount: sendGroups.append("")
        while len(sendGroups_data_cur) < self.groupsCount: sendGroups_data_cur.append("")
        while len(sendGroups_data_next) < self.groupsCount: sendGroups_data_next.append("")
        sheets.setRange(f"D3:D{2 + max(self.groupsCount, len(sendGroups))}", [sendGroups])
        sheets.setRange(f"H3:H{2 + max(self.groupsCount, len(sendGroups))}", [sendGroups_data_cur])
        sheets.setRange(f"I3:I{2 + max(self.groupsCount, len(sendGroups))}", [sendGroups_data_next])

    def check(self, issaving: bool = False):
        curWeek = datetime.datetime.now().isocalendar()[1]
        go = self.groups_week != curWeek
        if go:
            self.groups_week = curWeek
            self.groups_data_cur = self.groups_data_next[:]
            self.groups_data_next = []
            sheets.setRange("H2", [[str(curWeek)]])

        while len(self.groups) > len(self.groups_data_cur): self.groups_data_cur.append("")
        while len(self.groups) > len(self.groups_data_next): self.groups_data_next.append("")

        if not issaving and go:
            self.save_groups()

    def saveAll(self):
        self.check(True)



        sheets.setRange("A2", [[str(len(self.admins))]])
        sendAdmins = self.admins[:]
        while len(sendAdmins) < self.adminsCount: sendAdmins.append("")
        sheets.setRange(f"A3:A{2 + max(self.adminsCount, len(sendAdmins))}", [sendAdmins])

        sheets.setRange("G2", [[str(len(self.editors))]])
        sendEditors = self.editors[:]
        while len(sendEditors) < self.editorsCount: sendEditors.append("")
        sheets.setRange(f"G3:G{2 + max(self.editorsCount, len(sendEditors))}", [sendEditors])




        sheets.setRange("B2", [[str(len(self.teachers))]])
        sendTeachers = self.teachers[:]
        while len(sendTeachers) < self.teachersCount: sendTeachers.append("")
        sheets.setRange(f"B3:B{2 + max(self.teachersCount, len(sendTeachers))}", [sendTeachers])

        sheets.setRange("C2", [[str(len(self.pairs))]])
        sendPairs = self.pairs[:]
        while len(sendPairs) < self.pairsCount: sendPairs.append("")
        sheets.setRange(f"C3:C{2 + max(self.pairsCount, len(sendPairs))}", [sendPairs])

        self.save_groups()

        sheets.setRange("E2", [[str(len(self.students))]])
        sendStudents = self.students[:]
        while len(sendStudents) < self.studentsCount: sendStudents.append("")
        sheets.setRange(f"E3:E{2 + max(self.studentsCount, len(sendStudents))}", [sendStudents])

        haveUsers: list[int] = []
        for sett in self.settings:
            haveUsers.append(json.loads(sett)[0])
        for user in self.students:
            id = json.loads(user)[0]
            if not id in haveUsers:
                haveUsers.append(id)
                self.settings.append(json.dumps((id, False, False, False, False)))

        sheets.setRange("F2", [[str(len(self.settings))]])
        sendSettings = self.settings[:]

        while len(sendSettings) < self.settingsCount: sendSettings.append("")
        sheets.setRange(f"F3:F{2 + max(self.settingsCount, len(sendSettings))}", [sendSettings])

        self.resize()

        self.onSaveAll()


updatedData = UpdatedData()

emptyTeacherDay: group_data.DayDataTeacher = [[-1, -1, -1] for _ in range(6)]


teachersPairs: list[list[group_data.WeekDataTeacher]] = [[], []]


def recalculateTeachersPairs(nextWeek:bool):
    global updatedData, teachersPairs, emptyTeacherDay
    nextWeekInt = 1 if nextWeek else 0
    teachersPairs[nextWeekInt] = [[emptyTeacherDay[:] for _ in range(6)] for _ in range(updatedData.teachersCount)]

    toRead = updatedData.groups_data_next if nextWeek else updatedData.groups_data_cur

    for i in range(updatedData.groupsCount):                # Group
        data = toRead[i]
        if data.count("[") < 10:
            continue
        parsed: group_data.WeekData = json.loads(data)

        for d in range(6):                                  # Day
            day = parsed[d]
            p = -1
            for pair in [day[1], day[2], day[3]]:           # Pair
                p += 1
                offset = p + max(day[0], 0)
                if offset >= 6:
                    break
                if min(pair) == -1 or -1 in pair or pair[1] == -1:
                    continue

                teachersPairs[nextWeekInt][pair[1]][d][offset] = [pair[0], i, pair[2]]


def recalculateTeachersPairsAll():
    recalculateTeachersPairs(False)
    recalculateTeachersPairs(True)


updatedData.onSaveAll = recalculateTeachersPairsAll
recalculateTeachersPairsAll()



import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

bot = telebot.TeleBot(config.bot_token)


def kb(index: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(AllButtons[index], callback_data=AllButtonsIds[index])


def findStudent(userID) -> list | None:
    global updatedData
    i = 0
    for st in updatedData.students:
        parsed = json.loads(st)
        if parsed[0] == userID:
            return parsed
        i += 1
    return None


def findStudentIndex(userID) -> int:
    global updatedData
    i = 0
    for st in updatedData.students:
        if json.loads(st)[0] == userID:
            return i
        i += 1
    return -1


def findTeacherIndex(userID) -> int:
    global updatedData
    student = findStudent(userID)
    if student == None or not student[2] in updatedData.teachers:
        return -1
    return updatedData.teachers.index(student[2])


def findIsTeacher(userID) -> bool:
    global updatedData
    student = findStudent(userID)
    if student == None:
        return False
    return student[1] == "Teacher"


def findStudentGroup(userID) -> int:
    global updatedData
    student = findStudent(userID)
    if student == None or not student[1] in updatedData.groups:
        return -1
    return updatedData.groups.index(student[1])


def getIsDev(userID: int) -> bool:
    global updatedData
    return userID in updatedData.admins or userID in config.developers


def getIsEditor(userID: int) -> bool:
    global updatedData
    return getIsDev(userID) or userID in updatedData.editors


def getUserSettingsIndex(userID: int) -> int:
    global updatedData
    i = 0
    for st in updatedData.settings:
        if json.loads(st)[0] == userID:
            return i
        i += 1
    return -1


def getReturnIfTime() -> bool:
    nowDate = datetime.datetime.now()
    if nowDate.hour == 0 or (nowDate.hour == 23 and nowDate.minute >= 30):
        return True
    return False


def getUserSettings(userID: int) -> group_data.Settings:
    for i in range(updatedData.settingsCount):
        parsed: group_data.Settings = json.loads(updatedData.settings[i])
        if len(parsed) < 5:
            parsed = (parsed[0], parsed[1], parsed[2], parsed[3], False)
            updatedData.settings[i] = json.dumps(parsed)
        if parsed[0] == userID:
            return parsed
    return (userID, False, False, False, False)


@bot.callback_query_handler(func=lambda call: True)     # TODO
def on_button(query: CallbackQuery):
    global updatedData, startText

    id = -1
    data = query.data
    message = query.message
    userID = message.chat.id

    editText = ""
    markup = InlineKeyboardMarkup()
    resend = False

    if data in AllButtonsIds:
        id = AllButtonsIds.index(data)

    if id == 3:
        editText = startText
        markup = None

    elif id == 0:
        grpId = findStudentGroup(userID)
        if grpId >= 0:
            editText = f"Вы в группе <b>{updatedData.groups[grpId]}</b>:"
            markup.row(kb(3))
            markup.row(kb(4))
        else:
            editText = f"Вы не состоите в группе!"
            markup = None

    elif id == 1:
        if not findIsTeacher(userID):
            editText = f"Вы не преподаватель!"
            markup = None
        else:
            tchrId = findTeacherIndex(userID)
            if tchrId >= 0:
                editText = f"Вы <b>{updatedData.teachers[tchrId]}</b>:"
                markup.row(kb(3))
                markup.row(kb(5))
            else:
                editText = f"Вы не преподаватель!"
                markup = None

    elif id == 2 or id == 10:
        editText = "Выберите роль:"
        markup.row(kb(3))
        markup.row(kb(12))
        markup.row(kb(13))

    elif id == 30:
        i = getUserSettingsIndex(userID)
        x1, x2, x3, x4 = json.loads(updatedData.settings[i])[:4]
        updatedData.settings[i] = json.dumps((x1, x2, x3, x4, True))
        editText = "Отображения времени <b>включено</b>!\nВыберите тип расписания:"
        id = 6
    elif id == 31:
        i = getUserSettingsIndex(userID)
        x1, x2, x3, x4 = json.loads(updatedData.settings[i])[:4]
        updatedData.settings[i] = json.dumps((x1, x2, x3, x4, False))
        editText = "Отображения времени <b>выключено</b>!\nВыберите тип расписания:"
        id = 6

    if id == 6 or id == 22:
        if getReturnIfTime():
            editText = "Данная функция в это время недоступна!"
            markup = None
        else:
            if len(editText) == 0:
                editText = "Выберите тип расписания:"
            markup.row(kb(3))
            sett = getUserSettings(userID)
            markup.row(kb(31 if sett[4] else 30))
            markup.row(kb(7), kb(8))
            markup.row(kb(9))

    elif id == 7:
        studentIndex = findStudentIndex(userID)
        if studentIndex == -1:
            editText = "Вы не подключены к группе!"
            markup = None
        elif getReturnIfTime():
            editText = "Данная функция в это время недоступна!"
            markup = None
        else:
            nowDate = datetime.datetime.now().isocalendar()
            startDate = datetime.datetime.fromisocalendar(nowDate.year, nowDate.week, 1).strftime("%d.%m.%Y")
            endDate = datetime.datetime.fromisocalendar(nowDate.year, nowDate.week, 7).strftime("%d.%m.%Y")

            textPlus = f"\n{startDate} - {endDate}"

            img = None
            if findIsTeacher(userID):
                curWeek: group_data.WeekDataTeacher = teachersPairs[0][findTeacherIndex(userID)]

                img = imaginazer.toImageTeacher(
                    curWeek,
                    updatedData.pairs,
                    updatedData.groups
                )
            else:
                groupID = -1
                groupName = json.loads(updatedData.students[studentIndex])[1]
                if updatedData.groups.count(groupName) != 0:
                    groupID = updatedData.groups.index(groupName)
                if groupID == -1:
                    editText = "У вас отсутствует роль!"
                    markup = None
                elif updatedData.groups_data_cur[groupID].count("[") < 10:
                    editText = f"Расписание на эту текущую ещё не добавлено!{textPlus}"
                    markup = None
                else:
                    curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_cur[groupID])
                    img = imaginazer.toImage(
                        curWeek,
                        updatedData.pairs,
                        updatedData.teachers,
                        getUserSettings(userID)[4]
                    )
            if not img is None:
                img.seek(0)
                bot.send_photo(message.chat.id, img, f"Вот пары на текущую неделю{textPlus}")
                resend = True
            else:
                editText = "Произошла ошибка!"
                markup = None

    elif id == 8:
        studentIndex = findStudentIndex(userID)
        if studentIndex == -1:
            editText = "Вы не подключены к группе!"
            markup = None
        elif getReturnIfTime():
            editText = "Данная функция в это время недоступна!"
            markup = None
        else:
            nowDate = datetime.datetime.fromordinal(datetime.datetime.now().toordinal() + 7).isocalendar()
            startDate = datetime.datetime.fromisocalendar(nowDate.year, nowDate.week, 1).strftime("%d.%m.%Y")
            endDate = datetime.datetime.fromisocalendar(nowDate.year, nowDate.week, 7).strftime("%d.%m.%Y")

            textPlus = f"\n{startDate} - {endDate}"

            img = None
            if findIsTeacher(userID):
                curWeek: group_data.WeekDataTeacher = teachersPairs[1][findTeacherIndex(userID)]

                img = imaginazer.toImageTeacher(
                    curWeek,
                    updatedData.pairs,
                    updatedData.groups
                )
            else:
                groupID = -1
                groupName = json.loads(updatedData.students[studentIndex])[1]
                if updatedData.groups.count(groupName) != 0:
                    groupID = updatedData.groups.index(groupName)
                if groupID == -1:
                    editText = "У вас отсутствует роль!"
                    markup = None
                elif updatedData.groups_data_next[groupID].count("[") < 10:
                    editText = f"Расписание на эту следующую ещё не добавлено!{textPlus}"
                    markup = None
                else:
                    curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_next[groupID])
                    img = imaginazer.toImage(
                        curWeek,
                        updatedData.pairs,
                        updatedData.teachers,
                        getUserSettings(userID)[4]
                    )
            if not img is None:
                img.seek(0)
                bot.send_photo(message.chat.id, img, f"Вот пары на следующую неделю{textPlus}")
                resend = True
            else:
                editText = "Произошла ошибка!"
                markup = None

    elif id == 9:
        if getReturnIfTime():
            editText = "Данная функция в это время недоступна!"
            markup = None
        else:
            editText = "Выберите день:"
            markup.row(kb(22), kb(20), kb(21))
            markup.row(kb(14), kb(15), kb(16))
            markup.row(kb(17), kb(18), kb(19))

    elif "sh_day_" in data:
        if getReturnIfTime():
            editText = "Данная функция в это время недоступна!"
            markup = None
        else:
            dayIndex = ["0", "1", "2", "3", "4", "5", "cur", "next"].index(data.replace("sh_day_", ""))

            curDayI = datetime.datetime.now().isocalendar().weekday

            noSend = False

            if dayIndex == 6:
                if curDayI == 7:
                    noSend = True
                else:
                    dayIndex = curDayI - 1
            elif dayIndex == 7:
                if curDayI >= 6:
                    noSend = True
                else:
                    dayIndex = curDayI

            if not noSend:
                dayName = AllButtons[dayIndex + 14]

                img = None
                if findIsTeacher(userID):
                    img = imaginazer.toImageDayTeacher(
                        teachersPairs[0][findTeacherIndex(userID)][dayIndex],
                        dayName,
                        updatedData.pairs,
                        updatedData.groups
                    )
                else:
                    groupID = -1
                    groupName = json.loads(updatedData.students[findStudentIndex(userID)])[1]
                    if updatedData.groups.count(groupName) != 0:
                        groupID = updatedData.groups.index(groupName)
                    if groupID == -1:
                        editText = "У вас отсутствует роль!"
                    elif updatedData.groups_data_cur[groupID].count("[") < 10:
                        editText = "Расписание на эту неделю ещё не добавлено!"
                    else:
                        curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_cur[groupID])

                        img = imaginazer.toImageDay(
                            curWeek,
                            dayIndex,
                            updatedData.pairs,
                            updatedData.teachers,
                            getUserSettings(userID)[4]
                        )
                if not img is None:
                    img.seek(0)
                    nowDate = datetime.datetime.now().isocalendar()
                    bot.send_photo(message.chat.id, img, f"Вот пары на {dayName.lower()} ({datetime.datetime.fromisocalendar(nowDate.year, nowDate.week, dayIndex + 1).strftime("%d.%m.%Y")})")
                    resend = True
                else:
                    editText = "Произошла ошибка!"
                    markup = None
            else:
                editText = "Недоступный день! Выберите другой день:"
                markup.row(kb(22), kb(20), kb(21))
                markup.row(kb(14), kb(15), kb(16))
                markup.row(kb(17), kb(18), kb(19))

    elif id == 4 or id == 12:
        markup = btnsMarkup("sg_", updatedData.groups, 4)
        editText = "Выберите группу:"

    elif id == 5 or id == 13:
        markup = btnsMarkup("sf_", updatedData.teachers, 3)
        editText = "Выберите ФИО:"

    elif "sg_" in data:
        grp = data.replace("sg_", "")
        if grp in updatedData.groups:
            studentIndex = findStudentIndex(userID)
            if studentIndex != -1:
                updatedData.students.pop(studentIndex)
            updatedData.students.append(json.dumps([userID, grp], ensure_ascii=False))
            editText = f"Вы теперь в группе <b>{grp}</b>!"
            markup = None
        else:
            editText = "Неизвестная группа!"
            markup = btnsMarkup("sg_", updatedData.groups, 4)

    elif "sf_" in data:
        tchr = data.replace("sf_", "")
        if tchr in updatedData.teachers:
            studentIndex = findStudentIndex(userID)
            if studentIndex != -1:
                updatedData.students.pop(studentIndex)
            updatedData.students.append(json.dumps([userID, "Teacher", tchr], ensure_ascii=False))
            editText = f"Вы теперь <b>{tchr}</b>!"
            markup = None
        else:
            editText = "Неизвестное ФИО!"
            markup = btnsMarkup("sf_", updatedData.teachers, 3)

    elif "lg_" in data:
        index = int(data.replace("lg_", ""))
        datas = message.text.split("!")
        names = message.text.split("^")


        dataStr = "!"
        markup.row(kb(3))

        i = -1
        for grpData in datas:
            i += 1
            if i == 0 or i == len(datas) - 1:
                continue
            dataStr += grpData + "!"

        dataStr += "^"

        i = -1
        for name in names:
            i += 1
            if i == 0 or i == len(names) - 1:
                continue

            dataStr += name + "^"

            if i == index:
                urlData = [updatedData.pairs, updatedData.teachers, updatedData.groups, datas[i], 1]

                url = "https://drovyng.github.io/ATTS_Schedule_Bot_Website#customdata"
                url += json.dumps(urlData, ensure_ascii=False).replace(
                    "[", "q").replace("\"", "w").replace("]", "e").replace(" ", "r").replace(",", "t").replace(".", "y")
                url += "customdataend"

                markup2 = ReplyKeyboardMarkup(resize_keyboard=True)
                markup2.row(KeyboardButton("Загрузить данные «" + name + "»", web_app=WebAppInfo(url)))
                bot.send_message(message.chat.id, "Нажмите кнопку загрузки", reply_markup=markup2)

                markup.row(InlineKeyboardButton(">> " + name, callback_data=f"lg_{i}"))
            else:
                markup.row(InlineKeyboardButton(name, callback_data=f"lg_{i}"))

        editText = f"Выберите группу для загрузки...\n\n<tg-spoiler>{dataStr}</tg-spoiler>"

    elif id == 11:
        editText = "Выберите тип обращения:"
        markup.row(kb(3))
        markup.row(kb(24), kb(25))
        markup.row(kb(26), kb(27))

    elif 24 <= id <= 27:
        editText = f"Выбран тип «{AllButtons[id]}»\nНажмите «<b>Ответить</b>» на это сообщение для отправки\n<tg-spoiler>~{AllButtonsIds[id]}~</tg-spoiler>"
        markup.row(kb(28))

    elif id == 23:
        markup.row(kb(3))
        markup.row(kb(29))
        editText = "Открыто меню администрирования..."

    elif id == 29:
        markup = btnsMarkup("aes_", updatedData.groups, 4)
        editText = "Выберите группу для загрузки:"

    elif "aes_" in data:
        grp = data.replace("aes_", "")
        if grp in updatedData.groups:
            grpIndex = updatedData.groups.index(grp)

            urlData = [updatedData.pairs, updatedData.teachers, updatedData.groups,
                       updatedData.groups_data_cur[grpIndex], updatedData.groups_data_next[grpIndex]]

            url = "https://drovyng.github.io/ATTS_Schedule_Bot_Website#customdata"
            url += json.dumps(urlData, ensure_ascii=False).replace(
                "[", "q").replace("\"", "w").replace("]", "e").replace(" ", "r").replace(",", "t").replace(".", "y")
            url += "customdataend"

            markup2 = ReplyKeyboardMarkup(resize_keyboard=True)
            markup2.row(KeyboardButton("Изменить/Загрузить расписание «" + updatedData.groups[grpIndex] + "»",
                                       web_app=WebAppInfo(url)))

            bot.send_message(message.chat.id, "Нажмите кнопку загрузки", reply_markup=markup2)
        else:
            editText = "Неизвестная группа!"
            markup = btnsMarkup("aes_", updatedData.groups, 4)


    try:
        bot.answer_callback_query(query.id)
    except:
        pass

    if resend:
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, "Открыто меню:", reply_markup=menu_keyboard(message.chat.id))
        return
    if editText != "":
        if markup is None:
            markup = menu_keyboard(userID)
        bot.edit_message_text(editText, message.chat.id, message.message_id, reply_markup=markup, parse_mode="HTML")


def menu_keyboard(userID: int) -> InlineKeyboardMarkup:
    global updatedData
    isInGroup = findStudentIndex(userID) != -1
    isDev = getIsDev(userID)
    markup = InlineKeyboardMarkup()

    if isInGroup:
        markup.row(kb(6))

        groupBtnName = kb(1) if findIsTeacher(userID) else kb(0)
        markup.row(groupBtnName, kb(2))
    else:
        markup.row(kb(10))

    markup.row(kb(11))

    if isDev:
        markup.row(kb(23))

    return markup


def btnsMarkup(prefix: str, btns: list[str], maxLen: int = 5, backIndex = 3) -> InlineKeyboardMarkup:
    lengrp = len(btns)
    inrow = max(min(lengrp, maxLen), 1)
    rows = lengrp // inrow

    markup = InlineKeyboardMarkup()
    markup.row(kb(backIndex))

    b = 0
    for i in range(rows+1):
        inRow = []
        for j in range(0, min(lengrp - inrow * i, inrow)):
            inRow.append(InlineKeyboardButton(btns[b], callback_data=prefix+btns[b]))
            b += 1

        markup.row(*inRow)
    return markup


def getBtnsPage(fromList:list[str], page:int, limit:int = 5) -> list[str]:
    btns: list[str] = []
    i = -1
    for grp in fromList:
        i += 1
        if page * limit * 2 <= i < page * limit * 2 + limit * 2: btns.append(grp)
    return btns


@bot.message_handler(commands=['start', 'menu'])        # TODO <-- Чтобы не потерять
def start(message: Message):
    global startText

    bot.send_message(
        message.chat.id,
        startText,
        reply_markup=menu_keyboard(message.from_user.id),
        parse_mode="html"
    )


@bot.message_handler(content_types=["text"])
def on_message(message: Message):
    try:
        if not message.reply_to_message is None:
            reply = message.reply_to_message
            if reply.from_user.is_bot:
                if "fb_" in reply.text:
                    text = f"<b>Обращение типа [{AllButtons[AllButtonsIds.index(reply.text.split("~")[1])]}]\nИдентификатор: #{message.chat.id}#{message.message_id}#\nНажмите «<b>Ответить</b>» на это сообщение для ответа!</b>\n{message.text}"
                    sended = False
                    for i in config.developers:
                        try:
                            bot.send_message(i, text, parse_mode="html")
                            sended = True
                        except:
                            pass
                    for i in updatedData.admins:
                        try:
                            bot.send_message(i, text, parse_mode="html")
                            sended = True
                        except:
                            pass
                    if sended:
                        bot.send_message(message.chat.id,
                                         f"Ваше обращение было отправлено! Идентификатор обращения: [{message.chat.id}-{message.message_id}]")
                    else:
                        bot.send_message(message.chat.id,
                                         f"Ошибка! Ваше обращение не было отправлено!")
                    bot.send_message(
                        message.chat.id,
                        "Открыто меню:",
                        reply_markup=menu_keyboard(message.from_user.id),
                        parse_mode="html"
                    )
                elif reply.text.count("#") >= 3 and getIsDev(message.from_user.id):
                    reply_data = reply.text.split("#")

                    reply_chat = reply_data[1]

                    text = f"<b>Ответ по обращению [{reply_chat}-{reply_data[2]}]:</b>\n{message.text}"

                    bot.send_message(reply_chat, text, parse_mode="html")

                    bot.send_message(message.chat.id, "Ответ успешно отправлен!")
                    return
            return
    except:
        pass

    if message.text in KeyboardButtonsOld:
        bot.send_message(message.chat.id, "Данные команды устарели, пожалуйста используйте /menu!", reply_markup=telebot.types.ReplyKeyboardRemove())
        return

    if not getIsDev(message.chat.id):
        return

    if message.text == "Рестарт":
        bot.send_message(message.chat.id, f"Бот в процессе перезагрузки!")
        raise Exception("BotRestartCommand")
    elif message.text == "Обновить":
        bot.send_message(message.chat.id, f"Введите название файла")
        bot.register_next_step_handler_by_chat_id(message.chat.id, dev_action, True, 3, False, None)
    elif message.text == "Консоль":
        img = imaginazer.getScreenshot()
        img.seek(0)
        bot.send_photo(message.chat.id, img, "Вот скрин консоли")
    elif message.text == "Команда":
        bot.send_message(message.chat.id, f"Введите команду")
        bot.register_next_step_handler_by_chat_id(message.chat.id, dev_command)

# def on_message(message: Message):
#     global KeyboardButtonsOld, updatedData
#
#     text = message.text
#
#     try:
#         if message.reply_to_message != None and message.reply_to_message.from_user.is_bot:
#             reply_text = message.reply_to_message.text
#             if reply_text.count("#") >= 3:
#                 reply_data = reply_text.split("#")
#
#                 reply_chat = reply_data[1]
#
#                 text = f"<b>Ответ по обращению [{reply_chat}-{reply_data[2]}]:</b>\n{text}"
#
#                 bot.send_message(reply_chat, text, parse_mode="html")
#
#                 bot.send_message(message.chat.id, "Ответ успешно отправлен!")
#                 return
#     except:
#         pass
#
#     updatedData.check()
#
#     userID = message.from_user.id
#     isDev = getIsDev(userID)
#
#     textIndex = -1
#     if KeyboardButtonsOld.count(text) > 0:
#         textIndex = KeyboardButtonsOld.index(text)
#
#     if textIndex == 3:
#         start(message)
#     elif textIndex == 5:
#         studentIndex = findStudentIndex(userID)
#         if studentIndex == -1:
#             bot.send_message(message.chat.id, f"Вы не подключены к группе!", reply_markup=menu_keyboard(userID))
#             return
#
#         if getReturnIfTime(message):
#             return
#
#         nowDate = datetime.datetime.now().isocalendar()
#         startDate = datetime.datetime.fromisocalendar(nowDate.year, nowDate.week, 1).strftime("%d.%m.%Y")
#         endDate = datetime.datetime.fromisocalendar(nowDate.year, nowDate.week, 7).strftime("%d.%m.%Y")
#
#         textPlus = f"\n{startDate} - {endDate}"
#
#         img = None
#         if findIsTeacher(userID):
#             curWeek: group_data.WeekDataTeacher = teachersPairs[0][findTeacherIndex(userID)]
#
#             img = imaginazer.toImageTeacher(
#                 curWeek,
#                 updatedData.pairs,
#                 updatedData.groups
#             )
#         else:
#             groupID = -1
#             groupName = json.loads(updatedData.students[studentIndex])[1]
#             if updatedData.groups.count(groupName) != 0:
#                 groupID = updatedData.groups.index(groupName)
#             if groupID == -1 or updatedData.groups_data_cur[groupID].count("[") < 10:
#                 bot.send_message(message.chat.id, f"Расписание на эту текущую ещё не добавлено!{textPlus}",
#                                  reply_markup=menu_keyboard(userID))
#                 return
#             curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_cur[groupID])
#             img = imaginazer.toImage(
#                 curWeek,
#                 updatedData.pairs,
#                 updatedData.teachers
#             )
#         img.seek(0)
#         bot.send_photo(message.chat.id, img, f"Вот пары на текущую неделю{textPlus}", reply_markup=menu_keyboard(userID))
#
#     elif textIndex == 27:
#         studentIndex = findStudentIndex(userID)
#         if studentIndex == -1:
#             bot.send_message(message.chat.id, f"Вы не подключены к группе!", reply_markup=menu_keyboard(userID))
#             return
#
#         if getReturnIfTime(message):
#             return
#
#         nowDate = datetime.datetime.fromordinal(datetime.datetime.now().toordinal()+7).isocalendar()
#         startDate = datetime.datetime.fromisocalendar(nowDate.year, nowDate.week, 1).strftime("%d.%m.%Y")
#         endDate = datetime.datetime.fromisocalendar(nowDate.year, nowDate.week, 7).strftime("%d.%m.%Y")
#
#         textPlus = f"\n{startDate} - {endDate}"
#
#
#         img = None
#         if findIsTeacher(userID):
#             curWeek: group_data.WeekDataTeacher = teachersPairs[1][findTeacherIndex(userID)]
#
#             img = imaginazer.toImageTeacher(
#                 curWeek,
#                 updatedData.pairs,
#                 updatedData.groups
#             )
#         else:
#             groupID = -1
#             groupName = json.loads(updatedData.students[studentIndex])[1]
#             if updatedData.groups.count(groupName) != 0:
#                 groupID = updatedData.groups.index(groupName)
#             if groupID == -1 or updatedData.groups_data_next[groupID].count("[") < 10:
#                 bot.send_message(message.chat.id, f"Расписание на эту следующую ещё не добавлено!{textPlus}",
#                                  reply_markup=menu_keyboard(userID))
#                 return
#             curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_next[groupID])
#             img = imaginazer.toImage(
#                 curWeek,
#                 updatedData.pairs,
#                 updatedData.teachers
#             )
#         img.seek(0)
#         bot.send_photo(message.chat.id, img, f"Вот пары на следующую неделю{textPlus}", reply_markup=menu_keyboard(userID))
#
#     elif textIndex == 6:
#         studentIndex = findStudentIndex(userID)
#
#         if studentIndex == -1:
#             bot.send_message(message.chat.id, f"Вы не подключены к группе!", reply_markup=menu_keyboard(userID))
#             return
#
#         if getReturnIfTime(message):
#             return
#
#
#         markup = ReplyKeyboardMarkup(resize_keyboard=True)
#
#         markup.add(*days)
#
#         bot.send_message(message.chat.id, f"На какой день вы хотите узнать расписание?", reply_markup=markup)
#         bot.register_next_step_handler_by_chat_id(message.chat.id, get_pair_day)
#
#
#     elif textIndex == 0:
#         markup = btnsMarkup(getGroupsList(updatedData.groups, 0), 5)
#         btns = SelectGroupButtons[:]
#         btns.insert(2, "Стр. 1")
#         btns[1] = truefalseEmoji[0]
#         markup.row(*btns)
#
#         bot.send_message(message.chat.id, "Выберите Группу...", reply_markup=markup)
#         bot.register_next_step_handler(message, select_group, 0)
#
#     elif textIndex == 20:
#         markup = btnsMarkup(getGroupsList(updatedData.teachers, 0, 3), 3)
#         btns = SelectGroupButtons[:]
#         btns.insert(2, "Стр. 1")
#         btns[1] = truefalseEmoji[0]
#         markup.row(*btns)
#
#         bot.send_message(message.chat.id, "Выберите ФИО...", reply_markup=markup)
#         bot.register_next_step_handler(message, select_teacher, 0)
#
#     elif textIndex == 1 and isDev:
#         markup = ReplyKeyboardMarkup(resize_keyboard=True)
#
#         markup.row(
#             KeyboardButton(KeyboardButtonsOld[3])
#         )
#         markup.row(
#             KeyboardButton(KeyboardButtonsOld[23]),
#             KeyboardButton(KeyboardButtonsOld[24])
#         )
#         markup.row(
#             KeyboardButton(KeyboardButtonsOld[7]),
#             KeyboardButton(KeyboardButtonsOld[9]),
#             KeyboardButton(KeyboardButtonsOld[11])
#         )
#         #markup.row(
#             #KeyboardButton(KeyboardButtonsOld[10]),
#             #KeyboardButton(KeyboardButtonsOld[8]),
#             #KeyboardButton(KeyboardButtonsOld[12])
#         #)
#         markup.row(
#             KeyboardButton(KeyboardButtonsOld[13]),
#         )
#         markup.row(
#             KeyboardButton(KeyboardButtonsOld[14]),
#             KeyboardButton(KeyboardButtonsOld[15]),
#             KeyboardButton(KeyboardButtonsOld[16])
#         )
#
#         bot.send_message(message.chat.id, "Открыта панель администратора.", reply_markup=markup)
#     elif textIndex == 22:
#         markup = ReplyKeyboardMarkup(resize_keyboard=True)
#
#         urlData = [updatedData.pairs, updatedData.teachers, updatedData.groups, updatedData.groups_data_cur,
#                    updatedData.groups_data_next]
#
#         url = "https://drovyng.github.io/ATTS_Schedule_Bot_Website#customdata"
#         url += json.dumps(urlData, ensure_ascii=False).replace(
#             "[", "q").replace("\"", "w").replace("]", "e").replace(" ", "r").replace(",", "t").replace(".", "y")
#         url += "customdataend"
#
#         markup.row(
#             KeyboardButton(KeyboardButtonsOld[3])
#         )
#         markup.row(
#             KeyboardButton(KeyboardButtonsOld[2], web_app=WebAppInfo(url))
#         )
#
#         bot.send_message(message.chat.id, "Открыта панель редактора.", reply_markup=markup)
#
#     elif textIndex == 23 and isDev:
#         notifyCount = 0
#         for notify in updatedData.settings:
#             if notify.lower().count("false") < 3:
#                 notifyCount += 1
#
#         groups_students: dict[str, int] = {}
#
#         for i in range(updatedData.studentsCount):
#             grpId = json.loads(updatedData.students[i])[1]
#             if not grpId in groups_students:
#                 groups_students[grpId] = 1
#             else:
#                 groups_students[grpId] = groups_students[grpId] + 1
#
#         for grp in updatedData.groups:
#             if not grp in groups_students:
#                 groups_students[grp] = 0
#
#         textAdd = ""
#         for grp in groups_students:
#             textAdd += f"\n[{grp}]: {groups_students[grp]}"
#             if len(textAdd) >= 3980:
#                 break
#         bot.send_message(message.chat.id, f"Вот Статистика:\n  Уведомления: {notifyCount}\n  Группы:{textAdd}", reply_markup=menu_keyboard(userID))
#
#     elif textIndex == 24 and isDev:
#         textAdd = ""
#
#         for stud in updatedData.students:
#             parsed = json.loads(stud)
#             user_name = parsed[0]
#             try:
#                 user_name = bot.get_chat_member(parsed[0], parsed[0]).user.username
#             except:
#                 pass
#             textAdd += f"\n<a href='tg://user?id={parsed[0]}'>@{user_name}</a> - {parsed[1]}"
#             if parsed[1] == "Teacher":
#                 textAdd += f" - {parsed[2]}"
#             if len(textAdd) >= 3980:
#                 break
#         bot.send_message(message.chat.id, f"Вот Список:{textAdd}", reply_markup=menu_keyboard(userID), parse_mode="HTML")
#
#     elif textIndex == 13 and isDev:
#         bot.send_message(message.chat.id, f"Бот в процессе перезагрузки!",
#                          reply_markup=menu_keyboard(message.from_user.id))
#         raise Exception("BotRestartCommand")
#     elif textIndex == 14 and isDev:
#         bot.send_message(message.chat.id, f"Введите название файла")
#         bot.register_next_step_handler_by_chat_id(message.chat.id, dev_action, True, 3, False, None)
#     elif textIndex == 15 and isDev:
#         img = imaginazer.getScreenshot()
#         img.seek(0)
#         bot.send_photo(message.chat.id, img, "Вот скрин консоли", reply_markup=menu_keyboard(userID))
#     elif textIndex == 16 and isDev:
#         bot.send_message(message.chat.id, f"Введите команду")
#         bot.register_next_step_handler_by_chat_id(message.chat.id, dev_command)
#     elif textIndex == 17:
#         markup = ReplyKeyboardMarkup(resize_keyboard=True)
#
#         notifyIndex = getUserNotifyIndex(userID)
#         notifyData = [userID, False, False, False]
#
#         if notifyIndex != -1:
#             notifyData = json.loads(updatedData.settings[notifyIndex])
#
#         btns = []
#
#         for i in range(len(NotifyButtons) - 1):
#             isTrue = 0
#             if str(notifyData[i + 1]) != "False":
#                 isTrue = 1
#             btns.append(NotifyButtons[i] + " " + truefalseEmoji[isTrue])
#
#         btns.append(NotifyButtons[-1])
#
#         lengrp = len(btns)
#         inrow = min(lengrp, 2)
#         rows = lengrp // inrow
#
#         b = 0
#         for i in range(rows):
#             inRow = []
#             for j in range(0, min(lengrp - inrow * i, inrow)):
#                 inRow.append(KeyboardButton(btns[b]))
#                 b += 1
#             markup.row(*inRow)
#
#         bot.send_message(message.chat.id, "Выберите пункт:", reply_markup=markup)
#         bot.register_next_step_handler_by_chat_id(message.chat.id, notify_select, notifyData, 0, -1)
#
#     elif textIndex == 19 or textIndex == 21:
#         markup = ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.row(*WorkModeButtons)
#         bot.send_message(message.chat.id, "Выберите режим:", reply_markup=markup)
#         bot.register_next_step_handler_by_chat_id(message.chat.id, mode_select)
#
#     elif textIndex == 25:
#         addText = ""
#         for grp in range(updatedData.groupsCount):
#             yesno = 0 if updatedData.groups_data_cur[grp].count("[") < 10 else 1
#             addText += f"\n{updatedData.groups[grp]} - {truefalseEmoji[yesno]}"
#         bot.send_message(message.chat.id, f"Сейчас пары добавлены на группы:{addText}", reply_markup=menu_keyboard(userID))
#
#     elif textIndex == 26:
#         markup = ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.row(
#             KeyboardButton(FeedbackButtons[1]),
#             KeyboardButton(FeedbackButtons[2])
#         )
#         markup.row(
#             KeyboardButton(FeedbackButtons[3]),
#             KeyboardButton(FeedbackButtons[4])
#         )
#         markup.row(
#             KeyboardButton(FeedbackButtons[0])
#         )
#         bot.send_message(message.chat.id, f"Выберите тип обращения:", reply_markup=markup)
#         bot.register_next_step_handler_by_chat_id(message.chat.id, feedback_select)
#
#     elif textIndex >= 7 and textIndex < 13 and isDev:
#         isAdd = textIndex % 2 == 1
#         isWhat = (textIndex - 7) // 2
#         if not isAdd:
#             bot.send_message(message.chat.id, "Данная функция отключена!", reply_markup=menu_keyboard(userID))
#             return
#
#             markup = ReplyKeyboardMarkup(resize_keyboard=True)
#             strList = []
#             if isWhat == 0:
#                 strList = updatedData.groups
#             elif isWhat == 1:
#                 strList = updatedData.pairs
#             else:
#                 strList = updatedData.teachers
#
#             lengrp = len(strList)
#             inrow = min(lengrp, 5)
#             rows = lengrp // inrow
#
#             b = 0
#             for i in range(rows):
#                 inRow = []
#                 for j in range(0, min(lengrp - inrow * i, inrow)):
#                     inRow.append(KeyboardButton(strList[b]))
#                     b += 1
#                 markup.row(*inRow)
#
#             bot.send_message(message.chat.id, "Выберите то, что хотите удалить", reply_markup=markup)
#         else:
#             sendText = ""
#             if isWhat == 0:
#                 sendText = "й группы"
#             elif isWhat == 1:
#                 sendText = "й пары"
#             else:
#                 sendText = "го преподавателя"
#             bot.send_message(message.chat.id, f"Напишите название ново{sendText}")
#
#         bot.register_next_step_handler_by_chat_id(message.chat.id, dev_action, isAdd, isWhat, False, None)


def feedback_select(message: Message):
    global updatedData, NotifyButtons, KeyboardButtonsOld, FeedbackButtons

    text = message.text

    if text == FeedbackButtons[0]:
        start(message)
        return
    if text in FeedbackButtons:
        bot.send_message(message.chat.id, f"Теперь напишите само обращение:", reply_markup=None)
        bot.register_next_step_handler_by_chat_id(message.chat.id, feedback_print, FeedbackButtons.index(text))
        return
    bot.send_message(message.chat.id, f"Неверный тип [{text}]!")


def feedback_print(message: Message, getType: int):
    text = message.text
    text = f"<b>Обращение типа [{FeedbackButtons[getType]}]\nИдентификатор: #{message.chat.id}#{message.message_id}#\nОтветьте на это сообщение для ответа!</b>\n{text}"
    sended = False
    for i in config.developers:
        try:
            bot.send_message(i, text, parse_mode="html")
            sended = True
        except:
            pass
    for i in updatedData.admins:
        try:
            bot.send_message(i, text, parse_mode="html")
            sended = True
        except:
            pass
    if sended:
        bot.send_message(message.chat.id, f"Ваше обращение было отправлено! Идентификатор обращения: [{message.chat.id}-{message.message_id}]")
    else:
        bot.send_message(message.chat.id,
                         f"Ошибка! Ваше обращение не было отправлено!")


def dev_command(message: Message):
    exec(message.text)
    img = imaginazer.getScreenshot()
    img.seek(0)
    bot.send_photo(message.chat.id, img, "Вот скрин консоли", reply_markup=menu_keyboard(message.from_user.id))


def dev_action(message: Message, isAdd: bool, isWhat: int, isToConfirm: bool, name: Union[str | None]):
    global updatedData

    text = message.text
    userID = message.from_user.id
    if isToConfirm:
        if text == "Подтверждаю!":
            if isAdd:
                sendText = ""
                if isWhat == 0:
                    updatedData.groups.append(name)
                    updatedData.groups_data_cur.append("")
                    updatedData.groups_data_next.append("")
                    sendText = "а группа"
                elif isWhat == 1:
                    updatedData.pairs.append(name)
                    sendText = "а пара"
                elif isWhat == 2:
                    updatedData.teachers.append(name)
                    sendText = " преподаватель"
                elif isWhat == 3:
                    bot.send_message(message.chat.id, f"Пытаюсь обновить файл [{name}]...",
                                     reply_markup=menu_keyboard(userID))
                    raise Exception(f"UpdateFile|{name}")

                bot.send_message(message.chat.id, f"Успешно добавлен{sendText} [{name}]!",
                                 reply_markup=menu_keyboard(userID))

                updatedData.saveAll()
            else:
                if isWhat == 0:
                    if updatedData.groups.count(name) == 0:
                        bot.send_message(message.chat.id, f"Группы [{name}] не существует!",
                                         reply_markup=menu_keyboard(userID))
                        return
                    groupIndex = updatedData.groups.index(name)
                    updatedData.groups.pop(groupIndex)
                    updatedData.groups_data_cur.pop(groupIndex)
                    updatedData.groups_data_next.pop(groupIndex)
                    sendText = "а группа"
                elif isWhat == 1:
                    if updatedData.pairs.count(name) == 0:
                        bot.send_message(message.chat.id, f"Пары [{name}] не существует!",
                                         reply_markup=menu_keyboard(userID))
                        return
                    updatedData.pairs.remove(name)
                    sendText = "а пара"
                elif isWhat == 2:
                    if updatedData.teachers.count(name) == 0:
                        bot.send_message(message.chat.id, f"Преподавателя [{name}] не существует!",
                                         reply_markup=menu_keyboard(userID))
                        return
                    updatedData.teachers.remove(name)
                    sendText = " преподаватель"

                bot.send_message(message.chat.id, f"Успешно удален{sendText} [{name}]!",
                                 reply_markup=menu_keyboard(userID))

        else:
            if isAdd:
                bot.send_message(message.chat.id, "В создании отклонено!", reply_markup=menu_keyboard(userID))
            else:
                bot.send_message(message.chat.id, "В удалении отклонено!", reply_markup=menu_keyboard(userID))

    else:
        if not isAdd:
            if isWhat == 0:
                if updatedData.groups.count(text) == 0:
                    bot.send_message(message.chat.id, f"Группы [{text}] не существует!",
                                     reply_markup=menu_keyboard(userID))
                    return
            elif isWhat == 1:
                if updatedData.pairs.count(text) == 0:
                    bot.send_message(message.chat.id, f"Пары [{text}] не существует!",
                                     reply_markup=menu_keyboard(userID))
                    return
            else:
                if updatedData.teachers.count(text) == 0:
                    bot.send_message(message.chat.id, f"Преподавателя [{text}] не существует!",
                                     reply_markup=menu_keyboard(userID))
                    return
        else:
            if isWhat == 0 and updatedData.groups.count(text) != 0:
                bot.send_message(message.chat.id, f"Группа [{text}] уже существует!",
                                 reply_markup=menu_keyboard(userID))
                return
            elif isWhat == 1 and updatedData.pairs.count(text) != 0:
                bot.send_message(message.chat.id, f"Пара [{text}] уже существует!",
                                 reply_markup=menu_keyboard(userID))
                return
            elif isWhat == 2 and updatedData.teachers.count(text) != 0:
                bot.send_message(message.chat.id, f"Преподаватель [{text}] уже существует!",
                                 reply_markup=menu_keyboard(userID))
                return

        bot.send_message(message.chat.id, "Вы уверены? (Введите \"Подтверждаю!\")", reply_markup=menu_keyboard(userID))
        bot.register_next_step_handler_by_chat_id(message.chat.id, dev_action, isAdd, isWhat, True, text)


@bot.message_handler(content_types=["web_app_data"])
def on_webapp_msg(message):

    global updatedData

    data = group_data.loadWeekWeb(message.web_app_data.data)
    groupIndex = data[0]
    nextWeek = data[1] == 1
    weekData: group_data.WeekData = [
        data[2], data[3],
        data[4], data[5],
        data[6], data[7]
    ]
    if len(data) > 8:
        weekData = weekData + [
            data[8], data[9],
            data[10], data[11],
            data[12], data[13]
        ]
    weekDataJson = group_data.saveWeek(weekData)
    if groupIndex == -1:
        urlData = [updatedData.pairs, updatedData.teachers, updatedData.groups,
                   weekDataJson if not nextWeek else [], weekDataJson if nextWeek else []]

        url = "https://drovyng.github.io/ATTS_Schedule_Bot_Website#customdata"
        url += json.dumps(urlData, ensure_ascii=False).replace(
            "[", "q").replace("\"", "w").replace("]", "e").replace(" ", "r").replace(",", "t").replace(".", "y")
        url += "customdataend"

        markup2 = ReplyKeyboardMarkup(resize_keyboard=True)
        markup2.row(KeyboardButton("Исправить",
                                   web_app=WebAppInfo(url)))

        bot.send_message(message.chat.id, "Ошибка: Не введена группа!", reply_markup=markup2)
        return


    updatedData.check()

    lastTeachers = teachersPairs[:]

    (updatedData.groups_data_next if nextWeek else updatedData.groups_data_cur)[groupIndex] = weekDataJson

    recalculateTeachersPairsAll()

    if not nextWeek:
        for notify in updatedData.settings:
            parsed = json.loads(notify)
            x1, x2, x3, x4 = parsed

            studentGroup = findStudentGroup(x1)
            isTeacher = findIsTeacher(x1)

            if (studentGroup == groupIndex or isTeacher) and x4 == True:
                img = None
                if isTeacher:
                    index = findTeacherIndex(x1)
                    if lastTeachers[0][index] != teachersPairs[0][index]:
                        img = imaginazer.toImageTeacher(
                            teachersPairs[0][index],
                            updatedData.pairs,
                            updatedData.teachers
                        )
                    else:
                        continue
                else:
                    img = imaginazer.toImage(
                        weekData,
                        updatedData.pairs,
                        updatedData.teachers,
                        getUserSettings(x1)[4]
                    )
                img.seek(0)
                bot.send_photo(x1, img, f"⚠️ Пары на эту неделю были обновлены! ⚠️")

    updatedData.saveAll()

    bot.send_message(message.chat.id, f"Данные успешно применены!", reply_markup=telebot.types.ReplyKeyboardRemove())



import traceback

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message: Message):
    global updatedData, KeyboardButtonsOld
    import exel_file_parser
    try:
        userID = message.from_user.id

        if not getIsEditor(userID) or not message.document.file_name.endswith(".xls"):
            return

        bot.send_message(message.chat.id, f"Загрузка файла...")

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        bot.send_message(message.chat.id, "Файл Загружен! Парсим...")

        data = exel_file_parser.try_get_data(downloaded_file, updatedData.pairs, updatedData.teachers)

        markup = InlineKeyboardMarkup()

        dataStr = "!"
        markup.row(kb(3))
        names = []

        i = -1
        for grpData in data:
            i += 1
            grpName, week = grpData

            dataStr += json.dumps(week, ensure_ascii=False) + "!"
            markup.row(InlineKeyboardButton(grpName, callback_data=f"lg_{i+1}"))
            names.append(grpName)

        dataStr += "^"
        for grpName in names:
            dataStr += grpName + "^"

        bot.send_message(message.chat.id, f"Выберите группу, затем нажмите ещё раз для загрузки...\n\n<tg-spoiler>{dataStr}</tg-spoiler>", reply_markup=markup, parse_mode="HTML")


    except exel_file_parser.ParseDataError as err:
        bot.send_message(message.chat.id, "⚠️ ОШИБКА ПАРСИНГА!!! ⚠️")
        bot.send_message(message.chat.id, str(err))

    except Exception:
        err = traceback.format_exc(4, True)
        bot.send_message(message.chat.id, "Что-то Сломалось...")
        bot.send_message(message.chat.id, err)


import os

nowTime = datetime.datetime.now().hour
lastTime = 0
if os.path.exists("lastHour"):
    with open("lastHour", "r") as file:
        lastTime = int(file.read())

if lastTime != nowTime:
    curDay: int = datetime.datetime.now().isocalendar().weekday
    for notify in updatedData.settings:
        parsed: group_data.Settings = json.loads(notify)

        x1, x2, x3, x4 = parsed[:4]

        groupID = findStudentGroup(x1)
        if groupID == -1:
            continue

        if str(x2) != "False" and NotifyButtonsTimesInt[x2] == nowTime:
            try:
                dayIndex = curDay
                text = "завтра"
                addEndText = ""
                if x2 <= 12:
                    dayIndex -= 1
                    text = "сегодня"
                if dayIndex < 6:
                    curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_cur[groupID])
                    curDay: group_data.DayData = curWeek[dayIndex]

                    img = None
                    if findIsTeacher(x1):
                        img = imaginazer.toImageDayTeacher(
                            teachersPairs[0][findTeacherIndex(x1)][dayIndex],
                            days[dayIndex],
                            updatedData.pairs,
                            updatedData.groups
                        )
                    else:
                        img = imaginazer.toImageDay(
                            curWeek,
                            dayIndex,
                            updatedData.pairs,
                            updatedData.teachers,
                            getUserSettings(x1)[4]
                        )
                        addEndText = f"\nПриходить к {max(0, curDay[0])+1}-й паре!"
                    img.seek(0)
                    bot.send_photo(x1, img, f"Вот пары на {text}{addEndText}")
            except Exception:
                pass
        if str(x3) != "False" and NotifyButtonsTimesInt[x3] == nowTime and (
                (curDay == 7 and NotifyButtonsTimesInt[x3] > 12) or (curDay == 1 and NotifyButtonsTimesInt[x3] <= 12)):
            try:
                dayNextText = "следующую"
                if curDay != 7:
                    dayNextText = "эту"
                groups_data_where = updatedData.groups_data_next if curDay == 7 else updatedData.groups_data_cur
                if groups_data_where[groupID].count("[") < 10:
                    bot.send_message(x1, f"🔔 Извините, но расписание на {dayNextText} неделю ещё недоступно :( 🔔")
                    continue
                img = None
                if findIsTeacher(x1):
                    nextWeekInt = 1 if curDay == 7 else 0
                    curWeek: group_data.WeekDataTeacher = teachersPairs[nextWeekInt][findTeacherIndex(x1)]
                    img = imaginazer.toImageTeacher(
                        curWeek,
                        updatedData.pairs,
                        updatedData.groups
                    )
                else:
                    curWeek: group_data.WeekData = group_data.loadWeek(groups_data_where[groupID])
                    img = imaginazer.toImage(
                        curWeek,
                        updatedData.pairs,
                        updatedData.teachers,
                        getUserSettings(x1)[4]
                    )
                img.seek(0)
                bot.send_photo(x1, img, f"🔔 Вот пары на {dayNextText} неделю 🔔")
            except Exception:
                pass

    with open("lastHour", "w") as file:
        file.write(str(nowTime))



import threading, time
from run_saver import RunSaver


def thread_check_time(saver: RunSaver, updatedData: UpdatedData):
    time.sleep(5)

    e = -1

    while saver.running:
        if updatedData.saveTimer <= 0:
            updatedData.saveAll()
            updatedData.saveTimer = 60   # 1 minute
            e += 1
            if e >= 20:                  # 40 minutes
                saver.running = False
                bot.stop_bot()
                raise Exception("BotRestartCommand")

        updatedData.saveTimer -= 2
        time.sleep(2)                 # 10 minutes


def run_bot(saver: RunSaver):

    threading.Thread(target=thread_check_time, args=(saver, updatedData)).start()

    bot.polling(non_stop=True)