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
    "大好き\uDBC0\uDC78",
    "電話していい？",
    "はじめまして。\n畠山そらと申します。東京女子医科大学医学部の2年生です。趣味はドラマ鑑賞、音楽鑑賞、セルフネイルです。\nよろしくお願い致します。",
    "はじめまして、有栖川沙羅です。\n23歳、AB型。趣味はゲームと料理です。",
    "はじめまして！名前です。今20歳で大学3年です。休みの日は映画を見たり、飲みに行ったりしています。今後は就職活動を頑張りつつ、最後の学生生活を楽しみたいと思います。",
    "大学1年の吉野百華です。\n機械系に興味があり、大学では鳥人間コンテストと学生フォーミュラのサークルき所属しています。\n中高ではテニスと競技かるたをやっていました。\nTWICEとか坂道が好きです。\nよろしくお願いします。",
    "こんにちは、はじめまして\u1F60A \n押山凜です！\n4日前にラストティーンになった女の子です\u270C\n好きなことは、食べること、寝ること、笑うこと！\nこれからよろしくね\u1F647",
    "こんにちは\n茨木ほなみ、19才学生です\n好きな事はシーシャです\n愛犬が2匹います\n美容にお金を使うのが好きです\nよろしくお願いします",
    "佐々木です\nよろしくお願いします",
    "大学1年の白井と申します。大学ではコンピュータ理工学を学んでいますが、前からパソコン系の何かをやっていたわけでは無いので、課題に苦労しています。趣味は音楽系で、ギター弾きます。あと、なぜかコンビニ行くのが好きです。今一番欲しいものは時間です。",
    "趙曉松",
    "Hey, I hope you get back home safe.\nThanks so much for tonight.\nIt was fun.",
]


def DebugMessage(debugType, debugMessage):
    print("------------------------------------------------")
    print("【message", debugType, ":", debugMessage, "】")
    print("------------------------------------------------")
