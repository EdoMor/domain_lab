# q5
def m(i):
    m = 0
    x = 1
    while x <= i:
        m += x/(x+1)
        x += 1
    return m

for i in range(1,7):
    print(i, '\t\t' , m(i))

# C:\Users\97250\Desktop\פייתון\mvhan\venv\Scripts\python.exe C:/Users/97250/Desktop/פייתון/mvhan/הכנה.py
# 1 		 0.5
# 2 		 1.1666666666666665
# 3 		 1.9166666666666665
# 4 		 2.716666666666667
# 5 		 3.5500000000000003
# 6 		 4.4071428571428575

# q6

def pi(i):
    pi = 0
    x = 1
    while x <= i:
        pi += 4*(((-1)**(x+1))/(2*x-1))
        x += 1
    return pi

print('i', '\t\t\t', 'pi(i)')
for i in range(1,1001,100):
    print(i, '\t\t\t', pi(i))

# i 			 pi(i)
# 1 			 4.0
# 101 			 3.1514934010709914
# 201 			 3.1465677471829556
# 301 			 3.1449149035588526
# 401 			 3.144086415298761
# 501 			 3.143588659585789
# 601 			 3.143256545948974
# 701 			 3.1430191863875865
# 801 			 3.142841092554028
# 901 			 3.1427025311614294

# q7
def babyl(n):
    last = 1
    lastGuess = 1
    nextGuess = 0
    while abs(nextGuess-last) > 10**(-4):
        nextGuess = (lastGuess + (n/lastGuess))/2
        last = lastGuess
        lastGuess = nextGuess
    return nextGuess

n = int(input('enter a positive integer: '))
print(babyl(n))

# enter a positive integer: 5
# 2.236067977499978
# enter a positive integer: 25
# 5.000000000053722

# q12
def adding_3dict(d1,d2,d3):
    D = dict()
    k1 = set(d1.keys)
    k2 = set(d2.keys)
    k3 = set(d3.keys)
    p12 = k1 & k2
    p23 = k2 & k3
    p31 = k3 & k1
    p123 = k1 & k2 & k3
    D1 = d1 | d2 | d3
    for k in k1 | k2 | k3:
        if k in p12 and k not in p123:
            D[k] = (d1[k],d2[k])
        elif k in p23 and k not in p123:
            D[k] = (d2[k],d3[k])
        elif k in p31 and k not in p123:
            D[k] = (d1[k],d3[k])
        elif k in p123:
            D[k] = (d1[k],d2[k],d3[k])
        elif k in k1:
            d









