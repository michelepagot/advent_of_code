import logging
log = logging.getLogger(__name__)


def solve(input_str: str) -> [int, int]:
    p = [0, 0]
    for line in input_str.strip().splitlines():
        xl = [int(i) for i in line]
        xli = xl.index(max(xl[:-1]))
        res = xl[xli] * 10 + max(xl[xli+1:]) 
        #log.error("Processing line: %s max:%d at %d ... %s --> res:%d",
        #           line, xl[xli], xli, xl[xli+1:],res)
        p[0] += xl[xli] * 10 + max(xl[xli+1:])
        
    return p

