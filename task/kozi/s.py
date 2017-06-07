import csv
import sys
import os
series = 1
numberoftasks = 3
taskname = ['a','b','c']
numberoftasks = len(taskname)
kritval = [40,20,40,40,60,40,60]
krit = ['donepoints','posspoints','trivp','angen','annach','anz','anmath','arggen','argnach','argri']


def getpartis():
    partilist = []
    with open("participants/partiname.txt",'r') as f:
        for line in f:
            partilist.append(line.split())
    te = []
    for i in range(0,len(partilist)-1,2):
        te.append([partilist[i][0],int(partilist[i+1][0])])
    return te

def readpartdata(part):
    data = []
    f = open("participants/csv/"+part+".csv",'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    finally:
        f.close()
    return data

def getpersonaldata(partlist): #pers daten
    personal = []
    personal.append(partlist[0][1]) #partcode
    personal.append(partlist[1][1]) #partname
    return personal


def getoverallpoints(partlist): #insgesamte punktzahl
    overallpos = 0
    overallgain = 0
    for i in range(3,len(partlist),1):
        overallpos = overallpos + int(partlist[i][2]) #poss punkte, am anfang der liste
        overallgain = overallgain +float(partlist[i][11]) #erreichte punkte, am ende der liste

    return [round(overallgain,3),overallpos]


def findposofcurrentseries(partlist,sn): #findet position der aktuellen serie
    notfound = True
    pos = 2
    while notfound:
        pos = pos + 1
        if int(partlist[pos][0]) == sn:
            notfound = False
    return pos

def getseriespoints(partlist,sn,numberoft):
    pos = findposofcurrentseries(partlist,sn)
    seriespos  = 0
    seriesgain = 0
    for i in range(pos,pos+numberoft,1):
        seriespos = seriespos + int(partlist[i][2])
        seriesgain = seriesgain + float(partlist[i][11])
    return [round(seriesgain,3),seriespos]
        

def gettaskvalues(tasklist):
    taskpoints = [round(float(tasklist[11]),3),float(tasklist[2]),100*(1-float(tasklist[10]))] #gained,pos,triv
    for i in range(0,len(kritval),1):
        taskpoints.append(round(float(tasklist[i+3])*kritval[i],4))
    return taskpoints

def makepartdata(partlist,sn,numberoft):
    l = []
    l.append(getpersonaldata(partlist))
    l.append(getoverallpoints(partlist))
    l.append(getseriespoints(partlist,sn,numberoft))
    seriespos = findposofcurrentseries(partlist,sn)
    t = []
    for i in range(seriespos,seriespos+numberoft,1):
        t.append(gettaskvalues(partlist[i]))
    l.append(t)
    return l
                
def makedoc():
    with open('participants/pre.txt','r') as myfile:
        pream = myfile.read()
    with open('results.tex','w') as myfile:
        myfile.write(pream)

def makeheader(partlist,sn,numberoft):
    with open("participants/parti.txt",'r') as f:
        header = f.read()
    header = header.replace('series',str(sn))
    header = header.replace('partiname',partlist[0][1])
    header = header.replace('partcode',partlist[0][0])
    header = header.replace('seg',str(partlist[1][0]))
    header = header.replace('sep',str(partlist[1][1]))
    header = header.replace('allg',str(partlist[2][0]))
    header = header.replace('allp',str(partlist[2][1]))
    with open('results.tex','a') as myfile:
        myfile.write(header)
def maketable(partlist):
    res = partlist[3]   #alle punkte sind im letzten teil gespeichert
    for i in range(0,len(res),1): #iteration over all tasks
        with open("participants/table.txt","r") as f:
            tabled = f.read()
        tabled = tabled.replace('taskid',str(i+1))
        tabled = tabled.replace('taskname',taskname[i])
        for j in range(0,len(krit),1):
            tabled = tabled.replace(krit[j],str(res[i][j]))
        with open('results.tex','a') as myfile:
            myfile.write(tabled)



data = []
with open('data.txt','r') as f:
    for line in f:
        data.append(line.split())
        
series = int(data[0][0])
taskname = []
for i in range(1,len(data),1):
    cu = ''
    for j in range(0,len(data[i]),1):
        cu = cu+data[i][j]
        if j!= len(data[i])-1:
            cu = cu+ ' '
    taskname.append(cu)
numberoftasks = len(taskname)
schools = getpartis()
makedoc()
for currentschool in range(0,len(schools),1):
    for currentstudent in range(0,schools[currentschool][1],1):
        party = readpartdata(schools[currentschool][0]+str(currentstudent+1))
        party = makepartdata(party,series,numberoftasks)
        makeheader(party,series,numberoftasks)
        maketable(party)
        if currentschool != len(schools) and currentstudent!=schools[currentschool][1]:
            with open('results.tex','a') as myfile:
                myfile.write('\clearpage')
with open('results.tex','a') as myfile:
    myfile.write('\end{document}')
os.system("pdflatex results.tex")
print 'done'
        
    
