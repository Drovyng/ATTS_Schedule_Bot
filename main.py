from typing import Union

import config
import group_data, sheets, json
import imaginazer

ChatMessages: dict[str, Union[str, list, tuple]] = {
    "start": [
        "Привет! Если ты студент <b>Армавирского Техникума Технологии и Сервиса</b>, то с помощью этого бота ты можешь узнать расписание в любое время!",
        "Привет, разработчик! Я создан для того, чтобы студенты <b>Армавирского Техникума Технологии и Сервиса</b> могли узнать расписание в любое время!"
    ],
    "dev": "Включён режим разработчика"
}

KeyboardButtons: list[str] = [
    "Выбрать Группу 🗒",
    "Режим Разработчика 🔧",

    "Загрузить Расписание ✏️",
    "Меню 📋",

    "Выйти ❌",
    "Расписание 📄",
    "Расписание (День) 📄",

    "Добавить Группу",
    "Удалить Группу",
    "Добавить Пару",
    "Удалить Пару",
    "Добавить Преподавателя",
    "Удалить Преподавателя",

    "Перезагрузить бота 🔄",
    "Обновить файл",
    "Консоль",
    "Команда",

    "Уведомления 🔔",
    "Назад ◀️",
    "Режим Работы ⚡️"
]
NotifyButtons: list[str] = [
    "На след. день",
    "На след. неделю",
    "Измен. расписания",
    KeyboardButtons[3]
]
NotifyButtonsSelect: list[str] = [
    "Изменить ✏️",
    "Включить ✅",
    "Выключить ❌",
    KeyboardButtons[3]
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
    KeyboardButtons[3]
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
    KeyboardButtons[4],
    "⏪",
    "⏩",
    KeyboardButtons[3]
]
truefalseEmoji = ["❌", "✅"]
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", KeyboardButtons[3], "Сегодня", "Завтра"]

teacherGroup = "Преподаватель"
modes = ["Студент 🙋🏻", "Преподаватель ⭐️"]

import datetime

class UpdatedData():
    def __init__(self):
        self.devs: list[str] = []
        self.teachers: list[str] = []
        self.pairs: list[str] = []
        self.groups: list[str] = []
        self.students: list[str] = []
        self.groups_data_cur: list[str] = []
        self.groups_data_next: list[str] = []
        self.groups_week: int = 0

        self.notifies: list[str] = []

        self.onSaveAll = None

        self.resize()

        self.reloadAll()

    def resize(self):

        self.devsCount = len(self.devs)
        self.teachersCount = len(self.teachers)
        self.pairsCount = len(self.pairs)
        self.groupsCount = len(self.groups)
        self.studentsCount = len(self.students)
        self.notifiesCount = len(self.notifies)

    def reloadAll(self):
        self.devsCount = int(sheets.getRange("A2")[0][0])
        if self.devsCount > 0:
            self.devs = sheets.getRange(f"A3:A{2 + self.devsCount}")[0]

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

        self.notifiesCount = int(sheets.getRange("F2")[0][0])
        if self.notifiesCount > 0:
            self.notifies = sheets.getRange(f"F3:F{2 + self.notifiesCount}")[0]

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

        sheets.setRange("A2", [[str(len(self.devs))]])
        sendDevs = self.devs[:]
        while len(sendDevs) < self.devsCount: sendDevs.append("")
        sheets.setRange(f"A3:A{2 + max(self.devsCount, len(sendDevs))}", [sendDevs])

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

        sheets.setRange("F2", [[str(len(self.notifies))]])
        sendNotifies = self.notifies[:]
        while len(sendNotifies) < self.notifiesCount: sendNotifies.append("")
        sheets.setRange(f"F3:F{2 + max(self.notifiesCount, len(sendNotifies))}", [sendNotifies])

        self.resize()

        self.onSaveAll()


updatedData = UpdatedData()

emptyTeacherDay: group_data.DayDataTeacher = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]


