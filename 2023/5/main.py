"""
Advent of Code 2023 day 5
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

def main():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        score = [0, 0]
        for line in f.readlines():
            print(line)
        
    print("Part1:" + str(score[0]))
    print("Part2:" + str(score[1]))


if __name__ == "__main__":
    main()
