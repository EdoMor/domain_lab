def excell_stud(filename,n,newfile):
    f = open(filename,'r')
    d = {}
    for s in f:
        split = s.split('~')
        student = tuple(split[0:3])
        grade = split[4]
        if student in d and int(grade) >= 85:
            d[student] +=1
        elif student not in d and int(grade) >= 85:
            d[student] = 1
    es = []
    for k in d:
        if int(d[k]) >= n:
            es.append(k)
    g = open(newfile,'w')
    print(es,file=g)


# excell_stud("C:\\Users\\97250\\Desktop\\פייתון\\ex11\\studsFull.txt",3,"C:\\Users\\97250\\Desktop\\פייתון\\ex11\\newfile.txt")

def popular_course(filename):
    f = open(filename, 'r')
    d = {}
    for s in f:
        split = s.split('~')
        course = split[3]
        if course in d:
            d[course] += 1
        else:
            d[course] = 1

    # keys = list(d.keys())
    # max = d[keys[0]]
    # maxcourse = keys[0]
    # min = d[keys[0]]
    # mincourse = keys[0]
    # for k in range(1,len(d)):
    #     if d[keys[k]] > max:
    #         max = d[keys[k]]
    #         maxcourse =keys[k]
    #     elif d[keys[k]] < min:
    #         min = d[keys[k]]
    #         mincourse = keys[k]
    # print('the most popular course is: ',maxcourse,'. it has ',max,'students' )
    # print('the most unpopular course is: ',mincourse,'. it has ',min,'students' )

    maxcourse = []
    mincource = []
    for k , v in d.items():
        if v == max(list(d.values())):
            maxcourse.append(k)
        elif v == min(list(d.values)):
            mincource.append(k)
    print('the most popular courses are: ',maxcourse,'. it has ',max(list(d.values())),'students' )
    print('the most unpopular courses are: ',mincource,'. it has ',min(list(d.values())),'students' )



