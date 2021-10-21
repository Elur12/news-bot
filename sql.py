from logging import info
import sqlite3
import pickle
from sqlite3.dbapi2 import version


def arrayDecode(array):#Используеться для перевода байтовой переменной из таблицы в массив
    return pickle.loads(array)

def arrayEncode(array):#Используеться для перевода массива в байтовую переменную для таблцы
    return pickle.dumps(array)


def main():#Создаёт и подключаеться к БД(Преред первым подключение к этому коду надо запускать это)
    global sql, DataBase
    DataBase = sqlite3.connect('mainBase.db', check_same_thread=False)
    sql = DataBase.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
                id INT,
                code TEXT,
                chatId TEXT,
                TelegramChannel BLOB,
                DiscordChannel BLOB,
                VKChannel BLOB, 
                ChatIdCommand BLOB,
                Post BLOB)""")
    DataBase.commit()
    


def add(code, chatId, TelegramChannel, DiscordChannel, VKChannel, ChatIdCommand, Post):
    sql.execute("SELECT id FROM users")
    if(sql.fetchone() != None):
        sql.execute("SELECT id FROM users")
        id = sql.fetchall()[-1][0] + 1
        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, code, chatId, arrayEncode(TelegramChannel), arrayEncode(DiscordChannel), arrayEncode(VKChannel), arrayEncode(ChatIdCommand), arrayEncode(Post)))
    else:
        id = 0
        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, code, chatId, arrayEncode(TelegramChannel), arrayEncode(DiscordChannel), arrayEncode(VKChannel), arrayEncode(ChatIdCommand), arrayEncode(Post)))
    DataBase.commit()
    return id

def search(chatId):
    sql.execute("SELECT chatId, code FROM users WHERE chatId = ?", (chatId,))
    if(sql.fetchone() == None):
        return False
    return True

def get(chatId):
    sql.execute("SELECT * FROM users WHERE chatId = ?", (chatId,))
    info = sql.fetchone()
    return info[0], info[1], info[2], arrayDecode(info[3]), arrayDecode(info[4]), arrayDecode(info[5]), arrayDecode(info[6]), arrayDecode(info[7])

def append(id, TelegramChannel = None, DiscordChannel = None, VKChannel = None, ChatIdCommand = None, Post = None):
    sql.execute("SELECT * FROM users WHERE id = ?", (id,))
    info = sql.fetchone()
    TelegramChannels = arrayDecode(info[3])
    if(TelegramChannel != None): TelegramChannels.append(TelegramChannel)
    
    DiscordChannels = arrayDecode(info[4])
    if(DiscordChannel != None): DiscordChannels.append(DiscordChannel)

    VKChannels = arrayDecode(info[5])
    if(VKChannel != None): VKChannels.append(VKChannel)
    
    ChatIdCommands = arrayDecode(info[6])
    if(ChatIdCommand != None): ChatIdCommands.append(ChatIdCommand)

    Posts = arrayDecode(info[7])
    if(Post != None): Posts.append(Post)

    sql.execute("UPDATE users SET TelegramChannel=?, DiscordChannel=?, VKChannel=?, ChatIdCommand=?, Post=? WHERE id=?", (arrayEncode(TelegramChannels), arrayEncode(DiscordChannels), arrayEncode(VKChannels), arrayEncode(ChatIdCommands), arrayEncode(Posts), id))
    DataBase.commit()


if __name__ == "__main__":
    main()