from random import randint as ri
ul = lambda l, i, e: l.__setitem__(i, e); aof = 4; fsz = 5; isz = 3; rns = ['sword', 'monster', 'empty']; inv = []; plm = [['?????' for i in range(fsz)] for j in range(aof)]; curf = aof - 1; curr = 0; r = 'empty'; go = False; mwi = False
def vmr(m): sc=sum(r=='sword' for f in m for r in f); mc=sum(r=='monster' for f in m for r in f); msc=sum(r=='magic stones' for f in m for r in f); return sc >= 4 and mc >= 3 and msc >= 1
def cf(nusi, dsi, fsz): f = [rns[ri(0, 2)] for j in range(fsz - 2)]; f.insert(nusi, "stairs up"); f.insert(dsi, "stairs down"); return f
def cff(): f = cf(ri(0, fsz - 2), 0, fsz); f[0] = 'empty'; return f
def w(l, pusi): pusi[0] = l.index("stairs up"); return l
def cmf(pusi, fs): return [w(cf(ri(0, fsz - 2), pusi[0], fsz), pusi) for _ in range(fs)]
def cl2f(pusi): stlf = cf(ri(2, fsz - 2), pusi[0], fsz); pusi[0] = stlf.index("stairs up"); lf = cf(0, pusi[0] - 1, fsz - 1); lf[0] = 'prize'; lf.insert(1, 'boss monster'); return (stlf, lf)
def rm(aof):
    m = []; frs = cff(); pusi = [None]; pusi[0] = frs.index("stairs up"); m.append(frs)
    if aof - 3 > 0:
        mf = cmf(pusi, aof - 3); pusi[0] = mf[-1].index("stairs up")
        for f in mf: m.append(f)
    stlf, lf = cl2f(pusi); m.append(stlf); m.append(lf); fi = 0; rmi = 0
    while m[fi][rmi] in ['prize', 'boss monster', 'stairs up', 'stairs down'] or (fi == 0 and rmi == 0): fi = ri(0, aof - 1); rmi = ri(0, fsz - 1); ((m[fi][rmi] in ['prize', 'boss monster', 'stairs up', 'stairs down'] or (fi == 0 and rmi == 0)) or ul(m[fi], rmi, "magic stones"))
    while m[fi][rmi] in ['prize', 'boss monster', 'stairs up', 'stairs down', 'magic stones'] or (fi == 0 and rmi == 0): fi = ri(0, aof - 1); rmi = ri(0, fsz - 1); ((m[fi][rmi] in ['prize', 'boss monster', 'stairs up', 'stairs down', 'magic stones'] or (fi == 0 and rmi == 0)) or ul(m[fi], rmi, "exit gate"))
    return m[::-1]
def chf(f, sp, ep, s, sc):
    fcy = list(f); csc = sc; ii = False; bfg = f; bci = sp; fib = False
    for rmi in range(sp, ep, s):
        r = fcy[rmi]; (r in ['sword', 'monster', 'boss monster']) and (csc := csc + (r == 'sword') - (r in ['monster', 'boss monster'])); (r in ['sword', 'monster', 'boss monster']) and (ul(fcy, rmi, 'empty')); (r in ['stairs up', 'prize']) and (fib := True); (r in ['stairs up', 'prize']) and (bfg := fcy); (r in ['stairs up', 'prize']) and (bci := rmi); (csc > sc) and (bfg := fcy); (csc > sc) and (bci := rmi); (csc > sc) and (ii := True); (csc > sc) and (sc := csc)
        if csc < 0 or r in ['stairs up', 'prize']: break
    return (bfg, bci, ii, fib, sc)
def cfc(f, sp, sc):
    fcy = list(f); csc = sc; mssc = -1; egsc = -1
    for rmi in range(sp, -1, -1):
        (fcy[rmi] in ['sword', 'monster']) and (csc := csc + (fcy[rmi] == 'sword') - (fcy[rmi] == 'monster')); (fcy[rmi] in ['sword', 'monster']) and (ul(fcy, rmi, 'empty')); (csc > sc) and (sc := csc)
        if csc < 0: break
    for rmi in range(sp, fsz):
        (fcy[rmi] in ['sword', 'monster']) and (csc := csc + (fcy[rmi] == 'sword') - (fcy[rmi] == 'monster')); (fcy[rmi] in ['sword', 'monster']) and (ul(fcy, rmi, 'empty')); (csc > sc) and (sc := csc)
        if csc < 0: break
    if 'magic stones' in fcy:
        mssc = 0
        if fcy.index('magic stones') < sp:
            for rmi in range(sp, -1, -1): mssc = mssc - (fcy[rmi] == 'sword') + (fcy[rmi] == 'monster')
        else:
            for rmi in range(sp, fsz): mssc = mssc - (fcy[rmi] == 'sword') + (fcy[rmi] == 'monster')
    if 'exit gate' in fcy:
        egsc = 0
        if fcy.index('exit gate') < sp:
            for rmi in range(sp, -1, -1): egsc = egsc - (fcy[rmi] == 'sword') + (fcy[rmi] == 'monster')
        else:
            for rmi in range(sp, fsz): egsc = egsc - (fcy[rmi] == 'sword') + (fcy[rmi] == 'monster')
    return (sc, mssc, egsc)
