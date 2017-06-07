import csv
import sys
series = 2
numberoftasks = 3
taskname = ["Eisenbahnwaggon","Linsenpositionen","gute Ampel"]
def readpart():
    templ = []
    with open("participants/partiname.txt",'r') as f:
        for line in f:
                templ.append(line.split())
    return templ
    
def readpartdata(part):
    data = []
    f = open("participants/"+part+".csv", 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
           data.append(row)
    finally:
        f.close()
    return data
def totalpoints(partlist):
    liste = partlist[1]
    pp = 0
    gp = 0
    for i in range(0,len(liste),1):
        pp = pp+float(liste[i][2])
        gp = gp+float(liste[i][9])
    return [gp,pp]

def makepartdata(partdata):
    partlist = []
    personallist = []
    personallist.append(partdata[1][1])#name
    personallist.append(partdata[0][1])#studentcode
    possiblepoints = 0
    gainedpoints = 0
    for i in range(3,len(partdata),1):
        possiblepoints = possiblepoints + float(partdata[i][2])
        gainedpoints = gainedpoints + float(partdata[i][9])
    personallist.append(possiblepoints)
    personallist.append(gainedpoints)
    partlist.append(personallist)
    pos = 3
    checker = True
    pointlist = []
    while checker:
        if int(partdata[pos][0])==series:
            checker = False
        else:
            pos = pos +1
    for i in range(pos,pos+numberoftasks,1):
        pointlist.append(partdata[i])
    partlist.append(pointlist)
    return partlist

def maketotalpoints(alldata):
    for i in range(0,len(alldata),1):
        alldata[i][0] = alldata[i][0] + totalpoints(alldata[i])
    return alldata
        
liste = readpart()
allist = []
for i in range(1,len(liste)/2+1,2):
    school = liste[i-1][0]
    print "i",i
    print school
    for j in range(0,int(liste[i][0]),1):
        print j
        print int(liste[i][0])
        print allist
        allist =allist+ [makepartdata(readpartdata(school+str(j+1)))]        



with open('participants/pre.txt', 'r') as myfile:
    pream =myfile.read()
allist = maketotalpoints(allist)
outstring = pream
eig = ['partiname','partcode','allg','allp','seg','sep']
krit = ["angen","annach","anz","anmath","arggen","argnach","argri"]
for i in range(0,len(allist),1):
    with open("participants/parti.txt",'r') as f:
        data = f.read()
    data = data.replace('series',str(series))
    for j in range(0,len(eig),1):
        data = data.replace(eig[j],str(allist[i][0][j]))
    for j in range(0,len(allist[i][1]),1):
        with open("participants/table.txt","r") as f:
            tabled = f.read()
        tabled = tabled.replace('taskid',str(j+1))
        tabled = tabled.replace('taskname',taskname[j])
        tabled = tabled.replace('posspoints', allist[i][1][j][1])
        tabled = tabled.replace('donepoints', allist[i][1][j][9])
        for k in range(0,len(krit),1):
            tabled = tabled.replace(krit[k],allist[i][1][j][k+2])
        data = data + tabled
    
    data = data+"\clearpage"
    pream = pream+data
pream = pream+"\end{document}"
with open("result.tex", 'w') as myfile:
    myfile.write(pream)
            
            
            
                                    
    
#with open("participants/table.txt", 'r') as myfile:
#    data=myfile.read()#.replace('\n', '')
#krit = ("angen","annach","anzi","anma","arggen","argnach","argri")
#points = (40,20,40,40,60,40,60)
#table = data
#for i in range(0,7,1):
#    data = data.replace(krit[i],points[i])
#out = pream+data
#with open("participants/result.tex", 'w') as myfile:
#    myfile.write(out)
