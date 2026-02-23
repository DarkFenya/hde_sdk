from models import CreateMessageProto


class Messages:
    def __init__(self, api):
        self._api = api

    def create_message(self, message: CreateMessageProto, ticket_id: int):
        """
        Создать сообщение в тикете.

        Sync:  client.messages.create_message(msg, ticket_id=12345)
        Async: await async_client.messages.create_message(msg, ticket_id=12345)

        Args:
            message: Словарь с текстом сообщения {'text': '...', 'user_id': int | None}.
            ticket_id: ID тикета.
        """
        return self._api._request("POST", f"tickets/{ticket_id}/posts/", data=message)
