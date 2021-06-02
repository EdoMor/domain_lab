import pyvisa
import time
import numpy as np
import threading
import matplotlib.pyplot as plt
from matplotlib import animation
import types
import process_image
import constants

class Device:
    def __init__(self, idx=None, min_volt=-6, max_volt=6):
        self.min_volt=min_volt
        self.max_volt=max_volt
        self.scope = False
        self.rm = pyvisa.ResourceManager()
        if idx == None:
            for i in range(len(self.rm.list_resources())):
                print(str(i) + ')\t' + self.rm.list_resources()[i])
            idx = int(input('choose device: '))
        try:
            self.address = self.rm.list_resources()[idx]
        except pyvisa.errors.VisaIOError:
            raise RuntimeError("device not detected make sure it's actually connected this time")
        self.resource = self.rm.open_resource(self.address)
        self.resource.timeout = 10000
        self.resource.read_termination = '\n'
        self.resource.write_termination = '\n'
        self.id = self.resource.query('*IDN?')
        self.scorce = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.resource.write('OUTPUT OFF')
        # self.resource.query('SYStem:LOCal')
        # print(self.resource.query('SYStem:ERRor?'))
        self.rm.close()

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
        # self.resource.write('*WAI')
        return float(self.resource.query('APPLY?').replace('"','').split(',')[-1].lower())

    def set_voltage(self, voltage):
        '''

        :param voltage: target voltage (in volts)
        :return: 0 if command was successful and otherwise 1
        '''
        try:
            self.resource.write('*WAI')
            self.resource.write('APPLy:DC DEF, DEF, {} V'.format(voltage))
            return 0
        except:
            raise RuntimeError('unable to set voltage')

    def set_fn(self, function: np.array, t: np.array, hook=None, args=None):  # TODO: add surge protect
        process_image.incument_run(constants.ROOT,constants.RUNFILE)
        hook_values = []
        tv_values=[]
        start = time.time()
        def hooks():
            # if hook != None:
            #     if args != None:
            #         try:
            #             a=self.get_voltage()
            #             hook_values.append(hook(a)) #TODO: reconnecto args!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #         except:
            #             raise NameError('broken function in device.py line 82 go in there and change variable "a" back to "*args" and figure out how to evaluate pps.get_vlotage() inside set_fn() ')
            #     else:
            #         hook_values.append(hook())  # TODO: add filesave option
            if hook!=None:#                                ^
                a=[0]*len(args)#                           |
                for i in range(len(args)):#                |
                    if type(args[i])==types.MethodType:#   |
                        a[i]=args[i]()#                    |
                    else:#                                 |
                        a[i]=args[i]#                      |
            hook(*a)
            # hook_values.append(b)          #fix fot this | needs checking # stopped uppending need to remove line
            # !!!!!!!!!!!!!!!!!!!!!!!!!! removing line may break code !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for i in range(len(function)):
            self.set_voltage(function[i])  # TODO: add handling for failure of set_voltage in a function
            t, v = (time.time() - start, self.get_voltage())
            if self.scope == True:
                hooks()
                print(t, v)
                # tv_values.append((t,v))
                plt.plot(t, v, 'k.')
                plt.pause(0.001)
            else:
                hooks()
                print(t, v)
                # tv_values.append((t,v))
                time.sleep(0.001)
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
