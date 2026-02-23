from typing import Optional, TypedDict, Annotated, Any
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────────────

class TicketStatus(str, Enum):
    new = 'new'
    open = 'open'
    in_process = 'in-process'
    S20 = '20'
    awaiting_client = 'awaiting-client'
    closed = 'closed'


class TicketSource(str, Enum):
    telegram = 'Telegram'
    whatsapp = 'WhatsApp'
    system = 'system'
    api = 'api'
    email = 'email'


# ─── GET /tickets/ — query-параметры ─────────────────────────────────────────

class GetTicketExtraParams(TypedDict, total=False):
    """Редко используемые параметры (для Unpack в kwargs)."""
    from_date_updated: str
    to_date_updated: str
    freeze: int
    deleted: int
    order_by: Annotated[str, 'date_created{desc},date_updated{asc}']


class GetTicketParams(GetTicketExtraParams, total=False):
    """Полный набор query-параметров GET /tickets/."""
    search: str
    exact_search: int
    pid: int
    source_list: list[TicketSource]
    status_list: list[TicketStatus]
    priority_list: list[int]
    type_list: list[int]
    department_list: list[int]
    user_list: list[int]
    owner_list: list[int]
    page: int
    from_date_created: Annotated[str, '2025-10-23 08:55:18']
    to_date_created: str


# ─── POST /tickets/ — тело запроса ────────────────────────────────────────────

class CreateTicketParams(TypedDict, total=False):
    """Параметры для создания заявки (POST /tickets/).

    Обязательные: title, description.
    """
    pid: int
    title: str                     # required
    description: str               # required
    sla_date: Annotated[str, 'DD.MM.YYYY HH:MM']
    status_id: str
    priority_id: int
    type_id: int
    department_id: int
    ticket_lock: bool
    owner_id: int
    user_id: int
    user_email: str
    cc: list[str]
    bcc: list[str]
    followers: list[int]
    create_from_user: int
    custom_fields: dict[str, Any]
    tags: list[str | int]


# ─── PUT /tickets/:id/ — тело запроса ─────────────────────────────────────────

class UpdateTicketParams(TypedDict, total=False):
    """Параметры для обновления заявки (PUT /tickets/:id/).

    Все поля опциональны — передаётся только то, что нужно изменить.
    """
    pid: int
    title: str
    description: str
    sla_date: Annotated[str, 'DD.MM.YYYY HH:MM']
    status_id: str
    priority_id: int
    type_id: int
    department_id: int
    ticket_lock: bool
    owner_id: int
    user_id: int
    user_email: str
    cc: list[str]
    bcc: list[str]
    followers: list[int]
    custom_fields: dict[str, Any]
    tags: list[str | int]


# ─── POST /tickets/:id/posts/ — создание сообщения ────────────────────────────

class CreateMessageProto(TypedDict):
    text: str
    user_id: Optional[int] | None


# ─── GET /users/ — query-параметры ────────────────────────────────────────────

class GetUsersExtraParams(TypedDict, total=False):
    """Редко используемые параметры для получения пользователей."""
    from_date_created: str
    to_date_created: str
    from_date_updated: str
    to_date_updated: str
    order_by: str


class GetUsersParams(GetUsersExtraParams, total=False):
    """Полный набор параметров get_users_page."""
    page: int
    search: str
    exact_search: int
    group_list: str
    id_list: str
    organization_list: str


# ─── Response-модели (TypedDict) ──────────────────────────────────────────────

class Pagination(TypedDict, total=False):
    """Объект пагинации, возвращаемый API."""
    total: int
    per_page: int
    current_page: int
    total_pages: int


class TicketData(TypedDict, total=False):
    """Одна заявка, как её возвращает API."""
    id: int
    pid: int
    unique_id: str
    date_created: str
    date_updated: str
    title: str
    source: str
    status_id: str
    priority_id: int
    type_id: int
    department_id: int
    department_name: str
    owner_id: int
    owner_name: str
    owner_lastname: str
    owner_email: str
    user_id: int
    user_name: str
    user_lastname: str
    user_email: str
    cc: list[str]
    bcc: list[str]
    followers: list[int]
    ticket_lock: int
    sla_date: str | None
    sla_flag: int
    freeze_date: str | None
    freeze: int
    viewed_by_staff: int
    viewed_by_client: int
    rate: str
    rate_comment: str
    rate_date: str
    deleted: int
    custom_fields: list[dict[str, Any]] | list
    tags: list[str]
    jira_issues: list


class TicketsListResponse(TypedDict, total=False):
    """Ответ GET /tickets/."""
    data: dict[str, TicketData]
    pagination: Pagination


class TicketSingleResponse(TypedDict, total=False):
    """Ответ GET /tickets/:id/, POST /tickets/, PUT /tickets/:id/."""
    data: TicketData


# ─── Enums (Users) ────────────────────────────────────────────────────────────

class UserStatus(str, Enum):
    active = 'active'
    disabled = 'disabled'
    fired = 'fired'


# ─── POST /users/ — тело запроса ──────────────────────────────────────────────

class CreateUserParams(TypedDict, total=False):
    """Параметры для создания пользователя (POST /users/).

    Обязательные: name, email.
    """
    name: str                      # required
    email: str                     # required
    password: str
    group_id: int
    department: list[int]
    lastname: str
    alias: str
    phone: str
    skype: str
    website: str
    organization: str
    organiz_id: int
    status: str
    language: str
    notifications: int
    user_status: str
    custom_fields: dict[str, Any]


# ─── PUT /users/:id/ — тело запроса ───────────────────────────────────────────

class UpdateUserParams(TypedDict, total=False):
    """Параметры для обновления пользователя (PUT /users/:id/).

    Все поля опциональны — передаётся только то, что нужно изменить.
    """
    name: str
    email: str
    password: str
    group_id: int
    department: list[int]
    lastname: str
    alias: str
    phone: str
    skype: str
    website: str
    organization: str
    organiz_id: int
    status: str
    language: str
    notifications: int
    user_status: str
    custom_fields: dict[str, Any]


# ─── Response-модели (Users) ──────────────────────────────────────────────────

class UserGroupData(TypedDict, total=False):
    """Группа пользователя."""
    id: int
    type: str
    name: dict[str, str]
    disable: int


class UserData(TypedDict, total=False):
    """Один пользователь, как его возвращает API."""
    id: int
    date_created: str
    date_updated: str
    name: str
    lastname: str
    alias: str
    email: str
    phone: str
    skype: str
    website: str
    organization: str | dict[str, Any]
    status: str
    language: str
    notifications: int | str
    api_key: str
    group: UserGroupData
    department: list[int]
    ldap_username: str | None
    user_status: str
    custom_fields: list[dict[str, Any]] | list