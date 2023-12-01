"""
Advent of Code 2023 day 1
"""
import sys
import re

def get_digit_list_part1(line):
    ret = [c for c in line if c.isdigit()]
    # print(f"Part1 Line:{line.strip()}  -->  ret:{ret}")
    return ret


TRANSLATOR = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def translate_word_to_digit(word):
    """
    get `four` and return `4`
    """
    return str(TRANSLATOR.index(word)+1)


def translate_digit_to_word(digit):
    """
    get `4` and return `four`
    """
    return TRANSLATOR[int(digit)-1]

def get_digit_list_part2(line):
    ret = []
    base_regexp = '(' + '|'.join(TRANSLATOR) + '|[1-9])'
    re_list = [ re.compile(rf'{base_regexp}.*'), re.compile(rf'.*{base_regexp}')]
    for re_this in re_list:
        match = re_this.search(line)
        if match:
            this_number = match.groups(1)[0]
            if this_number.isdigit():
                ret.append(this_number)
            else:
                ret.append(translate_word_to_digit(this_number))
    # print(f"Part2 Line:{line.strip()}  -->  ret:{ret}")
    return ret


with open(sys.argv[1], 'r', encoding='utf-8') as f:
    score = [0, 0]
    for line in f.readlines():
        digit_list = [get_digit_list_part1(line), get_digit_list_part2(line)]
        #print(f"line:{line.strip()}  -->  digit_list: {digit_list}")
        for part_idx in range(2):
            if digit_list[part_idx]:
                score[part_idx] += int(''.join([digit_list[part_idx][0], digit_list[part_idx][-1]]))
                #print(f"score[{part_idx}] increased to {score[part_idx]}")

print("Part1:" + str(score[0]))
print("Part2:" + str(score[1]))
