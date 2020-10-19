from flask import Flask, request, abort
import os
import random
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.exceptions import LineBotApiError
from config import app, manager, line_bot_api, handler, texts, DebugMessage


@app.route("/")
def index():
    print("hello, this is linebot sendReplyMessage.")


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


def sendReplyMessage(event):
    text = texts[random.randint(0, len(texts)-1)]
    messages = TextSendMessage(text=text)
    DebugMessage("message", text)

    try:
        line_bot_api.reply_message(
            event.reply_token, messages)
        DebugMessage("reply_message", "success")
    except LineBotApiError as e:
        DebugMessage("reply_message", e)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sendReplyMessage(event)


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
