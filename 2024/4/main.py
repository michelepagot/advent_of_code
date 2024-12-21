import sys

def solution1(data):
    count =0
    r_l=len(data)
    for r in range(r_l):
        c_l=len(data[r])
        for c in range(c_l):
            print(f"Origin:{(r,c)}")
            word = ""
            if c < c_l-3:
                for xc in range(c,c+4):
                    word += data[r][xc]
                print(f"Horizontal Righ:{word}")
                if word == "XMAS" or word == "SAMX":
                    count += 1
                    print(f"Found:{count}")
            word =""
            if r < r_l-3:
                for yr in range(r,r+4):
                    word += data[yr][c]
                print(f"Vertical Down:{word}")
                if word == "XMAS" or word == "SAMX":
                    count += 1
                    print(f"Found:{count}")
            word=""
            if r < r_l-3 and c<c_l-3:
                for delta in range(0,4):
                    word += data[r+delta][c+delta]
                print(f"Diagonal Right Down:{word}")
                if word == "XMAS" or word == "SAMX":
                    count += 1
                    print(f"Found:{count}")
            word=""
            if r < r_l-3 and c>=delta:
                for delta in range(0,4):
                    word += data[r+delta][c-delta]
                print(f"Diagonal Left Down:{word}")
                if word == "XMAS" or word == "SAMX":
                    count += 1
                    print(f"Found:{count}")
    return count

def solution2(m):
    count =0
    r_l=len(m)
    for r in range(r_l):
        c_l=len(m[r])
        for c in range(c_l):
            print(f"Origin:{(r,c)}")
            word=""
            if r < r_l - 2 and c < c_l - 2 and m[r+1][c+1] == "A":
                word = m[r][c] + m[r][c+2] + m[r+2][c] + m[r+2][c+2]
            print(f"--{word}--")
            if word == "MMSS" or word == "SMSM" or word == "SSMM" or word == "MSMS":
                count += 1
                print(f"Found:{count}")
    return count

def main(input_file):
    with open(input_file, 'r') as f:
        data=[d.strip() for d in f.readlines()]
    print(f"data:{data}")
    return (solution1(data), solution2(data))

if __name__ == "__main__":
    res = main(sys.argv[1])
    print(f"Part1:{res[0]}")
    print(f"Part2:{res[1]}")