teachersPairs: list[list[group_data.WeekDataTeacher]] = [[], []]

def recalculateTeachersPairs(nextWeek: bool):
    global updatedData, teachersPairs, emptyTeacherDay
    nextWeekInt = 1 if nextWeek else 0
    teachersPairs[nextWeekInt] = [[emptyTeacherDay, emptyTeacherDay, emptyTeacherDay, emptyTeacherDay, emptyTeacherDay, emptyTeacherDay] for i in updatedData.teachersCount]

    toRead = updatedData.groups_data_cur if nextWeek else updatedData.groups_data_next

    for i in range(updatedData.groupsCount):
        data = toRead[i]
        if data.count("[") < 10:
            continue
        parsed: group_data.WeekData = json.loads(data)

        for d in range(len(parsed)):
            day = parsed[d]
            p = -1
            for pair in [day[1], day[2], day[3]]:
                p += 1
                offset = p + day[0]
                if offset >= 6:
                    break
                if pair[0] == -1:
                    continue

                teachersPairs[nextWeekInt][pair[1]][offset] = [pair[0], i, pair[2]]

def recalculateTeachersPairsAll():
    recalculateTeachersPairs(False)
    recalculateTeachersPairs(True)


updatedData.onSaveAll = recalculateTeachersPairsAll
recalculateTeachersPairsAll()


import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

bot = telebot.TeleBot(config.bot_token)
developers: list[int] = [
    1157843932,  # Дмитрий
    1085752896  # Быленко М.И.
]


def getChatMessage(key: str, isDev: bool = False):
    global ChatMessages

    msg = ChatMessages[key]
    if isinstance(msg, list | tuple):
        if isDev and len(msg) > 1:
            return msg[1]
        else:
            return msg[0]
    else:
        return msg


def findStudent(userID) -> list:
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

def findStudentGroup(userID) -> int:
    global updatedData
    student = findStudent()
    if student == None or not student[1] in updatedData.groups:
        return -1
    return updatedData.groups.index(student[1])


def getIsDev(userID: int) -> bool:
    global updatedData
    return userID in updatedData.devs or userID in developers


def getUserNotifyIndex(userID: int) -> int:
    global updatedData
    i = 0
    for st in updatedData.notifies:
        if json.loads(st)[0] == userID:
            return i
        i += 1
    return -1


def menu_keyboard(userID: int) -> ReplyKeyboardMarkup:
    global developers, updatedData
    isInGroup = findStudentIndex(userID) != -1
    isDev = getIsDev(userID)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    if isInGroup:
        markup.row(KeyboardButton(KeyboardButtons[5]), KeyboardButton(KeyboardButtons[6]),
                   KeyboardButton(KeyboardButtons[0]))
        markup.row(KeyboardButton(KeyboardButtons[19]), KeyboardButton(KeyboardButtons[17]))
    else:
        markup.row(KeyboardButton(KeyboardButtons[0]))

    if isDev:
        markup.row(KeyboardButton(KeyboardButtons[1]))

    return markup

def btnsMarkup(btns: list[str], maxLen:int = 5) -> ReplyKeyboardMarkup:
    lengrp = len(btns)
    inrow = min(lengrp, maxLen)
    rows = lengrp // inrow

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    b = 0
    for i in range(rows):
        inRow = []
        for j in range(0, min(lengrp - inrow * i, inrow)):
            inRow.append(KeyboardButton(btns[b]))
            b += 1
        markup.row(*inRow)
    return markup


def getGroupsList(course:int) -> list[str]:
    btns = []
    for grp in updatedData.groups:
        courseYear = datetime.datetime.now().isocalendar()[0] - course
        if grp.startswith(str(courseYear)[-2:]):
            btns.append(grp)


