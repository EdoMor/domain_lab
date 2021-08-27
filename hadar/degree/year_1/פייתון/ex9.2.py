##ex9.2

def same_vowels(s1,s2):
    vowels = ['a','e','i','o','u']
    vowels_s1 = []
    vowels_s2 = []
    for i in list(s1):
        if i in vowels:
            vowels_s1.append(i)
    for i in list(s2):
        if i in vowels:
            vowels_s2.append(i)
    if len(vowels_s2) != len(vowels_s1):
        return 'False'
    elif set(vowels_s1) != set(vowels_s2):
        return 'False'
    else:
        return 'True'


##================ RESTART: C:/Users/97250/Desktop/פייתון/ex9.2.py ===============
##>>> same_vowels('aabcefiok','xcexvcxaioa')
##'True'
##>>> same_vowels('aabcefiok','xcexvcxaioia')
##'False'




