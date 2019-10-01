import os

import requests

BOT_API_KEY = os.environ["TELEGRAM_BOT_API_KEY"]
CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

URL_BASE = f"https://api.telegram.org/bot{BOT_API_KEY}/"


def _call(endpoint, data):
    res = requests.post(URL_BASE + endpoint, json=data)
    res.raise_for_status()
    return res.json()


def send_message(text):
    data = {"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True}
    return _call("sendMessage", data)


def pin_message(message_id):
    data = {"chat_id": CHAT_ID, "message_id": message_id, "disable_notification": True}
    return _call("pinChatMessage", data)
