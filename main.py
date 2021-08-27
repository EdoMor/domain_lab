import random
import device
import device as dev
import time
import numpy as np
import matplotlib.pyplot as plt
from process_image import get_H_B_point2
from run_files import make_run_files


def main():
     with device.Device(0) as pps:
        print(pps.id)

        def g(x):
            return x

        steps = 1000
        max = 5
        t = np.concatenate((np.linspace(0, max, steps), np.linspace(max, -max, 2 * steps), np.linspace(-max, 0, steps),
                            np.linspace(0, max, steps), np.linspace(max, -max, 2 * steps), np.linspace(-max, 0, steps)))

        t=t[3158:]
        f=g(t)
        pps.set_fn(f, t, get_H_B_point2, [pps.get_voltage])
        print('done with the run')
        pps.set_voltage(0)


# def sin4(x):
#     return (5 * np.sin(x))
#
# def main():
#      with device.Device(0) as pps:
#         print(pps.id)
#         ccccc=0
#         for run in range(280):
#             jumps = np.array(random.sample(range(1,50000), 1000))/65000
#             t = [0]*1000
#             for i in range(999):
#                 t[i+1]=t[i]+jumps[i]
#             f = sin4(t)
#             pps.set_fn(f, t, get_H_B_point2, [pps.get_voltage])
#             print('done with run: ',ccccc)
#             ccccc+=1
#             pps.set_voltage(0)



# def sin4(x, a, b):
#     if max(a*np.sin(x)+b)>=4.1:
#         return 4.1*(a*np.sin(x)+b)/max((a*np.sin(x)+b))
#     if min(a*np.sin(x)+b)<=-4.1:
#         return 4.1 * (a * np.sin(x) + b) / abs(min((a * np.sin(x) + b)))
#     return (a * np.sin(x) + b)
#
# def multirun():
#     paramfam = [[4.1,0]]
#     for a in np.linspace(0.5,4.1,20):
#             for b in np.linspace(-4.1,4.1,20):
#                 paramfam.append([a, b])
#     # print(len(paramfam))
#     # for params in paramfam:
#     #     t = np.arange(0, 10 * np.pi, 0.1)
#     #     f = sin4(t, *params)
#     #     plt.plot(t, f, '.')
#     #     plt.ylim([-4.2,4.2])
#     #     plt.pause(0.001)
#     #     plt.clf()
#     # exit(0)
#     with device.Device(0) as pps:
#         print(pps.id)
#         ccccc=0
#         for params in paramfam[142:]:
#             t = np.arange(0, 10 * np.pi, 0.315)
#             f = sin4(t, *params)
#             pps.set_fn(f, t, get_H_B_point, [pps.get_voltage])
#             print('done with run: ',ccccc)
#             ccccc+=1
#         pps.set_voltage(0)
#
#
# def f_fam(x, p, b):
#     a = 4.1/(1+p)
#     return a*np.sin(x) + a*p*np.sin(b*x)
#
# def run():
#     p_range = np.arange(0, 1, 0.04)
#     b_range = np.arange(0, 50, 2)
#
#     with device.Device() as dw:
#         run_count = 0
#         for p in p_range:
#             for b in b_range:
#                 x = np.arange(0, 2.5 * np.pi, 2.5 * np.pi / (b * 10 + 100 / (b+1)))
#                 f = f_fam(x, p, b)
#                 dw.set_fn(f, x, get_H_B_point, [dw.get_voltage])
#                 print('done with run: ', run_count)
#                 run_count += 1
#         dw.set_voltage(0)
#
# def main():
#     ccccc=1
#     f = np.array(list(np.arange(0,2.5,0.01))+list(np.arange(2.5,-2.5,-0.01))+list(np.arange(-2.5,0,0.01)))
#     plt.plot(f,'.',markersize=0.2)
#     plt.show()
#     with device.Device(0) as pps:
#         pps.set_fn(f, f, get_H_B_point, [pps.get_voltage])
#         print('done with run: ', ccccc)
#         ccccc += 1
#         pps.set_voltage(0)



if __name__ == '__main__':
    main()

