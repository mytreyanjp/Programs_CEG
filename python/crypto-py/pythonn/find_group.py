def is_group(S,op):
    for a in S:
        for b in S:
            if op(a,b) not in S:
                return False
    for a in S:
        for b in S:
            for c in S:
                if op(op(a,b),c)!=op(a,op(b,c)):
                    return False
    idd=None
    for e in S:
        if all(op(e,a)==a and op(a,e)==a for a in S):
            idd=e
            break
    if idd is None:
        return False
    
    for a in S:
        has_inv=False
        for b in S:
            if op(a,b)==idd and op(b,a)==idd:
                has_inv=True
                break
        if not has_inv:
            return False
    
    return True

S=input("Enter the set separated by commas: ").split(',')
S=[int(i) for i in S]
mod=int(input("Enter the mod value: "))
operation = input("Enter the operation (+, -, *): ")

if operation == '+':
    op = lambda a,b: (a+b) % mod
elif operation == '-':
    op = lambda a,b: (a-b) % mod
elif operation == '*':
    op = lambda a,b: (a*b) % mod
else:
    print("Invalid operation")
    exit(1)

print("Is a group" if is_group(S,op) else "Not a group")
