from typing import Optional, TypedDict, Annotated
from enum import Enum


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


class GetTicketExtraParams(TypedDict, total=False):
    """Редко используемые параметры (для Unpack в kwargs)"""
    from_date_updated: str
    to_date_updated: str
    freeze: int
    deleted: int


class GetTicketParams(GetTicketExtraParams, total=False):
    """Полный набор параметров get_tickets_page"""
    search_query: str
    source_list: list[TicketSource]
    status_list: list[TicketStatus]
    department_list: list[int]
    page: int
    from_date_created: Annotated[str, '2025-10-23 08:55:18']
    to_date_created: str

class CreateMessageProto(TypedDict):
    text: str
    user_id: Optional[int] | None = None #todo default = id supai bota


class GetUsersExtraParams(TypedDict, total=False):
    """Редко используемые параметры для получения пользователей"""
    from_date_created: str
    to_date_created: str
    from_date_updated: str
    to_date_updated: str
    order_by: str


class GetUsersParams(GetUsersExtraParams, total=False):
    """Полный набор параметров get_users_page"""
    page: int
    search: str
    exact_search: int
    group_list: str
    id_list: str
    organization_list: str



