def add(a,b): #a,b: str, used to avoid floating point error (hopefully)
    nega,negb=('-' in a),('-' in b)
    a,b=a[1*nega:],b[1*negb:]
    if '.' not in a:
        a+='.'
    if '.' not in b:
        b+='.'
    idxa,idxb=a.index('.'),b.index('.')
    La,Lb=len(a),len(b)
    a,b=a[:idxa]+a[idxa+1:],b[:idxb]+b[idxb+1:]
    if idxa<idxb:
        idx=idxb
        a='0'*(idxb-idxa)+a
    else:
        idx=idxa
        b='0'*(idxa-idxb)+b
    if La-idxa<Lb-idxb:
        a+='0'*(Lb-La+idxa-idxb)
    else:
        b+='0'*(La-Lb+idxb-idxa)
    L=len(a)
    pow=idx-L
    A,B=[int(i)*(-2*nega+1) for i in a],[int(i)*(-2*negb+1) for i in b]
    S=str(sum([(A[i]+B[i])*10**(L-i-1) for i in range(L)]))
    S=S[:pow]+'.'+S[pow:]
    return S
def isolateNumbers(content):
    go=False
    res=[]
    ans=""
    for i in content:
        if go and not (i.isdigit() or i=='.'):
            go=False
            res.append(ans)
            ans=""
        if not go and (i.isdigit() or i=='-'):
            go=True
        if go:
            ans+=i
    return res
def pairify(nums):
    res=[]
    ans=[]
    for num in nums:
        ans.append(num)
        if len(ans)==2:
            res.append(ans[:])
            ans=[]
    return res
def explicitify(pairs):
    res=[pairs[0][:]]
    pairs=pairs[1:]
    ans=[]
    for pair in pairs:
        ans.append(pair[:])
        if len(ans)==3:
            for an in ans:
                an[0]=add(an[0],res[-1][0])
                an[1]=add(an[1],res[-1][1])
            res+=ans[:]
            ans=[]
    return res
def bezier(p1,p2,p3,p4,mint):
    return f"({1+mint}-t)^3({p1[0]},{p1[1]})+3(t-{mint})({1+mint}-t)^2({p2[0]},{p2[1]})+3(t-{mint})^2({1+mint}-t)({p3[0]},{p3[1]})+(t-{mint})^3({p4[0]},{p4[1]})"
def lineseg(p1,p2,mint):
    return f"(t-{mint})({p1[0]},{p1[1]})+({1+mint}-t)({p2[0]},{p2[1]})"
def piezify(B):
    res=""
    for i in range(len(B)):
        res+=f"{i}\\leq t\\leq{i+1}:{B[i]},"
    return '\\left\\{'+res[:-1]+'\\right\\}'
def circuit(P):
    B=[bezier(P[3*i],P[3*i+1],P[3*i+2],P[3*i+3],i) for i in range(len(P)//3)]
    B.append(lineseg(P[-1],P[0],len(P)//3))
    return piezify(B),len(P)//3+1

c=0
filepath=input("SVG Path: ")
maxt=0
eqList="["
colorList="C=["
with open(filepath,'r') as file:
    for line in file:
        c+=1
        if line[1:5]=="path":
            color=line[line.index('fill="#')+7:]
            color=color[:line.index('"')]
            line=line[line.index('d="')+3:]
            line=line[:line.index('"')]
            eq,pott=circuit(explicitify(pairify(isolateNumbers(line))))
            if pott>maxt:
                maxt=pott
            eqList+=eq+','
            colorList+="rgb("+','.join([str(int(color[2*i:2*i+2],16)) for i in range(3)])+'),'
        if c>10:
            break
    eqList=eqList[:-1]+']'
    colorList=colorList[:-1]+']'
print(eqList)
print()
print(colorList)
print()
print(f"maxt:{maxt}")