from typing import Unpack, Annotated

from models import GetTicketExtraParams, GetTicketParams, TicketSource, TicketStatus


class Tickets:
    def __init__(self, api):
        self._api = api

    def get_tickets_page(
        self,
        search_query: str | None = None,
        source_list: list[TicketSource] | None = None,
        status_list: list[TicketStatus] | None = None,
        from_date_created: Annotated[str, '2025-10-23 08:55:18'] | None = None,
        to_date_created: str | None = None,
        department_list: list[int] | None = None,
        page: int = 1,
        **kwargs: Unpack[GetTicketExtraParams],
    ):
        """
        Получить одну страницу тикетов.

        Args:
            search_query: Поисковый запрос.
            source_list: Список источников (TicketSource.telegram, .whatsapp).
            status_list: Список статусов (TicketStatus.new, .open, .in_process, ...).
            from_date_created: Дата создания ОТ (формат: '2025-10-23 08:55:18').
            to_date_created: Дата создания ДО.
            department_list: Список ID отделов.
            page: Номер страницы (с 1).
            **kwargs: Дополнительные фильтры (from_date_updated, to_date_updated, freeze, deleted).
        """
        params: GetTicketParams = {
            "search_query": search_query,
            "source_list": source_list,
            "status_list": status_list,
            "from_date_created": from_date_created,
            "to_date_created": to_date_created,
            "department_list": department_list,
            "page": page,
            **kwargs,
        }
        return self._api._request("GET", "tickets", params)

    def get_tickets_lazy(
        self,
        search_query: str | None = None,
        source_list: list[TicketSource] | None = None,
        status_list: list[TicketStatus] | None = None,
        department_list: list[int] | None = None,
        **kwargs: Unpack[GetTicketExtraParams],
    ):
        """
        Генератор страниц тикетов — загружает по одной странице.

        Sync:  for page in client.tickets.get_tickets_lazy(): ...
        Async: async for page in async_client.tickets.get_tickets_lazy(): ...

        Args:
            search_query: Поисковый запрос.
            source_list: Список источников.
            status_list: Список статусов.
            department_list: Список ID отделов.
            **kwargs: Дополнительные фильтры (from_date_updated, to_date_updated, freeze, deleted).
        """
        params = {
            "search_query": search_query,
            "source_list": source_list,
            "status_list": status_list,
            "department_list": department_list,
            **kwargs,
        }
        return self._api._paginate_lazy(self.get_tickets_page, params)

    def get_tickets_all(
        self,
        search_query: str | None = None,
        source_list: list[TicketSource] | None = None,
        status_list: list[TicketStatus] | None = None,
        department_list: list[int] | None = None,
        **kwargs: Unpack[GetTicketExtraParams],
    ):
        """
        Загружает все страницы тикетов сразу.

        Sync:  pages = client.tickets.get_tickets_all()
        Async: pages = await async_client.tickets.get_tickets_all()

        Args:
            search_query: Поисковый запрос.
            source_list: Список источников.
            status_list: Список статусов.
            department_list: Список ID отделов.
            **kwargs: Дополнительные фильтры (from_date_updated, to_date_updated, freeze, deleted).
        """
        params = {
            "search_query": search_query,
            "source_list": source_list,
            "status_list": status_list,
            "department_list": department_list,
            **kwargs,
        }
        return self._api._paginate_all(self.get_tickets_page, params)
