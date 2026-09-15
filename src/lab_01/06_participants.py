n=int(input('in_1: '))
o=0
z=0
for i in range(n):
    s=input(f'in_{i+2}: ').split()
    if s[3]=='True':
        o+=1
    else:
        z+=1
    if o+z==3:
        print('out:',o, z)
        break