import os

import requests

bot_api_key = os.environ["TELEGRAM_BOT_API_KEY"]
chat_id = int(os.environ["TELEGRAM_CHAT_ID"])

url_base = "https://api.telegram.org/bot" + bot_api_key + "/"


def _call(endpoint, data):
    res = requests.post(url_base + endpoint, json=data)
    res.raise_for_status()
    return res.json()


def send_message(text):
    data = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
    return _call("sendMessage", data)


def pin_message(message_id):
    data = {"chat_id": chat_id, "message_id": message_id, "disable_notification": True}
    return _call("pinChatMessage", data)
