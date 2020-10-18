from flask import Flask, request, abort
import os
import random

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

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

texts = [
    "おはよう\u263A",
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


def sendMessage():
    to = ["U3938e2a7863ee6516ff6dc83fce2024e"]
    messages = TextSendMessage(text=texts[random.randint(0, len(texts)-1)])
    print(messages)
    try:
        line_bot_api.push_message("U3938e2a7863ee6516ff6dc83fce2024e", messages=messages)
    except LineBotApiError as e:
        print(e)
    try:
        line_bot_api.multicast(to, messages=messages)
    except LineBotApiError as e:
        print(e)
    try:
        line_bot_api.broadcast(messages=messages)
    except LineBotApiError as e:
        print(e)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    messages = TextSendMessage(text=texts[random.randint(0, len(texts)-1)])
    print(messages)
    try:
        line_bot_api.reply_message(event.reply_token, messages)
    except LineBotApiError as e:
        print(e)
    sendMessage()


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