def chw(m):
    if not vmr(m): return False
    mcy = list(m); sc = 0; cmsc = -1; cegc = -1
    for index in range(len(mcy) - 1, -1, -1):
        f = mcy[index]; fib = False; ep = fsz; sp = f.index("stairs down") if "stairs down" in f else 0; bfg = f; bci = sp; s = 1
        while True:
            ii = False; bfg, bci, ii, fib, sc = chf(bfg, sp, ep, s, sc)
            if fib: sc, nmsc, negc = cfc(bfg, bci, sc); cmsc = nmsc if nmsc > cmsc else cmsc; cegc = negc if negc > cegc else cegc; break
            ep, s = (s == 1) * -1 + (not (s==1)) * fsz, -s 
            if ii: continue
            bfg, bci, ii, fib, sc = chf(bfg, sp, ep, s, sc); ep, s = (s == 1) * -1 + (not (s==1)) * fsz, -s 
            if ii: continue
            return False
    if sc - cmsc - cegc >= 0: return True
    return False
while not mwi: m = rm(aof); mwi = chw(m)
def ph(): print("left: Takes you to the room to your left\nright: Takes you to the room to your right\nup: Takes you to the floor above you only if there are stairs up in your room\ndown: Takes you to the floor below you only if there are stairs down in your room\nfight: Allowd you to fight the monster if there is one in your room\ngrab: Allows you to grab the item in the room\ninventory: Allows you to see the items you have\nmap: Allows you to see the map of the maze with the rooms you have visited\nopen: Used to open the exit gate with a key\nend: Quits the game")
def ppm(): 
    for tof in [((fi == curf and rmi == curr), fi, rmi) for fi in range(aof) for rmi in range(fsz)]: b, fi, rmi = tof; ((b) and (print(f"[{'You':^14}]", end= "  ") or True)) or print(f"[{plm[fi][rmi]:^14}]", end= "  "); (rmi == fsz - 1) and print()
