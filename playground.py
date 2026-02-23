import asyncio
import os
import random
import string
import time
from datetime import datetime, timedelta

import httpx
from dotenv import load_dotenv

from clients.api_client import HdeApi
from clients.api_client_async import HdeApiAsync
from clients.pachka_api import PachkaApi
from config import main_b2c_departments, monitoring_chat_id, tags_test
from models import CreateMessageProto, TicketStatus

load_dotenv()

HDE_TOKEN = os.getenv("HDE_TOKEN")
HDE_EMAIL = os.getenv("HDE_EMAIL")
HDE_BASE_URL = os.getenv("HDE_BASE_URL")
PACHKA_TOKEN = os.getenv("PACHCA_API_TOKEN")


client = HdeApi(HDE_TOKEN, HDE_EMAIL, HDE_BASE_URL)
pachka = PachkaApi(PACHKA_TOKEN)

#   async def main():
#       async with HdeApiAsync(HDE_TOKEN, HDE_EMAIL, HDE_BASE_URL) as async_client:
#           response = await async_client.tickets.get_tickets_page(page=1)
#           async for page in async_client.tickets.get_tickets_lazy():
#               ...
#           all_pages = await async_client.tickets.get_tickets_all()
#
# ─────────────────────────────────────────────────────────────────────────────



