from typing import Union

import config
import group_data, sheets, json
import imaginazer

KeyboardButtons: list[str] = [
    "Выбрать Группу 🗒",
    "Админ 🔧",

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
    "Выбрать Роль ⚡️",
    "Выбрать ФИО 🔆",
    "Сменить Роль ⚡️",
    "Редактор 🧷",
    "Статистика",
    "Список",

    "Список 📋",         # 25 index
    "Обратная связь 📝"  # 26 index
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
WorkModeButtons = [
    "Студент 🙋🏻",
    "Преподаватель 🔆",
    KeyboardButtons[3]
]
FeedbackButtons = [
    KeyboardButtons[3],
    "Вопрос ❓",
    "Ошибка 🚫",
    "Предложение 🤔",
    "Другое 🌐"
]
truefalseEmoji = ["❌", "✅"]
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", KeyboardButtons[3], "Сегодня", "Завтра"]

modes = ["Студент 🙋🏻", "Преподаватель ⭐️"]

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

        self.notifies: list[str] = []

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
        self.notifiesCount = len(self.notifies)

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

        sheets.setRange("F2", [[str(len(self.notifies))]])
        sendNotifies = self.notifies[:]
        while len(sendNotifies) < self.notifiesCount: sendNotifies.append("")
        sheets.setRange(f"F3:F{2 + max(self.notifiesCount, len(sendNotifies))}", [sendNotifies])

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
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

bot = telebot.TeleBot(config.bot_token)



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


def getUserNotifyIndex(userID: int) -> int:
    global updatedData
    i = 0
    for st in updatedData.notifies:
        if json.loads(st)[0] == userID:
            return i
        i += 1
    return -1


def menu_keyboard(userID: int) -> ReplyKeyboardMarkup:
    global updatedData
    isInGroup = findStudentIndex(userID) != -1
    isDev = getIsDev(userID)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    if isInGroup:
        groupBtnName = KeyboardButtons[20] if findIsTeacher(userID) else KeyboardButtons[0]
        markup.row(KeyboardButton(KeyboardButtons[5]), KeyboardButton(KeyboardButtons[6]),
                   KeyboardButton(groupBtnName))

    if isInGroup:
        markup.row(KeyboardButton(KeyboardButtons[25]), KeyboardButton(KeyboardButtons[26]))
        markup.row(KeyboardButton(KeyboardButtons[21]), KeyboardButton(KeyboardButtons[17]))
    else:
        markup.row(KeyboardButton(KeyboardButtons[19]))
        markup.row(KeyboardButton(KeyboardButtons[26]))

    btns = []
    if getIsEditor(userID):
        btns.append(KeyboardButton(KeyboardButtons[22]))
    if isDev:
        btns.append(KeyboardButton(KeyboardButtons[1]))

    markup.row(*btns)

    return markup

def btnsMarkup(btns: list[str], maxLen:int = 5) -> ReplyKeyboardMarkup:
    lengrp = len(btns)
    inrow = max(min(lengrp, maxLen), 1)
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


def getGroupsList(fromList:list[str], page:int, limit:int = 5) -> list[str]:
    btns: list[str] = []
    i = -1
    for grp in fromList:
        i += 1
        if page * limit * 2 <= i < page * limit * 2 + limit * 2: btns.append(grp)
    return btns


@bot.message_handler(commands=['start', 'clear', 'menu'])
def start(message: Message):
    global KeyboardButtons

    userID = message.from_user.id
    isDev = getIsDev(userID)
    
    text1 = ""
    text2 = ""

    if isDev:
        text2 = " (разработчик)"
    elif getIsEditor(userID):
        text2 = " (редактор)"

    if findIsTeacher(userID):
        text1 = ", преподаватель"
    elif findStudentIndex(userID) != -1:
        text1 = ", студент"

    bot.send_message(
        message.chat.id,
        f"Привет<b>{text1}{text2}!</b> Я создан для того, чтобы студенты и преподаватели <b>Армавирского Техникума Технологии и Сервиса</b> могли узнать расписание в любое время!", reply_markup=menu_keyboard(userID),
        parse_mode="html"
    )


@bot.message_handler()
def on_message(message: Message):
    global KeyboardButtons, updatedData

    text = message.text

    try:
        if message.reply_to_message != None and message.reply_to_message.from_user.is_bot:
            reply_text = message.reply_to_message.text
            if reply_text.count("#") >= 3:
                reply_data = reply_text.split("#")

                reply_chat = reply_data[1]

                text = f"<b>Ответ по обращению [{reply_chat}-{reply_data[2]}]:</b>\n{text}"

                bot.send_message(reply_chat, text, parse_mode="html")

                bot.send_message(message.chat.id, "Ответ успешно отправлен!")
                return
    except:
        pass

    updatedData.check()

    userID = message.from_user.id
    isDev = getIsDev(userID)

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
            if groupID == -1 or updatedData.groups_data_cur[groupID].count("[") < 10:
                bot.send_message(message.chat.id, f"Расписание на эту неделю ещё не добавлено!",
                                 reply_markup=menu_keyboard(userID))
                return
            curWeek: group_data.WeekData = group_data.loadWeek(updatedData.groups_data_cur[groupID])
            img = imaginazer.toImage(
                curWeek,
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
        markup = btnsMarkup(getGroupsList(updatedData.groups, 0), 5)
        btns = SelectGroupButtons[:]
        btns.insert(2, "Стр. 1")
        btns[1] = truefalseEmoji[0]
        markup.row(*btns)

        bot.send_message(message.chat.id, "Выберите Группу...", reply_markup=markup)
        bot.register_next_step_handler(message, select_group, 0)

    elif textIndex == 20:
        markup = btnsMarkup(getGroupsList(updatedData.teachers, 0, 3), 3)
        btns = SelectGroupButtons[:]
        btns.insert(2, "Стр. 1")
        btns[1] = truefalseEmoji[0]
        markup.row(*btns)

        bot.send_message(message.chat.id, "Выберите ФИО...", reply_markup=markup)
        bot.register_next_step_handler(message, select_teacher, 0)

    elif textIndex == 1 and isDev:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        markup.row(
            KeyboardButton(KeyboardButtons[3])
        )
        markup.row(
            KeyboardButton(KeyboardButtons[23]),
            KeyboardButton(KeyboardButtons[24])
        )
        markup.row(
            KeyboardButton(KeyboardButtons[7]),
            KeyboardButton(KeyboardButtons[9]),
            KeyboardButton(KeyboardButtons[11])
        )
        #markup.row(
            #KeyboardButton(KeyboardButtons[10]),
            #KeyboardButton(KeyboardButtons[8]),
            #KeyboardButton(KeyboardButtons[12])
        #)
        markup.row(
            KeyboardButton(KeyboardButtons[13]),
        )
        markup.row(
            KeyboardButton(KeyboardButtons[14]),
            KeyboardButton(KeyboardButtons[15]),
            KeyboardButton(KeyboardButtons[16])
        )

        bot.send_message(message.chat.id, "Открыта панель администратора.", reply_markup=markup)
    elif textIndex == 22:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        urlData = [updatedData.pairs, updatedData.teachers, updatedData.groups, updatedData.groups_data_cur,
                   updatedData.groups_data_next]

        url = "https://drovyng.github.io/ATTS_Schedule_Bot_Website#customdata"
        url += json.dumps(urlData, ensure_ascii=False).replace(
            "[", "q").replace("\"", "w").replace("]", "e").replace(" ", "r").replace(",", "t").replace(".", "y")
        url += "customdataend"

        markup.row(
            KeyboardButton(KeyboardButtons[3])
        )
        markup.row(
            KeyboardButton(KeyboardButtons[2], web_app=WebAppInfo(url))
        )

        bot.send_message(message.chat.id, "Открыта панель редактора.", reply_markup=markup)

    elif textIndex == 23 and isDev:
        notifyCount = 0
        for notify in updatedData.notifies:
            if notify.lower().count("false") < 3:
                notifyCount += 1

        groups_students: dict[str, int] = {}

        for i in range(updatedData.studentsCount):
            grpId = json.loads(updatedData.students[i])[1]
            if not grpId in groups_students:
                groups_students[grpId] = 1
            else:
                groups_students[grpId] = groups_students[grpId] + 1

        for grp in updatedData.groups:
            if not grp in groups_students:
                groups_students[grp] = 0

        textAdd = ""
        for grp in groups_students:
            textAdd += f"\n[{grp}]: {groups_students[grp]}"
            if len(textAdd) >= 3980:
                break
        bot.send_message(message.chat.id, f"Вот Статистика:\n  Уведомления: {notifyCount}\n  Группы:{textAdd}", reply_markup=menu_keyboard(userID))

    elif textIndex == 24 and isDev:
        textAdd = ""

        for stud in updatedData.students:
            parsed = json.loads(stud)
            user_name = parsed[0]
            try:
                user_name = bot.get_chat_member(parsed[0], parsed[0]).user.username
            except:
                pass
            textAdd += f"\n<a href='tg://user?id={parsed[0]}'>@{user_name}</a> - {parsed[1]}"
            if parsed[1] == "Teacher":
                textAdd += f" - {parsed[2]}"
            if len(textAdd) >= 3980:
                break
        bot.send_message(message.chat.id, f"Вот Список:{textAdd}", reply_markup=menu_keyboard(userID), parse_mode="HTML")

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
        
    elif textIndex == 19 or textIndex == 21:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(*WorkModeButtons)
        bot.send_message(message.chat.id, "Выберите режим:", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, mode_select)

    elif textIndex == 25:
        addText = ""
        for grp in range(updatedData.groupsCount):
            yesno = 0 if updatedData.groups_data_cur[grp].count("[") < 10 else 1
            addText += f"\n{updatedData.groups[grp]} - {truefalseEmoji[yesno]}"
        bot.send_message(message.chat.id, f"Сейчас пары добавлены на группы:{addText}", reply_markup=menu_keyboard(userID))

    elif textIndex == 26:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(
            KeyboardButton(FeedbackButtons[1]),
            KeyboardButton(FeedbackButtons[2])
        )
        markup.row(
            KeyboardButton(FeedbackButtons[3]),
            KeyboardButton(FeedbackButtons[4])
        )
        markup.row(
            KeyboardButton(FeedbackButtons[0])
        )
        bot.send_message(message.chat.id, f"Выберите тип обращения:", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, feedback_select)

    elif textIndex >= 7 and textIndex < 13 and isDev:
        isAdd = textIndex % 2 == 1
        isWhat = (textIndex - 7) // 2
        if not isAdd:
            bot.send_message(message.chat.id, "Данная функция отключена!", reply_markup=menu_keyboard(userID))
            return

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


def feedback_select(message: Message):
    global updatedData, NotifyButtons, KeyboardButtons, FeedbackButtons

    text = message.text
    userID = message.from_user.id

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
    count = 0
    for i in config.developers:
        try:
            bot.send_message(i, text, parse_mode="html")
            count += 1
        except:
            pass
    for i in updatedData.admins:
        try:
            bot.send_message(i, text, parse_mode="html")
            count += 1
        except:
            pass
    bot.send_message(message.chat.id, f"Ваше обращение было отправлено {count} администраторам! Идентификатор обращения: [{message.chat.id}-{message.message_id}]")


def mode_select(message: Message):
    global updatedData, NotifyButtons, KeyboardButtons, WorkModeButtons

    text = message.text

    if text == KeyboardButtons[3]:
        start(message)
        return
    if text == WorkModeButtons[0]:
        markup = btnsMarkup(getGroupsList(updatedData.groups, 0), 5)
        btns = SelectGroupButtons[:]
        btns.insert(2, "Стр. 1")
        btns[1] = truefalseEmoji[0]
        markup.row(*btns)

        bot.send_message(message.chat.id, "Выберите Группу...", reply_markup=markup)
        bot.register_next_step_handler(message, select_group, 0)
        return
    if text == WorkModeButtons[1]:
        markup = btnsMarkup(getGroupsList(updatedData.teachers, 0, 3), 3)
        btns = SelectGroupButtons[:]
        btns.insert(2, "Стр. 1")
        btns[1] = truefalseEmoji[0]
        markup.row(*btns)

        bot.send_message(message.chat.id, "Выберите ФИО...", reply_markup=markup)
        bot.register_next_step_handler(message, select_teacher, 0)
        return




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
            bot.send_message(message.chat.id, f"Выберите время для отправки уведомления [{punkt}]:", reply_markup=btnsMarkup(btns))
            bot.register_next_step_handler_by_chat_id(message.chat.id, notify_select, notifyData, 2, curSelected)
        elif toggleOn and curSelected == 2:
            x1, x2, x3, x4 = notifyData
            notifyData = x1, x2, x3, True
            set_notify_data(notifyData)
            
            bot.send_message(message.chat.id, f"Вы успешно включили уведомление [{punkt}]!", reply_markup=menu_keyboard(userID))
        elif text == NotifyButtonsSelect[2]:
            x1, x2, x3, x4 = notifyData
            if curSelected == 0: x2 = False
            elif curSelected == 1: x3 = False
            elif curSelected == 3: x4 = False
            notifyData = x1, x2, x3, x4
            set_notify_data(notifyData)
            
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

    curDay = datetime.datetime.now().isocalendar().weekday
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

    img = None
    if findIsTeacher(userID):
        img = imaginazer.toImageDayTeacher(
            teachersPairs[0][findTeacherIndex(userID)][dayIndex],
            days[dayIndex],
            updatedData.pairs,
            updatedData.groups
        )
    else:
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


def select_teacher(message: Message, course:int):
    global KeyboardButtons, updatedData
    text = message.text
    userID = message.from_user.id
    studentIndex = findStudentIndex(userID)
    whoAmI = ""

    if studentIndex != -1:
        if json.loads(updatedData.students[studentIndex])[1] == "Teacher":
            whoAmI = json.loads(updatedData.students[studentIndex])[2]
        
    if text == SelectGroupButtons[3]:
        start(message)
        return
    if text == SelectGroupButtons[1]:
        markup = btnsMarkup(getGroupsList(updatedData.teachers, course-1, 3), 3)
        btns = SelectGroupButtons[:]
        btns.insert(2, f"Стр. {course}")

        if len(getGroupsList(updatedData.teachers, course - 2, 3)) == 0:
            btns[1] = truefalseEmoji[0]

        markup.row(*btns)

        bot.send_message(message.chat.id, "Выберите ФИО...", reply_markup=markup)
        bot.register_next_step_handler(message, select_teacher, course-1)
        return
    if text == SelectGroupButtons[2]:
        markup = btnsMarkup(getGroupsList(updatedData.teachers, course+1, 3), 3)
        btns = SelectGroupButtons[:]
        btns.insert(2, f"Стр. {course+2}")

        if len(getGroupsList(updatedData.teachers, course + 2, 3)) == 0:
            btns[3] = truefalseEmoji[0]

        markup.row(*btns)

        bot.send_message(message.chat.id, "Выберите ФИО...", reply_markup=markup)
        bot.register_next_step_handler(message, select_teacher, course+1)
        return
    if text == SelectGroupButtons[0]:
        if studentIndex == -1:
            bot.send_message(message.chat.id, f"Вы и так не преподаватель!", reply_markup=menu_keyboard(userID))
        else:
            updatedData.students.pop(studentIndex)
            bot.send_message(message.chat.id, f"Вы больше не [{whoAmI}]!",
                             reply_markup=menu_keyboard(userID))
            
        return

    if text in updatedData.teachers:
        if whoAmI != text:
            if studentIndex != -1:
                updatedData.students.pop(studentIndex)
            updatedData.students.append(json.dumps([userID, "Teacher", text], ensure_ascii=False))
            
            bot.send_message(message.chat.id, f"Теперь вы [{text}]!", reply_markup=menu_keyboard(userID))
        else:
            bot.send_message(message.chat.id, f"Вы уже [{text}]!",
                             reply_markup=menu_keyboard(userID))
        return

    bot.send_message(message.chat.id, f"Неизвестный вариант ответа.", reply_markup=menu_keyboard(userID))


def select_group(message: Message, course:int):
    global KeyboardButtons, updatedData
    text = message.text
    userID = message.from_user.id
    studentIndex = findStudentIndex(userID)
    group = ""

    if studentIndex != -1:
        group = json.loads(updatedData.students[studentIndex])[1]
        
    if text == SelectGroupButtons[3]:
        start(message)
        return
    if text == SelectGroupButtons[1]:
        markup = btnsMarkup(getGroupsList(updatedData.groups, course-1), 5)
        btns = SelectGroupButtons[:]
        btns.insert(2, f"Стр. {course}")

        if len(getGroupsList(updatedData.groups, course - 2)) == 0:
            btns[1] = truefalseEmoji[0]

        markup.row(*btns)

        bot.send_message(message.chat.id, "Выберите Группу...", reply_markup=markup)
        bot.register_next_step_handler(message, select_group, course-1)
        return
    if text == SelectGroupButtons[2]:
        markup = btnsMarkup(getGroupsList(updatedData.groups, course+1), 5)
        btns = SelectGroupButtons[:]
        btns.insert(2, f"Стр. {course+2}")

        if len(getGroupsList(updatedData.groups, course + 2)) == 0:
            btns[3] = truefalseEmoji[0]

        markup.row(*btns)

        bot.send_message(message.chat.id, "Выберите Группу...", reply_markup=markup)
        bot.register_next_step_handler(message, select_group, course+1)
        return
    if text == SelectGroupButtons[0]:
        if studentIndex == -1:
            bot.send_message(message.chat.id, f"Вы и так не подключены к группе!", reply_markup=menu_keyboard(userID))
        else:
            updatedData.students.pop(studentIndex)
            bot.send_message(message.chat.id, f"Вы больше не подключены к группе [{group}]!",
                             reply_markup=menu_keyboard(userID))
            
        return

    if text in updatedData.groups:
        if group != text:
            if studentIndex != -1:
                updatedData.students.pop(studentIndex)
            updatedData.students.append(json.dumps([userID, text], ensure_ascii=False))
            
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
        data[2], data[3],
        data[4], data[5],
        data[6], data[7]
    ]
    weekDataJson = group_data.saveWeek(weekData)

    updatedData.check()

    lastTeachers = teachersPairs[:]

    (updatedData.groups_data_next if nextWeek else updatedData.groups_data_cur)[groupIndex] = weekDataJson

    recalculateTeachersPairsAll()

    if not nextWeek:
        for notify in updatedData.notifies:
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
                        updatedData.teachers
                    )
                img.seek(0)
                bot.send_photo(x1, img, f"⚠️ Пары на эту неделю были обновлены! ⚠️")

    updatedData.saveAll()

    bot.send_message(message.chat.id, f"Данные успешно применены!")


