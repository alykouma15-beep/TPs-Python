


def marchesmax2(n:int): #Demandé dans l'exo qui rend possible 1 ou 2 marches à la fois
    resultats=[]
    
    def backtrack(reste:int,chemin:list[int]):
        if reste==0:
            resultats.append(chemin.copy()) #J'ai rajouté copy() car sans cela je me suis aperçu que tout s'effacait à chaque fois car
                                            #python utilise des references vers les listes au lieu des vraies listes copiés
            return
        
        for i in range(1,min(reste+1,3)): #j'ai rajouté le minimum car dans l'arbre il arrive souvent des moment ou le reste est inférieur à 2
            chemin.append(i)
            backtrack(reste-i,chemin)
            chemin.pop()
            
    backtrack(n,[])
    return resultats

def marchespeuimporte(n:int): #j'ai créé une fonction plus complète permettant tout type de combinaisons de sommes donc peu importe la marche
    resultats=[]
    
    def backtrack(reste:int,chemin:list[int]):
        if reste==0:
            if len(chemin)>1: # pour exclure le cas trivial n seul
                resultats.append(chemin.copy()) #J'ai rajouté copy() car sans cela je me suis aperçu que tout s'effacait à chaque fois car
                                            #python utilise des references vers les listes au lieu des vraies listes copiés
            return
        
        for i in range(1,reste+1): #sans limites de marches
            chemin.append(i)
            backtrack(reste-i,chemin)
            chemin.pop()
            
    backtrack(n,[])
    return resultats

test=4

max2=marchesmax2(test)
print(f"{max2}\n On a {len(max2)} possibilités en se limitant à 2 marches MAX")
possibilte=marchespeuimporte(test)
print(f"{possibilte}\n On a donc {len(possibilte)} possibilités sans limites de marches ")


def nombremot(c:str):
    chaine=c
    mots=[]
    last=0
    mot=""
    for i,el in enumerate(chaine):
        if el==' ' or el == '\n':
            mot=chaine[last:i]
            mots.append(mot)
            last=i+1
    mots.append(chaine[last:])
    print(mots)
    print(f"{len(mots)} mots")
    

test="Bonjour tout le monde, commencez a coder"

nombremot(test)
print(f"il y a {len(test.split(' '))} mots avec split également") # C'est le raccourci direct avec split



