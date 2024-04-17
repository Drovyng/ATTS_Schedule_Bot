from typing import Union

import config
import group_data, sheets, json
import imaginazer

ChatMessages:dict[str, Union[str, list, tuple]] = {
    "start": [
        "Привет! Если ты студент <b>Армавирского Техникума Технологии и Сервиса</b>, то с помощью этого бота ты можешь узнать расписание в любое время!",
        "Привет, разработчик! Я создан для того, чтобы студенты <b>Армавирского Техникума Технологии и Сервиса</b> могли узнать расписание в любое время!"
    ],
    "dev": "Включён режим разработчика"
}

KeyboardButtons:list[str] = [
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

    "Перезагрузить бота 🔄"
]
import datetime

class UpdatedData():
    def __init__(self):
        self.devs:list[str] = []
        self.teachers:list[str] = []
        self.pairs:list[str] = []
        self.groups:list[str] = []
        self.students:list[str] = []
        self.groups_data_cur:list[str] = []
        self.groups_data_next:list[str] = []
        self.groups_week:int = 0

        self.resize()

        self.reloadAll()

    def resize(self):

        self.devsCount = len(self.devs)
        self.teachersCount = len(self.teachers)
        self.pairsCount = len(self.pairs)
        self.groupsCount = len(self.groups)
        self.studentsCount = len(self.students)

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

    def check(self, issaving:bool = False):
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

        self.resize()


updatedData = UpdatedData()



import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

bot = telebot.TeleBot(config.bot_token)
developers: list[int] = [
    1157843932,     # Дмитрий
    1085752896      # Быленко М.И.
]

def getChatMessage(key:str, isDev:bool = False):
    global ChatMessages

    msg = ChatMessages[key]
    if isinstance(msg, list | tuple):
        if isDev and len(msg) > 1:
            return msg[1]
        else:
            return msg[0]
    else:
        return msg


def findStudentIndex(userID) -> int:
    global updatedData
    i = 0
    for st in updatedData.students:
        if json.loads(st)[0] == userID:
            return i
        i += 1
    return -1


def getIsDev(userID:int) -> bool:
    global updatedData
    return userID in updatedData.devs or userID in developers


def menu_keyboard(userID:int) -> ReplyKeyboardMarkup:
    global developers, updatedData
    isInGroup = findStudentIndex(userID) != -1
    isDev = getIsDev(userID)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)


    if isInGroup:
        markup.row(KeyboardButton(KeyboardButtons[5]), KeyboardButton(KeyboardButtons[6]), KeyboardButton(KeyboardButtons[0]))
    else:
        markup.row(KeyboardButton(KeyboardButtons[0]))

    if isDev:
        markup.row(KeyboardButton(KeyboardButtons[1]))

    return markup


@bot.message_handler(commands=['start', 'clear'])
def start(message: Message):
    global KeyboardButtons

    userID = message.from_user.id
    isDev = getIsDev(userID)

    bot.send_message(message.chat.id, getChatMessage("start", isDev), reply_markup=menu_keyboard(userID), parse_mode="html")


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
            bot.send_message(message.chat.id, f"Расписание на эту неделю ещё не добавлено!", reply_markup=menu_keyboard(userID))
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
        if studentIndex == -1:
            bot.send_message(message.chat.id, f"Вы не подключены к группе!", reply_markup=menu_keyboard(userID))
            return
        groupID = -1
        groupName = json.loads(updatedData.students[studentIndex])[1]
        if updatedData.groups.count(groupName) != 0:
            groupID = updatedData.groups.index(groupName)
        if groupID == -1 or updatedData.groups_data_next[groupID].count("[") < 10:
            bot.send_message(message.chat.id, f"Расписание на следующую неделю ещё не добавлено!", reply_markup=menu_keyboard(userID))
            return
        img = imaginazer.toImage(
            group_data.loadWeek(
                updatedData.groups_data_next[groupID]
            ),
            updatedData.pairs,
            updatedData.teachers
        )
        img.seek(0)
        bot.send_photo(message.chat.id, img, "Вот пары на следующую неделю", reply_markup=menu_keyboard(userID))

    elif textIndex == 0:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        groups = updatedData.groups[:]
        if not isDev and groups.count("Тест") > 0:
            groups.remove("Тест")

        groups.append(KeyboardButtons[3])
        groups.append(KeyboardButtons[4])

        lengrp = len(groups)
        inrow = min(lengrp, 5)
        rows = lengrp // inrow

        b = 0
        for i in range(rows):
            inRow = []
            for j in range(0, min(lengrp - inrow * i, inrow)):
                inRow.append(KeyboardButton(groups[b]))
                b += 1
            markup.row(*inRow)

        bot.send_message(message.chat.id, "Выберите Группу...", reply_markup=markup)
        bot.register_next_step_handler(message, select_group, groups)

    elif textIndex == 1 and isDev:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        url = "https://drovyng.github.io/ATTS_Schedule_Bot_Website#customdata"
        url += json.dumps([updatedData.pairs, updatedData.teachers, updatedData.groups],ensure_ascii=False).replace("[", "q").replace("\"", "w").replace("]", "e").replace(" ", "r").replace(",", "t").replace(".", "y")
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
            KeyboardButton(KeyboardButtons[13])
        )

        bot.send_message(message.chat.id, getChatMessage("dev"), reply_markup=markup)
    elif textIndex == 13 and isDev:
        bot.send_message(message.chat.id, f"Бот в процессе перезагрузки!",
                         reply_markup=menu_keyboard(message.from_user.id))
        raise Exception("BotRestartCommand")
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


