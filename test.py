import requests
import os,base64
from PIL import Image
from io import BytesIO
import  telebot
from config import TOKEN
import json
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

fileid = 'AgACAgUAAx0CRXWu7QADLl4y1Qgzj2QIqOcx44Qs8jDtB-YVAAJpqTEbU4eZVduCWVc_afK2naolMwAEAQADAgADeQAD2doCAAEYBA'
myurl = 'https://api.telegram.org/bot'+TOKEN + '/getFile?file_id=' + fileid
print(myurl)
html = requests.get(url=myurl).text
file_path = json.loads(html)['result']['file_path']
getFileUrl='https://api.telegram.org/file/bot' + TOKEN + '/' + file_path
file_res = requests.get(url=getFileUrl)
# 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
image = Image.open(BytesIO(file_res.content)) 
# 得到这个图片的base64编码
ls_f=base64.b64encode(BytesIO(file_res.content).read())
# 打印出这个base64编码
print(ls_f)
