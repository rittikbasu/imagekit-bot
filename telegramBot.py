import telebot
import json
from decouple import config
from main import getImagekitURL

token = config("TELEGRAM_TOKEN")

bot = telebot.TeleBot(
    token, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    print('fileInfo =', str(file_info))
    file_path = file_info.file_path
    process_json = str(file_info).replace("'", '"')
    file_dict = json.loads(process_json)
    file_name = file_dict['file_unique_id']
    file_size = file_dict['file_size']
    print('file_name =', file_name, file_size)
    file_url = "https://api.telegram.org/file/bot{0}/{1}".format(
        token, file_path)
    imagekitURL = getImagekitURL(file_url, file_name)
    bot.reply_to(message, imagekitURL)


bot.polling()
