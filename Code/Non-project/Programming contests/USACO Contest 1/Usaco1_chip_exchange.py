ans_list = []
for _ in range(int(input())):
    A_chips, B_chips, Ca, Cb, Fa = map(int, input().split())
    A_chips, B_chips =((B_chips // Cb) * Ca) + A_chips, B_chips % Cb
    Fa, A_chips = Fa - A_chips, 0

    if Fa <= 0:
        ans_list.append(0)
        continue

    additional_b_chips =  Cb - 1 - B_chips
    
    if Ca < Cb:
        exchanges = ((Fa - 1) // Ca)
        additional_a_chips = Fa - exchanges * Ca
        ans_list.append(additional_a_chips + additional_b_chips + exchanges * Cb)
    else:
        ans_list.append(Fa + additional_b_chips)
print("\n".join(map(str, ans_list)))