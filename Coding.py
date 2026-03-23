def tableau_modif(tab):
    tabm = []
    prod=1
    for i,val in enumerate(tab):
        for j,val in enumerate(tab):
            if j!=i:
                 prod=prod*tab[j]
        tabm.append(prod)
        prod=1
    return tabm