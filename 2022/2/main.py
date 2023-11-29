import sys
import re


def translate(value, code):
    if code[0] == value:
        return 'R'
    elif code[1] == value:
        return 'P'
    elif code[2] == value:
        return 'S'
    else:
        return None


with open(sys.argv[1], 'r', encoding='utf-8') as f:
    score = 0
    for line in f.readlines():
        match = re.search(r'([ABC]) ([YXZ])', line)
        if match:
            # A for Rock, B for Paper, and C for Scissors
            opponent = translate(match.group(1), ['A', 'B', 'C'])
            # X for Rock, Y for Paper, and Z for Scissors
            you = translate(match.group(2), ['X', 'Y', 'Z'])

            #print("You:" + you + " Opponent:" + opponent)
            
            # 1 for Rock, 2 for Paper, and 3 for Scissors
            if you == 'R':
                score += 1
            elif you == 'P':
                score += 2
            elif you == 'S':
                score += 3

            # 0 if you lost, 3 if the round was a draw, and 6 if you won
            if you == opponent:
                score += 3
            if you == 'S' and opponent == 'P':
                score += 6
            elif you == 'R' and opponent == 'S':
                score += 6
            elif you == 'P' and opponent == 'R':
                score += 6

            
print("Part1:" + str(score))
print("Part2:" + str(0))
