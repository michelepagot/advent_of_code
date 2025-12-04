import time
import sys
import statistics

from utils import (
    solve as solve_serial,
    solve1 as solve_serial1,
    solve_pool_map,
    solve_pool_imap_unordered,
)


def bench(func, input_str: str, runs: int = 3):
    # warmup
    _ = func(input_str)
    times = []
    out = None
    for _ in range(runs):
        t0 = time.perf_counter()
        out = func(input_str)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    mn = min(times)
    avg = sum(times) / len(times)
    std = statistics.stdev(times) if len(times) > 1 else 0.0
    return mn, avg, std, out


def main(path: str):
    with open(path, "r") as f:
        s = f.read()

    tests = [
        ("serial", solve_serial),
        ("serial1", solve_serial1),
        ("pool_map", solve_pool_map),
        ("pool_imap_unordered", solve_pool_imap_unordered),
    ]

    for name, fn in tests:
        print(f"Running: {name}")
        mn, avg, std, out = bench(fn, s, runs=5)
        print(f"{name}: out={out} min={mn:.6f}s avg={avg:.6f}s std={std:.6f}s")


if __name__ == "__main__":
    path = "input.txt"
    if len(sys.argv) > 1:
        path = sys.argv[1]
    main(path)
