import device
import device as dev
import time
import numpy as np
import matplotlib.pyplot as plt
from process_image import get_H_B_point
from run_files import make_run_files


def sin4(x, a, b, c, d):
    return a * np.sin(b * x) + c * np.sin(d * x)

def multirun():
    with device.Device(0) as pps:
        print(pps.id)
        paramfam = []
        n = 5
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        a = np.arange(1, 5, 4 / n)[i]
                        c = np.arange(0, 1, 1 / n)[j]
                        b = np.arange(1, 1.5, 0.5 / n)[k]
                        d = np.arange(0, 30, 30 / n)[l]
                        paramfam.append([a, b, c, d])
        ccccc=0
        for params in paramfam:
            t = np.arange(0, 2 * np.pi, 0.1)
            f = sin4(t, *params)
        #     plt.plot(t,f)
        # plt.show()
        # print(len(paramfam))
            h, vt = pps.set_fn(f, t, get_H_B_point, [pps.get_voltage])
            fname = make_run_files()
            with open(fname + '/voltage points.txt', 'w') as fo:
                for i in vt:
                    fo.write(str(i) + '\n')
            print('done with run: ',ccccc)
            ccccc+=1
        pps.set_voltage(0)

def main():
    # t=np.arange(0,10,10)
    # plt.plot(t,sin4(t,5,1,1.5,100),'.')
    # plt.pause(0.001)
    # with device.Device(0) as pps:
        # print(pps.id)
        # f = sin4(t, *[5,1,1.5,100])
        # pps.set_fn(f, t, get_H_B_point, [pps.get_voltage])
    get_H_B_point()



if __name__ == '__main__':
    main()
