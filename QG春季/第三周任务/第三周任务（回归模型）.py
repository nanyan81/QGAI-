import numpy as np
import pandas as pd

# =========================
# 1. 读取数据 + 构造标签
# =========================
data = pd.read_csv("winequality-red.csv", sep=';')

# 新增分类标签：好酒=1，坏酒=0
data['good_bad'] = (data['quality'] > 6).astype(int)

print("数据预览：")
print(data[['quality', 'good_bad']].head())


# =========================
# 2. 特征与标签划分
# =========================
X = data.drop(columns=['quality', 'good_bad']).values
y_reg = data['quality'].values
y_clf = data['good_bad'].values


# =========================
# 3. 标准化
# =========================
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X = (X - X_mean) / X_std

# 加偏置项
X = np.hstack([np.ones((X.shape[0], 1)), X])


# =========================
# 4. 划分训练测试集
# =========================
def train_test_split(X, y, test_size=0.2):
    np.random.seed(42)
    idx = np.random.permutation(len(X))
    test_size = int(len(X) * test_size)

    test_idx = idx[:test_size]
    train_idx = idx[test_size:]

    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


X_train, X_test, y_train_reg, y_test_reg = train_test_split(X, y_reg)
_, _, y_train_clf, y_test_clf = train_test_split(X, y_clf)


# =========================
# 5. 线性回归（手写）
# =========================
class LinearRegression:
    def __init__(self, lr=0.01, epochs=1000):
        self.lr = lr
        self.epochs = epochs

    def fit(self, X, y):
        self.theta = np.zeros(X.shape[1])

        for _ in range(self.epochs):
            y_pred = X.dot(self.theta)
            grad = (1 / len(y)) * X.T.dot(y_pred - y)
            self.theta -= self.lr * grad

    def predict(self, X):
        return X.dot(self.theta)


# =========================
# 6. 逻辑回归（手写）
# =========================
class LogisticRegression:
    def __init__(self, lr=0.01, epochs=1000):
        self.lr = lr
        self.epochs = epochs

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        self.theta = np.zeros(X.shape[1])

        for _ in range(self.epochs):
            z = X.dot(self.theta)
            h = self.sigmoid(z)
            grad = (1 / len(y)) * X.T.dot(h - y)
            self.theta -= self.lr * grad

    def predict_proba(self, X):
        return self.sigmoid(X.dot(self.theta))

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)


# =========================
# 7. 模型训练
# =========================
lin_model = LinearRegression(lr=0.01, epochs=2000)
lin_model.fit(X_train, y_train_reg)

log_model = LogisticRegression(lr=0.01, epochs=2000)
log_model.fit(X_train, y_train_clf)


# =========================
# 8. 模型评估
# =========================

# ——线性回归评估——
y_pred_reg = lin_model.predict(X_test)

# MSE
mse = np.mean((y_pred_reg - y_test_reg) ** 2)

# R²
ss_total = np.sum((y_test_reg - np.mean(y_test_reg)) ** 2)
ss_res = np.sum((y_test_reg - y_pred_reg) ** 2)
r2 = 1 - ss_res / ss_total


# ——逻辑回归评估——
y_pred_clf = log_model.predict(X_test)

accuracy = np.mean(y_pred_clf == y_test_clf)

# 混淆矩阵
tp = np.sum((y_pred_clf == 1) & (y_test_clf == 1))
tn = np.sum((y_pred_clf == 0) & (y_test_clf == 0))
fp = np.sum((y_pred_clf == 1) & (y_test_clf == 0))
fn = np.sum((y_pred_clf == 0) & (y_test_clf == 1))


# =========================
# 9. 输出结果
# =========================
print("\n===== 线性回归 =====")
print("MSE:", mse)
print("R²:", r2)

print("\n===== 逻辑回归 =====")
print("Accuracy:", accuracy)

print("\n混淆矩阵：")
print(f"TP: {tp}, FP: {fp}")
print(f"FN: {fn}, TN: {tn}")

data.to_csv("winequality-red-with-label.csv", index=False, sep=';')
print("已导出新CSV文件：winequality-red-with-label.csv")