def dev_action(message: Message, isAdd:bool, isWhat:int, isToConfirm:bool, name:Union[str | None]):
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
                else:
                    updatedData.teachers.append(name)
                    sendText = " преподаватель"
                updatedData.saveAll()
                bot.send_message(message.chat.id, f"Успешно добавлен{sendText} [{name}]!", reply_markup=menu_keyboard(userID))
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
                else:
                    if updatedData.teachers.count(name) == 0:
                        bot.send_message(message.chat.id, f"Преподавателя [{name}] не существует!",
                                         reply_markup=menu_keyboard(userID))
                        return
                    updatedData.teachers.remove(name)
                    sendText = " преподаватель"
                updatedData.saveAll()
                bot.send_message(message.chat.id, f"Успешно удален{sendText} [{name}]!", reply_markup=menu_keyboard(userID))

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
            elif updatedData.teachers.count(text) != 0:
                bot.send_message(message.chat.id, f"Преподаватель [{text}] уже существует!",
                                 reply_markup=menu_keyboard(userID))
                return

        bot.send_message(message.chat.id, "Вы уверены? (Введите \"Подтверждаю!\")", reply_markup=menu_keyboard(userID))
        bot.register_next_step_handler_by_chat_id(message.chat.id, dev_action, isAdd, isWhat, True, text)



def select_group(message: Message, groups: list[str]):
    global KeyboardButtons, updatedData, developers
    text = message.text
    userID = message.from_user.id
    studentIndex = findStudentIndex(userID)
    group = ""
    if studentIndex != -1:
        group = json.loads(updatedData.students[studentIndex])[1]

    if text == KeyboardButtons[3]:
        start(message)
        return

    if studentIndex == -1 and text == KeyboardButtons[4]:
        bot.send_message(message.chat.id, f"Вы и так не подключены к группе!", reply_markup=menu_keyboard(userID))
    else:
        updatedData.students.pop(studentIndex)
        updatedData.saveAll()
        if text == KeyboardButtons[4]:
            bot.send_message(message.chat.id, f"Вы больше не подключены к группе [{group}]!", reply_markup=menu_keyboard(userID))

    if text in groups:
        if group != text:
            updatedData.students.append(json.dumps([userID, text], ensure_ascii=False))
            updatedData.saveAll()
            bot.send_message(message.chat.id, f"Вы подключены к группе [{text}]!", reply_markup=menu_keyboard(userID))
        else:
            bot.send_message(message.chat.id, f"Вы уже подключены в группе [{text}]!", reply_markup=menu_keyboard(userID))
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
    updatedData.saveAll()

    bot.send_message(message.chat.id, f"Данные успешно применены!", reply_markup=menu_keyboard(message.from_user.id))

bot.polling(non_stop=True)
