def extended_euclidean(a,b):
    r1,r2=a,b
    s1,s2=1,0
    t1,t2=0,1
    while r2>0:
        q=r1//r2
        r=r1-q*r2
        r1,r2=r2,r

        s=s1-q*s2
        s1,s2=s2,s
        
        t=t1-q*t2
        t1,t2=t2,t
        s,t=s1,t1
    return r1,s,t

a,b= map(int,input("Enter a,b:").split(','))
gcd,x,y=extended_euclidean(a,b)
if x<0:
    x+=26
if y<0:
    y+=26
print(f'GCD of {a},{b} :{gcd}')
print(f'Coefficients: X={x},Y={y}')
