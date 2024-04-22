from io import BytesIO
from colorama import init, Fore, Style
init(autoreset=True)

import telebot, config, pyautogui, traceback, config
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(config.bot_token)

KeyboardButtons = [
    "Команда",
    "Консоль",
    "Выйти из аварийного режима"
]
markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.row(KeyboardButton(KeyboardButtons[0]))
markup.row(KeyboardButton(KeyboardButtons[1]))
markup.row(KeyboardButton(KeyboardButtons[2]))

def getScreenshot() -> BytesIO:
    import pyautogui
    output = BytesIO()
    pyautogui.screenshot().save(output, format='PNG')
    return output


for dev in config.developers:
    try:
        img = getScreenshot()
        img.seek(0)
        user_name = bot.get_chat_member(dev, dev).user.username
        bot.send_photo(dev, img, f"⚠️ ВНИМАНИЕ!!! БОТ ЗАПУЩЕН В АВАРИЙНОМ РЕЖИМЕ!!! <a href='tg://user?id={dev}'>@{user_name}</a>️ ⚠️", reply_markup=markup, parse_mode="HTML")
    except:
        try:
            user_name = bot.get_chat_member(dev, dev).user.username
            bot.send_message(dev, f"⚠️ ВНИМАНИЕ!!! БОТ ЗАПУЩЕН В АВАРИЙНОМ РЕЖИМЕ!!! <a href='tg://user?id={dev}'>@{user_name}</a>️ ⚠️", reply_markup=markup, parse_mode="HTML")
        except:
            pass

@bot.message_handler()
def on_message(message: Message):
    global KeyboardButtons, markup
    if not message.from_user.id in config.developers:
        bot.send_message(message.chat.id, "⚠️Ведутся работы по исправлению ошибок! Бот в данный момент недоступен!⚠️")
    else:
        text = message.text
        if not text in KeyboardButtons:
            return
        if text == KeyboardButtons[0]:
            bot.send_message(message.chat.id, "Жду команду...", reply_markup=None)
            bot.register_next_step_handler_by_chat_id(message.chat.id, listen_command)
            return
        if text == KeyboardButtons[1]:
            try:
                img = getScreenshot()
                img.seek(0)
                bot.send_photo(message.chat.id, img, "Скриншот консоли", reply_markup=markup)
            except:
                pass
        if text == KeyboardButtons[2]:
            newMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
            newMarkup.row(KeyboardButton("Меню 📋"))
            bot.send_message(message.chat.id, "Выполняется перезагрузка бота...", reply_markup=newMarkup)
            bot.stop_bot()
            quit()


def listen_command(message: Message):
    global markup
    try:
        exec(message.text)
    except:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + traceback.format_exc(chain=True))
    try:
        img = getScreenshot()
        img.seek(0)
        bot.send_photo(message.chat.id, img, "Скриншот консоли", reply_markup=markup)
    except:
        pass

bot.polling(non_stop=True)
