import device as dev
import time
import numpy as np
import matplotlib.pyplot as plt
from process_image import get_B_H_point


def main():
    t = np.arange(0, 2, 1 / 10)
    f = np.sin(2 * np.pi * t) + 1.2
    plt.plot(t, f, '.')
    plt.show()
    # with dev.Device(0) as pps:
    #     print(pps.id)
    #     pps.toggel_scorce()
    #     pps.scope = True
    #     hv ,tv= pps.set_fn(f, t, get_B_H_point, (0,))
    #     print('hv:\n\n', hv)
    #     print('hv:\n\n', tv)


if __name__ == '__main__':
    main()
