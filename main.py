import dotenv
import os

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
    neg='-' in S
    if neg:
        S=S[1:]
    S=S[:pow]+'.'+S[pow:]
    if neg:
        S='-'+S
    return S
def deeify(n):
    neg=('-' in n)
    if neg:
        n=n[1:]
    pow=int(n[n.index('e')+1:])
    n=n[:n.index('e')]
    if '.' not in n:
        n+='.'
    idx=n.index('.')
    n=n[:idx]+n[idx+1:]
    L=len(n)
    if pow<=0:
        if idx<=-pow:
            n='0.'+'0'*(-pow-idx)+n
        else:
            n=n[:idx+pow]+'.'+n[idx+pow:]
    else:
        if L-idx<=pow:
            n=n+'0'*(pow+idx-L)+'.0'
        else:
            n=n[:idx+pow]+'.'+n[idx+pow:]
    if neg:
        n='-'+n
    return n
def isolateNumbers(content):
    go=False
    res=[]
    ans=""
    ise=False
    for i in content:
        if i=='e':
            ise=True
            ans+=i
            continue
        if go and not (i.isdigit() or i=='.' or (ise and i=='-')):
            go=False
            if ise:
                ans=deeify(ans)
            ise=False
            res.append(ans)
            ans=""
        if not go and (i.isdigit() or i=='-'):
            go=True
        if go:
            ans+=i
        if i=='s':
            res+=['0','0']
    return res
def pairify(nums):
    res=[]
    ans=[]
    for num in nums:
        ans.append(num)
        if len(ans)==2:
            if '-' not in ans[1]:
                ans[1]='-'+ans[1]
            else:
                ans[1]=ans[1][1:]
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
def bezier(p1,p2,p3,p4,mint,maxt):
    return f"({1+mint}-{maxt}t)^3({p1[0]},{p1[1]})+3({maxt}t-{mint})({1+mint}-{maxt}t)^2({p2[0]},{p2[1]})+3({maxt}t-{mint})^2({1+mint}-{maxt}t)({p3[0]},{p3[1]})+({maxt}t-{mint})^3({p4[0]},{p4[1]})"
def lineseg(p1,p2,mint,maxt):
    return f"({maxt}t-{mint})({p1[0]},{p1[1]})+({1+mint}-{maxt}t)({p2[0]},{p2[1]})"
def piezify(B):
    maxt=len(B)
    res=""
    for i in range(len(B)):
        res+=f"{i}\\leq {maxt}t\\leq{i+1}:{B[i]},"
    return '\\left\\{'+res[:-1]+'\\right\\}'
def circuit(P):
    B=[bezier(P[3*i],P[3*i+1],P[3*i+2],P[3*i+3],i,len(P)//3+1) for i in range(len(P)//3)]
    B.append(lineseg(P[-1],P[0],len(P)//3,len(P)//3+1))
    return piezify(B)
def htmlify(eq):
    ans=""
    for char in eq:
        if char=='\\':
            ans+='\\'
        ans+=char
    return ans

dotenv.load_dotenv()
filepath=os.getenv("SVGPATH")
eqList=""
bigList="["
colorList="C=["
html="<script src=\"https://www.desmos.com/api/v1.11/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6\"></script>\n<div id=\"calculator\"></div>\n<script>\n    var elt=document.getElementById('calculator');\n    var calculator=Desmos.GraphingCalculator(elt);"
ln=0
with open(filepath,'r') as file:
    for line in file:
        if line[1:5]=="path":
            ln+=1
            color=line[line.index('fill="')+6:]
            color=color[:color.index('"')]
            line=line[line.index('d="')+3:]
            line=line[:line.index('"')]
            eq=circuit(explicitify(pairify(isolateNumbers(line))))
            html+=f"\n    calculator.setExpression({{latex:'{htmlify(eq)}',color:'{color}',fill:true,fillOpacity:1,lineWidth:0,lineOpacity:0}});"
            eqList+=f"f_{{{ln}}}(t)="+eq+'\n'
            eqList+=eq+'\n'
            bigList+=f"f_{{{ln}}}(t),"
            color=color[1:]
            colorList+="rgb("+','.join([str(int(color[2*i:2*i+2],16)) for i in range(3)])+'),'
    eqList=eqList[:-1]
    bigList=bigList[:-1]+']\n'
    colorList=colorList[:-1]+']\n'
with open("out.txt",'w') as file:
    file.write(colorList+bigList+eqList)
with open("out.html",'w') as file:
    file.write(html+"\n</script>")