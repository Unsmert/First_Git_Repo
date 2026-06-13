#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the 'playGame' function below.
# The function is expected to return a STRING.
# The function accepts STRING deck as parameter.
preprocess = {
    " ": " ",
    "D": "D",
    "C": "C",
    "H": "H",
    "S": "S",
    "K": "13",
    "Q": "12",
    "J": "11",
    "T": "10",
    "9": "9",
    "8": "8",
    "7": "7",
    "6": "6",
    "5": "5",
    "4": "4",
    "3": "3",
    "2": "2",
    "A": "1"
    }
play_dict = { "D": ("C", "S"), "H": ("C", "S"), "C": ("D", "H"), "S": ("D", "H") }
def playable(query, target): 
    bottom_is_numerically_smaller_by_one = int(query[:-1]) == int(target[:-1]) - 1 
    symbols_are_opposites = target[-1] in play_dict[query[-1]] 
    return bottom_is_numerically_smaller_by_one and symbols_are_opposites 

def playGame(deck): 
    processed_deck = "".join([preprocess[char] for char in deck]) 
    list_deck = processed_deck.split() 
    p1_hand = list_deck[0:13:2] 
    p2_hand = list_deck[1:14:2] 
    hands = [p1_hand, p2_hand] 
    pile_1 = [list_deck[14]] 
    pile_2 = [list_deck[15]] 
    pile_3 = [list_deck[16]] 
    pile_4 = [list_deck[17]] 
    corner_1 = [] 
    corner_2 = [] 
    corner_3 = [] 
    corner_4 = [] 
    piles = [pile_1, corner_1, pile_2, corner_2, pile_3, corner_3, pile_4, corner_4] 
    draw_pile = list_deck[18:] 
    player = 0 
    while True: player_hand = hands[player] 
    did_step_1 = False 
    did_step_2 = False 
    # Step one: 
    # Check piles in clockwise order 
    # Start at the top pile (pile_1) 
    # Check piles in clockwise order 
    # Piles are going to have the left be the top 
    # and the right be the bottom 
    # Upper loop is to loop through the start piles 
    for init_index, initial_pile in enumerate(piles): 
        # Lower loop is for the target piles 
        for target_index, target_pile in enumerate(piles): 
            # Naturally need to ensure target piles are not the same 
            if init_index == target_index: 
                continue 
            # Need to check if piles are empty. If they are, move on if len(initial_pile) == 0 or len(target_pile) == 0: continue bottom_card_of_initial = initial_pile[-1] top_card_of_target = target_pile[0] if playable(bottom_card_of_initial, top_card_of_target): did_step_1 = True lowest_num = 14 card_index = 0 for index, card in enumerate(player_hand): if int(card[:-1]) < lowest_num: card_index = index lowest_num = int(card[:-1]) moved_pile = initial_pile piles[target_index] = moved_pile + target_pile piles[init_index] = [player_hand.pop(card_index)] break if did_step_1: break # Step two: # Check through cards in hand, left to right # Check if the card can be played, clockwise starting with topmost # If it can be played, play it and re-loop player_hand_size = len(player_hand) hand_index = 0 while hand_index < player_hand_size: query_card = player_hand[hand_index] if query_card[:-1] == "13": for pile_index in range(1, 8, 2): pile = piles[pile_index] if len(pile) == 0: pile.append(player_hand.pop(hand_index)) break hand_index = 0 player_hand_size -= 1 continue else: for index, target_pile in enumerate(piles): if len(target_pile) == 0: continue top_card = target_pile[0] if playable(query_card, top_card): did_step_2 = True piles[index] = [player_hand.pop(hand_index)] + target_pile hand_index = -1 player_hand_size -= 1 break hand_index += 1 if not (did_step_1 or did_step_2): if draw_pile: player_hand.append(draw_pile.pop(0)) if len(player_hand) == 0: ans_list = [str(player + 1)] for pile in piles: if len(pile) == 0: ans_list.append("E") else: num = pile[0][:-1] for key in preprocess.keys(): if num == preprocess[key]: char = key break ans_list.append(char + pile[0][-1]) return " ".join(ans_list) player = not player if __name__ == '__main__': fptr = open(os.environ['OUTPUT_PATH'], 'w') deck = input() result = playGame(deck) fptr.write(result + '\n') fptr.close() What's the difference between the intended algorithm and my code? And why am I timing out?