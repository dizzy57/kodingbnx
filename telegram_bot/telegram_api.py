import os

import requests

BOT_API_KEY = os.environ["TELEGRAM_BOT_API_KEY"]
CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

URL_BASE = f"https://api.telegram.org/bot{BOT_API_KEY}/"


class TelegramApi:
    def __init__(self):
        self.session = requests.session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return False

    def _call(self, endpoint, data):
        res = self.session.post(URL_BASE + endpoint, json=data)
        res.raise_for_status()
        return res.json()

    def send_message(self, text):
        data = {"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True}
        return self._call("sendMessage", data)

    def pin_message(self, message_id):
        data = {
            "chat_id": CHAT_ID,
            "message_id": message_id,
            "disable_notification": True,
        }
        return self._call("pinChatMessage", data)
