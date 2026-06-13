import sys
input=sys.stdin.read
Test_cases, k = map(int, input().split())
for _ in range(Test_cases):
    FjString=int(input())
    S=input()
    N=FjString
    Length = 3*N
    if N%2==1:
        print(-1)
        continue
    half=Length//2
    if S[:half]==S[half:]:
        print(1)
        print('1 '*Length)
        continue
    found=False
    for rem in 'COW':
        R=''.join(c for c in S if c!=rem)
        rhalf=len(R)//2
        if R[:rhalf]==R[rhalf:]:
            found=True
            M=2
            assign=[0]*Length
            op1=1
            op2=2
            for i in range(Length):
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
    assign=[0]*Length
    op={'C':1,'O':2,'W':3}
    for i in range(Length):
        assign[i]=op[S[i]]
    print(M)
    print(' '.join(map(str,assign)))