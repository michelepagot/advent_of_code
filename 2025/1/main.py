import utils

with open('input.txt', 'r') as f:
    sol = utils.solve(f.read(), 50)
    print(f"Part1:{sol[0]}")
    print(f"Part2:{sol[1]}")
