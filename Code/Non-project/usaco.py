import sys
input=sys.stdin.read
data=input().split()
index=0
T=int(data[index])
index+=1
k=int(data[index])
index+=1
for _ in range(T):
    FjString=int(data[index])
    index+=1
    S=data[index]
    index+=1
    N=FjString
    L=3*N
    if N%2==1:
        print(-1)
        continue
    half=L//2
    if S[:half]==S[half:]:
        print(1)
        print('1 '*L)
        continue
    found=False
    for rem in 'COW':
        R=''.join(c for c in S if c!=rem)
        rhalf=len(R)//2
        if R[:rhalf]==R[rhalf:]:
            found=True
            M=2
            assign=[0]*L
            op1=1
            op2=2
            for i in range(L):
                if S[i]==rem:
                    assign[i]=op1
                else:
                    assign[i]=op2
            print(M)
            print(' '.join(map(str,assign)))
            break
    if found:
        continue
    M=3
    assign=[0]*L
    op={'C':1,'O':2,'W':3}
    for i in range(L):
        assign[i]=op[S[i]]
    print(M)
    print(' '.join(map(str,assign)))

