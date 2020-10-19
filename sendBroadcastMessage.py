from flask import Flask, request, abort
from flask_script import Manager, Server
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
    print("hello, this is linebot sendMessage.")


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
def sendBroadcastMessage():
    text = texts[random.randint(0, len(texts)-1)]
    messages = TextSendMessage(text=text)
    print("----【message: ", text, "】----")

    try:
        line_bot_api.broadcast(messages=messages)
        DebugMessage("broadcast", "success")
    except LineBotApiError as e:
        DebugMessage("broadcast", e)


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    manager.add_command('runserver', Server(
        host='0.0.0.0', port=port, debug=True))
    manager.run()
