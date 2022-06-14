from pydoc import tempfilepager
from time import sleep
from tinydb import TinyDB, Query
import telebot
import subprocess as sb
import threading
from telebot import types
USERID = 999711677
TELEGRAMTOKEN = 'your token'

bot = telebot.TeleBot(TELEGRAMTOKEN, threaded=False)
db = TinyDB('mangaDB.json')
q = Query()


def getMangaInfo(url): #    https://mangalib.me/promisecinderella?section=info
    p = sb.Popen(["python3", "browsing.py", url], stdout=sb.PIPE)
    out, err = p.communicate()
    out = list(out.decode("utf-8").replace('\n', '').split('¿'))
    print(out)
    return out

def dirtyStuff():
    while True:
        mangas = db.all()
        for manga in mangas:
            info = getMangaInfo(manga['link'])
            if int(manga['chapters']) != int(info[0]):
                db.update({'chapters': int(info[0])}, q.link == manga['link'])
                print('updated manga {} '.format(info[1]))
                bot.send_message(USERID, '{} вышла {} глава 🗞'.format(info[1], info[0]))
            else:
                print('no update manga {}'.format(info[1]))
            #sleep(2)
        print('waiting 10800 seconds to update manga!')
        sleep(10800)


def menu_mark():
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton("настроить⚙️")
    return markup.add(itembtn1)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == USERID:
        bot.send_message(message.chat.id, 'Привет плохая Настюшка :3', reply_markup=menu_mark())
@bot.message_handler(content_types=['text'])   
def text(message):
    print(message.from_user.id)
    print(message.text)
    if message.from_user.id == USERID and 'https://mangalib' in message.text:
        manga = db.search(q.link == message.text)
        print(manga)
        if manga:
            info = getMangaInfo(message.text)
            db.remove(q.link == message.text)
            bot.send_message(message.chat.id, 'Успешно удалил {} 🤧'.format(info[1]))
        else:
            info = getMangaInfo(message.text)
            bot.send_message(message.chat.id, 'Успешно добавил в список отслеживания {}✌️'.format(info[1]))
            db.insert({'link': message.text,'name': info[1], 'chapters': int(info[0])})
    elif message.text == 'настроить⚙️' and message.from_user.id == USERID:
        mangas = db.all()
        if not mangas:
            bot.send_message(message.chat.id, 'ты ничего не отслеживаешь🧋')
        for manga in mangas:
            mj_markup = types.InlineKeyboardMarkup()
            m1 = types.InlineKeyboardButton('❌Удалить', callback_data=manga['link'])
            mj_markup.add(m1)
            bot.send_message(message.chat.id, manga['name'], reply_markup=mj_markup)

        

@bot.callback_query_handler(lambda query: query.data)
def call_back(data):
    db.remove(q.link == data.data)
    bot.delete_message(data.from_user.id,data.message.id)

def async_function(): 
    threading.Timer(5.0, dirtyStuff).start() # Restart in 5 seconds 
    print("async_function started") 

async_function()
bot.polling(non_stop=True)


# klesberg was not here