import sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    elfi = []
    zaino = 0
    for line in f.readlines():
        if line == '\n':
            elfi.append(zaino)
            zaino = 0
        else:
            zaino += int(line)
elfi.sort(reverse=True)
print("Part1:" + str(elfi[0]))
print("Part2:" + str(sum(elfi[0:3])))
