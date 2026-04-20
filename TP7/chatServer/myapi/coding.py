def ordonne(a:list[int],b:list[int]):
    a.sort()
    b.sort()
    temp=0
    l=len(b)
    i=0
    print("Avant",a,b)
    while b:
        temp=b[i] #Variable temporaire unique qui n'est pas un tableau
        b.remove(temp) #Je supprime d'abord l'element de b donc je reduis au préalable son espace mémoire
        a.append(temp)
    a.sort()
    print("Après",a)

a=[1, 2, 3]
b=[2, 5, 6]

ordonne(a,b)
        