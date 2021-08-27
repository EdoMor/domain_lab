##ex10.1

def is_prime(n):
    if n==2:
        return True
    else:
        if n % 2 == 0:
            return False
        else:
            for p in range(3, int(n ** 0.5) + 1, 2):
                if not n % p:
                    return False
            else:
                return True

def prime_sum(n):
    for i in range(2,n//2 + 1):
        if is_prime(i) and is_prime(n-i):
            return [i , n-i]

a,b = eval(input("enter 2 different natural numbers larger than 2: "))
for k in range(a,b):
    if not k % 2:
        print(k ,'=', prime_sum(k)[0], '+', prime_sum(k)[1])


##===================================================== RESTART: C:\Users\97250\Desktop\פייתון\ex10.1.py =====================================================
##enter 2 different natural numbers larger than 2: 1000,1100
##1000 = 3 + 997
##1002 = 5 + 997
##1004 = 7 + 997
##1006 = 23 + 983
##1008 = 11 + 997
##1010 = 13 + 997
##1012 = 3 + 1009
##1014 = 5 + 1009
##1016 = 3 + 1013
##1018 = 5 + 1013
##1020 = 7 + 1013
##1022 = 3 + 1019
##1024 = 3 + 1021
##1026 = 5 + 1021
##1028 = 7 + 1021
##1030 = 11 + 1019
##1032 = 11 + 1021
##1034 = 3 + 1031
##1036 = 3 + 1033
##1038 = 5 + 1033
##1040 = 7 + 1033
##1042 = 3 + 1039
##1044 = 5 + 1039
##1046 = 7 + 1039
##1048 = 17 + 1031
##1050 = 11 + 1039
##1052 = 3 + 1049
##1054 = 3 + 1051
##1056 = 5 + 1051
##1058 = 7 + 1051
##1060 = 11 + 1049
##1062 = 11 + 1051
##1064 = 3 + 1061
##1066 = 3 + 1063
##1068 = 5 + 1063
##1070 = 7 + 1063
##1072 = 3 + 1069
##1074 = 5 + 1069
##1076 = 7 + 1069
##1078 = 17 + 1061
##1080 = 11 + 1069
##1082 = 13 + 1069
##1084 = 23 + 1061
##1086 = 17 + 1069
##1088 = 19 + 1069
##1090 = 3 + 1087
##1092 = 5 + 1087
##1094 = 3 + 1091
##1096 = 3 + 1093
##1098 = 5 + 1093








