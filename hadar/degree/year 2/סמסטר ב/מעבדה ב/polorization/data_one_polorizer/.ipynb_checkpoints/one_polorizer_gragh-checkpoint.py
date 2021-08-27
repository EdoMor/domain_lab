import numpy as np
import pandas as pd
import openpyxl
from matplotlib import pyplot as plt
import pathlib

Load_I0 = pd.read_excel(r'C:\Users\97250\Desktop\LAB_B2\polorization\data_one_polorizer\m00.xlsx')
I0_np = np.array(Load_I0)
I0 = I0_np[6:, 1]
# I0_time = I0_np[6:, 0]
# plt.plot(I0_time, I0)
Mean_I0 = I0.mean()
# print(Mean_I0)

intensity = []
time = []
for i in range(2, 18):
    path = str(pathlib.Path().absolute()) + r'\m' + f'{i}.xlsx'
    data = np.array(pd.read_excel(path))
    intensity.append(data[6:, 1].transpose())
    time.append(data[6:, 0].transpose())
# print(intensity)

# see the data visually:
# for i in range(16):
#     plt.plot(time[i], intensity[i])
#     plt.show()

Mean_intensity = []
for i in intensity:
    Mean_intensity.append(i.mean())
# print(Mean_intensity)

Angle = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
                  100, 110, 120, 130, 155, 180]) * np.pi / 180
# print([1, 2] * 2)

plt.scatter(Angle, Mean_intensity)
plt.show()
