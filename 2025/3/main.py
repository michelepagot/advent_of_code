import utils

with open('input.txt', 'r') as f:
    sol = utils.solve(f.read())
    print(f"Part1:{sol[0]}")
    print(f"Part2:{sol[1]}")
