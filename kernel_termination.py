import numpy as np
from sklearn.decomposition import PCA


def kernel1():
    kernel1 = np.zeros([84, 138])

    # horizontal (24x)
    for row in range(6):
        for col in range(4):
            for i in range(4):
                kernel1[2 * (col + i) + (14 * row), col + 4 * row] = 2
                kernel1[2 * (col + i) + (14 * row) + 1, 69 + col + 4 * row] = 2

    # vertical (21x)
    for row in range(3):
        for col in range(7):
            for i in range(4):
                kernel1[2 * col + 14 * (row + i), 24 + col + 7 * row] = 2
                kernel1[2 * col + 14 * (row + i) + 1, 24 + 69 + col + 7 * row] = 2

    # diagonal (12x)
    for row in range(3):
        for col in range(4):
            for i in range(4):
                kernel1[2 * (col + i) + 14 * (row + i), 45 + col + 4 * row] = 2
                kernel1[2 * (col + i) + 14 * (row + i) + 1, 45 + 69 + col + 4 * row] = 2

    # diagonal (12x)
    for row in range(3):
        for col in range(4):
            for i in range(4):
                kernel1[2 * (col + 3 - i) + 14 * (row + i), 57 + col + 4 * row] = 2
                kernel1[2 * (col + 3 - i) + 14 * (row + i) + 1, 57 + 69 + col + 4 * row] = 2

    return kernel1

def kernel1_horizontal():
    kernel1 = np.zeros([84, 24])

    # horizontal (24x)
    for row in range(6):
        for col in range(4):
            for i in range(4):
                kernel1[2 * (col + i) + (14 * row), col + 4 * row] = 2
                # kernel1[2 * (col + i) + (14 * row) + 1, 24 + col + 4 * row] = 2

    return kernel1


X = np.transpose(kernel1_horizontal())
print(X.shape)
print(X)
pca = PCA(n_components=24)
pca.fit(X)
print(pca.explained_variance_ratio_)
#[0.9924... 0.0075...]
print(pca.singular_values_)
#[6.30061... 0.54980...]
print("transform X")
print(pca.transform(X))

