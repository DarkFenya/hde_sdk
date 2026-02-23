import asyncio
from typing import Optional

import httpx as h
from dotenv import load_dotenv

from tickets import Tickets
from messages import Messages
from users import Users
from utils import serialise_params

load_dotenv()


class HdeApiAsync:
    """
    Асинхронный клиент. Используется через async with:

        async with HdeApiAsync(TOKEN, EMAIL, BASE_URL) as client:
            response = await client.tickets.get_tickets_page(page=1)
            async for page in client.tickets.get_tickets_lazy():
                ...
            all_pages = await client.tickets.get_tickets_all()
    """

    def __init__(self, hde_token: str, hde_email: str, hde_base_url: str):
        self.HDE_TOKEN = hde_token
        self.HDE_EMAIL = hde_email
        self.HDE_BASE_URL = hde_base_url
        self.auth = h.BasicAuth(self.HDE_EMAIL, self.HDE_TOKEN)
        self._client: Optional[h.AsyncClient] = None

        self.tickets = Tickets(self)
        self.messages = Messages(self)
        self.users = Users(self)

    async def __aenter__(self):
        self._client = h.AsyncClient(
            auth=self.auth,
            base_url=self.HDE_BASE_URL,
            timeout=15,
            verify=False,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> h.AsyncClient:
        if self._client is None:
            raise RuntimeError(
                "Клиент не инициализирован. Используй: async with HdeApiAsync(...) as client"
            )
        return self._client

    async def _request(
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
                response = await self.client.get(path, params=params)
            elif m == "POST":
                response = await self.client.post(path, params=params, json=data)
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

    async def _paginate_lazy(self, fetch_func, params: dict):
        """Async-генератор: используй async for page in client.tickets.get_tickets_lazy()"""
        current_page = 1
        params_copy = params.copy()
        params_copy.pop("page", None)

        while True:
            response = await fetch_func(**params_copy, page=current_page)
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

    async def _paginate_all(
        self,
        fetch_func,
        params: dict,
        max_concurrent: int = 5,
    ) -> list:
        """
        Загружает все страницы параллельно.
        Используй: all_pages = await client.tickets.get_tickets_all()
        """
        params_copy = params.copy()
        params_copy.pop("page", None)

        first_response = await fetch_func(**params_copy, page=1)
        if not first_response:
            return []

        first_data = first_response.json()

        def _extract(data):
            if isinstance(data, dict):
                for key in ["tickets", "users", "items", "data"]:
                    if key in data:
                        data = data[key]
                        break
            if isinstance(data, dict):
                data = list(data.values())
            return data

        all_pages = [_extract(first_data)]

        total_pages = 1
        if isinstance(first_data, dict) and "pagination" in first_data:
            total_pages = first_data["pagination"].get("total_pages", 1)

        if total_pages > 1:
            semaphore = asyncio.Semaphore(max_concurrent)

            async def fetch_page(page_num):
                async with semaphore:
                    response = await fetch_func(**params_copy, page=page_num)
                    if response:
                        return _extract(response.json())
                    return []

            tasks = [fetch_page(p) for p in range(2, total_pages + 1)]
            remaining = await asyncio.gather(*tasks)
            all_pages.extend(remaining)

        return all_pages
