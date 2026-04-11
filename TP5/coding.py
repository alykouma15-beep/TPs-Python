def nombre1(a:int):
    count=0
    b=bin(a)[2:]
    for bit in b:
        if bit=='1':
            count+=1
    return bin(count)[2:]

test=3
print(f"entree {test}<=>{bin(test)[2:]} -> sortie {int(nombre1(test),2)}<=>{nombre1(test)}")


def swap(a:int,i,j):
    b=bin(a)[2:]
    b=list(b)
    temp=b[i]
    b[i]=b[j]
    b[j]=temp
    return int(''.join(map(str,b)),2)
test=73
print(f"entree {test}<=>{bin(test)[2:]} -> sortie {swap(test,1,6)}<=>{bin(swap(test,1,6))[2:]}")

