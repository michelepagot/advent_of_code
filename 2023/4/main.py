"""
Advent of Code 2023 day 4
"""
import sys
import logging
import re

log = logging.getLogger()
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
log.addHandler(handler)

re_card = re.compile(r"Card\s+(\d+):(.*)")
            
def parse_line(line):
    this_card = {}
    match = re_card.search(line)
    if match:
        this_card['id'] = int(match.group(1))
        data = match.group(2).split('|')
        this_card['winning_numbers'] = []
        for num in data[0].strip().split(' '):
            if num.isdigit():
                this_card['winning_numbers'].append(int(num))
        this_card['your_numbers'] = []
        for num in data[1].strip().split(' '):
            if num.isdigit():
                this_card['your_numbers'].append(int(num))
    return this_card


def winning_numbers(data):
    matches = 0
    for your_num in data['your_numbers']:
        if your_num in data['winning_numbers']:
            matches += 1
    return matches


def main():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        score = [0, 0]
        points = 0
        scratchcards = []
        for line in f.readlines():
            print(line)
            scratchcards.append(parse_line(line))
        matches = []
        for data in scratchcards:
            matches.append(winning_numbers(data))

        points = [0]*len(matches)
        point_multipliers = [1]*len(matches)
        for idx, card_match in enumerate(matches):
            if card_match > 0:
                print(f"Card {idx} has {card_match} matches so {(2**(card_match-1))} points")
                points[idx] = 2**(card_match-1)
                print(f"Add, {point_multipliers[idx]} times, multiplier for cards {[(idx + i + 1) for i in range(card_match)]}")
                for i in range(card_match):
                    target_card = idx + i + 1
                    if target_card < len(matches):
                        point_multipliers[idx + i + 1] += point_multipliers[idx]

        score[0] = sum(points)

        print(point_multipliers)
        for idx, point in enumerate(points):
            score[1] += point * point_multipliers[idx]
        score[1] = sum(point_multipliers)

    print("Part1:" + str(score[0]))
    print("Part2:" + str(score[1]))


if __name__ == "__main__":
    main()
