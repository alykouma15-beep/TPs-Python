
from bisect import bisect_left


def couple(tab):
    cp=[]
    re=set(tab) #je simplifie la complexité en introduisant les sets ce qui permet d'enlever les doublons et donc de reduire la complexité
    for el in re:
        for jl in re:
            if el+jl==0:
                cp.append((el,jl))
                re=re-set([el,jl])
    return f"Les couples sont {cp}"

def trio_non_optimal(tab):
    trio=[]
    re=set(tab) #je simplifie la complexité en introduisant les sets ce qui permet d'enlever les doublons et donc de reduire la complexité
    for el in re:
        for jl in re:
            for tl in re:
                if el+jl+tl==0:
                    trio.append((el,jl,tl)) #Pas optimal du tout. On avoisine les O(N¨3)
    return f"Les trios sont {trio}"
    

def trio_tri(tab):#on utilisera une recherche ordonnée qui s'applique à une liste triée
    tab.sort()#Une liste ordonnée sans doublons
    trio=[]
    for i in range(len(tab)): # pour ne pas recalculer le même element
        for j in range(i+1,len(tab)):
            tl=bisect_left(tab,-(tab[i]+tab[j]),j+1) #fonction binary search qui va donc resoudre la transposition de l'équation c=-(a+b)
            if tl<len(tab) and tab[tl]==-(tab[i]+tab[j]): #element existe
                trio.append((tab[i],tab[j],tab[tl]))
    return f"Les trios sont {trio}"        #Algo optimal avec complexité passé de O(N^3) à O(N^2Log(N)) grâce à la puissance du tri + binary search
                
test=[1, 20, 15, 3, 5, -4, 41]
print(trio_non_optimal(test))