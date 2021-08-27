##ex6.2

lst = eval(input("enter the list: "))
friends = []
for n in lst:
    friends.append(n[0])

range1 = range(len(friends))
flag = 1
count = []
for m in friends:
    if m == 0:
        continue
    for k in range1:
        if k == friends.index(m):
            continue
        if friends[k] == m:
            flag += 1
            friends[k] = 0
    else:
        count.append(flag)
        flag = 1

j = 0
while j < len(friends):
    while j < len(friends) and friends[j] == 0:
        del friends[j]
    j += 1

for i in range(len(friends)):
    print(friends[i],'-', count[i],'times')

day = []
for n in lst:
    day.append(n[1][0])

flag1 = 0
flag2 = 0
flag3 = 0
for s in day:
    if 1 <= s <= 10:
        flag1 +=  1
    elif 11 <= s <= 20:
        flag2 +=  1
    elif 21 <= s <= 31:
        flag3 += 1
day_count = [flag1, flag2, flag3]
print('Third of the month with most visits:', day_count.index(max(day_count))+1)

# C:\Users\97250\PycharmProjects\ex1\venv\Scripts\python.exe C:/Users/97250/Desktop/פייתון/ex6.2.py
# enter the list: [["moshe",(11,3,2017)],["yair",(22,11,1017)],["haim",(10,6,2017)],["hilel",(3,4,2017)],["moshe",(11,4,2017)],["hilel",(23,8,2017)],["moshe",(22,9,2017)],["moshe",(31,1,2017)]]
# moshe - 4 times
# yair - 1 times
# haim - 1 times
# hilel - 2 times
# Third of the month with most visits: 3












