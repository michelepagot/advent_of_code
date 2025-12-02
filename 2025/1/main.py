def dirmod(a,b):
    res = a%b
    return res if not res else res-b if a<0 else res


def rotate(size: int, start: int, move: int) -> (int, int):
    # In [1]: 5%3
    # Out[1]: 2
    #
    # In [2]: -5%3
    # Out[2]: 1
    return dirmod(start + move, size) , abs((start + move) // size)


def dial(start: int, val: str) -> int :
    move = int(val[1:])
    if "L" == val[0]:
        move = move * (-1)
    return rotate(100, start, move)


def solve(input_str: str, start: int) -> [int, int]:
    p = [0, 0]
    s = start
    for m in [line for line in input_str.splitlines()]:
        print(f"dial(m:{m} s:{s}) <-- p:{p}")
        (s, c) = dial(s, m)
        if s == 0:
            p[0] += 1
        p[1] += c
        print(f"s:{s} c:{c} -->p:{p}")
    return p


with open('input.txt', 'r') as f:
    sol = solve(f.read(), 50)
    print(f"Part1:{sol[0]}")
    print(f"Part2:{sol[1]}")