@bot.message_handler(commands=['start', 'clear', 'menu'])
def start(message: Message):
    global KeyboardButtons

    userID = message.from_user.id
    isDev = getIsDev(userID)

    bot.send_message(message.chat.id, getChatMessage("start", isDev), reply_markup=menu_keyboard(userID),
                     parse_mode="html")


@bot.message_handler()
def on_message(message: Message):
    global KeyboardButtons, updatedData

    updatedData.check()

    userID = message.from_user.id
    isDev = getIsDev(userID)
    text = message.text

    textIndex = -1
    if KeyboardButtons.count(text) > 0:
        textIndex = KeyboardButtons.index(text)

    if textIndex == 3:
        start(message)
    elif textIndex == 5:
        studentIndex = findStudentIndex(userID)
        if studentIndex == -1:
            bot.send_message(message.chat.id, f"Вы не подключены к группе!", reply_markup=menu_keyboard(userID))
            return
        groupID = -1
        groupName = json.loads(updatedData.students[studentIndex])[1]
        if updatedData.groups.count(groupName) != 0:
            groupID = updatedData.groups.index(groupName)
        if groupID == -1 or updatedData.groups_data_cur[groupID].count("[") < 10:
            bot.send_message(message.chat.id, f"Расписание на эту неделю ещё не добавлено!",
                             reply_markup=menu_keyboard(userID))
            return
        img = imaginazer.toImage(
            group_data.loadWeek(
                updatedData.groups_data_cur[groupID]
            ),
            updatedData.pairs,
            updatedData.teachers
        )
        img.seek(0)
        bot.send_photo(message.chat.id, img, "Вот пары на эту неделю", reply_markup=menu_keyboard(userID))

    elif textIndex == 6:
        studentIndex = findStudentIndex(userID)

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add(*days)
        studentIndex = findStudentIndex(userID)
        if studentIndex == -1:
            bot.send_message(message.chat.id, f"Вы не подключены к группе!", reply_markup=menu_keyboard(userID))
            return

        bot.send_message(message.chat.id, f"На какой день вы хотите узнать расписание?", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, get_pair_day)


    elif textIndex == 0:
        markup = btnsMarkup(getGroupsList(0), 5)
        btns = SelectGroupButtons[:]
        btns.insert(2, "1-й Курс")
        btns[1] = truefalseEmoji[0]
        markup.row(*btns)

        bot.send_message(message.chat.id, "Выберите Группу...", reply_markup=markup)
        bot.register_next_step_handler(message, select_group, 0)

    elif textIndex == 1 and isDev:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        urlData = [updatedData.pairs, updatedData.teachers, updatedData.groups, updatedData.groups_data_cur, updatedData.groups_data_next]
        
        

        url = "https://drovyng.github.io/ATTS_Schedule_Bot_Website#customdata"
        url += json.dumps(urlData, ensure_ascii=False).replace(
            "[", "q").replace("\"", "w").replace("]", "e").replace(" ", "r").replace(",", "t").replace(".", "y")
        url += "customdataend"

        markup.row(
            KeyboardButton(KeyboardButtons[2], web_app=WebAppInfo(url)),
            KeyboardButton(KeyboardButtons[3])
        )
        markup.row(
            KeyboardButton(KeyboardButtons[7]),
            KeyboardButton(KeyboardButtons[8]),
            KeyboardButton(KeyboardButtons[9])
        )
        markup.row(
            KeyboardButton(KeyboardButtons[10]),
            KeyboardButton(KeyboardButtons[11]),
            KeyboardButton(KeyboardButtons[12])
        )
        markup.row(
            KeyboardButton(KeyboardButtons[13]),
        )
        markup.row(
            KeyboardButton(KeyboardButtons[14]),
            KeyboardButton(KeyboardButtons[15]),
            KeyboardButton(KeyboardButtons[16])
        )

        bot.send_message(message.chat.id, getChatMessage("dev"), reply_markup=markup)
    elif textIndex == 13 and isDev:
        bot.send_message(message.chat.id, f"Бот в процессе перезагрузки!",
                         reply_markup=menu_keyboard(message.from_user.id))
        raise Exception("BotRestartCommand")
    elif textIndex == 14 and isDev:
        bot.send_message(message.chat.id, f"Введите название файла")
        bot.register_next_step_handler_by_chat_id(message.chat.id, dev_action, True, 3, False, None)
    elif textIndex == 15 and isDev:
        img = imaginazer.getScreenshot()
        img.seek(0)
        bot.send_photo(message.chat.id, img, "Вот скрин консоли", reply_markup=menu_keyboard(userID))
    elif textIndex == 16 and isDev:
        bot.send_message(message.chat.id, f"Введите команду")
        bot.register_next_step_handler_by_chat_id(message.chat.id, dev_command)
    elif textIndex == 17:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        notifyIndex = getUserNotifyIndex(userID)
        notifyData = [userID, False, False, False]

        if notifyIndex != -1:
            notifyData = json.loads(updatedData.notifies[notifyIndex])

        btns = []

        for i in range(len(NotifyButtons) - 1):
            isTrue = 0
            if str(notifyData[i + 1]) != "False":
                isTrue = 1
            btns.append(NotifyButtons[i] + " " + truefalseEmoji[isTrue])

        btns.append(NotifyButtons[-1])

        lengrp = len(btns)
        inrow = min(lengrp, 2)
        rows = lengrp // inrow

        b = 0
        for i in range(rows):
            inRow = []
            for j in range(0, min(lengrp - inrow * i, inrow)):
                inRow.append(KeyboardButton(btns[b]))
                b += 1
            markup.row(*inRow)

        bot.send_message(message.chat.id, "Выберите пункт:", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, notify_select, notifyData, 0, -1)
        
    elif textIndex == 19:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, "Выберите режим:", reply_markup=markup)
        #bot.register_next_step_handler_by_chat_id(message.chat.id, notify_select, notifyData, 0, -1)

    elif textIndex >= 7 and textIndex < 13 and isDev:
        isAdd = textIndex % 2 == 1
        isWhat = (textIndex - 7) // 2
        if not isAdd:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            strList = []
            if isWhat == 0:
                strList = updatedData.groups
            elif isWhat == 1:
                strList = updatedData.pairs
            else:
                strList = updatedData.teachers

            lengrp = len(strList)
            inrow = min(lengrp, 5)
            rows = lengrp // inrow

            b = 0
            for i in range(rows):
                inRow = []
                for j in range(0, min(lengrp - inrow * i, inrow)):
                    inRow.append(KeyboardButton(strList[b]))
                    b += 1
                markup.row(*inRow)

            bot.send_message(message.chat.id, "Выберите то, что хотите удалить", reply_markup=markup)
        else:
            sendText = ""
            if isWhat == 0:
                sendText = "й группы"
            elif isWhat == 1:
                sendText = "й пары"
            else:
                sendText = "го преподавателя"
            bot.send_message(message.chat.id, f"Напишите название ново{sendText}")

        bot.register_next_step_handler_by_chat_id(message.chat.id, dev_action, isAdd, isWhat, False, None)


