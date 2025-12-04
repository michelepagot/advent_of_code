import logging
log = logging.getLogger(__name__)

def rotate(size: int, start: int, move: int) -> (int, int):
    log.debug(f"rotate::size:{size} start:{start} move:{move}")
    if move == 0:
        return start, 0
    amove = abs(move)
    if amove % size == 0:
        return start, amove // size
    rot = amove // size
    mod = amove % size
    if move > 0:
        dest = start + mod
        if dest < size:
            return dest, rot
        if dest % size == 0:
            return 0, rot
        return dest % size, rot + 1
    if move < 0:
        dest = start - mod
        if dest >= 0:
            return dest, rot
        if dest < 0:
            if start != 0:
                rot += 1
            return size + dest, rot


def solve(input_str: str, start: int) -> [int, int]:
    p = [0, 0]
    s = start
    for m in [line for line in input_str.splitlines()]:
        move = int(m[1:])
        if move == 0:
            continue
        if "L" == m[0]:
            move *= (-1)
        log.debug(f"solve::rotate(100,s:{s} move:{move}) <-- p:{p}")
        (s, c) = rotate(100, s, move)
        log.debug("solve::s:%s,c:%s",s,c)
        if s == 0:
            p[0] += 1
            p[1] += 1
        p[1] += c
        log.debug(f"solve::s:{s} c:{c} -->p:{p}")
    return p

