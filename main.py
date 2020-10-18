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

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
    return "hello world!"


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    texts = [
        "おはよう\u1F600",
        "\uDBC0\uDC78"
    ]
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=texts[random.randint(0, len(texts)-1)]))


def main():
    texts = [
        "おはよう\u1F600",
        "\uDBC0\uDC78"
    ]
    to = ["aaotfsm"]
    messages = TextSendMessage(
        text=texts[random.randint(0, len(texts)-1)])
    line_bot_api.push_message("aaotfsm", messages=messages)
    line_bot_api.multicast(to, messages=messages)
    line_bot_api.broadcast(messages=messages)


if __name__ == "__main__":
    #    app.run()
    main()
    # port = int(os.getenv("PORT"))
    # app.run(host="0.0.0.0", port=port)
