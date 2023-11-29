"""
Advent of Code 2022 day 3
"""
import sys

class Rackpack():
    def __init__(self, description) -> None:
        half = int(len(description)/2)
        self.compartments =  [ description[0:half], description[half:] ]
        for l in self.compartments[0]:
            if l in self.compartments[1]:
                self.common = l
                if l.islower():
                    # Lowercase item types a through z have priorities 1 through 26.
                    self.rating = ord(l) - 96
                else:
                    # Uppercase item types A through Z have priorities 27 through 52.
                    self.rating = ord(l) - 65 + 27

    def __str__(self) -> str:
        ret = "Comp1:" + self.compartments[0]
        ret += ' Comp2:' + self.compartments[1]
        ret += " Common:" + self.common
        ret += " Rating:" + str(self.rating)
        return ret
        
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    score = [0, 0]
    for line in f.readlines():
        this_rackpack = Rackpack(line)
        print(this_rackpack)
        score[0] += this_rackpack.rating

print("Part1:" + str(score[0]))
print("Part2:" + str(score[1]))
