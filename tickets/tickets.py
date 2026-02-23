from typing import Unpack, Annotated, Any

from models import (
    GetTicketExtraParams,
    GetTicketParams,
    CreateTicketParams,
    UpdateTicketParams,
    TicketSource,
    TicketStatus,
)


class Tickets:
    def __init__(self, api):
        self._api = api

    # ── GET /tickets/ ─────────────────────────────────────────────────────────

    def get_tickets_page(
        self,
        search: str | None = None,
        exact_search: int | None = None,
        pid: int | None = None,
        source_list: list[TicketSource] | None = None,
        status_list: list[TicketStatus] | None = None,
        priority_list: list[int] | None = None,
        type_list: list[int] | None = None,
        department_list: list[int] | None = None,
        user_list: list[int] | None = None,
        owner_list: list[int] | None = None,
        from_date_created: Annotated[str, '2025-10-23 08:55:18'] | None = None,
        to_date_created: str | None = None,
        page: int = 1,
        **kwargs: Unpack[GetTicketExtraParams],
    ):
        """
        Получить одну страницу тикетов.

        Sync:  client.tickets.get_tickets_page(page=1)
        Async: await async_client.tickets.get_tickets_page(page=1)

        Args:
            search: Поисковый запрос.
            exact_search: Точное совпадение (1 — да, 0 — нет).
            pid: ID родительской заявки.
            source_list: Список источников (TicketSource.telegram, .whatsapp, ...).
            status_list: Список статусов (TicketStatus.new, .open, .in_process, ...).
            priority_list: Список ID приоритетов.
            type_list: Список ID типов.
            department_list: Список ID отделов.
            user_list: Список ID владельцев (клиентов).
            owner_list: Список ID исполнителей.
            from_date_created: Дата создания ОТ (формат: 'YYYY-MM-DD HH:MM:SS').
            to_date_created: Дата создания ДО.
            page: Номер страницы (с 1).
            **kwargs: Дополнительные фильтры (from_date_updated, to_date_updated,
                      freeze, deleted, order_by).
        """
        params: GetTicketParams = {
            "search": search,
            "exact_search": exact_search,
            "pid": pid,
            "source_list": source_list,
            "status_list": status_list,
            "priority_list": priority_list,
            "type_list": type_list,
            "department_list": department_list,
            "user_list": user_list,
            "owner_list": owner_list,
            "from_date_created": from_date_created,
            "to_date_created": to_date_created,
            "page": page,
            **kwargs,
        }
        return self._api._request("GET", "tickets", params)

    # ── GET /tickets/:id/ ─────────────────────────────────────────────────────

    def get_ticket_by_id(self, ticket_id: int):
        """
        Получить заявку по ID.

        Возвращает наиболее актуальные данные по конкретной заявке
        (в отличие от get_tickets_page, который использует индекс).

        Sync:  client.tickets.get_ticket_by_id(12345)
        Async: await async_client.tickets.get_ticket_by_id(12345)

        Args:
            ticket_id: Технический ID заявки.
        """
        return self._api._request("GET", f"tickets/{ticket_id}/")

    # ── POST /tickets/ ────────────────────────────────────────────────────────

    def create_ticket(
        self,
        title: str,
        description: str,
        pid: int | None = None,
        sla_date: str | None = None,
        status_id: str | None = None,
        priority_id: int | None = None,
        type_id: int | None = None,
        department_id: int | None = None,
        ticket_lock: bool | None = None,
        owner_id: int | None = None,
        user_id: int | None = None,
        user_email: str | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        followers: list[int] | None = None,
        create_from_user: int | None = None,
        custom_fields: dict[str, Any] | None = None,
        tags: list[str | int] | None = None,
    ):
        """
        Создать заявку.

        Sync:  client.tickets.create_ticket(title='...', description='...')
        Async: await async_client.tickets.create_ticket(title='...', description='...')

        Args:
            title: Тема заявки (обязательно).
            description: Описание заявки (обязательно).
            pid: ID родительской заявки.
            sla_date: Дата и время SLA (DD.MM.YYYY HH:MM).
            status_id: ID статуса.
            priority_id: ID приоритета.
            type_id: ID типа.
            department_id: ID департамента.
            ticket_lock: Блокировка заявки.
            owner_id: ID исполнителя.
            user_id: ID владельца (клиента).
            user_email: Email клиента (если нет user_id, создаст пользователя).
            cc: Адресаты копий письма.
            bcc: Адресаты скрытых копий.
            followers: Список ID сотрудников-наблюдателей.
            create_from_user: 1 — от имени клиента, 0 — от имени сотрудника.
            custom_fields: Индивидуальные поля {'field_id': value}.
            tags: Метки.
        """
        data: CreateTicketParams = {
            "title": title,
            "description": description,
        }
        # Добавляем только не-None поля
        _optional = {
            "pid": pid,
            "sla_date": sla_date,
            "status_id": status_id,
            "priority_id": priority_id,
            "type_id": type_id,
            "department_id": department_id,
            "ticket_lock": ticket_lock,
            "owner_id": owner_id,
            "user_id": user_id,
            "user_email": user_email,
            "cc": cc,
            "bcc": bcc,
            "followers": followers,
            "create_from_user": create_from_user,
            "custom_fields": custom_fields,
            "tags": tags,
        }
        for k, v in _optional.items():
            if v is not None:
                data[k] = v

        return self._api._request("POST", "tickets/", data=data)

    # ── PUT /tickets/:id/ ─────────────────────────────────────────────────────

    def update_ticket(
        self,
        ticket_id: int,
        title: str | None = None,
        description: str | None = None,
        pid: int | None = None,
        sla_date: str | None = None,
        status_id: str | None = None,
        priority_id: int | None = None,
        type_id: int | None = None,
        department_id: int | None = None,
        ticket_lock: bool | None = None,
        owner_id: int | None = None,
        user_id: int | None = None,
        user_email: str | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        followers: list[int] | None = None,
        custom_fields: dict[str, Any] | None = None,
        tags: list[str | int] | None = None,
    ):
        """
        Обновить заявку.

        Передавай только те поля, которые нужно изменить.

        Sync:  client.tickets.update_ticket(12345, status_id='closed')
        Async: await async_client.tickets.update_ticket(12345, status_id='closed')

        Args:
            ticket_id: Технический ID заявки.
            title: Тема заявки.
            description: Описание заявки.
            pid: ID родительской заявки.
            sla_date: Дата и время SLA (DD.MM.YYYY HH:MM), '' для сброса.
            status_id: ID статуса.
            priority_id: ID приоритета.
            type_id: ID типа.
            department_id: ID департамента.
            ticket_lock: Блокировка заявки.
            owner_id: ID исполнителя, '' для сброса.
            user_id: ID владельца (клиента).
            user_email: Email клиента.
            cc: Адресаты копий, [] для сброса.
            bcc: Адресаты скрытых копий, [] для сброса.
            followers: Список ID сотрудников-наблюдателей, [] для сброса.
            custom_fields: Индивидуальные поля {'field_id': value}.
            tags: Метки, [] для сброса.
        """
        data: UpdateTicketParams = {}
        _fields = {
            "title": title,
            "description": description,
            "pid": pid,
            "sla_date": sla_date,
            "status_id": status_id,
            "priority_id": priority_id,
            "type_id": type_id,
            "department_id": department_id,
            "ticket_lock": ticket_lock,
            "owner_id": owner_id,
            "user_id": user_id,
            "user_email": user_email,
            "cc": cc,
            "bcc": bcc,
            "followers": followers,
            "custom_fields": custom_fields,
            "tags": tags,
        }
        for k, v in _fields.items():
            if v is not None:
                data[k] = v

        return self._api._request("PUT", f"tickets/{ticket_id}/", data=data)

    # ── DELETE /tickets/:id/ ──────────────────────────────────────────────────

    def delete_ticket(self, ticket_id: int, hard_delete: bool = False):
        """
        Удалить заявку.

        Sync:  client.tickets.delete_ticket(12345)
        Async: await async_client.tickets.delete_ticket(12345)

        Args:
            ticket_id: Технический ID заявки.
            hard_delete: True — полное удаление, False — перенос в удалённые.
        """
        params = {"delete": "true"} if hard_delete else None
        return self._api._request("DELETE", f"tickets/{ticket_id}/", params=params)

    # ── Пагинация ─────────────────────────────────────────────────────────────

    def get_tickets_lazy(
        self,
        search: str | None = None,
        exact_search: int | None = None,
        pid: int | None = None,
        source_list: list[TicketSource] | None = None,
        status_list: list[TicketStatus] | None = None,
        priority_list: list[int] | None = None,
        type_list: list[int] | None = None,
        department_list: list[int] | None = None,
        user_list: list[int] | None = None,
        owner_list: list[int] | None = None,
        **kwargs: Unpack[GetTicketExtraParams],
    ):
        """
        Генератор страниц тикетов — загружает по одной странице.

        Sync:  for page in client.tickets.get_tickets_lazy(): ...
        Async: async for page in async_client.tickets.get_tickets_lazy(): ...

        Args:
            search: Поисковый запрос.
            exact_search: Точное совпадение (1 — да, 0 — нет).
            pid: ID родительской заявки.
            source_list: Список источников.
            status_list: Список статусов.
            priority_list: Список ID приоритетов.
            type_list: Список ID типов.
            department_list: Список ID отделов.
            user_list: Список ID владельцев.
            owner_list: Список ID исполнителей.
            **kwargs: Дополнительные фильтры (from_date_updated, to_date_updated,
                      freeze, deleted, order_by).
        """
        params = {
            "search": search,
            "exact_search": exact_search,
            "pid": pid,
            "source_list": source_list,
            "status_list": status_list,
            "priority_list": priority_list,
            "type_list": type_list,
            "department_list": department_list,
            "user_list": user_list,
            "owner_list": owner_list,
            **kwargs,
        }
        return self._api._paginate_lazy(self.get_tickets_page, params)

    def get_tickets_all(
        self,
        search: str | None = None,
        exact_search: int | None = None,
        pid: int | None = None,
        source_list: list[TicketSource] | None = None,
        status_list: list[TicketStatus] | None = None,
        priority_list: list[int] | None = None,
        type_list: list[int] | None = None,
        department_list: list[int] | None = None,
        user_list: list[int] | None = None,
        owner_list: list[int] | None = None,
        **kwargs: Unpack[GetTicketExtraParams],
    ):
        """
        Загружает все страницы тикетов сразу.

        Sync:  pages = client.tickets.get_tickets_all()
        Async: pages = await async_client.tickets.get_tickets_all()

        Args:
            search: Поисковый запрос.
            exact_search: Точное совпадение (1 — да, 0 — нет).
            pid: ID родительской заявки.
            source_list: Список источников.
            status_list: Список статусов.
            priority_list: Список ID приоритетов.
            type_list: Список ID типов.
            department_list: Список ID отделов.
            user_list: Список ID владельцев.
            owner_list: Список ID исполнителей.
            **kwargs: Дополнительные фильтры (from_date_updated, to_date_updated,
                      freeze, deleted, order_by).
        """
        params = {
            "search": search,
            "exact_search": exact_search,
            "pid": pid,
            "source_list": source_list,
            "status_list": status_list,
            "priority_list": priority_list,
            "type_list": type_list,
            "department_list": department_list,
            "user_list": user_list,
            "owner_list": owner_list,
            **kwargs,
        }
        return self._api._paginate_all(self.get_tickets_page, params)
