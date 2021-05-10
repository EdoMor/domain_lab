import pyvisa
import time
import numpy as np
import threading
import matplotlib.pyplot as plt
from matplotlib import animation


class Device:
    def __init__(self, idx=None, min_volt=-6, max_volt=6):
        self.scope = False
        self.rm = pyvisa.ResourceManager()
        if idx == None:
            for i in range(len(self.rm.list_resources())):
                print(str(i) + ')\t' + self.rm.list_resources()[i])
            idx = int(input('choose device: '))
        self.address = self.rm.list_resources()[idx]
        self.resource = self.rm.open_resource(self.address)
        self.resource.timeout = 10000
        self.resource.read_termination = '\n'
        self.resource.write_termination = '\n'
        self.id = self.resource.query('*IDN?')
        self.scorce = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.t.join()
        try:
            self.resource.write('OUTPUT OFF')
            self.resource.query('SYSTem:LOCal')
        except pyvisa.errors.VisaIOError:
            pass
        self.rm.close()
        # time.sleep(5)
        # exit(0)

    # def threaded(fn):
    #     def wrapper(self, dt):
    #         self.t = threading.Thread(target=fn, args=(self, dt,)).start()
    #
    #     return wrapper

    # def scorce_status(self):
    #     status=
    #     return status

    def toggel_scorce(self):
        if self.scorce:
            self.resource.write('OUTPUT OFF')
            self.scorce = False
        else:
            self.resource.write('OUTPUT ON')
            self.scorce = True

    def get_voltage(self):
        '''

        :return: voltage measured at output
        '''
        self.resource.write('*WAI')
        return float(self.resource.query('MEASURE:VOLTAGE?'))

    def set_voltage(self, voltage):
        '''

        :param voltage: target voltage (in volts)
        :return: 0 if command was successful and otherwise 1
        '''
        try:
            self.resource.write('*WAI')
            self.resource.write('VOLTAGE {}V'.format(voltage))
            return 0
        except:
            raise RuntimeError('unable to set voltage')

    def set_fn(self, function: np.array, t: np.array, hook=None, args=None):  # TODO: add surge protect
        hook_values = []
        tv_values=[]
        start = time.time()
        def hooks():
            if hook != None:
                if args != None:
                    hook_values.append(hook(*args))
                else:
                    hook_values.append(hook())  # TODO: add filesave option
        for i in range(len(function)):
            self.set_voltage(function[i])  # TODO: add handling for failure of set_voltage in a function
            while True:
                t, v = (time.time() - start, self.get_voltage())
                if self.scope == True:
                    print(t, v)
                    tv_values.append((t,v))
                    plt.plot(t, v, 'k.')
                    hooks()
                    plt.pause(0.001)
                else:
                    print(t, v)
                    tv_values.append((t,v))
                    hooks()
                    time.sleep(0.001)

                if np.isclose(v, function[i], 1e-2):
                    break
        return hook_values,tv_values

    # @threaded
    # def scope(self, dt):
    #     t = 0
    #     while True:
    #         print(t, self.get_voltage())
    #         t += dt
    #         time.sleep(dt)

    def command_status(self):
        '''

        :return: returns 1 if all operations are done
        '''
        return self.resource.query('*OPC?')

    def reset(self):
        self.resource.query('*RST')
