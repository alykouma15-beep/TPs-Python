chiffrerom1={1:"I",5:"V",10:"X",50:"L",100:"C",500:"D",1000:"M"}
l=[2,3]
chiffrerom={1:"I",5:"V",10:"X",50:"L",100:"C",500:"D",1000:"M"}
for c in chiffrerom1.keys():
    if str(c).startswith('1'):
        for i in l:
            chiffrerom[(c*i)]=chiffrerom1[c]
            for j in range(i-1):
                chiffrerom[(c*i)]+=chiffrerom1[c]    #Je definis cette fois-ci le dictionnaire de chiffres romains complet avec des règles appliqués automatiquement
decile={}
for i in range(100): #Dictionnaire de nombre de décimales
    decile[i]=pow(10,i)

def romain(e):
    e=str(e) #Je transforme l'entier en string
    i=0
    ro=""
    while i<len(e):
        if int(e[i])==0:#Si on rencontre des 0 on passe
            i+=1
            continue
        restant=len(e)-i-1 #Je cherche le nombre de décimale restant pour savoir si c'est un millième ou un centieme
        if (int(e[i])*decile[restant]) in chiffrerom.keys(): #Si un équivalent romain existe tant mieux c'est le plus simple
            ro+=chiffrerom[(int(e[i])*decile[restant])]
            i+=1
        else:
            nombresup=(int(e[i])*decile[restant])#Sinon on cherche un romain superieur et un inferieurequi seront soustraits
            while True:     
                if nombresup in chiffrerom.keys():
                    break
                nombresup+=1
            nombreinf=0
            while True:
                if nombreinf in chiffrerom.keys() and nombresup-nombreinf==int(e[i])*decile[restant]:
                    break
                nombreinf+=1
            ro+=(chiffrerom[nombreinf]+chiffrerom[nombresup]) #Ajout en disposant d'abord le romain inferieur par conformité à l'écriture romaine
            i+=1
    return ro

test=151
print(romain(test))