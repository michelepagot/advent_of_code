import sys
import re
import math

def part1(data):
    result_1 = 0
    for m in [map(int, match.group(1).split(',')) for match in re.finditer(r'mul\((\d{1,3},\d{1,3})\)', data)]:
        result_1 += math.prod(m)
    return result_1

def part2(data):
    do = 1
    res_2 = 0
    for match in re.finditer(r"mul\((\d{1,3},\d{1,3})\)|do\(\)|don't\(\)", data):
        if 'mul' in str(match):
            res_old = res_2
            s_split = match.group(1).split(',')
            prod_l = map(int, s_split)
            p_i = math.prod(prod_l)
            if do:
                res_2 += p_i
            print(f"mul --> {match.group(1)} s_split:{s_split} prod_l:{prod_l}|{[p for p in prod_l]} p_i:{p_i} do:{do} res_old:{res_old} --> res_2:{res_2}")
        elif "don't" in str(match):
            do = 0
            print("Dont")
        elif "do" in str(match):
            do = 1
            print("Do")
        else:
            print("!!!!!!!!!!!Unexpected match!!!!!!!!!!!!!")
    return res_2

def main(input_file):
    with open(input_file, 'r') as f:
        data=f.read()
    print(f"data:{data}")
    return (part1(data), part2(data))

if __name__ == "__main__":
    res = main(sys.argv[1])
    print(f"Part1:{res[0]}")
    print(f"Part2:{res[1]}")