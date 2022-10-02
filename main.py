import os
import json
from urllib.parse import urlparse
from replit import db
from telebot import telebot
from keepalive import keep_alive
from imagekit import getImagekitURL
from db import writeToDB, getUserData

token = os.environ.get("TELEGRAM_TOKEN", "Key Not Found")

bot = telebot.TeleBot(token, parse_mode='HTML')

def checkFileSize(key, file_size):
    if key in db.keys():
        storageUsed = db[key]["storageUsed"] + file_size
    else:
        storageUsed = file_size
    print(storageUsed)
    if (storageUsed) > 100000000:
        return "You have exhausted your 100MB limit"
    elif file_size > 25000000:
        return "File size is too large"
    else:
        return storageUsed

def imagekitResponse(key, file_url, file_name, storageUsed, isUrl=False):
    imagekit_data = getImagekitURL(file_url, file_name)
    if imagekit_data:
        imagekit_url = imagekit_data[0]
        file_id = imagekit_data[1]
        if isUrl:
            size = imagekit_data[2]
            writeToDB(key=key, image_link=imagekit_url, file_size=size, file_id=file_id)
        else:
            writeToDB(key=key, image_link=imagekit_url, file_size=storageUsed, file_id=file_id)
        return imagekit_url
    else:
        return 'Only image files are supported'

def processImageData(key, file_name, file_path, isUrl=False, file_size=0):
    print(file_size, file_name, file_path)
    if url:
        storageUsed = checkFileSize(key=key, file_size=0)
        if type(storageUsed) != 'str':
            response = imagekitResponse(key=key, file_url=file_path, file_name=file_name, storageUsed=storageUsed, isUrl=True)
            return response
        else:
            return storageUsed
    else:
        storageUsed = checkFileSize(key, file_size)
        if type(storageUsed) != 'str':
            file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
            response = imagekitResponse(key=key, file_url=file_url, file_name=file_name, storageUsed=storageUsed)
            return response
        else:
            return storageUsed


def is_url(string):
    try:
        urlparse(string)
        return True
    except:
        return False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['images'])
def data(message):
    cid = message.chat.id
    key = str(cid)
    response = getUserData(key)
    bot.reply_to(message, response, disable_web_page_preview=True)


@bot.message_handler(content_types=['photo'])
def photo(message):
    cid = message.chat.id
    key = str(cid)
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    file_path = file_info.file_path
    process_json = str(file_info).replace("'", '"')
    file_dict = json.loads(process_json)
    file_name = file_dict['file_unique_id']
    file_size = float(file_dict['file_size'])
    reply = processImageData(key=key, file_size=file_size, file_name=file_name, file_path=file_path)
    print("reply: ", reply)
    bot.reply_to(message, reply, disable_web_page_preview=True)


@bot.message_handler(content_types=['document'])
def file(message):
    cid = message.chat.id
    key = str(cid)
    process_json = str(message.document).replace("'", '"')
    file_dict = json.loads(process_json)
    mime_type = file_dict['mime_type'].split('/')[0]
    if mime_type == 'image':
        fileID = file_dict['file_id']
        file_info = bot.get_file(fileID)
        file_path = file_info.file_path
        file_name = file_dict['file_unique_id']
        file_size = float(file_dict['file_size'])
        reply = processImageData(key=key, file_size=file_size, file_name=file_name, file_path=file_path)
        print("reply: ", reply)
        bot.reply_to(message, reply, disable_web_page_preview=True)
    else:
        bot.reply_to(message, "Only image files are supported")

@bot.message_handler(func=lambda m: True)
def url(message):
    cid = message.chat.id
    key = str(cid)
    text = message.text
    if is_url(text):
        file_name = message.id
        response = processImageData(key=key, isUrl=True, file_name=file_name, file_path=text)
        bot.reply_to(message, response, disable_web_page_preview=True)
    else:
        bot.reply_to(message, "Please enter a valid url")


while True:
    keep_alive()
    bot.infinity_polling()
