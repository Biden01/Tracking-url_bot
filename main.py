import os

import telebot
from telebot import types
import config, time, os

api = config.api
bot = telebot.TeleBot(api)
do = "start"


@bot.message_handler(commands=["start132"])
def change_do(message):
    global do
    do = "start"
    bot.send_message(message.chat.id, "Бот запущен")


@bot.message_handler(commands=["stop465"])
def change_do(message):
    global do
    do = "stop"
    bot.send_message(message.chat.id, "Бот остановлен")


@bot.message_handler(commands=['start'])
def send_start(message):
    if do == "start":
        if " " in message.text:
            referrer_id = message.text.split()[1]
            seconds = time.time()
            text = ""
            files = os.listdir("data")
            if f"{referrer_id}-caption" in files:
                with open(f"data/{referrer_id}-caption", "r") as f:
                    text = f.read()
            try:
                with open(f"data/{referrer_id}.txt", "r") as f:
                    data = f.read()
                if str(message.from_user.id) not in data:
                    with open(f"data/{referrer_id}.txt", "a+") as f:
                        f.write(f"{message.from_user.id} ")
                    with open(f"data/{referrer_id}-text.txt", "a+") as f:
                        f.write(f"{message.from_user.username}({message.from_user.first_name} {message.from_user.last_name}), {time.ctime(seconds+21600)}  ")
                if text != "":
                    bot.send_message(chat_id=message.chat.id, text=text)
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton(text=f"Написать пользователю", url="t.me/"+str(message.from_user.username))
                if message.from_user.username != None and message.from_user.username != "None":
                    markup.add(btn1)
                bot.send_message(chat_id=referrer_id, text=f"👤 {message.from_user.username}({message.from_user.first_name} {message.from_user.last_name}), посетил(а) вашу страницу\n⏱️Время: {time.ctime(seconds+21600)}", reply_markup=markup)
            except FileNotFoundError:
                bot.send_message(message.chat.id, "Вы ввели не существующую реферальную ссылку")


@bot.message_handler(commands=['history'])
def send_history(message):
    if do == "start":
        try:
            with open(f"data/{message.from_user.id}.txt", "r") as f:
                all_id=f.read().split()
            with open(f"data/{message.from_user.id}-text.txt", "r") as f:
                all_text=f.read().split("  ")
            bot.send_message(chat_id=message.chat.id,text="По вашей ссылке перешли "+str(len(all_id)-1)+" 👤")
            for i in range(len(all_id)-1):
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton(text="Написать пользователю",url="t.me/"+str(all_text[i].split(",")[0].split("(")[0]))
                if str(all_text[i].split(",")[0].split("(")[0]) != None and str(all_text[i].split(",")[0].split("(")[0]) != "None":
                    markup.add(btn1)
                bot.send_message(chat_id=message.chat.id,text=all_text[i], reply_markup=markup)
        except FileNotFoundError:
            bot.send_message(chat_id=message.chat.id,text="История пуста")


@bot.message_handler(commands=['get_url'])
def send_url(message):
    if do == "start":
        bot.send_message(message.chat.id, "размести эту ссылку в любом месте -Telegram, Instagram, Whatsapp, и т.д. Разместите это в любой социальной сети.")
        bot.send_message(message.chat.id, f"https://!t.me/Xanuntitle_bot?start={message.from_user.id}")
        with open(f"data/{message.from_user.id}.txt", "a+") as f:
            f.write("")


@bot.message_handler(commands=['add_caption'])
def add_caption(message):
    if do == "start":
        msg = bot.send_message(message.chat.id, "Напишите текст")
        bot.register_next_step_handler(msg, add_text)


def add_text(message):
    with open(f"data/{message.from_user.id}-caption", "w") as f:
        f.write(message.text)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, "Текст сохранен")


@bot.message_handler(commands=['report'])
def report(message):
    users_link = 0
    users = set()
    for file in os.listdir("data"):
        if "caption" not in file and "text" not in file:
            users_link += 1
        elif "caption" not in file and "text" in file:
            with open("data/"+file, "r") as f:
                user = f.read().split("  ")[:-1]
                for i in range(len(user)):
                    users.add(user[i])
    users = list(users)
    for i in range(len(users)):
        text = users[i]
        uus = []
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Написать пользователю",url="t.me/" + str(text.split(",")[0].split("(")[0]))
        if str(text.split(",")[0].split("(")[0]) != None and str(text.split(",")[0].split("(")[0]) != "None":
            markup.add(btn1)
        bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.send_message(chat_id=message.chat.id, text="Пользователи которые создали ссылку " + str(users_link) + "!")
    bot.send_message(chat_id=message.chat.id, text="Пользователи которые перешли по ссылке" + str(len(users)) + "!")


bot.infinity_polling()