def prt(): (efft) and (print(ft)); (not efft) and print(bt); return input('Command? ')
def grt(pr): return "A deafening silence fills the vicinity, all of the warmth and light stripped from the room. The surface is bare and have no company as you stand in this flavorless expanse. " * (pr == "empty") + "A seemingly reliable sword rests upright in a pedastal as you enter, though the oxidation dims the shine and glimmer. " * (pr == "sword") + "A low hum vibrates through the air, rune-etched stones come into view. You feel raw and untamed energy emanating from the gems." * (pr == "magic stones") + "The stone walls tremble slightly, cracked and crumbling from erosion. Ancient steps spiral upward into darkness, worn down by countless footsteps long since faded from memory." * (pr == "stairs up") + "A chilling draft rises from the depths below. The steps descend into shadows, the darkness swalling the path whence you once came. " * (pr == "stairs down") + "A dread comes over you as you enter this room. You can almost grasp the air from the musky energy. Your hands shake with anticipation as you encounter a ghastly beast" * (pr == "monster") + "The room is curdled with a thick bloodlust, a low growl vibrates the floor as you eye an unsettling silhoutte. A harrowing brute emerges from the miserably thick ambience, making your blood run cold." * (pr == "boss monster") + "Your steps reverberate through the air, clanking on the medal, the atmosphere humming with reward and completion. This is it; the prize you've fought hard to claim. " * (pr == "prize") + "A tall wooden gate, weathered by time, stands sealed before you, emanating a faint magical pulse. An ornate iron keyhole lies carved into its center." * (pr == "exit gate"), "You are in an empty room" * (pr == "empty") + "There is a sword in this room." * (pr == "sword") + "There are magical stones in this room." * (pr == "magic stones") + "There are stairs in this room going up" * (pr == "stairs up") + "There are stairs in this room going down" * (pr == "stairs down") + "There is a monster in this room." * (pr == "monster") + "There is a boss monster in this room." * (pr == "boss monster") + "There is a prize in this room." * (pr == "prize") + "Before you lies the exit gate. " * (pr == "exit gate") + "The Boss's Diary lies in this room. " * (pr == "Boss's Diary")
def ga(rc, a): global go; (a == 'help') and (ph()); (a == 'map') and (ppm()); (a == 'end') and (go := True) and (print("You choose to give up. ")); (a == 'inventory') and (print(f"You have: {', '.join(inv)}")); (a in ['fight', 'grab', 'open']) and (print(f"Invalid Input - There is nothing to {a}")); (a in ['up', 'down']) and (print(f"Invalid Input - You cannot go {a}")); (a not in ['help', 'map', 'end', 'inventory', 'left', 'right', 'fight', 'grab', 'open', 'up', 'down']) and (print("Invalid Input - That is an invalid action")); return (mh(rc, a) if a in ['left', 'right'] else (rc, "N/A"))
def mh(rc, lor): (lor == "left" and curr == 0) and print("There is no room to your left"); (lor == 'right' and curr == fsz - 1) and print("There is no room to your right"); return ((rc - 1, 'left') if (lor == "left" and curr > 0) else ((rc + 1, 'right') if (lor == 'right' and curr < fsz - 1) else (rc, 'N/A')))
def em(rc): a=prt(); global curr; global prea; curr, prea = ga(rc, a)
def er(tom): gio, gino = True, False; global curr; a = prt(); global m; w = False; curr = curr - (a == 'left' and prea == 'right') + (a == 'right' and prea == 'left'); ((a == 'fight') and all(im in inv for im in reqi)) and (print(f"You defeated the {tom}!") or True) and ([inv.remove(im) for im in reqi] or True) and (w := True) and ul(m[curf], curr, "empty"); ((a == 'fight') and not w) and (print(f"You attempted to fight {tom} without a required item and lost! \nYou had: {', '.join(inv)}\nYou needed: a {' and '.join(reqi)}")); ((a == 'left' and prea == 'left') or (a == 'right' and prea == 'right')) and (print(f"You attempted to run past the {tom} and died")); (a not in ['fight', 'left', 'right']) and (ga(curr, a)); return (gio if ((a == 'left' and prea == 'left') or (a == 'right' and prea == 'right') or (a == 'fight' and not w) or (a == 'end')) else gino)
def ir(rc, im): a = prt(); global curr; global prea; global m; t = (curr, prea); (a == 'grab') and ((len(inv) >= isz) and (print("You cannot carry any more items"))); (a == 'grab') and ((len(inv) < isz) and (print(f"[{im} has been added to inventory]") or True) and ul(m[curf], curr, 'empty')); (a == 'grab') and ((len(inv) < isz) and (inv.append(im))); (a == 'grab') and ((len(inv) < isz) and (ul(m[curf], curr, 'empty'))); (a != 'grab') and (t := ga(rc, a)); curr, prea = t
def sr(rc, uod): a = prt(); global curr; global prea; global curf; t = (curr, prea); curf = curf - (a == uod and uod == "up") + (a == uod and uod == "down"); (not ((a == uod and uod == "up") or (a == uod and uod == "down"))) and (t := ga(rc, a)); curr, prea = t
def pzr(): a = prt(); global curr; global prea; global m; global isz; (a == 'grab') and (print("[Key has been added to inventory]") or True) and (inv.insert(0, 'key') or True) and (isz := isz + 1) and (((len(inv) >= isz) and (print("You cannot carry any more items") or True) and ul(m[curf], curr, "Boss's Diary")) or ((print("[The Boss's Diary has been added to inventory]") or True) and (inv.append("Boss's Diary") or True) and ul(m[curf], curr, 'empty'))); t = (curr, prea); (a != 'grab' and not go) and (t := ga(curr, a)); curr, prea = t
def gr(): a = prt(); global prea; global curr; global go; (a == 'open' and 'key' in inv) and (go := True) and (print("You insert the key... \nThe gate groans open, and light floods in. \nYou step through — free at last. ")); (a == 'open' and 'key' not in inv) and print("You need a key to open the gate. "); t = (curr, prea); (not go) and (t := ga(curr, a)); curr, prea = t
while not go: r = m[curf][curr]; efft = plm[curf][curr] == '?????'; plm[curf][curr] = r; ft, bt = grt(r); (r == 'empty') and (em(curr)); (r in ["sword", "magic stones", "Boss's Diary"]) and (ir(curr, r)); (r in ['stairs up', 'stairs down']) and (sr(curr, r[7:])); reqi = ['sword'] if r == 'monster' else ['sword', 'magic stones']; (r in ["monster", "boss monster"]) and (go := er(r)); (r == 'prize') and (pzr()); (r == 'exit gate') and (gr())