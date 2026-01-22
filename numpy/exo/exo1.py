import numpy as np

# 1
mat7 = 7 * np.ones((3, 3))
print(mat7)

# 2
matRand = np.random.rand(3, 3)
print(matRand)

# 3
arr = np.arange(0, 10)
print(f"{arr[3:8] = }")

# 4
matArange = np.arange(9).reshape(3, 3)
print(f"{matArange = }")
print(f"{matArange[:, -1] = }")

# 5
print(np.random.rand(1, 10).mean())

# 6
print(np.random.rand(4, 3).sum(axis=0))
