import telebot
import psycopg2
from config import *
from telebot import types

bot = telebot.TeleBot(token=token)
db_con = psycopg2.connect(db_uri, sslmode='require')
db_cur = db_con.cursor()

laba_data = ''

def exists_user(id_user):
    db_cur.execute("SELECT id_user FROM users")
    users = db_cur.fetchall()
    if len(users) != 0:
        for user in users[0]:
            if id_user == user:
                return True
    db_cur.execute(f"INSERT INTO users(id_user) VALUES({id_user})")
    db_con.commit()
    return False

def add_info(id_user, variant, who):
    db_cur.execute("UPDATE users SET variant = %s, who = %s WHERE id_user = %s", (variant, who, id_user))
    db_con.commit()

def check_lab(id_user, lab):
    db_cur.execute(f"SELECT lr9, lr10, lr11, lr12, lr13, lr14, lr15, all_labs FROM users WHERE id_user = {id_user}")
    labs = db_cur.fetchone()
    if labs[-1] == False:
        if  lab == 'all':
            return True
        elif labs[int(lab) - 9] == False:
            return True
        else:
            return False
    else:
        return False
    
def get_variant(id_user):
    db_cur.execute(f'SELECT variant FROM users WHERE id_user = {id_user}')
    return db_cur.fetchone()

def set_lab(id_user, lab):
    if lab == 'all':
        db_cur.execute(f'UPDATE users SET all_labs = true WHERE id_user = {id_user}')
        db_con.commit()
    else:
        db_cur.execute('UPDATE users SET lr%s = true WHERE id_user = %s', (int(lab), id_user))
        db_con.commit()

def get_info(id_user):
    db_cur.execute(f'SELECT variant, who FROM users WHERE id_user = {id_user}')
    db_con.commit()
    return db_cur.fetchone()

price = {'9': '2.5 byn', '10': '3 byn', '11': '3 byn', '12': '3 byn',
         '13': '3 byn', '14': '3.5 byn', '15': '3.5 byn', 'all': '20'}


@bot.message_handler(commands=['start'])
def start(message):
    if exists_user(message.from_user.id):
        bot.send_message(
            message.chat.id, 'Привет, выбирай лабу', reply_markup=labs_kb)
    else:
        bot.send_message(message.chat.id, 'Введи свой вариант')


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global laba_data
    if call.data == 'yes':
        msgs = call.message.text.split('\n')
        txt = msgs[0] + '\n' + msgs[1] + '\n' + msgs[2]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt)
        btn_menu = types.KeyboardButton('Лабы')
        kb_menu = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        kb_menu.add(btn_menu)
        set_lab(call.from_user.id, laba_data)
        bot.send_message(
            call.message.chat.id, 'Жди, я их скоро отправлю\nЕсть вопрос? Напиши сюда @Evgesha_play', reply_markup=kb_menu)
        info_user = get_info(call.from_user.id)
        bot.send_message(id_chat, f'Заказ\nВариант {info_user[0]}\nЛаба {laba_data}\nКто @{info_user[1]}') 
    elif call.data == 'no':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
        bot.send_message(call.message.chat.id,
                         'Выбери снова', reply_markup=labs_kb)
    else:
        laba_data = call.data
        id_user = call.from_user.id
        if check_lab(id_user, call.data):
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            variant = get_variant(call.from_user.id)[0]
            btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
            btn_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
            yn_kb = types.InlineKeyboardMarkup()
            yn_kb.add(btn_yes, btn_no)
            bot.send_message(call.message.chat.id, f'{laba_data} лаба\nВариант {variant}\nЦена {price[laba_data]}\nВсё верно?', reply_markup=yn_kb)
        else:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, 'Я тебе уже делал эту лабу. Выбирай снова', reply_markup=labs_kb)


@bot.message_handler(content_types=['text'])
def eror_message(message):
    id_user = message.from_user.id
    if message.text == 'Лабы':
        bot.send_message(message.chat.id, 'Выбирай лабу', reply_markup=labs_kb)
    else:
        try:
            if 1 <= int(message.text) <= 26:
                variant = message.text
                who = message.from_user.username
                add_info(id_user, variant, who)
                bot.send_message(id_user, "Выбирай лабу", reply_markup=labs_kb)
            else:
                bot.send_message(
                    message.chat.id, "Ты ввел не правильный вариант\nПопробуй еще раз")
        except ValueError:
            bot.send_message(
                message.chat.id, "Я тебя не понимаю(", reply_markup=labs_kb)


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
