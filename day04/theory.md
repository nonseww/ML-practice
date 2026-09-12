# SQL

**orders**

|  id | user_id | product  | price |
| --: | ------: | -------- | ----: |
|   1 |      10 | Phone    |   500 |
|   2 |      10 | Mouse    |    50 |
|   3 |      20 | Keyboard |   100 |
|   4 |      20 | Monitor  |   300 |
|   5 |      30 | Mouse    |    50 |

## 1. Введение

```SQL
SELECT *
FROM orders;
```

`SELECT` - что хотим получить
`FROM` - из какой таблицы

## 2. WHERE - фильтрация строк

```SQL
SELECT *
FROM orders
WHERE price > 100;
```

Получим:

|  id | user_id | product | price |
| --: | ------: | ------- | ----: |
|   1 |      10 | Phone   |   500 |
|   4 |      20 | Monitor |   300 |

Работает как:

```python
df[df["price"] > 100]
```

## 3. Несколько условий

```SQL
SELECT *
FROM orders
WHERE price > 50 AND user_id = 20;
```

Работает как:

```python
df[(df["price"] > 50) & (df["user_id"] == 20)]
```

## 4. Выбрать только нужные столбцы

```SQL
SELECT user_id, price
FROM orders;
```

Получим:

| user_id | price |
| ------: | ----: |
|      10 |   500 |
|      10 |    50 |
|      20 |   100 |
|      20 |   300 |
|      30 |    50 |

Работает как:

```python
df[["user_id", "price"]]
```

## 5. Агрегатные функции

Пусть нас интересует **средняя цена** всех заказов:

```SQL
SELECT AVG(price)
FROM orders;
```

Работает как:

```python
df["price"].mean()
```

| Функция   | Что делает |
| --------- | ---------- |
| `COUNT()` | считает    |
| `SUM()`   | сумма      |
| `AVG()`   | среднее    |
| `MIN()`   | минимум    |
| `MAX()`   | максимум   |

## 6. GROUP BY

Мы хотим узнать **среднюю цену отдельно для каждого юзера**.

```SQL
SELECT user_id, AVG(price)
FROM orders
GROUP BY user_id;
```

Получим:

| user_id | AVG(price) |
| ------: | ---------: |
|      10 |        275 |
|      20 |        200 |
|      30 |         50 |

Работает как:

```python
df.groupby("user_id")["price"].mean()
```

## 7. GROUP BY + несколько агрегатов

Например, хотим для каждого юзера:

- количество заказов
- общую сумму
- среднюю цену
- максимальную цену

```SQL
SELECT
    user_id,
    COUNT(*) AS orders_count,
    SUM(price) AS total_price,
    AVG(price) AS avg_price,
    MAX(price) AS max_price
FROM orders
GROUP BY user_id;
```

Получим:

| user_id | orders_count | total_price | avg_price | max_price |
| ------: | -----------: | ----------: | --------: | --------: |
|      10 |            2 |         550 |       275 |       500 |
|      20 |            2 |         400 |       200 |       300 |
|      30 |            1 |          50 |        50 |        50 |

Работает как:

```python
df.groupby("user_id")["price"].agg([
    "count", "sum", "mean", "max"
])
```

## 8. Правило GROUP BY

> Каждая группа должна давать однозначное значение для обычных выбранных столбцов, либо столбец должен быть агрегирован.

Пусть у нас есть:

```SQL
SELECT user_id, AVG(price)
FROM orders
GROUP BY user_id;
```

Почему мы можем написать `user_id`? Потому что он есть в:

```SQL
GROUP BY user_id
```

А `AVG(price)` - агрегатная функция.

А это чаще всего некорректно:

```SQL
SELECT user_id, product, AVG(price)
FROM orders
GROUP BY user_id;
```

Почему? Пусть у нас:

```
user_id = 10
Phone 500
Mouse 50
```

