##ex8.2

list1 = list(input("enter a string: "))
dict_letters = {}
for k in list1:
    letter = k
    if letter not in dict_letters:
        dict_letters[k] = 1
    else:
        dict_letters[k] += 1
print ('letter\tfrequency')

dict_keys = list(dict_letters.keys())
dict_keys.sort()

for i in dict_keys:
    print(i,'\t\t',dict_letters[i])


##============= RESTART: C:\Users\97250\Desktop\פייתון\ex8.1\ex8.2.py ============
##enter a string: "Some things in life are bad They can really make you mad Other things just make you swear and curse When you're chewing on life's gristle Don't grumble, give a whistle And this'll help things turn out for the best And Always look on the bright side Of life Always look on the light side Of life"
##letter	frequency
##  		 56
##" 		 2
##' 		 4
##, 		 1
##A 		 4
##D 		 1
##O 		 3
##S 		 1
##T 		 1
##W 		 1
##a 		 12
##b 		 4
##c 		 3
##d 		 7
##e 		 27
##f 		 7
##g 		 9
##h 		 15
##i 		 17
##j 		 1
##k 		 4
##l 		 17
##m 		 5
##n 		 15
##o 		 14
##p 		 1
##r 		 11
##s 		 15
##t 		 17
##u 		 8
##v 		 1
##w 		 5
##y 		 7
##>>> 
