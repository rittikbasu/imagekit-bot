import os
import json
from replit import db
from telebot import telebot
from keepalive import keep_alive
from imagekit import getImagekitURL

token = os.environ.get("TELEGRAM_TOKEN","Key Not Found")

bot = telebot.TeleBot(
    token, parse_mode=None)

def checkFileSize(file_size, file_name, file_path):
    print(file_size, file_name, file_path)
    if file_size > 2000000:
        print("File size is too large")
        return "File size is too large"
    else:
        file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
        print(file_url)
        imagekit_url = getImagekitURL(file_url, file_name)
        print(imagekit_url)
        return imagekit_url


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    file_path = file_info.file_path
    process_json = str(file_info).replace("'", '"')
    file_dict = json.loads(process_json)
    file_name = file_dict['file_unique_id']
    file_size = float(file_dict['file_size'])
    reply = checkFileSize(file_size, file_name, file_path)
    print("reply: ", reply)
    bot.reply_to(message, reply)


@bot.message_handler(content_types=['document'])
def file(message):
    process_json = str(message.document).replace("'", '"')
    file_dict = json.loads(process_json)
    mime_type = file_dict['mime_type'].split('/')[0]
    if mime_type == 'image':
        fileID = file_dict['file_id']
        file_info = bot.get_file(fileID)
        file_path = file_info.file_path
        file_name = file_dict['file_unique_id']
        file_size = float(file_dict['file_size'])
        reply = checkFileSize(file_size, file_name, file_path)
        print("reply: ", reply)
        bot.reply_to(message, reply)
    else:
        bot.reply_to(message, "Only image files supported")


while True:
    keep_alive()
    bot.infinity_polling()