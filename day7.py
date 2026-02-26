import numpy as np

a = np.arange(12)

b= np.reshape(a,(4,3))

c = np.reshape(a,(3,4))

d = np.reshape(a,(4,-1))
print("a",a)
print("b",b)
print("c:",c)
print("d(-1,自动计算维度值):",d)
