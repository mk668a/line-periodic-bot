from flask import Flask, request, abort
from flask_script import Manager, Server
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

# flask appからmanager作成
app = Flask(__name__)
manager = Manager(app)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

texts = [
    "おはよう\u263A",
    "\uDBC0\uDC78",
    "電話していい？",
    "それな",
]


def DebugMessage(debugType, debugMessage):
    print("------------------------------------------------")
    print("【message", debugType, ":", debugMessage, "】")
    print("------------------------------------------------")
