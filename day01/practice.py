from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

data = [
    {"age": 18, "income": 25000, "bought": 0},
    {"age": 21, "income": 32000, "bought": 0},
    {"age": 25, "income": 45000, "bought": 1},
    {"age": 28, "income": 52000, "bought": 1},
    {"age": 32, "income": 60000, "bought": 1},
    {"age": 35, "income": 70000, "bought": 1},
    {"age": 40, "income": 80000, "bought": 1},
    {"age": 45, "income": 90000, "bought": 1},
    {"age": 50, "income": 95000, "bought": 1},
    {"age": 55, "income": 110000, "bought": 1},
    {"age": 19, "income": 28000, "bought": 0},
    {"age": 23, "income": 35000, "bought": 0},
    {"age": 27, "income": 40000, "bought": 1},
    {"age": 31, "income": 48000, "bought": 1},
    {"age": 37, "income": 55000, "bought": 1},
    {"age": 42, "income": 65000, "bought": 1},
    {"age": 48, "income": 72000, "bought": 1},
    {"age": 52, "income": 85000, "bought": 1},
    {"age": 22, "income": 60000, "bought": 1},
    {"age": 60, "income": 30000, "bought": 0},
]

# Наша задача:

# создать небольшой dataset;
# разделить его на train/test;
# обучить модель;
# сделать predictions;
# посчитать accuracy.

X = [[elem["age"], elem["income"]] for elem in data]
y = [elem["bought"] for elem in data]

X_train, X_test, y_train, y_test = train_test_split(X, y)
model = DecisionTreeClassifier(max_depth=100)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(accuracy)