import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score, adjusted_rand_score, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 推荐
plt.rcParams['axes.unicode_minus'] = False
# =========================
# 1. 读取数据
# =========================
df = pd.read_csv("Iris.csv")

# 删除Id列
df = df.drop(columns=["Id"])

# 特征
X = df[[
    "SepalLengthCm",
    "SepalWidthCm",
    "PetalLengthCm",
    "PetalWidthCm"
]]

# 标签
y_true = df["Species"]

# =========================
# 2. 标签编码（解决混淆矩阵问题）
# =========================
le = LabelEncoder()
y_true_encoded = le.fit_transform(y_true)

# =========================
# 3. 标准化
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# 4. 肘部法选择K（加分点）
# =========================
inertia = []
K_range = range(1, 10)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# 画图
plt.figure()
plt.plot(K_range, inertia, marker='o')
plt.xlabel("K值")
plt.ylabel("Inertia")
plt.title("肘部法则")
plt.show()

# =========================
# 5. KMeans聚类（K=3）
# =========================
kmeans = KMeans(n_clusters=3, random_state=42)
y_pred = kmeans.fit_predict(X_scaled)

# =========================
# 6. 模型评估
# =========================
sil_score = silhouette_score(X_scaled, y_pred)
ari_score = adjusted_rand_score(y_true_encoded, y_pred)
cm = confusion_matrix(y_true_encoded, y_pred)

print("====== 模型评估 ======")
print("轮廓系数:", sil_score)
print("ARI:", ari_score)
print("混淆矩阵:\n", cm)

# =========================
# 7. PCA降维可视化（强力加分）
# =========================
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure()
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_pred)
plt.title("KMeans聚类结果（PCA降维）")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

# =========================
# 8. 导出结果
# =========================
df["Cluster"] = y_pred
df.to_csv("Iris_KMeans_Result.csv", index=False)

print("结果已导出：Iris_KMeans_Result.csv")

# =========================
# 9. 标签对应关系（解释用）
# =========================
print("真实标签编码对应关系：")
for i, label in enumerate(le.classes_):
    print(f"{i} -> {label}")