def set_notify_data(notifyData):
    global updatedData
    userIndex = getUserNotifyIndex(notifyData[0])
    jsoned = json.dumps(notifyData)
    if userIndex == -1:
        updatedData.notifies.append(jsoned)
    else:
        updatedData.notifies[userIndex] = jsoned


def notify_select(message: Message, notifyData, layer:int = 0, curSelected:int = 0):
    global updatedData, NotifyButtons, KeyboardButtons, NotifyButtonsTimes, NotifyButtonsSelect

    text = message.text
    userID = message.from_user.id

    if text == KeyboardButtons[3]:
        start(message)
        return

    if layer == 0:
        punkt = text[:-2]
        if punkt in NotifyButtons:
            punktIndex = NotifyButtons.index(punkt)
            punktToggled = notifyData[punktIndex+1]
            btns = []
            if punktToggled:
                if punktIndex != 2:
                    btns.append(NotifyButtonsSelect[0])
                btns.append(NotifyButtonsSelect[2])
            else:
                btns.append(NotifyButtonsSelect[1])     # Включить
            btns.append(NotifyButtonsSelect[3])         # Назад

            bot.send_message(message.chat.id, f"Открыты настройки пункта [{punkt}]:", reply_markup=btnsMarkup(btns))
            bot.register_next_step_handler_by_chat_id(message.chat.id, notify_select, notifyData, 1, punktIndex)

    elif layer == 1:
        punkt = NotifyButtons[curSelected]
        punktToggled = notifyData[curSelected+1]
        toggleOn = (not punktToggled and text == NotifyButtonsSelect[1])
        if (punktToggled and text == NotifyButtonsSelect[0]) or (toggleOn and curSelected != 2):
            btns = NotifyButtonsTimes[:]
            bot.send_message(message.chat.id, f"Выберите время для присылания уведомление [{punkt}]:", reply_markup=btnsMarkup(btns))
            bot.register_next_step_handler_by_chat_id(message.chat.id, notify_select, notifyData, 2, curSelected)
        elif toggleOn and curSelected == 2:
            x1, x2, x3, x4 = notifyData
            notifyData = x1, x2, x3, True
            set_notify_data(notifyData)
            updatedData.saveAll()
            bot.send_message(message.chat.id, f"Вы успешно включили уведомление [{punkt}]!", reply_markup=menu_keyboard(userID))
        elif text == NotifyButtonsSelect[2]:
            x1, x2, x3, x4 = notifyData
            if curSelected == 0: x2 = False
            elif curSelected == 1: x3 = False
            elif curSelected == 3: x4 = False
            notifyData = x1, x2, x3, x4
            set_notify_data(notifyData)
            updatedData.saveAll()
            bot.send_message(message.chat.id, f"Вы успешно отключили уведомление [{punkt}]!",
                             reply_markup=menu_keyboard(userID))

    elif layer == 2:
        punkt = NotifyButtons[curSelected]
        if text in NotifyButtonsTimes:
            timeIndex = NotifyButtonsTimes.index(text)
            x1, x2, x3, x4 = notifyData
            if curSelected == 0: x2 = timeIndex
            elif curSelected == 1: x3 = timeIndex
            notifyData = x1, x2, x3, x4
            set_notify_data(notifyData)
            updatedData.saveAll()
            bot.send_message(message.chat.id, f"Вы успешно включили уведомление [{punkt}] на время [{NotifyButtonsTimes[timeIndex]}]!", reply_markup=menu_keyboard(userID))



