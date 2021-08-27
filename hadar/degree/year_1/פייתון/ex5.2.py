##ex5.2

n = 7
count = 0
while count < 3:
    i = 1
    divider = []
    while i < n:
        if not n % i:
            divider.append(i)
        i += 1
    if sum(divider) == n:
        print(n)
        count +=1
    n += 1

##================ RESTART: C:/Users/97250/Desktop/פייתון/ex5.2.py ===============
##28
##496
##8128
