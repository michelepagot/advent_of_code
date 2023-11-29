"""
Advent of Code 2022 day 2
"""
import sys
import re


def translate(value, code):
    """
    Translate ABC and XYZ to a generic SPR
    """
    ret = None
    if code[0] == value:
        ret = 'R'
    elif code[1] == value:
        ret = 'P'
    elif code[2] == value:
        ret = 'S'
    print(f"translate(value={value}, code={code}) --> {ret}")
    return ret

def score_your_hand(you):
    """
    Calculate score for your hand

    1 for Rock, 2 for Paper, and 3 for Scissors
    """
    ret = None
    if you == 'R':
        ret = 1
    elif you == 'P':
        ret = 2
    elif you == 'S':
        ret = 3
    print(f"score_your_hand(you={you}) --> {ret}")
    return ret

def score_the_challenge(you, opponent):
    """
    Calculate the score for the challenge

    0 if you lost, 3 if the round was a draw, and 6 if you won
    """
    ret = 0
    if you == opponent:
        ret = 3
    elif (
        (you == "S" and opponent == "P")
        or (you == "R" and opponent == "S")
        or (you == "P" and opponent == "R")
    ):
        ret = 6
    print(f"score_the_challenge(you={you}, opponent={opponent}) --> {ret}")
    return ret


def your_hand_part2(result, opponent):
    """
    X means you need to lose
    Y means you need to end the round in a draw
    Z means you need to win
    """
    ret = None
    if result == 'Y':
        ret = opponent
    elif result == 'X':
        # you need to loose
        if opponent == 'S':
            ret = 'P'
        elif opponent == 'P':
            ret = 'R'
        elif opponent == 'R':
            ret = 'S'
    elif result == 'Z':
        # you need to win
        if opponent == 'S':
            ret = 'R'
        elif opponent == 'P':
            ret = 'S'
        elif opponent == 'R':
            ret = 'P'
    print(f"your_hand_part2(result={result}, opponent={opponent})")
    return ret

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    score = [0, 0]
    you = ['', '']
    for line in f.readlines():
        match = re.search(r'([ABC]) ([YXZ])', line)
        if match:
            # A for Rock, B for Paper, and C for Scissors
            opponent = translate(match.group(1), ['A', 'B', 'C'])
            # X for Rock, Y for Paper, and Z for Scissors
            you[0] = translate(match.group(2), ['X', 'Y', 'Z'])
            you[1] = your_hand_part2(match.group(2), opponent)

            for part in [0, 1]:
                score[part] += score_your_hand(you[part])
                score[part] += score_the_challenge(you[part], opponent)

            # X means you need to lose
            # Y means you need to end the round in a draw
            # Z means you need to win

print("Part1:" + str(score[0]))
print("Part2:" + str(score[1]))
