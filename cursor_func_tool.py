from matplotlib.widgets import Cursor
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector

# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots(figsize=(8, 6))

x, y = 4*(np.random.rand(2, 100) - .5)
ax.plot(x, y, 'o')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

cursor = Cursor(ax, useblit=True, color='red', linewidth=2)


def onselect(verts):
    global f
    f = (list(zip(*verts))[0])


lasso = LassoSelector(ax, onselect)

plt.show()
plt.plot(f)
plt.show()