Сгруппировали юзера 10 в одну группу. Но какой продукт брать? Непонятно.

## 9. HAVING

Пусть мы хотим **найти пользователей, у которых средняя стоимость заказа больше 200**.

Это работать не будет:

```SQL
WHERE AVG(price) > 200
```

Потому что `WHERE` фильтрует **отдельные строки до группировки**. А нам нужно фильтровать уже получившиеся группы.

Для этого можем заюзать `HAVING`.

```SQL
SELECT user_id, AVG(price) AS avg_price
FROM orders
GROUP BY user_id
HAVING AVG(price) > 200;
```

Получим:

| user_id | avg_price |
| ------: | --------: |
|      10 |       275 |

Работает как:

```python
result = df.groupby("user_id")["price"].mean().reset_index(name="avg_price")
result = result[result["avg_price"] > 200]
```

## 10. WHERE vs HAVING

```
таблица
↓
WHERE - фильтруем отдельные строки
↓
GROUP BY - собираем строки в группы
↓
агрегация - AVG / SUM / COUNT ...
↓
HAVING - фильтруем готовые группы
```

Пример:

```SQL
SELECT user_id, AVG(price)
FROM orders
WHERE price > 50
GROUP BY user_id
HAVING AVG(price) > 200;
```

Действия:

1. Выкинули заказы `price <= 50`
2. Оставшиеся строки сгруппировали по юзеру
3. Посчитали среднее
4. Оставили только группы со средним > 200

Работает как:

```python
result = df[df["price"] > 50].groupby("user_id")["price"].mean().reset_index(name="avg_price")
result = result[result["avg_price"] > 200]
```

## 11. COUNT(\*) vs COUNT(column)

Пусть есть таблица:

**orders**

|  id | user_id | price |
| --: | ------: | ----: |
|   1 |      10 |   100 |
|   2 |      10 |  NULL |
|   3 |      20 |   300 |
|   4 |      20 |   200 |

```SQL
SELECT COUNT(*)
FROM orders;
```

Отдаст 4, потому что `COUNT(*)` считает строки.

А:

```SQL
SELECT COUNT(price)
FROM orders;
```

Отдаст 3, потому что `COUNT(column)` не считает `NULL`.

## 12. DISTINCT

Допустим у нас есть

```
user_id
10
10
20
20
20
30
```

```SQL
SELECT COUNT(user_id)
FROM orders;
```

Вернет 6. А:

```SQL
SELECT COUNT(DISTINCT user_id)
FROM orders;
```

Вернет 3, потому что он считает только количество уникальных.

## 13. NULL

Так `NULL` проверять нельзя:

```SQL
WHERE price = NULL
```

Надо:

```SQL
WHERE price IS NULL
```

## 14. Агрегаты и NULL

Большинство агрегатных функций игнориуют `NULL`.

- SUM
- AVG
- MIN
- MAX

## 15. JOIN

Пусть есть две таблицы:

**users**

| user_id | name  |
| ------: | ----- |
|       1 | Анна  |
|       2 | Борис |
|       3 | Катя  |

**orders**

| order_id | user_id | price |
| -------: | ------: | ----: |
|      101 |       1 |   500 |
|      102 |       1 |   300 |
|      103 |       2 |   700 |
|      104 |       4 |   200 |

Мы хотим получить:

| name  | price |
| ----- | ----: |
| Анна  |   500 |
| Анна  |   300 |
| Борис |   700 |

```SQL
SELECT users.name, orders.price
FROM users
JOIN orders
    ON users.user_id = orders.user_id;
```

```python
users.merge(orders, on="user_id")[["name", "price"]]
```

## 16. INNER JOIN

Он оставляет **только совпавшие строки**.

```SQL
SELECT users.name, orders.price
FROM users
INNER JOIN orders
    ON users.user_id = orders.user_id;
```

Работает как:

```python
users.merge(orders, on="user_id", how="inner")[["name", "price"]]
```

