from math import tan, atan
import numpy as np

img = np.array([[0, 5,10], [50, 230,211]])
b = lambda x: 1 if x>=128 else 0
b_v = np.vectorize(b)
res = b_v(img).astype(np.uint8)


print(list(reversed(range(10))))
