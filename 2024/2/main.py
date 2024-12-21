import sys

def valid_1(deltas):
    all_positive = all(d>0 for d in deltas)
    all_negative = all(d<0 for d in deltas)
    all_small = all(abs(d)<=3 for d in deltas)
    #print(f"[valid_1] deltas:{deltas} all_positive:{all_positive} all_negative:{all_negative} all_small:{all_small}")
    if ((not all_positive) and (not all_negative)) or (not all_small):
        return False
    return True

def valid_2(l):
    for i_skip, _ in enumerate(l):
        l_skip = [v for i, v in enumerate(l) if i_skip != i]
        deltas_skip = [(v-l_skip[i-1]) for i, v in enumerate(l_skip) if i > 0]
        all_positive = all(d>0 for d in deltas_skip)
        all_negative = all(d<0 for d in deltas_skip)
        all_small = all(abs(d)<=3 for d in deltas_skip)
        print(f"i_skip:{i_skip}  l_skip:{l_skip}  deltas_skip:{deltas_skip} all_positive:{all_positive} all_negative:{all_negative} all_small:{all_small}")
        if (all_positive or all_negative) and all_small:
            return True
    return False

def main(input_file):
    with open(input_file, 'r') as f:
        data=[[int(n) for n in row.strip().split(' ')] for row in f.readlines()]
  
    print(f"data:{data}")
    score_1 = 0
    score_2 = 0
    for l in data:
        ok_1 = 1
        ok_2 = 1
        deltas = [(v-l[i-1]) for i, v in enumerate(l) if i > 0]
        if (not valid_1(deltas)):
            print(f"NOK 1 l:{l}")
            ok_1 = 0
            if not valid_2(l):
                print("NOK 2")
                ok_2 = 0
        score_1 += ok_1
        score_2 += ok_2

    return (score_1, score_2)

if __name__ == "__main__":
    res = main(sys.argv[1])
    print(f"Part1:{res[0]}")
    print(f"Part2:{res[1]}")