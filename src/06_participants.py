n=int(input())
o=0
z=0
for i in range(n):
    s=input().split()
    if s[3]=='True':
        o+=1
    else:
        z+=1
print(o, z)