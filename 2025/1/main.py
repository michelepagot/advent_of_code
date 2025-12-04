import sys
import utils

def main():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        sol = utils.solve(f.read(), 50)
        print(f"Part1:{sol[0]}")
        print(f"Part2:{sol[1]}")

if __name__ == "__main__":
    main()
