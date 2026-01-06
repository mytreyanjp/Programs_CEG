def generate_receding(m,ranged):
    classes={}
    for a in range(m):
        classes[a]=[]
        for k in range(-ranged,ranged+1):
            val=a+k*m
            classes[a].append(val)
    return classes

mod=int(input("Enter the mod to generate it's receding classes:"))
receding_classes=generate_receding(mod,20)

for i in receding_classes:
    print(f'[{i}] mod {mod}={receding_classes[i]}')