"""
Advent of Code 2023 day 5
"""
import sys
import logging
import re

log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )
log.addHandler(handler)


def decode_almanac(lines):
    """
    From input text to seed list and almanac dict
    """
    almanac = {}
    seeds = None
    # regexp to read the first line of the file, the list of seeds
    re_seeds = re.compile(r'seeds: ([\d\s]+)')

    # regexp to get all the maps titles
    re_map_title = re.compile(r'([a-z]+-to-[a-z]+) map:')

    # regexp to get all the maps
    re_maps = re.compile(r'^(\d+) (\d+) (\d+)', re.MULTILINE)
    for line in lines:
        log.debug("line:%s", line.strip())
        if seeds is None:
            match = re_seeds.search(line)
            if match:
                seeds = [int(x) for x in match.group(1).split()]
                log.debug("seeds:%s", seeds)
                continue
        match_title = re_map_title.search(line)
        if match_title:
            log.debug("-- match_title --")
            map_title = match_title.group(1)
            log.debug("map_title:%s", map_title)
            if map_title not in almanac:
                almanac[map_title] = []
            continue
        match_maps = re_maps.search(line)
        if match_maps:
            log.debug("-- match_maps --")
            destination_range = int(match_maps.group(1))
            source_range = int(match_maps.group(2))
            range_length = int(match_maps.group(3))
            log.debug("destination_range:%s source_range:%s range_length:%s",
                      destination_range, source_range, range_length)
            almanac[map_title].append([destination_range, source_range, range_length])
    return seeds, almanac


def translate_to_next(value, translators):
    """
    Giving a list of ranges, the one usually associated to an almanac element,
    translate a value
    """
    for translator in translators:
        stop = translator[1] + translator[2]
        log.debug('translator:%s value:%s start:%s stop:%s', translator, value, translator[1], stop)
        if translator and value >= translator[1] and value < stop:
            return value + translator[0] - translator[1]
    return value


def next_key(key, almanac):
    """
    Giving an almanac and a key, 
    search for the right almanac section title like `seed-to-something`
    and get the key of the next section, that in this example is `something`
    """
    for k in almanac.keys():
        match = re.search(rf'{key}-to-(.*)', k)
        if match:
            return k, match.group(1)
    return '', ''


def get_list_seeds(seeds):
    """
    New seed list decoder for the part 2
    """
    tot = 0
    for idx in range(int(len(seeds)/2)):
        start = seeds[idx*2]
        length = seeds[1+idx*2]
        log.debug("get_list_seeds --> staret:%s length:%s", start, length)
        
        # For the moment comment it as this strategy is not ok, it result in a too long list
        # ret += [seed + start for seed in range(seeds[idx_length])]

        # Just estimate how bad it is
        tot += length      

    log.debug("number of seeds for the part2 --> %s", tot)
    return tot


def main():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        score = [None, 0]
        seeds, almanac = decode_almanac(f.readlines())
        log.debug("almanac:%s", almanac)
        locations = []
        log.info("Number of seeds for the part1 %d", len(seeds))
        import time
        t0 = time.time()
        for seed in seeds:
            current_key = 'seed'
            current_value = seed
            while(current_key != 'location'):
                log.debug("START --> current_key:%s current_value:%s", current_key, current_value)
                this_key, current_key = next_key(current_key, almanac)
                log.debug("this_key:%s  current_key:%s", this_key, current_key)
                current_value = translate_to_next(current_value, almanac[this_key])
                log.debug("END --> current_key:%s current_value:%s", current_key, current_value)
            locations.append(current_value)
        t1 = time.time()
        print(f"Time per seed:{(t1-t0)/len(seeds)}")
        part2_seeds_num = get_list_seeds(seeds)
        print(f"Estimated time for the part2 that has {part2_seeds_num} seeds --> {((t1-t0)/len(seeds))*part2_seeds_num}")
        #for key, value in almanac.items():
        #    print(key, len(value), sum([x[2] for x in value]), [x[0] for x in value] )
        score[0] = min(locations)
    print("Part1:" + str(score[0]))
    print("Part2:" + str(score[1]))


if __name__ == "__main__":
    main()