import sys,os
sys.path.append("mpldatacursor")
sys.path.append("mpldatacursor/mpldatacursor")
import matplotlib.pyplot as plt
import numpy as np
from mpldatacursor import datacursor

x1, y1 = np.random.random((2, 5))
x2, y2 = np.random.random((2, 5))

fig, ax = plt.subplots()
ax.plot(x1, y1, 'ro', markersize=12, label='Series A')
ax.plot(x2, y2, 'bo', markersize=12, label='Series B')
ax.legend()

datacursor()
plt.show()
