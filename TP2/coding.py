def doublons(tab)->bool:
    for i,el in enumerate(tab):
        for j,el2 in enumerate(tab):
            if i!=j and el==el2:
                return True
    return False


tab = [1,2,3,4]

print(doublons(tab))


def est_anagrame(s,t):
    for i in range(len(s)):
        if s[i]!=t[len(t)-i-1]:
            return False
    return True

g="abcd"
f="dcba"

print(est_anagrame(g,f))
        