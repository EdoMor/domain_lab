import device
import device as dev
import time
import numpy as np
import matplotlib.pyplot as plt
from process_image import get_B_H_point


def main():
    with device.Device(0) as pps:
        print(pps.id)
        pps.set_voltage(-1.1)
        print(pps.get_voltage())
        t = np.arange(0, 1, 0.1)
        f = 3*np.sin(t)
        pps.set_fn(f,t,get_B_H_point)


if __name__ == '__main__':
    main()