def dev_command(message: Message):
    exec(message.text)
    img = imaginazer.getScreenshot()
    img.seek(0)
    bot.send_photo(message.chat.id, img, "Вот скрин консоли", reply_markup=menu_keyboard(message.from_user.id))


def get_pair_day(message: Message):
    global updatedData

    text = message.text
    userID = message.from_user.id

    if text == KeyboardButtons[3]:
        start(message)
        return

    studentIndex = findStudentIndex(userID)
    if studentIndex == -1:
        bot.send_message(message.chat.id, f"Вы не подключены к группе!", reply_markup=menu_keyboard(userID))
        return
    groupID = -1
    groupName = json.loads(updatedData.students[studentIndex])[1]
    if updatedData.groups.count(groupName) != 0:
        groupID = updatedData.groups.index(groupName)
    if groupID == -1 or updatedData.groups_data_cur[groupID].count("[") < 10:
        bot.send_message(message.chat.id, f"Расписание на эту неделю ещё не добавлено!",
                         reply_markup=menu_keyboard(userID))
        return

    if days.count(text) == 0:
        bot.send_message(message.chat.id, f"Неизвестный день!", reply_markup=menu_keyboard(userID))
        return
    curDay = datetime.datetime.now().isocalendar().weekday;
    dayIndex = 0
    if text == "Сегодня":
        if curDay == 7:
            bot.send_message(message.chat.id, f"Недоступный день!", reply_markup=menu_keyboard(userID))
            return
        dayIndex = curDay - 1
    elif text == "Завтра":
        if curDay >= 6:
            bot.send_message(message.chat.id, f"Недоступный день!", reply_markup=menu_keyboard(userID))
            return
        dayIndex = curDay
    else:
        dayIndex = days.index(text)

    curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_cur[groupID])
    curDay: group_data.DayData = curWeek[dayIndex]

    img = imaginazer.toImageDay(
        curDay,
        days[dayIndex],
        updatedData.pairs,
        updatedData.teachers
    )
    img.seek(0)
    bot.send_photo(message.chat.id, img, f"Вот пары на {text.lower()}", reply_markup=menu_keyboard(userID))


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
                updatedData.saveAll()
                bot.send_message(message.chat.id, f"Успешно добавлен{sendText} [{name}]!",
                                 reply_markup=menu_keyboard(userID))
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
                updatedData.saveAll()
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


