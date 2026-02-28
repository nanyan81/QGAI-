import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fig = plt.figure() # 创建了一个没有轴的画布

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

ax = fig.add_subplot(121)

x = np.linspace(0,10,100)
ax.plot(x,np.sin(x),label='sin(x)')
ax.set_title('正弦曲线')
ax.legend()

ax1 = fig.add_subplot(122)

x1 = np.linspace(0,10,100)
ax1.plot(x1,np.cos(x1),label='cos(x)')
ax1.set_title('余弦曲线')
ax1.legend()

plt.show()



