from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    fbeta_score
)

import pandas as pd

y_true = [
    1, 1, 1, 1, 1,
    0, 0, 0, 0, 0
]

y_pred = [
    1, 1, 0, 1, 0,
    1, 0, 0, 0, 0
]

# TP = 3
# TN = 4
# FP = 1
# FN = 2

print(confusion_matrix(y_true, y_pred))

df = pd.DataFrame({
    "user": ["A", "B", "C"],
    "price": [100, 200, 300]
})

print(df["price"])