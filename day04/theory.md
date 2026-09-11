# SQL

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
