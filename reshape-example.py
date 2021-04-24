import numpy as np

a = np.arange(84).reshape((42, 2))
print(a)
print(a[2,1])
print("ravel")
# print(np.ravel(a))
# print(a.reshape((3, 2)))
print(a.transpose().reshape((2, 6, 7)))