from flask import Flask, request, abort
from flask_script import Manager
import os
import random
from rq import Queue
from worker import conn
from bottle import route, run
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from linebot.exceptions import LineBotApiError

app = Flask(__name__)
manager = Manager(app)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# redis
q = Queue(connection=conn)

texts = [
    "おはよう\u263A",
    "電話していい？",
    "\uDBC0\uDC78"
]


@app.route("/")
def index():
    print("hello world")


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@manager.command
def sendMessage():
    messages = TextSendMessage(text=texts[random.randint(0, len(texts)-1)])
    print("messages: ", messages)

    try:
        line_bot_api.broadcast(messages=messages)
        print("broadcast: success")
    except LineBotApiError as e:
        print("broadcast: ", e)


@route('/index')
def index():
    result = q.enqueue(sendMessage)
    return result


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    messages = TextSendMessage(text=texts[random.randint(0, len(texts)-1)])
    print("messages: ", messages)
    # try:
    #     line_bot_api.reply_message(event.reply_token, messages)
    #     print("broadcast: success")
    # except LineBotApiError as e:
    #     print("reply_message: ", e)
    sendMessage()


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
    manager.run()
    sendMessage()
