import telebot
import config
import random
import string
import random

import sql

from telebot import types
 
bot = telebot.TeleBot(config.TOKENBOT)

lenCode = 8

sql.main()#Инцилизируем БД


class user():
    id = 0
    code = ''
    chatId = ''
    

    TelegramChannel = []
    DiscordChannel = []
    VKChannel = []

    ChatIdCommand = []
    Post = []
    def __init__(self, chatId) -> None:
        self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=lenCode))
        self.chatId = chatId

        if(sql.search(chatId)):
            self.id, self.code, self.chatId, self.TelegramChannel, self.DiscordChannel, self.VKChannel, self.ChatIdCommand, self.Post = sql.get(chatId)
        else:
            self.id = sql.add(self.code, chatId, self.TelegramChannel, self.DiscordChannel, self.VKChannel, self.ChatIdCommand, self.Post)


@bot.message_handler(commands=['start'])
def welcome(message):                                       #Создам класс пользователя, отправляем ему приветственное сообщение 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    butNewPost = types.KeyboardButton("Создать пост")
    markup.add(butNewPost)

    butSocialSettings = types.KeyboardButton("Настройки соц. сетей")
    butSocialAdd = types.KeyboardButton("Добавить соц. сеть")
    markup.add(butSocialSettings, butSocialAdd)

    butCommandSettings = types.KeyboardButton("Настроить участников")
    butCommandAdd = types.KeyboardButton("Добавить участника")
    butPostEdit = types.KeyboardButton("Изменить пост")
    markup.add(butCommandSettings, butCommandAdd, butPostEdit)

    newUser = user(message.chat.id)
    bot.send_message(message.chat.id, config.STARTMESSAGE, parse_mode="html", reply_markup=markup)


@bot.message_handler(func=lambda message: message.forward_from_chat)
def posts_from_channels(message):
    print(message.text)

if __name__ == "__main__":
    bot.polling(none_stop=True)