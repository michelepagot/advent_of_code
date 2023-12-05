"""
Advent of Code 2023 day 2
"""
import sys
import re

VALID_COLORS = ['green', 'red', 'blue']

class SmallBag():
    def __init__(self, text_def):
        """
        Initialize bag content from text line like

        12 red cubes, 13 green cubes, and 14 blue cubes
        """
        self.bag_content = {}
        for match in re.findall(rf'(\d+) ({"|".join(VALID_COLORS)}) cubes', text_def):
            self.bag_content[match[1]] = int(match[0])
        print(f"bag_content:{self.bag_content}")

    def is_compatible(self, grab):
        """
        Tell if a grab is compatible with current bag content.
        Grab is provided as dict {'blue': 1, 'green': 2, 'red': 0},
        """
        res = []
        for color in VALID_COLORS:
            res.append(grab[color] <= self.bag_content[color] )
            #print(f"self.bag_content['{color}'] = {self.bag_content[color]} grab['{color}'] = {grab[color]} res:{res}")
        return all(res)


def parse_grabs(game):
    """
    From a string like `1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue`
    return a list like
    [
        {'blue': 1, 'green': 2, 'red': 0},
        {'blue': 4, 'green': 3, 'red': 1},
        {'blue': 1, 'green': 1, 'red': 0},
    ]
    """
    print(f"parse_game({game})")
    re_parse_game = {}
    for color in VALID_COLORS:
        re_parse_game[color] = re.compile( rf"(\d+) ({color})" )
    ret = []
    for turn_string in game.split(';'):
        print(f"Turn:{turn_string}")
        turn = {}
        for color in VALID_COLORS:
            match = re_parse_game[color].search(turn_string)
            if match:
                turn[color] = int(match[1])
            else:
                turn[color] = 0
        ret.append(turn)
    print(f"parse_game ret:{ret}")        
    return ret


re_parse_line = re.compile(r'Game (\d+):(.*)')


def parse_line(line):
    """
    From input.txt like `Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue`
    get a dict like
    {
      'id': 2,
      'games': [
        {'blue': 1, 'green': 2, 'red': 0},
        {'blue': 4, 'green': 3, 'red': 1},
        {'blue': 1, 'green': 1, 'red': 0},
        ]
    }
    """
    res = {'id': None, 'games': []}
    match = re_parse_line.search(line)
    print(f"parse_line({line})")
    if match:
        res['id'] = int(match.group(1))
        res['games'] = parse_grabs(match.group(2))
    print(f"parse_line ret:{res}")
    return res


def min_bag(grabs):
    # Initialize the return
    ret = {}
    for color in VALID_COLORS:
        ret[color] = 0

    for grab in grabs:
        for color in VALID_COLORS:
            if grab[color] > ret[color]:
                ret[color] = grab[color]
    print(f"min_bag({grabs}) --> {ret}")
    return ret

the_bag = SmallBag('12 red cubes, 13 green cubes, and 14 blue cubes')

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    score = [0, 0]
    for line in f.readlines():
        print(f"line:{line.strip()}")
        current_game = parse_line(line)
        valid_game = [the_bag.is_compatible(grab) for grab in current_game['games']]
        print(f"valid_game:{valid_game}")
        if all(valid_game):
            score[0] += current_game['id']
        line_score = 1
        for value in min_bag(current_game['games']).values():
            line_score *= value
            print(f"min:{value}  line_score:{line_score}")
        score[1] += line_score

     
print("Part1:" + str(score[0]))
print("Part2:" + str(score[1]))
