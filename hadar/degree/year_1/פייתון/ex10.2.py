##ex10.2

##Ex1

def get_penta_num(n):
    return n*(3*n -1)/2

l = 0
for i in range(1,101):
    print('%4d' % get_penta_num(i), end=' ')
    l +=1
    if  not l % 10:
        print()

##=============== RESTART: C:\Users\97250\Desktop\פייתון\ex10.2.py ===============
##   1    5   12   22   35   51   70   92  117  145 
## 176  210  247  287  330  376  425  477  532  590 
## 651  715  782  852  925 1001 1080 1162 1247 1335 
##1426 1520 1617 1717 1820 1926 2035 2147 2262 2380 
##2501 2625 2752 2882 3015 3151 3290 3432 3577 3725 
##3876 4030 4187 4347 4510 4676 4845 5017 5192 5370 
##5551 5735 5922 6112 6305 6501 6700 6902 7107 7315 
##7526 7740 7957 8177 8400 8626 8855 9087 9322 9560 
##9801 10045 10292 10542 10795 11051 11310 11572 11837 12105 
##12376 12650 12927 13207 13490 13776 14065 14357 14652 14950 
##


##Ex2

def sumDigits(n):
    digits = list(str(n))
    for i in range(len(digits)):
        digits[i] = int(digits[i])
    return sum(digits)

n = int(input('enter an integer: '))
print('The sum of the digits: ',sumDigits(n))


##=============== RESTART: C:\Users\97250\Desktop\פייתון\ex10.2.py =============== 
##enter an integer: 234
##The sum of the digits:  9
##
##=============== RESTART: C:\Users\97250\Desktop\פייתון\ex10.2.py =============== 
##enter an integer: 5913
##The sum of the digits:  18

##Ex3

def reverse(n):
    digits = list(str(n))
    reverse = []
    for i in range(1,len(digits)+1):
        reverse.append(digits[-i])
    return int(''.join(reverse))

# >>> reverse(234)
# 432
# >>> reverse(93628)
# 82639




