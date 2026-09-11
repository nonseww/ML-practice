# Pandas

## 1. Что такое Pandas

**Pandas** - библиотеки Python для работы с табличными данными.

Основные структуры:

- **DataFrame** - таблица целиком.
- **Series** - один столбец таблицы.

```python
import pandas as pd

df = df.DataFrame({
    "name": ["Anna", "Bob", "Kate"],
    "age": [20, 30, 40],
    "salary": [100, 200, 300]
})
```

## 2. Выбор столбца

```python
df["age"] # один столбец; Series
df[["name", "age"]] # несколько столбцов; DataFrame
```

## 3. Фильтрация строк

```python
df["age"] > 30 # условие, создает булеву Series False False Ture
df[df["age"] > 30] # фильтрация, будут только строки где age > 30
df[(df["age"] > 20) & (df["salary"] > 150)] # &, |, ~
```

## 4. loc

`loc` обращается к данным по **названиям** (labels) индексов и столбцов.

```python
df.loc[СТРОКА, СТОЛБЕЦ] # общий вид
df.loc[1, "salary"] # -> 200
df.loc[1] # -> строка под индексом 1
df.loc[:, "salary"] # столбец salary
```

### `loc` + условие

```python
df.loc[УСЛОВИЕ, СТОЛБЕЦ] # общий вид
df.loc[df["age"] > 30, "name"] # выберем строки где age > 30, затем из них возьмем name
df.loc[df["age"] > 30, ["name", "salary"]] # взять несколько столбцов
```

## 5. iloc

`iloc` обращается к данным по **числовой позиции**.

```python
df.iloc[1, 2] # строка 1, столбец 2
```

## 6. Срезы loc и iloc

```python
df.iloc[0:2] # берет позиции 0 и 1
df.loc[0:2] # берет 0, 1, 2
```

## 7. sort_values()

```python
df.sort_values("salary") # сортировка DataFrame по столбцу
# по умолчанию - по возрастанию
df.sort_values("salary", ascending=False) # по убыванию
df.sort_values(["age", "salary"]) # по нескольким столбцам
```

## 8. value_counts()

```python
df["city"].value_counts() # считает, сколько раз встречается каждое значение
df["city"].value_counts().idxmax() # самое частое значение
df["city"].value_counts().max() # максимальное количество
```

## 9. groupby()

`groupby()` объединяет строки в группы по определённому признаку.

```python
df.groupby("user")["price"].mean()
```

Логика:

`groupby("user")` - разбить данные по пользователям (группки с одинаковым "user")
`["price"]` - взять столбец "price"
`.mean()` - посчитать среднюю цену для каждого пользователя

Также можно юзать:

> `mean()`, `.sum()`, `.count()`, `.min()`, `.max()`

## 10. agg()

`agg()` позволяет считать сразу несколько статистик:

```python
df.groupby("user")["price"].agg(
    ["mean", "sum", "min", "max"]
) # посчитает все эти метрики
```

## 11. merge()

`merge()` используется, чтобы **соединить две таблицы по ключу**.

```python
users = pd.DataFrame({
    "user_id": [1, 2],
    "name": ["Anna", "Bob"]
})

orders = pd.DataFrame({
    "user_id": [1, 1, 2],
    "price": [100, 200, 300]
})

users.merge(orders, on="user_id") # соединить таблицы по столбцу user_id
```

## 12. Типы merge

### inner

```python
users.merge(orders, on="user_id", how="inner")
```

Оставляет только ключи, которые есть **в обеих таблицах**.

### left

```python
users.merge(orders, on="user_id", how="left")
```

Сохраняет **все строки левой таблицы**.
Если соответствия справа нет -> `NaN`.

### right

```python
users.merge(orders, on="user_id", how="right")
```

Сохраняет **все строки правой таблицы**.
Если соответствия слева нет -> `NaN`.

### outer

```python
users.merge(orders, on="user_id", how="outer")
```

Сохраняет все ключи из обеих таблиц. Если не пересекаются, то `NaN`.
