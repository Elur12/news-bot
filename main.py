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


queryVer = []


class user():
    id = 0
    code = ''
    chatId = ''
    

    TelegramChannels = []
    DiscordChannels = []
    VKChannels = []

    ChatIdCommands = []
    Posts = []
    def __init__(self, chatId) -> None:
        self.chatId = chatId

        if(sql.search(chatId)):
            self.id, self.code, self.chatId, self.TelegramChannels, self.DiscordChannels, self.VKChannels, self.ChatIdCommands, self.Posts = sql.get(chatId)
        else:
            self.id = sql.add(self.code, chatId, self.TelegramChannels, self.DiscordChannels, self.VKChannels, self.ChatIdCommands, self.Posts)
            self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=lenCode))

    def GET(self):
        print(sql.get(self.chatId))

    def append(self, TelegramChannel = None, DiscordChannel = None, VKChannel = None, ChatIdCommand = None, Post = None):
        if(TelegramChannel != None): self.TelegramChannels.append(TelegramChannel)
        if(DiscordChannel != None):self.DiscordChannels.append(DiscordChannel)
        if(VKChannel != None):self.VKChannels.append(VKChannel)
        if(ChatIdCommand != None):self.ChatIdCommands.append(ChatIdCommand)
        if(Post != None):self.Posts.append(Post)
        sql.append(self.id, TelegramChannel=TelegramChannel, DiscordChannel=DiscordChannel, VKChannel=VKChannel, ChatIdCommand=ChatIdCommand, Post=Post)

    def addPost(self, post):
        self.append(Post=post)
        for i in self.TelegramChannels:
            i.Post(post)
        for i in self.VKChannels:
            i.Post(post)
        for i in self.DiscordChannels:
            i.Post(post)


class Verefi():
    typeSoc = 0#0-Telegram, 1-Discord, 2-VK
    apiOrId = 0
    verefiCode = ''

    parentID = 0

    verefi = False
    def __init__(self, parent, type) -> None:
        self.typeSoc = type
        self.verefiCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=lenCode))
        self.parentID = parent


    def getCode(self):
        return self.verefiCode

    def setApiOrId(self, api):
        self.apiOrId = api
    
    def Post(self, post):
        if(self.typeSoc == 0):
            bot.send_message(self.apiOrId, post.text)

class post():
    text = ''
    def __init__(self, text) -> None:
        self.text = text

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


@bot.message_handler(content_types=['text'])
def mesageGet(message):
    text = message.text
    chatUser = user(message.chat.id)
    if(text == "Добавить соц. сеть"):
        #Проходим верефикацию и настройку и добавляем
        addSocialMessage(chatUser)
    elif(text == "Создать пост"):
        chatUser.addPost(post("TEST AAAAAAAAAa"))
        


@bot.channel_post_handler(content_types=['text'])
def Test(message):
    for i in queryVer:
        if(i.getCode() == message.text):
            i.setApiOrId(message.chat.id)
            user(i.parentID).append(TelegramChannel = i)
            queryVer.remove(i)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'addDiscord':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'addTelegram':
                bot.send_message(call.message.chat.id, config.ADDTG)
                TelegramVerefi(call.message)
            elif call.data == 'addVK':
                bot.send_message(call.message.chat.id, 'ОК')
 
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=config.ADDMESSAGE,
                reply_markup=None)
 
    except Exception as e:
        print(repr(e))





def addSocialMessage(chatUser):
    markup = types.InlineKeyboardMarkup(row_width=3)
    discordButton = types.InlineKeyboardButton("Дискорд", callback_data='addDiscord')

    VKButton = types.InlineKeyboardButton("ВК", callback_data='addVK')
    telegramButton = types.InlineKeyboardButton("Телеграм", callback_data='addTelegram')
    markup.add(discordButton, VKButton, telegramButton)
    bot.send_message(chatUser.chatId, config.ADDMESSAGE, reply_markup=markup)


def TelegramVerefi(mes):
    newVerefi = Verefi(mes.chat.id, 0)
    bot.send_message(mes.chat.id, newVerefi.getCode())
    queryVer.append(newVerefi)


if __name__ == "__main__":
    bot.polling(none_stop=True)