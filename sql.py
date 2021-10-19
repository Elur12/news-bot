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
        id = sql.fetchall()[-1][0] + 1
        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, code, chatId, arrayEncode(TelegramChannel), arrayEncode(DiscordChannel), arrayEncode(VKChannel), arrayEncode(ChatIdCommand), arrayEncode(Post)))
    else:
        id = 0
        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, code, chatId, arrayEncode(TelegramChannel), arrayEncode(DiscordChannel), arrayEncode(VKChannel), arrayEncode(ChatIdCommand), arrayEncode(Post)))
    DataBase.commit()
    return id

def search(chatId):
    sql.execute("SELECT chatId FROM users WHERE chatId = ?", (chatId,))
    if(sql.fetchone() == None):
        return False
    return True

def get(chatId):
    sql.execute("SELECT * FROM users WHERE chatId = ?", (chatId,))
    return sql.fetchone()

if __name__ == "__main__":
    main()