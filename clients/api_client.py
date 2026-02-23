import os

import httpx as h
from dotenv import load_dotenv

from tickets import Tickets
from messages import Messages
from users import Users
from utils import serialise_params

load_dotenv()


class HdeApi:
    """
    Синхронный клиент.

        client = HdeApi(TOKEN, EMAIL, BASE_URL)
        response = client.tickets.get_tickets_page(page=1)
        for page in client.tickets.get_tickets_lazy():
            ...
        all_pages = client.tickets.get_tickets_all()
    """

    def __init__(self, hde_token: str, hde_email: str, hde_base_url: str):
        self.HDE_TOKEN = hde_token
        self.HDE_EMAIL = hde_email
        self.HDE_BASE_URL = hde_base_url
        self._http = self._init_client()

        self.tickets = Tickets(self)
        self.messages = Messages(self)
        self.users = Users(self)

    def _init_client(self) -> h.Client:
        auth = h.BasicAuth(self.HDE_EMAIL, self.HDE_TOKEN)
        return h.Client(auth=auth, base_url=self.HDE_BASE_URL, timeout=15, verify=False)

    def _request(
        self,
        method: str,
        path: str,
        params: object | None = None,
        data: object | None = None,
    ) -> h.Response | None:
        try:
            if params is not None:
                params = serialise_params(params)
        except Exception as e:
            print(f"[_request] Ошибка сериализации params: {e}")
            return None

        try:
            m = method.upper()
            if m == "GET":
                response = self._http.get(path, params=params)
            elif m == "POST":
                response = self._http.post(path, params=params, json=data)
            else:
                print(f"[_request] Неподдерживаемый метод: {m}")
                return None
            response.raise_for_status()
        except h.ConnectError as e:
            print(f"[_request] Ошибка подключения: {e}")
            return None
        except h.HTTPStatusError as e:
            print(f"[_request] HTTP ошибка: {e}")
            return None

        return response

    def _paginate_lazy(self, fetch_func, params: dict):
        """Генератор: используй for page in client.tickets.get_tickets_lazy()"""
        current_page = 1
        params_copy = params.copy()
        params_copy.pop("page", None)

        while True:
            response = fetch_func(**params_copy, page=current_page)
            if response is None:
                break

            try:
                data = response.json()
                if isinstance(data, dict):
                    for key in ["tickets", "users", "items", "data"]:
                        if key in data:
                            data = data[key]
                            break
                if isinstance(data, dict):
                    data = list(data.values())
                if not data:
                    break
                yield data
            except Exception as e:
                print(f"[_paginate_lazy] Ошибка парсинга: {e}")
                break

            current_page += 1

    def _paginate_all(self, fetch_func, params: dict) -> list:
        return list(self._paginate_lazy(fetch_func, params))
