chiffre={"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000} #Initialisation du dictionnaire romain
    
def entier(ro):
    i=0
    e=0
    while i<len(ro):
        if i<len(ro)-1 and chiffre[ro[i+1]]>chiffre[ro[i]]:#Si on repere un motif pouvant être une soustraction au lieu de deux vrais chiffres romains on les prends à 2
            e+=chiffre[ro[i+1]]-chiffre[ro[i]]
            i+=2
        else:
            e+=chiffre[ro[i]]
            i+=1
    return e
        
            
test="MCMXCIV"

print(entier(test))

