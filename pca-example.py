import numpy as np
from sklearn.decomposition import PCA
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
pca = PCA(n_components=2)
pca.fit(X)
print(pca.explained_variance_ratio_)
#[0.9924... 0.0075...]
print(pca.singular_values_)
#[6.30061... 0.54980...]
print("transform X")
print(pca.transform(X))

print("transform I")
print(pca.transform(np.eye(2)))

print("inverse transform I")
print(pca.inverse_transform(np.eye(2)))

V = pca.transform(np.eye(2))
U = pca.inverse_transform(np.eye(2))

print("V*U")
print(np.matmul(V, U))

print("X*V")
print(np.matmul(X, V))

print("X*V*U")
print(np.matmul(np.matmul(X, V),U))
