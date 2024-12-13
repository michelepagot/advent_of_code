import re
import itertools

def antinodes(A, B):
    return [tuple([ (2 * B[r]) - A[r] for r in [0,1]]) , tuple([ (2 * A[r]) - B[r] for r in [0,1]])]

with open('input', 'r') as f:
     data = f.readlines()

parsed = {}
data_2d = [[x for x in line.strip()] for line in data]
for row_i, row in enumerate(data_2d):
    print(f"Parse row[{row_i}]={row}")
    for col_i, col in enumerate(row):
        if re.search(r'[a-zA-Z0-9]', col):
            print(f"Parse tail[{row_i}][{col_i}]={col} ")
            if col in parsed:
                print(f"Append to existing freq list {parsed[col]}")
                parsed[col].append((row_i, col_i))
            else:
                print(f"Create new freq list")
                parsed[col] = [(row_i, col_i)]
res = set()
d_rows = len(data_2d)
d_cols = len(data_2d[0])
for p in parsed:
    print(f"-- Antenna freq ['{p}']:{parsed[p]}")
    for x in itertools.combinations(parsed[p], 2):
        print(f"Calculate antinodes for pair {x}")
        for a in antinodes(x[0], x[1]):
            if a[0] >= 0 and a[1] >= 0 and a[0] < d_rows and a[1] < d_cols:
                print(f"Adding antinode {a}")
                res.add(a)
print(f"Solution1 {len(res)}")