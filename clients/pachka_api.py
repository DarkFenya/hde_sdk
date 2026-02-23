import requests
from typing import Optional
class PachkaApi:
    def __init__(self, token: str):
        self.token = token
        self.base_url = 'https://api.pachka.com'

    def send_message(
        self, chat_id: str, text: str, display_name: Optional[str] = None
    ) -> None:
        """
        Отправляет сообщение в Pachca чат.

        Args:
            chat_id: ID чата
            text: Текст сообщения
            display_name: Опциональное имя отправителя
        """
        url = "https://api.pachca.com/api/shared/v1/messages"
        headers = {"Authorization": f"Bearer {self.token}"}
        msg = {"entity_type": "discussion", "entity_id": int(chat_id), "content": text}
        if display_name:
            msg["display_name"] = display_name
        try:
            r = requests.post(url, headers=headers, json={"message": msg}, timeout=30)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Error sending message: {e}")