import traceback

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message: Message):
    global updatedData, KeyboardButtons
    import exel_file_parser
    try:
        userID = message.from_user.id

        if not getIsEditor(userID) or not message.document.file_name.endswith(".xls"):
            return

        bot.send_message(message.chat.id, f"Загрузка файла {message.document.file_name}")

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        bot.send_message(message.chat.id, "Файл Загружен! Парсим...")

        data = exel_file_parser.try_get_data(downloaded_file, updatedData.pairs, updatedData.teachers)

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        dataNames = []
        dataWeeks = []

        for grpData in data:
            grpName, week = grpData
            dataNames.append(grpName)
            dataWeeks.append(week)
            markup.row(KeyboardButton(grpName))

        markup.row(KeyboardButtons[3])

        bot.send_message(message.chat.id, "Выберите, затем нажмите для загрузки...", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, button_docs_photo, dataNames, dataWeeks)


    except exel_file_parser.ParseDataError as err:
        print(err)
        bot.send_message(message.chat.id, "⚠️ ОШИБКА ПАРСИНГА!!! ⚠️")
        bot.send_message(message.chat.id, str(err))

    except Exception:
        err = traceback.format_exc(4, True)
        print(err)
        bot.send_message(message.chat.id, "Что-то Сломалось...")
        bot.send_message(message.chat.id, err)