> JOIN работает как INNER JOIN.

## 17. LEFT JOIN

Сохраняем **все строки из левой таблицы**, даже если соответствия справа нет.

```SQL
SELECT users.name, orders.price
FROM users
LEFT JOIN orders
    ON users.user_id = orders.user_id;
```

Получим:

| name  | price |
| ----- | ----: |
| Анна  |   500 |
| Анна  |   300 |
| Борис |   700 |
| Катя  |  NULL |

Работает как:

```python
users.merge(orders, on="user_id", how="left")[["name", "price"]]
```

## 18. RIGHT / OUTER JOIN

Работают как `right` и `outer` в `pandas`.

## 19. Оконные функции - что?

Раньше мы использовали `GROUP BY`.

К примеру:

```SQL
SELECT user_id, AVG(price)
FROM orders
GROUP BY user_id;
```

Было:

user_id | price
1 | 100
1 | 300
1 | 500
2 | 200
2 | 700

Получали:

user_id | avg
1 | 300
2 | 450

А оконная функция позволяет посчитать что-то **внутри группы, но при этом сохранить исходные строки**.

Пусть:

| user_id | event_time |
| ------- | ---------- |
| 1       | 10:00      |
| 1       | 12:00      |
| 1       | 15:00      |
| 2       | 09:00      |
| 2       | 11:00      |

Мы можем присвоить каждому событию номер:

| user_id | event_time | номер |
| ------- | ---------- | ----- |
| 1       | 10:00      | 3     |
| 1       | 12:00      | 2     |
| 1       | 15:00      | 1     |
| 2       | 09:00      | 2     |
| 2       | 11:00      | 1     |

И потом оставить только номер `1`.

## 20. ROW_NUMBER()

Синтаксис:

```SQL
ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY event_time DESC
)
```

- `ROW_NUMBER()` - пронумеруй строки: 1, 2, 3...
- `OVER (...)` - говорит, **по какому окну** это делать.
- `PARTITION BY user_id` - "для каждого пользователя отдельно".

То есть нумерация начинается заново:

```
user 1 : 1, 2, 3
user 2 : 1, 2
user 3 : 1, 2, 3, 4
...
```

- `ORDER BY event_time DESC` - сортируем по убыванию, то есть сначала самые новые события.

То есть нумеруем в каждой группке `user_id` отдельно, изолированно.

Таким образом:

```SQL
SELECT
    user_id,
    event_time.
    ROW_NUMBER() OVER (
        PARTITION BY user_id
        ORDER BY edvent_time DESC
    ) AS rn
FROM events;
```

Результат:

| user_id | event_time | rn  |
| ------- | ---------- | --- |
| 1       | 15:00      | 1   |
| 1       | 12:00      | 2   |
| 1       | 10:00      | 3   |
| 2       | 11:00      | 1   |
| 2       | 09:00      | 2   |

Работает как:

```python
df = df.sort_values("event_time", ascending=False)
df["rn"] = df.groupby("user_id").cumcount() + 1
```

## 21. Найти последнее событие

Допустим, мы хотим получить только `rn = 1`. Но оконную функцию нельзя просто так использовать в `WHERE` того же уровня запроса.

Делаем подразпрос:

```SQL
SELECT *
FROM (
    SELECT
        user_id,
        event_time,
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY event_time DESC
        ) AS rn
    FROM events
) t
WHERE rn = 1;
```

`t` это просто имя получившейся таблицы из внутреннего `SELECT`.

Получаем:

| user_id | event_time |
| ------- | ---------- |
| 1       | 15:00      |
| 2       | 11:00      |

Работает как:

```python
df = df.sort_values("event_time", ascending=False)
last_result = df.groupby("user_id").head(1)

# или

df = df.sort_values("event_time", ascending=False)
df["rn"] = df.groupby("user_id").cumcount() + 1
last_result = df[df["rn"] == 1]
```
