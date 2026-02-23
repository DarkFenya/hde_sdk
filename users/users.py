from typing import Unpack

from models import GetUsersExtraParams, GetUsersParams


class Users:
    def __init__(self, api):
        self._api = api

    def get_users_page(
        self,
        page: int = 1,
        search: str | None = None,
        exact_search: int | None = None,
        group_list: str | None = None,
        id_list: str | None = None,
        organization_list: str | None = None,
        **kwargs: Unpack[GetUsersExtraParams],
    ):
        """
        Получить одну страницу пользователей.

        Args:
            page: Номер страницы (30 пользователей на странице).
            search: Поиск по имени / email.
            exact_search: Точное совпадение поля search (1 — да, 0 — нет).
            group_list: ID групп через запятую.
            id_list: ID пользователей через запятую.
            organization_list: ID компаний через запятую.
            **kwargs: Дополнительные фильтры (from_date_created, to_date_created,
                      from_date_updated, to_date_updated, order_by).
        """
        params: GetUsersParams = {
            "page": page,
            "search": search,
            "exact_search": exact_search,
            "group_list": group_list,
            "id_list": id_list,
            "organization_list": organization_list,
            **kwargs,
        }
        return self._api._request("GET", "users/", params)

    def get_users_lazy(
        self,
        search: str | None = None,
        exact_search: int | None = None,
        group_list: str | None = None,
        id_list: str | None = None,
        organization_list: str | None = None,
        **kwargs: Unpack[GetUsersExtraParams],
    ):
        """
        Генератор страниц пользователей — загружает по одной странице.

        Sync:  for page in client.users.get_users_lazy(): ...
        Async: async for page in async_client.users.get_users_lazy(): ...

        Args:
            search: Поиск по имени / email.
            exact_search: Точное совпадение (1 — да, 0 — нет).
            group_list: ID групп через запятую.
            id_list: ID пользователей через запятую.
            organization_list: ID компаний через запятую.
            **kwargs: Дополнительные фильтры (from_date_created, to_date_created,
                      from_date_updated, to_date_updated, order_by).
        """
        params = {
            "search": search,
            "exact_search": exact_search,
            "group_list": group_list,
            "id_list": id_list,
            "organization_list": organization_list,
            **kwargs,
        }
        return self._api._paginate_lazy(self.get_users_page, params)

    def get_users_all(
        self,
        search: str | None = None,
        exact_search: int | None = None,
        group_list: str | None = None,
        id_list: str | None = None,
        organization_list: str | None = None,
        **kwargs: Unpack[GetUsersExtraParams],
    ):
        """
        Загружает все страницы пользователей сразу.

        Sync:  pages = client.users.get_users_all()
        Async: pages = await async_client.users.get_users_all()

        Args:
            search: Поиск по имени / email.
            exact_search: Точное совпадение (1 — да, 0 — нет).
            group_list: ID групп через запятую.
            id_list: ID пользователей через запятую.
            organization_list: ID компаний через запятую.
            **kwargs: Дополнительные фильтры (from_date_created, to_date_created,
                      from_date_updated, to_date_updated, order_by).
        """
        params = {
            "search": search,
            "exact_search": exact_search,
            "group_list": group_list,
            "id_list": id_list,
            "organization_list": organization_list,
            **kwargs,
        }
        return self._api._paginate_all(self.get_users_page, params)
