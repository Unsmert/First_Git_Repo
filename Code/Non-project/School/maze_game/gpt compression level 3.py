import copy as C
from random import randint as R
A,B,D,T,F=4,5, {1:'sword',2:'monster',3:'empty'},1,0
v=lambda m:sum(x=='sword'for f in m for x in f)>=4 and sum(x=='monster'for f in m for x in f)>=3 and any('magic stones'in f for f in m)
def cf(u,d,n):
    f=[D[R(1,3)]for _ in range(n-2)]
    f.insert(u,'stairs up')
    f.insert(d,'stairs down')
    return f
def f1():
    f=cf(R(0,B-2),0,B)
    f[0]='empty'
    return f
def fl(p):
    s=cf(R(2,B-2),p,B)
    p=s.index('stairs up')
    l=cf(0,p-1,B-1)
    l[0]='prize'
    l.insert(1,'boss monster')
    return s,l
def rm(n):
    m=[f1()]
    p=m[0].index('stairs up')
    if n-3>0:
        for _ in range(n-3):
            f=cf(R(0,B-2),p,B)
            p=f.index('stairs up')
            m.append(f)
    s,l=fl(p)
    m+=[s,l]
    fi,ri=0,0
    while m[fi][ri] in ['prize','boss monster','stairs up','stairs down'] or (fi==0 and ri==0):
        fi,ri=R(0,n-1),R(0,B-1)
    m[fi][ri]='magic stones'
    return m[::-1]
def chk_floor(f,s,e,st,c):
    fc=C.deepcopy(f)
    cs=c
    bf=f
    bi=s
    im=be=F
    for i in range(s,e,st):
        if i<0 or i>=len(fc) or cs<0: break
        r=fc[i]
        if r=='sword': cs+=1; fc[i]='empty'
        elif r in ['monster','boss monster']: cs-=1; fc[i]='empty'
        elif r in ['stairs up','prize']: be=T; bf=fc; bi=i; break
        if cs>c: bf=fc; bi=i; c=cs; im=T
    return bf,bi,im,be,cs
def conf_floor(f,s,c):
    fc=C.deepcopy(f)
    cs=c
    ms=-1
    for i in range(s,-1,-1):
        if fc[i]=='sword': cs+=1; fc[i]='empty'
        elif fc[i]=='monster': cs-=1; fc[i]='empty'
        if cs>c: c=cs
        if cs<0: break
    for i in range(s,B):
        if fc[i]=='sword': cs+=1; fc[i]='empty'
        elif fc[i]=='monster': cs-=1; fc[i]='empty'
        if cs>c: c=cs
        if cs<0: break
    if 'magic stones' in fc:
        ms=0
        if fc.index('magic stones')<s:
            for i in range(s,-1,-1):
                if fc[i]=='sword': ms-=1
                elif fc[i]=='monster': ms+=1
        else:
            for i in range(s,B):
                if fc[i]=='sword': ms-=1
                elif fc[i]=='monster': ms+=1
    return c,ms
def ch_dir(d): return (-1,-1) if d==1 else (B,1)
def chk_win(m):
    m=C.deepcopy(m)
    if not v(m): return F
    c=0
    mc=-1
    for idx in range(len(m)-1,-1,-1):
        f=m[idx]
        s=f.index('stairs down') if 'stairs down' in f else 0
        e=B
        bf=f
        bi=s
        st=1
        while 1:
            bf,bi,im,be,c=chk_floor(bf,s,e,st,c)
            if be:
                c,nmc=conf_floor(bf,bi,c)
                mc=nmc if nmc>mc else mc
                break
            e,st=ch_dir(st)
            if im: continue
            bf,bi,im,be,c=chk_floor(bf,s,e,st,c)
            e,st=ch_dir(st)
            if im: continue
            return F
    return c-mc>=0
m=w=F
while not w:
    m=rm(A)
    w=chk_win(m)
inv=[]
cf= A-1
cr=0
go=F
def help_msg(): print('left: move left\nright: move right\nup: stairs up\ndown: stairs down\nfight: fight monster\ngrab: pick item\ninventory: show inventory')
def act(r,a):
    if a=='help': help_msg()
    if a=='end': return '!'
    if a=='inventory': print(f"You have: {', '.join(inv)}")
    if a in ['left','right']: return move(r,a)
    if a in ['fight','grab']: print(f"There is nothing to {a}")
    if a in ['up','down']: print(f"You cannot go {a}")
    else: print('Invalid'); return r
def move(r,d):
    if d=='left' and cr>0: return r-1
    if d=='right' and cr<B-1: return r+1
    print('No room'); return r
def empty(r):
    print('Empty room')
    return act(r,input('Command? '))
def mon(t):
    req=['sword'] if t=='monster' else ['sword','magic stones']
    print("Monster!" if t=='monster' else "Boss!")
    a=input('Command? ')
    if a not in ['help','fight','left','right']: print('Invalid'); return F
    if a=='help': help_msg(); return F
    if a!='fight': print(f'Failed to flee {t}'); return T
    if all(x in inv for x in req):
        print(f'Defeated {t}!')
        for x in req: inv.remove(x)
        m[cf][cr]='empty'
        return F
def itm(r,i):
    print("Sword!" if i=='sword' else "Magic stones!")
    a=input('Command? ')
    if a=='grab':
        if len(inv)>=3: print('Cannot carry more')
        else: inv.append(i); print(f"[{i}] added"); m[cf][cr]='empty'; return r
    return act(r,a)
def stair(f,r,d):
    print(f'Stairs {d}')
    a=input('Command? ')
    if a==d and d=='up': return (f-1,r)
    if a==d and d=='down': return (f+1,r)
    return (f,act(r,a))
while not go:
    for flr in m: print(flr)
    rmv = m[cf][cr]
    if rmv=='empty': cr=empty(cr)
    elif rmv in ['sword','magic stones']: cr=itm(cr,rmv)
    elif rmv=='stairs up': cf,cr=stair(cf,cr,'up')
    elif rmv=='stairs down': cf,cr=stair(cf,cr,'down')
    elif rmv in ['monster','boss monster']: go=mon(rmv)
    elif rmv=='prize': print('YOU WON'); go=T