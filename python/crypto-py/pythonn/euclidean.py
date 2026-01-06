def euclidean(a,b):
    r1,r2=a,b
    while r2>0:
        q=r1//r2
        r=r1-q*r2
        r1,r2=r2,r
    return r1

a,b= map(int,input("Enter a,b:").split(','))
print("GCD:",euclidean(a,b))