import logging
log = logging.getLogger(__name__)
from multiprocessing import Pool, cpu_count


def is_invalid_part1(i: int) -> bool:
    #log.error("is_valid_part1:%s", i)
    numero = str(i)
    l = len(numero)
    if l % 2 :
        #log.error("is_valid_part1:%s:len_odd", i)
        return False
    half = l // 2
    return numero[0:half] == numero[half:]


def is_invalid_part2(i: int) -> bool:
    #log.error("is_invalid_part2:%s", i)
    numero = str(i)
    l = len(numero)
    for r in range(l // 2,0,-1):
        #log.error("is_valid_part2: r:%d l mod r:%d", r, l % r)
        if l % r != 0:
            continue
        #log.error("is_valid_part2: r:%d l//r:%d :: '%s' :: '%s'",
        #          r, l//r,
        #          numero[0:r], numero[0:r]*(l//r))
        if numero[0:r]*(l//r) == numero:
            #log.error("is_invalid_part2: True for i:%s", i)
            return True
    return False


def is_invalid_part1_str(numero: str) -> bool:
    """Like `is_invalid_part1` but accepts the string form to avoid
    repeated `str()` conversions when checking both rules for the same id.
    """
    l = len(numero)
    if l % 2:
        return False
    half = l // 2
    return numero[0:half] == numero[half:]


def is_invalid_part2_str(numero: str) -> bool:
    """Like `is_invalid_part2` but accepts the string form.
    Iterates factors of the length and checks for periodic repetition.
    """
    l = len(numero)
    for r in range(l // 2, 0, -1):
        if l % r != 0:
            continue
        if numero[0:r] * (l // r) == numero:
            return True
    return False


def find_invalids(id_range: [int, int]) -> [[int], [int]]:
    #log.error("find_invalids_part2:%s", id_range)
    res =  ([],[])
    for i in range(id_range[0], id_range[1]+1):
        if is_invalid_part1(i):
            res[0].append(i)
        if is_invalid_part2(i):
            res[1].append(i)
    return res


def find_invalids_sums(id_range: [int, int]) -> [int, int]:
    """Return the sums of invalid ids for part1 and part2 in the range.

    This avoids creating lists of all invalid ids and therefore reduces
    memory pressure and allocation overhead.
    """
    s1 = 0
    s2 = 0
    # Local refs to avoid global lookups in the loop
    _is1 = is_invalid_part1_str
    _is2 = is_invalid_part2_str
    start, end = id_range
    for i in range(start, end + 1):
        numero = str(i)
        if _is1(numero):
            s1 += i
        if _is2(numero):
            s2 += i
    return [s1, s2]


def solve_pool_map(input_str: str, processes: int | None = None) -> [int, int]:
    """Parallel implementation using `Pool.map`.

    Each `id_range` is processed in parallel by `find_invalids` and
    results are aggregated. `processes=None` lets Pool choose `cpu_count()`.
    """
    id_ranges = [(int(r[0]), int(r[1])) for r in [p.split('-') for p in input_str.strip().split(',')]]
    invalids_part1 = []
    invalids_part2 = []
    # Use Pool.map to run find_invalids across ranges in parallel
    with Pool(processes=processes) as p:
        results = p.map(find_invalids, id_ranges)

    for res in results:
        invalids_part1.extend(res[0])
        invalids_part2.extend(res[1])

    return [sum(invalids_part1), sum(invalids_part2)]


def solve_pool_imap_unordered(input_str: str, processes: int | None = None) -> [int, int]:
    """Parallel implementation using `Pool.imap_unordered`.

    This version collects results as they finish and may reduce latency
    when ranges have uneven workloads.
    """
    id_ranges = [(int(r[0]), int(r[1])) for r in [p.split('-') for p in input_str.strip().split(',')]]
    invalids_part1 = []
    invalids_part2 = []
    with Pool(processes=processes) as p:
        for res in p.imap_unordered(find_invalids, id_ranges):
            invalids_part1.extend(res[0])
            invalids_part2.extend(res[1])

    return [sum(invalids_part1), sum(invalids_part2)]


def solve(input_str: str) -> [int, int]:
    #log.error("solve:%s", input_str)
    id_ranges = [(int(r[0]), int(r[1])) for r in [p.split('-') for p in input_str.strip().split(',')]]
    invalids_part1 = []
    invalids_part2 = []
    for r in id_ranges:
        res = find_invalids(r)
        invalids_part1 += res[0]
        invalids_part2 += res[1]
    return [sum(invalids_part1),sum(invalids_part2)]

def solve1(input_str: str) -> [int, int]:
    #log.error("solve:%s", input_str)
    id_ranges = [(int(r[0]), int(r[1])) for r in [p.split('-') for p in input_str.strip().split(',')]]
    invalids_part1 = 0
    invalids_part2 = 0
    for r in id_ranges:
        s1, s2 = find_invalids_sums(r)
        invalids_part1 += s1
        invalids_part2 += s2
    return [invalids_part1, invalids_part2]
