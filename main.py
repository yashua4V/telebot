
import  telebot
from telebot import types
from config import TOKEN , WXIP
import requests
import os,base64
from PIL import Image
from io import BytesIO
import random
import json

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['linkstart'])
def link_open(message):
    print(str(message))
    if message.from_user.username == 'linke9054592735':
        bot.send_message(message.chat.id, 'master')
        os.system('ssh -p 34567 root@%s "/root/wxvpn.sh 1800" & ' % WXIP)
        bot.send_message(message.chat.id, 'vpn已开，时限30分钟，vpn信息请咨询管理')
    elif message.from_user.username == 'rouli666':
        
        os.system('ssh -p 34567 root@%s "/root/wxvpn.sh 1800" & ' % WXIP)
        bot.send_message(message.chat.id, 'vpn已开，时限30分钟，vpn信息请咨询管理')
    else:
        bot.send_message(message.chat.id, '你没有权限')
    pass
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '点餐请发/+菜名或/菜名,如‘/馒头’不会搜索到烤馒头')


@bot.message_handler(commands=['help'])
def send_welcome1(message):
    bot.send_message(message.chat.id, text='点餐请发/+菜名或/菜名,如‘/馒头’不会搜索到烤馒头')
@bot.message_handler(regexp='^/\*.*')
def test(message):
    myurl = 'http://127.0.0.1/getmenu'
    chatid = message.chat.id
    
#   print ('\n'.join(['%s:%s' % item for item in types.__dict__.items()]))
    markup = types.InlineKeyboardMarkup()
    print(str(markup.__dict__.items()))
    itembtn1 = types.InlineKeyboardButton('A',url='http://192.168.1.185')
    itembtn2 = types.InlineKeyboardButton('B',url='http://192.168.1.185')

    print(str(itembtn1.__dict__.items()))
    markup.add(itembtn1,itembtn2)

    if message.content_type == 'text':
        text = message.text
        data = {'tag':text}
        re = requests.post(myurl,data)
        r = json.loads(re.text)
        if r['status'] == 'success':
#            for i in r['img_list']:
#                imgdata=base64.b64decode(i)
#                bot.send_photo(chatid, imgdata)
            imgdata = base64.b64decode(r['img_list'][random.randint(0,len(r['img_list'])-1)])
            bot.send_photo(chatid, imgdata, reply_markup=markup)
        else:
            text = '没有搜索到菜单，发送菜单图片添加'
            bot.send_message(chat_id=message.chat.id,reply_to_message_id=message.message_id,text=text)


@bot.message_handler(regexp='^/\+.*')
def command_url(message):
    myurl = 'http://127.0.0.1/getmenu'
    chatid = message.chat.id
    if message.content_type == 'text':
        text = message.text
        data = {'tag':text}
        re = requests.post(myurl,data)
        r = json.loads(re.text)
        if r['status'] == 'success':
#            for i in r['img_list']:
#                imgdata=base64.b64decode(i)
#                bot.send_photo(chatid, imgdata)
            imgdata = base64.b64decode(r['img_list'][random.randint(0,len(r['img_list'])-1)])
            bot.send_photo(chatid, imgdata)
        else:
            text = '没有搜索到菜单，发送菜单图片添加'
            bot.send_message(chat_id=message.chat.id,reply_to_message_id=message.message_id,text=text)

@bot.message_handler(regexp='^/.*')
def command_url_pls(message):
    myurl = 'http://127.0.0.1/getmenupls'
    chatid = message.chat.id
    print(str(message))
    if message.content_type == 'text':
        text = message.text
        data = {'tag':text}
        re = requests.post(myurl,data)
        r = json.loads(re.text)
        if r['status'] == 'success':
#            for i in r['img_list']:
#                imgdata=base64.b64decode(i)
#                bot.send_photo(chatid, imgdata)
            imgdata = base64.b64decode(r['img_list'][random.randint(0,len(r['img_list'])-1)])
            bot.send_photo(chatid, imgdata)
        else:
            text = '没有搜索到菜单，发送菜单图片添加'
            bot.send_message(chat_id=message.chat.id,reply_to_message_id=message.message_id,text=text)


def get_imgfile2Base64(fileid):
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
    return ls_f
def post_imgbase64(imgbase64,fileid,mini_imgbase64,miniFile_id):
    myurl = 'http://127.0.0.1/ocrtest'
    data = {'imgbase64':imgbase64,'file_id':fileid,'mini_imgbase64':mini_imgbase64,'miniFile_id':miniFile_id}
    r = requests.post(myurl,data)
    return r

def listener(messages):
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'photo':
            text = m.photo[-1]
            minitext = m.photo[0]
            file_id = text.file_id
            miniFile_id=minitext.file_id
            file_size = text.file_size
            if file_size < 120000:
                return 'filesize is too small'
            imgbase64 = get_imgfile2Base64(file_id)
            mini_imgbase64 = get_imgfile2Base64(miniFile_id)
            respon = post_imgbase64(imgbase64,file_id,mini_imgbase64,miniFile_id)
            print(respon.text)
#            bot.send_message(chatid,text)
if __name__ == '__main__':
    bot.set_update_listener(listener)
    bot.polling()
