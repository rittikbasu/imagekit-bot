import os
import json
from telebot import telebot
from keepalive import keep_alive
from db import getUserData
from helper import processImageData, is_url
import texts

token = os.environ.get("TELEGRAM_TOKEN", "Key Not Found")

bot = telebot.TeleBot(token, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    bot.reply_to(message, texts.start)
    bot.send_message(cid, texts.help, disable_web_page_preview=True)

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, texts.help, disable_web_page_preview=True)

@bot.message_handler(commands=['images'])
def data(message):
    cid = message.chat.id
    key = str(cid)
    response = getUserData(key)
    bot.reply_to(message, response, disable_web_page_preview=True)


@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.reply_to(message, "Processing...")
    cid = message.chat.id
    key = str(cid)
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    file_path = file_info.file_path
    process_json = str(file_info).replace("'", '"')
    file_dict = json.loads(process_json)
    file_name = file_dict['file_unique_id']
    file_size = float(file_dict['file_size'])
    reply = processImageData(key=key, token=token, file_size=file_size, file_name=file_name, file_path=file_path)
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
        bot.reply_to(message, "Processing...")
        fileID = file_dict['file_id']
        file_info = bot.get_file(fileID)
        file_path = file_info.file_path
        file_name = file_dict['file_unique_id']
        file_size = float(file_dict['file_size'])
        reply = processImageData(key=key, token=token, file_size=file_size, file_name=file_name, file_path=file_path)
        print("reply: ", reply)
        bot.reply_to(message, reply, disable_web_page_preview=True)
    else:
        bot.reply_to(message, "Only image files are supported.")

@bot.message_handler(func=lambda m: True)
def url(message):
    cid = message.chat.id
    key = str(cid)
    text = message.text
    if is_url(text):
        bot.reply_to(message, "Processing...")
        file_name = message.id
        response = processImageData(key=key, token=token, isUrl=True, file_name=file_name, file_path=text)
        bot.reply_to(message, response, disable_web_page_preview=True)
    else:
        bot.reply_to(message, "Please enter a valid url or click /help")


while True:
    keep_alive()
    bot.infinity_polling()
