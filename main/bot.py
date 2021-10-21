import telebot
from telebot import types
import re

TOKEN = "1848770701:AAHHDSLoIR9FHpmA93wX6y8w4KlDVZ5jCRI"

bot = telebot.TeleBot(TOKEN)

def send_order(chat_id=None, data=None):
	text = f'ФИО: {data["full_name"]}\nТел.:{data["tel"]}\n\n' + '-' * 50 + '\n\n'

	n = 0
	summa = 0
	for value in data['order'].values():
		n += 1
		text += f'~Продукт {n}~\nНазвание: {value["name"]}\nКоличество: {value["count"]}\nЦена: {value["price"]}\n\n'

		summa += value["price"] * value["count"]

	summa = str(summa)
	count = len(summa)
	while count > 3:
		count -= 3
		summa = summa[:count] + ' ' + summa[count:]

	text += '\n' + '-' * 50 + f'\nИтого: {summa} сум' 

	bot.send_message(
		chanel_id,
		text
	)
