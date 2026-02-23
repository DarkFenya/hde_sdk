import json
import httpx
from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any
from config import ListToStrParams


def delete_none(obj: Any) -> dict[str, Any]:
    """Удаляет пары с None из словаря/датакласса."""
    if obj is None:
        return {}
    if is_dataclass(obj):
        data = asdict(obj)
    elif isinstance(obj, Mapping):
        data = dict(obj)
    else:
        raise TypeError(f"Unsupported type for delete_none: {type(obj)}")
    return {k: v for k, v in data.items() if v is not None}

def _stringify_value(v: Any) -> str:
    """Преобразует значение в строку (извлекая .value из Enum)."""
    if isinstance(v, Enum):
        return str(v.value)
    return str(v)

def _stringify_list(items: list) -> str:
    """Преобразует список в строку через запятую."""
    return ','.join(_stringify_value(item) for item in items)

def serialise_params(obj: Any) -> dict[str, Any]:
    """Готовит параметры запроса: убирает None, сериализует списки и Enum."""
    data = delete_none(obj)
    
    for k, v in data.items():
        # 1. Если это список
        if isinstance(v, list):
            if k in ListToStrParams:
                # В строку через запятую (для API)
                data[k] = _stringify_list(v)
            else:
                # В список строковых значений (для стандартной передачи параметров)
                data[k] = [_stringify_value(item) for item in v]
        
        # 2. Если это одиночный Enum
        elif isinstance(v, Enum):
            data[k] = v.value
            
    return data

def _random_message(min_length=50, max_length=200) -> str:
    words = [
        "тестовое", "сообщение", "проверка", "гипотеза", "эксперимент",
        "данные", "анализ", "система", "работает", "корректно",
        "отправка", "получение", "обработка", "функционал", "модуль",
        "интеграция", "API", "сервис", "запрос", "ответ",
    ]
    length = random.randint(min_length, max_length)
    result = []
    current = 0
    while current < length:
        word = random.choice(words)
        result.append(word)
        current += len(word) + 1
    text = " ".join(result)
    return text[:length]





    # def _iterator(client, method, path):
    #     httpx.Client = client
    #     while True:
    #         with httpx.Client as c : httpx.Client:
    #             r = c
