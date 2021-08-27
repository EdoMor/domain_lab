
# q1
my_list = [[x, x**2, x**3]for x in range(1, 10, 2)]

# q2
L1, L2, L3 = eval(input('3 lists: '))
list1=[]
for x in L1:
    for y in L2:
        for z in L3:
            if x>y and x>z and y>2*z:
                list1.append([x,y,z])
print(list1)

# C:\Users\97250\Desktop\פייתון\ex12\venv\Scripts\python.exe C:/Users/97250/Desktop/פייתון/ex12/ex12.1.py
# # 3 lists: [8,11,12,13],[1,5,9],[4,8,10]
# # [[11, 9, 4], [12, 9, 4], [13, 9, 4]]

L1, L2, L3 = eval(input('3 lists: '))
list2=[[x,y,z]for x in L1 for y in L2 for z in L3 if x>y if x>z if y>2*z]

# L1, L2, L3 = eval(input('3 lists: '))
# 3 lists: [8,11,12,13],[1,5,9],[4,8,10]
# >>> list2=[[x,y,z]for x in L1 for y in L2 for z in L3 if x>y if x>z if y>2*z]
# >>> list2
# [[11, 9, 4], [12, 9, 4], [13, 9, 4]]

# q3
bases = ['U', 'C', 'A', 'G']
codons = [x+y+z for x in bases for y in bases for z in bases]

# >>> codons
# ['UUU', 'UUC', 'UUA', 'UUG', 'UCU', 'UCC', 'UCA', 'UCG', 'UAU', 'UAC', 'UAA', 'UAG', 'UGU', 'UGC', 'UGA', 'UGG', 'CUU', 'CUC', 'CUA', 'CUG', 'CCU', 'CCC', 'CCA', 'CCG', 'CAU', 'CAC', 'CAA', 'CAG', 'CGU', 'CGC', 'CGA', 'CGG', 'AUU', 'AUC', 'AUA', 'AUG', 'ACU', 'ACC', 'ACA', 'ACG', 'AAU', 'AAC', 'AAA', 'AAG', 'AGU', 'AGC', 'AGA', 'AGG', 'GUU', 'GUC', 'GUA', 'GUG', 'GCU', 'GCC', 'GCA', 'GCG', 'GAU', 'GAC', 'GAA', 'GAG', 'GGU', 'GGC', 'GGA', 'GGG']

# q4
trya = list({(x, y, z) for x in range(1, 30) for y in range(1, 30) for z in range(1, 30) if x**2 + y**2 == z**2 if x < y < z  })

# trya
# [(15, 20, 25), (12, 16, 20), (8, 15, 17), (9, 12, 15), (6, 8, 10), (7, 24, 25), (20, 21, 29), (10, 24, 26), (5, 12, 13), (3, 4, 5)]