def select_group(message: Message, course:int):
    global KeyboardButtons, updatedData, developers
    text = message.text
    userID = message.from_user.id
    studentIndex = findStudentIndex(userID)
    group = ""
    changed = False

    if studentIndex != -1:
        group = json.loads(updatedData.students[studentIndex])[1]

    if text == truefalseEmoji[0]:
        bot.register_next_step_handler(message, select_group, updatedData.groups, course)
        
    if text == SelectGroupButtons[0]:
        start(message)
        return
    if text == SelectGroupButtons[1]:
        markup = btnsMarkup(getGroupsList(course-1), 5)
        btns = SelectGroupButtons[:]
        btns.insert(2, f"{course}-й Курс")
        markup.row(*btns)
        
        if len(getGroupsList(course-1)) == 0:
            btns[1] = truefalseEmoji[0]

        bot.send_message(message.chat.id, "Выберите Группу...", reply_markup=markup)
        bot.register_next_step_handler(message, select_group, course-1)
        return
    if text == SelectGroupButtons[2]:
        markup = btnsMarkup(getGroupsList(course+1), 5)
        btns = SelectGroupButtons[:]
        btns.insert(2, f"{course}-й Курс")
        markup.row(*btns)
        
        if len(getGroupsList(course+2)) == 0:
            btns[3] = truefalseEmoji[0]

        bot.send_message(message.chat.id, "Выберите Группу...", reply_markup=markup)
        bot.register_next_step_handler(message, select_group, course+1)
        return
    if text == SelectGroupButtons[3]:
        if studentIndex == -1:
            bot.send_message(message.chat.id, f"Вы и так не подключены к группе!", reply_markup=menu_keyboard(userID))
        else:
            updatedData.students.pop(studentIndex)
            bot.send_message(message.chat.id, f"Вы больше не подключены к группе [{group}]!",
                             reply_markup=menu_keyboard(userID))
            updatedData.saveAll()
        return

    if text in updatedData.groups:
        if group != text:
            if studentIndex != -1:
                updatedData.students.pop(studentIndex)
            updatedData.students.append(json.dumps([userID, text], ensure_ascii=False))
            updatedData.saveAll()
            bot.send_message(message.chat.id, f"Вы подключены к группе [{text}]!", reply_markup=menu_keyboard(userID))
        else:
            bot.send_message(message.chat.id, f"Вы уже подключены к группе [{text}]!",
                             reply_markup=menu_keyboard(userID))
        return

    bot.send_message(message.chat.id, f"Неизвестный вариант ответа.", reply_markup=menu_keyboard(userID))


