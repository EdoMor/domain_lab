import pyvisa
import time
import numpy as np
import threading


class Device:
    def __init__(self, idx=None, min_volt=-6, max_volt=6):
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
        self.t.join()
        try:
            self.resource.write('OUTPUT OFF')
            self.resource.query('SYSTem:LOCal')
        except pyvisa.errors.VisaIOError:
            pass
        self.rm.close()

    def threaded(fn):
        def wrapper(self, dt):
            self.t = threading.Thread(target=fn, args=(self, dt,)).start()
        return wrapper

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
        return self.resource.query('MEASURE:VOLTAGE?')

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

    def set_fn(self, function: np.array, t: np.array):  # TODO: add surge protect

        self.set_voltage(function[0])
        for i in range(1, len(function[1:])):
            time.sleep(float(t[i] - t[i - 1]))
            self.set_voltage(function[i])  # TODO: add handling for failure of set_voltage in a function

    @threaded
    def scope(self, dt):
        t = 0
        while True:
            print(t, self.get_voltage())
            t += dt
            time.sleep(dt)

    def command_status(self):
        '''

        :return: returns 1 if all operations are done
        '''
        return self.resource.query('*OPC?')

    def reset(self):
        self.resource.query('*RST')
