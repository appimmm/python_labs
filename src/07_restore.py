s=input()
first=0
for i in range(len(s)):
    if s[i].isupper():
        first=i
        break
sec=0
for i in range(first,len(s)):
    if s[i].isdigit():
        sec=i+1
        break
shag=sec-first
res=''
for i in range(first,len(s),shag):
    res+=s[i]
    if s[i]=='.':
        break
print(res)