@bot.message_handler(content_types=["web_app_data"])
def on_webapp_msg(message):
    global updatedData
    data = group_data.loadWeekWeb(message.web_app_data.data)
    groupIndex = data[0]
    if groupIndex == -1:
        bot.send_message(message.chat.id, "Ошибка: Не введена группа!")
        return
    nextWeek = data[1] == 1

    weekData: group_data.WeekData = [
        data[2], data[3], data[4],
        data[5], data[6], data[7]
    ]
    weekDataJson = group_data.saveWeek(weekData)

    updatedData.check()

    if nextWeek:
        updatedData.groups_data_next[groupIndex] = weekDataJson
    else:
        updatedData.groups_data_cur[groupIndex] = weekDataJson
        
        for notify in updatedData.notifies:
            parsed = json.loads(notify)
            x1, x2, x3, x4 = parsed
            
            studentGroup = findStudentGroup(x1)
            
            if studentGroup == groupIndex and x4 == True:
                img = None
                if studentGroup == teacherGroup:
                    pass
                else:
                    img = imaginazer.toImage(
                        weekData,
                        updatedData.pairs,
                        updatedData.teachers
                    )
                img.seek(0)
                bot.send_photo(x1, img, f"⚠️ Пары на эту неделю были обновлены! ⚠️")
                
    updatedData.saveAll()

    bot.send_message(message.chat.id, f"Данные успешно применены!", reply_markup=menu_keyboard(message.from_user.id))



import threading, time, os
from run_saver import RunSaver


def thread_check_time(saver: RunSaver, updatedData: UpdatedData, hoursList: list[int], daysList: list[str]):
    time.sleep(5)
    
    i = 0
    
    while saver.running:
        
        if i == 0:
            nowTime = datetime.datetime.now().hour
            lastTime = 0
            if os.path.exists("lastHour"):
                with open("lastHour", "r") as file:
                    lastTime = int(file.read())

            if lastTime != nowTime:
                curDay = datetime.datetime.now().isocalendar().weekday
                for notify in updatedData.notifies:
                    parsed = json.loads(notify)
                    x1, x2, x3, x4 = parsed

                    groupID = findStudentGroup(x1)
                    if groupID == -1:
                        continue

                    if str(x2) != "False" and hoursList[x2] == nowTime:
                        try:
                            dayIndex = curDay
                            text = "завтра"
                            if x2 <= 12:
                                dayIndex -= 1
                                text = "сегодня"
                            if dayIndex < 6:
                                curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_cur[groupID])
                                curDay: group_data.DayData = curWeek[dayIndex]

                                img = imaginazer.toImageDay(
                                    curDay,
                                    days[dayIndex],
                                    updatedData.pairs,
                                    updatedData.teachers
                                )
                                img.seek(0)
                                bot.send_photo(x1, img, f"Вот пары на {text}")
                        except Exception:
                            pass
                    if str(x3) != "False" and hoursList[x3] == nowTime and ((curDay == 7 and hoursList[x3] > 12) or (curDay == 1 and hoursList[x3] <= 12)):
                        try:
                            dayNextText = "следующую"
                            if curDay == 1: dayNextText = "эту"
                            if updatedData.groups_data_next[groupID].count("[") < 10:
                                bot.send_message(x1, f"🔔 Извините, но расписание на {dayNextText} неделю ещё недоступно :( 🔔")
                                continue
                            curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_next[groupID])

                            img = imaginazer.toImage(
                                curWeek,
                                updatedData.pairs,
                                updatedData.teachers
                            )
                            img.seek(0)
                            bot.send_photo(x1, img, f"🔔 Вот пары на следующую неделю 🔔")
                        except Exception:
                            pass

                with open("lastHour", "w") as file:
                    file.write(str(nowTime))
        i += 1
        i %= 300
        time.sleep(2)                 # 10 minutes


def run_bot(saver: RunSaver):
    
    threading.Thread(target=thread_check_time, args=(saver, updatedData, NotifyButtonsTimesInt, days)).start()

    bot.polling(non_stop=True)