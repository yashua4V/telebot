#!/usr/bin/python3
import telebot
from config import TOKEN
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '大家好，我是机器人')


@bot.message_handler(commands=['help'])
def send_welcome1(message):
    bot.send_message(reply_to_message_id=message.message_id, chat_id=message.chat.id, text='有什么可以帮您')


@bot.message_handler()
def echo(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.polling()
