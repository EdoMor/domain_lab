import matplotlib.pyplot as plt
import numpy as np


class Hysteron():
    def __init__(self, function1, function2, drop1, drop2, starting_point):
        self.function1 = function1
        self.function2 = function2
        self.alpha = drop1
        self.beta = drop2
        self.last_value = starting_point  # delete
        if starting_point <= self.alpha:
            self.current_function = self.function1
        elif starting_point >= self.beta:
            self.current_function = self.function2
        else:
            self.current_function = function1  # TODO: add stabiliry check

    def __call__(self, x, *args, **kwargs):
        def calc(x):
            self.last_value = x
            if x <= self.alpha:
                self.current_function = self.function1
            elif x >= self.beta:
                self.current_function = self.function2
            return self.current_function(x)

        return np.array(list(map(calc, x)))

f=[]
for i in range(len(np.linspace(-5, 5, 10))):
    q = np.linspace(-5, 5, 10)
    f.append(Hysteron(lambda x: 0, lambda x: 1, q[i], q[i] + 1, 0))


def Hsum(F, x):
    y = 0
    for f in F:
        y = y+np.array(f(x))
    return y


x = list(np.linspace(-5, 5, 10))+list(np.linspace(5, -5, 10))
plt.plot(x,f[5](x))
plt.show()
