import re
import itertools

def c_per(a,n):
     if isinstance(n,int):
         return (a[0]*n, a[1]*n)

def c_diff(a,b):
     return (a[0]-b[0], a[1]-b[1])

def c_sum(a,b):
     return (a[0]+b[0], a[1]+b[1])

def antinodes(A, B, M):
    res = []
    V = c_diff(c_per(B,2), A)
    if V[0] >= 0 and V[1] >= 0 and V[0] < M[0] and V[1] < M[1]:
        res.append(V)
    V = c_diff(c_per(A,2), B)
    if V[0] >= 0 and V[1] >= 0 and V[0] < M[0] and V[1] < M[1]:
        res.append(V)
    return res

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
        print(f"    Calculate antinodes for pair {x}")
        for a in antinodes(x[0], x[1], (d_rows, d_cols)):
            print(f"    Adding antinode {a}")
            res.add(a)
print(f"Solution1 {len(res)}")