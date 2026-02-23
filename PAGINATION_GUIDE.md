# Пагинация

Три способа получить данные. Во всех случаях JSON уже распарсен — `.json()` вызывать не нужно.

## 1. Одна страница

```python
response = client.tickets.get_tickets_page(page=1)
data = response.json()
```

Используй, если нужна только конкретная страница или хочешь сам управлять пагинацией.

## 2. Ленивая загрузка — `get_tickets_lazy()`

```python
for page in client.tickets.get_tickets_lazy():
    for ticket in page:
        print(ticket['id'])
```

Загружает по одной странице за раз. Подходит когда страниц много или хочется начать обработку сразу, не дожидаясь конца.

Можно прервать в любой момент:

```python
for page in client.tickets.get_tickets_lazy():
    process(page)
    if enough:
        break
```

## 3. Все страницы сразу — `get_tickets_all()`

```python
all_pages = client.tickets.get_tickets_all()
all_tickets = [t for page in all_pages for t in page]
```

Загружает всё в память, зато проще работать с итоговым списком. Хорошо для небольших выборок и агрегаций.

---

Те же методы есть у `users` и `messages`.
