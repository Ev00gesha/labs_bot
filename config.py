from telebot import types 
token = "5473129549:AAHyOWislkaxdNCHfNM6WTn5qJKK3Whyvn0"
id_chat = 692369767
db_uri = "postgres://feyyrvllcqtgjw:8f26e1654701a51bf72961a04ccd43105c9502f8a5449b30cc80c9f798267f7d@ec2-54-75-184-144.eu-west-1.compute.amazonaws.com:5432/def7qv8o8418m2"

btn_lr9 = types.InlineKeyboardButton(text='ЛР 9 (2.5 byn)', callback_data='9')
btn_lr10 = types.InlineKeyboardButton(text='ЛР 10 (3 byn)', callback_data='10')
btn_lr11 = types.InlineKeyboardButton(text='ЛР 11 (3 byn)', callback_data='11')
btn_lr12 = types.InlineKeyboardButton(text='ЛР 12 (3 byn)', callback_data='12')
btn_lr13 = types.InlineKeyboardButton(text='ЛР 13 (3 byn)', callback_data='13')
btn_lr14 = types.InlineKeyboardButton(text='ЛР 14 (3.5 byn)', callback_data='14')
btn_lr15 = types.InlineKeyboardButton(text='ЛР 15 (3.5 byn)', callback_data='15')
btn_all = types.InlineKeyboardButton(text='Все за 20 byn', callback_data='all') 
labs_kb = types.InlineKeyboardMarkup()
labs_kb.add(btn_lr9, btn_lr10, btn_lr11, btn_lr12, btn_lr13, btn_lr14, btn_lr15, btn_all)