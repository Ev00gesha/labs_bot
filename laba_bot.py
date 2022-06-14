from gettext import bind_textdomain_codeset
import telebot
from config import *
from telebot import types

bot = telebot.TeleBot(token=token)
laba_data = ''
variant = ''
who = 0

price = {'9':'2.5 byn', '10':'3 byn', '11':'3 byn', '12':'3 byn', '13':'3 byn', '14':'3.5 byn', '15':'3.5 byn', 'all':'20'}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, выбирай лабу', reply_markup=labs_kb)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global laba_data
    if call.data == 'yes':
        msgs = call.message.text.split('\n')
        txt = msgs[0] + '\n' + msgs[1]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=txt)
        btn_menu = types.KeyboardButton('Лабы')
        kb_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb_menu.add(btn_menu)
        bot.send_message(id_chat, f'Заказ\nЛаба {laba_data}\nВариант {variant}\nКто @{who}')
        bot.send_message(call.message.chat.id, 'Жди, я их скоро отправлю\nЕсть вопрос? Напиши сюда @Evgesha_play', reply_markup=kb_menu)
    elif call.data == 'no':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Выбери снова', reply_markup=labs_kb)
    else:
        
        laba_data = call.data
        bot.send_message(call.message.chat.id, 'Какой ты вариант?')    

@bot.message_handler(content_types=['text'])
def eror_message(message):
    global variant, who
    if message.text == 'Лабы':
        bot.send_message(message.chat.id, 'Выбирай лабу', reply_markup=labs_kb)
    else:
        try:
            if 1 <= int(message.text) <= 26:
                btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
                btn_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
                inl_kb = types.InlineKeyboardMarkup()
                inl_kb.add(btn_yes, btn_no)
                variant = message.text
                who = message.from_user.username
                bot.send_message(message.chat.id, f"Ты выбрал {'все лабы за 20 byn' if laba_data == 'all' else f'{laba_data} лабу за {price[laba_data]}'}\nВариант {message.text}\nВсё верно?", reply_markup=inl_kb)
            else:
                bot.send_message(message.chat.id, "Ты ввел не правильный вариант\nПопробуй еще раз")
        except ValueError:
            bot.send_message(message.chat.id, "Я тебя не понимаю(", reply_markup=labs_kb)

def main():
    bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
    main()