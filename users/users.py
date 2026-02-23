from typing import Unpack, Any

from models import (
    GetUsersExtraParams,
    GetUsersParams,
    CreateUserParams,
    UpdateUserParams,
)


class Users:
    def __init__(self, api):
        self._api = api

    # ── GET /users/ ───────────────────────────────────────────────────────────

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

        Sync:  client.users.get_users_page(page=1)
        Async: await async_client.users.get_users_page(page=1)

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

    # ── GET /users/:id/ ──────────────────────────────────────────────────────

    def get_user_by_id(self, user_id: int):
        """
        Получить пользователя по ID.

        Sync:  client.users.get_user_by_id(123)
        Async: await async_client.users.get_user_by_id(123)

        Args:
            user_id: ID пользователя.
        """
        return self._api._request("GET", f"users/{user_id}/")

    # ── POST /users/ ─────────────────────────────────────────────────────────

    def create_user(
        self,
        name: str,
        email: str,
        password: str | None = None,
        group_id: int | None = None,
        department: list[int] | None = None,
        lastname: str | None = None,
        alias: str | None = None,
        phone: str | None = None,
        skype: str | None = None,
        website: str | None = None,
        organization: str | None = None,
        organiz_id: int | None = None,
        status: str | None = None,
        language: str | None = None,
        notifications: int | None = None,
        user_status: str | None = None,
        custom_fields: dict[str, Any] | None = None,
    ):
        """
        Создать пользователя.

        Sync:  client.users.create_user(name='Иван', email='ivan@example.com')
        Async: await async_client.users.create_user(name='Иван', email='ivan@example.com')

        Args:
            name: Имя пользователя (обязательно).
            email: Email пользователя (обязательно).
            password: Пароль.
            group_id: ID группы (клиент / сотрудник / администратор).
            department: Список ID доступных департаментов.
            lastname: Фамилия.
            alias: Псевдоним.
            phone: Телефон.
            skype: Скайп.
            website: Адрес сайта.
            organization: Название компании (создаст новую, если не существует).
            organiz_id: ID существующей компании (игнорируется, если передан organization).
            status: Статус: 'active', 'disabled', 'fired'.
            language: Язык ('ru', 'en', ...).
            notifications: Уведомления на почту (1 — вкл, 0 — выкл).
            user_status: Статус активности ('online', 'offline').
            custom_fields: Индивидуальные поля {'field_id': value}.
        """
        data: CreateUserParams = {
            "name": name,
            "email": email,
        }
        _optional = {
            "password": password,
            "group_id": group_id,
            "department": department,
            "lastname": lastname,
            "alias": alias,
            "phone": phone,
            "skype": skype,
            "website": website,
            "organization": organization,
            "organiz_id": organiz_id,
            "status": status,
            "language": language,
            "notifications": notifications,
            "user_status": user_status,
            "custom_fields": custom_fields,
        }
        for k, v in _optional.items():
            if v is not None:
                data[k] = v

        return self._api._request("POST", "users/", data=data)

    # ── PUT /users/:id/ ──────────────────────────────────────────────────────

    def update_user(
        self,
        user_id: int,
        name: str | None = None,
        email: str | None = None,
        password: str | None = None,
        group_id: int | None = None,
        department: list[int] | None = None,
        lastname: str | None = None,
        alias: str | None = None,
        phone: str | None = None,
        skype: str | None = None,
        website: str | None = None,
        organization: str | None = None,
        organiz_id: int | None = None,
        status: str | None = None,
        language: str | None = None,
        notifications: int | None = None,
        user_status: str | None = None,
        custom_fields: dict[str, Any] | None = None,
    ):
        """
        Обновить пользователя.

        Передавай только те поля, которые нужно изменить.

        Sync:  client.users.update_user(123, phone='+7999...')
        Async: await async_client.users.update_user(123, phone='+7999...')

        Args:
            user_id: ID пользователя.
            name: Имя.
            email: Email.
            password: Пароль.
            group_id: ID группы.
            department: Список ID доступных департаментов.
            lastname: Фамилия.
            alias: Псевдоним.
            phone: Телефон.
            skype: Скайп.
            website: Адрес сайта.
            organization: Название компании.
            organiz_id: ID существующей компании.
            status: Статус: 'active', 'disabled', 'fired'.
            language: Язык ('ru', 'en', ...).
            notifications: Уведомления на почту (1 — вкл, 0 — выкл).
            user_status: Статус активности.
            custom_fields: Индивидуальные поля {'field_id': value}.
        """
        data: UpdateUserParams = {}
        _fields = {
            "name": name,
            "email": email,
            "password": password,
            "group_id": group_id,
            "department": department,
            "lastname": lastname,
            "alias": alias,
            "phone": phone,
            "skype": skype,
            "website": website,
            "organization": organization,
            "organiz_id": organiz_id,
            "status": status,
            "language": language,
            "notifications": notifications,
            "user_status": user_status,
            "custom_fields": custom_fields,
        }
        for k, v in _fields.items():
            if v is not None:
                data[k] = v

        return self._api._request("PUT", f"users/{user_id}/", data=data)

    # ── DELETE /users/:id/ ────────────────────────────────────────────────────

    def delete_user(self, user_id: int):
        """
        Удалить пользователя.

        Sync:  client.users.delete_user(123)
        Async: await async_client.users.delete_user(123)

        Args:
            user_id: ID пользователя.
        """
        return self._api._request("DELETE", f"users/{user_id}/")

    # ── Пагинация ─────────────────────────────────────────────────────────────

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