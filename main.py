from add_watermark import WaterMark
from dotenv import load_dotenv
import json
import os
import requests
import threading
import urllib.request
from flask import Flask, render_template, request
import telegram

app = Flask(__name__)

# load_dotenv()


APIKEY = os.environ.get('APIKEY')
URL = f"https://api.telegram.org/bot{APIKEY}/"

session = {}
IMAGE_PATH = "image.png"


@app.route("/", methods=['GET', 'POST'])
def webhook():
    bot = telegram.Bot(token=os.environ["APIKEY"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.effective_chat.id
        text = update.message.text
        first_name = update.effective_chat.first_name
        message = update.message
        if message is not None:
            if message.photo is not None and len(message.photo) > 0:
                # message.reply_photo()
                watermark(message)
            else:
                bot.sendMessage(chat_id=chat_id, text=f"not a photo",
                                reply_to_message_id=message.message_id)
        bot.sendMessage(chat_id=chat_id, text=f"an error occurred")

        # Reply with the same message
        return 'ok'
    return 'error'


def index():
    return webhook()


# def index():
#     response = requests.get(URL + 'getUpdates')
#     updates = response.json()
#     # print(get_updates)
#     result = updates['result']
#     # print(result)
#     if (len(result) > 0):
#         if 'last_update_id' not in session:
#             # get last update
#             last_update_num = len(result) - 1
#             update_id = result[last_update_num]['update_id']
#             session['last_update_id'] = update_id
#         else:
#             for update in result:
#                 # respond to all new messages
#                 update_id = update['update_id']
#                 if (update_id > session['last_update_id']):
#                     print(update)
#                     message = update['message']
#                     chat = message['chat']
#                     if 'photo' not in message:
#                         answer = "not a photo"
#                         response = requests.get(
#                             f"{URL}sendMessage?chat_id={chat['id']}&text={answer}"
#                             f"&reply_to_message_id={message['message_id']}"
#                             f"&parse_mode=HTML")
#                     else:
#                         watermark(message)
#                     print(response.json())
#                     session['last_update_id'] = update_id
#     return 0


def watermark(message):
    file_id = message.photo[- 1].file_id
    # file_id = message['photo'][len(message['photo']) - 1]['file_id']
    getFile = requests.get(f'{URL}getFile?file_id={file_id}').json()
    file_path = getFile['result']['file_path']
    photo_url = f"https://api.telegram.org/file/bot{APIKEY}/{file_path}"
    data = {'chat_id': message.chat.id}
    # data = {'chat_id': message['chat']['id']}

    # downloads the image frorm telegram
    urllib.request.urlretrieve(photo_url, IMAGE_PATH)
    wm = WaterMark(IMAGE_PATH)
    ret, path = wm.addWaterMark()
    if ret == WaterMark.FAILURE:
        answer = "Failed processing image"
        response = requests.get(
            f"{URL}sendMessage?chat_id={data['chat_id']}&text={answer}"
            f"&reply_to_message_id={message.message_id}"
            f"&parse_mode=HTML")
        return

    with open(path, 'rb') as f:
        files = {'photo': f}
        response = requests.post(
            f"https://api.telegram.org/bot{APIKEY}/sendPhoto?"
            f"chat_id={data['chat_id']}&"
            f"reply_to_message_id={message.message_id}",
            files=files)

        # response = requests.get(
        #     f"{URL}sendMessage?chat_id={chat['id']}&text={answer}"
        #     f"&reply_to_message_id={message['message_id']}"
        #     f"&parse_mode=HTML")

# answer = f"You have just sent a photo: = {photo_url}"


# def run_update():
#     threading.Timer(5.0, run_update).start()
#     index()


# run_update()

# class TelegramBot:
#     def __init__(self):
#         self.__YOURAPIKEY = os.environ.get('YOURAPIKEY')
#         self.__URL = f"https://api.telegram.org/bot{self.__YOURAPIKEY}/"
#         self.__last_update_id = 0
#         self.__setLastUpdate()
