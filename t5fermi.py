__author__ = 'Siddharth Kumar'
import re
import math

class GRB:

    def __init__(self,name,ra,dec):

        self.NAME = str(name)
        self.RA = float(ra)
        self.DEC = float(dec)


        #self.NAME = str(name)+' ('+str(self.RA)+','+str(self.DEC)+')' for debug

def HMS2deg(ra='', dec=''):

  RA, DEC, rs, ds = '', '', 1, 1

  if dec:
    D, M, S = [float(i) for i in dec.split()]
    if str(D)[0] == '-':
      ds, D = -1, abs(D)
    deg = D + (M/60) + (S/3600)
    DEC = '{0}'.format(deg*ds)

  if ra:
    H, M, S = [float(i) for i in ra.split()]
    if str(H)[0] == '-':
      rs, H = -1, abs(H)
    deg = (H*15) + (M/4) + (S/240)
    RA = '{0}'.format(deg*rs)

  if ra and dec:
    return [RA, DEC]
  else:
    return RA or DEC


fermi = open('FERMI_TABLE.txt','r')
t5 = open('t5.txt','r')

t5.readline()

range = 1

t5list = []

FermiList = []
for line in t5:

    line=re.sub(' +',' ',line)

    RA = line.split()[1]
    DEC = line.split()[2]
    NAME = 'J'+line.split()[0]

    t5list.append(GRB(NAME,RA,DEC))

for line in fermi:

    line = re.sub(' +',' ',line)
    line = re.sub(',',' ',line)
    line = re.sub('\)',' ',line)
    line = re.sub('}',' ',line)

    RA=line.split()[0]
    DEC = line.split()[1]
    NAME = line.split()[2]

    FermiList.append(GRB(NAME,RA,DEC))

results=0

print('T5 OBJECT -> FERMI OBJECT')

list3 = []
list4 = []
results=0
for T5 in t5list:

    list = []
    list2=[]

    for Fermi in FermiList:
        list.append(((T5.RA-Fermi.RA)**2+(T5.DEC-Fermi.DEC)**2)**.5)

    print(T5.NAME,'-> ',end='')


    b = False

    for l in list:

        if l <= 1 and b:
            print(',',FermiList[list.index(l)].NAME,'AT DIST =',l,end=', ')
            list2.append(FermiList[list.index(l)].NAME)


        if l <= 1:
            print(FermiList[list.index(l)].NAME,'AT DIST =',l,end='')
            results+=1
            b=True
            list4.append('TRUE')
            list2.append(FermiList[list.index(l)].NAME)

        

    if b == False:
        print('NO RESULTS WITHIN RANGE OF',range,'-> CLOSEST = ',FermiList[list.index(min(list))].NAME,'AT DIST =',min(list))
        list4.append('FALSE')
    else:
        print('')

    if len(list2)>1:
        s=T5.NAME+' HAS '+str(len(list2))+' RESULTS -> '
        for q in list2:
            s+=q+', '
        s=s[:-2]
        list3.append(s)

print('---------------------------------------------------------------------------')

print(results,'HAVE RESULTS WITHIN RANGE OF',range,'DEGREE',end='')

if range>1:
    print('s')
else:
    print('')

print('---------------------------------------------------------------------------')

for r in list3:
    print(r)
print('---------------------------------------------------------------------------')

for a in list4:
    print(a)

print(len(list4)-len(t5list))