def button_docs_photo(message: Message, dataNames, dataWeeks):

    try:
        if message.text is None and not message.web_app_data is None and not message.web_app_data.data is None:
            on_webapp_msg(message)
    except:
        pass
    if message.text.replace(">> ", "") in dataNames:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        selected = dataNames.index(message.text.replace(">> ", ""))

        for i in range(len(dataNames)):
            grpName, week = dataNames[i], dataWeeks[i]

            if i == selected:
                urlData = [updatedData.pairs, updatedData.teachers, updatedData.groups, [json.dumps(week)], 1]

                url = "https://drovyng.github.io/ATTS_Schedule_Bot_Website#customdata"
                url += json.dumps(urlData, ensure_ascii=False).replace(
                    "[", "q").replace("\"", "w").replace("]", "e").replace(" ", "r").replace(",", "t").replace(".", "y")
                url += "customdataend"
                print(url)
                markup.row(KeyboardButton(">> " + grpName, web_app=WebAppInfo(url)))
            else:
                markup.row(KeyboardButton(grpName))

        markup.row(KeyboardButtons[3])

        bot.send_message(message.chat.id, "Выберите, затем нажмите для загрузки...", reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(message.chat.id, button_docs_photo, dataNames, dataWeeks)
        return

    start(message)


import os

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
                            curDay,
                            days[dayIndex],
                            updatedData.pairs,
                            updatedData.teachers
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
                        updatedData.teachers
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
            updatedData.saveTimer = 60         # 1 minute
            e += 1
            if e >= 25:
                saver.running = False
                bot.stop_bot()
                raise Exception("BotRestartCommand")

        updatedData.saveTimer -= 2
        time.sleep(2)                 # 10 minutes


def run_bot(saver: RunSaver):
    
    threading.Thread(target=thread_check_time, args=(saver, updatedData)).start()

    bot.polling(non_stop=True)