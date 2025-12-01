"""
Advent of Code 2023 day 5
"""
import sys
import logging
import re
import time

log = logging.getLogger()
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )
log.addHandler(handler)


def main():
    score = [0, 0]
    seeds = []
    this_map = []
    all_maps = []
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        for line in f.readlines():
            log.debug("----- %s -----", line)
            if 'seeds:' in line:
                seeds = [int(s) for s in line[6:].split()]
            elif ' map:' in line:
                log.debug("This map:%s", this_map)
                this_map.clear()
            elif len(line) > 2:
                # destination range start, the source range start, and the range length.
                this_map = [int(v) for v in line.split()[0:3]]
                delta = this_map[0] - this_map[1]
                all_maps.append((this_map[1], 'i', delta))
                all_maps.append((this_map[1] + this_map[2] - 1, 'f', delta))
                all_maps_last_ids = len(all_maps) - 1
                for idx, val in enumerate(all_maps):
                    log.debug("Evaluate element idx:%d val:%s of all_maps:%s all_maps_last_ids:%d",
                              idx, val, all_maps, all_maps_last_ids)
                    if idx < all_maps_last_ids and val[1] == 'i' and all_maps[idx+1][1] == 'f' and val[2] == all_maps[idx+1][2]:
                        log.debug("val:%s is in the right place", val)
                    else:
                        log.debug("val:%s is NOT in the right place in respect to the next:%s", val, all_maps[idx+1])

                log.debug("range:%s all_maps:%s",
                          this_map,
                          all_maps)

        log.debug("seeds:%s", seeds)
    print("Part1:" + str(score[0]))
    print("Part2:" + str(score[1]))


if __name__ == "__main__":
    main()
