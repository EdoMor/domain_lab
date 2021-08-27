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




