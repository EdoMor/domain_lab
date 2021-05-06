import device as dev
import time
import numpy as np
import matplotlib.pyplot as plt


def main():
    t = np.arange(0, 2, 1 / 10)
    f = np.sin(2 * np.pi * t) + 1.2
    # plt.plot(t,f,'.')
    # plt.show()
    with dev.Device(0) as pps:
        print(pps.id)
        pps.scope_on(0.005)
        pps.toggel_scorce()
        print('done')
        pps.scope_off()
        # pps.set_fn(f, t)



if __name__ == '__main__':
    main()
