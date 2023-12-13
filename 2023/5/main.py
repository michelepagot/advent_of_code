"""
Advent of Code 2023 day 5
"""
import sys
import logging
import re
import time

log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )
log.addHandler(handler)


class Almanac():
    """
    Get input.txt, decode it and create a friendly usable representation for it.
    It is more targeted for part2
    """

    def __init__(self, lines) -> None:
        self.seeds = None
        # Two different representations of the same data
        self.translators = {}
        self.translators_boundary = {}
        
        # regexp to read the first line of the file: the list of seeds
        re_seeds = re.compile(r'seeds: ([\d\s]+)')

        # regexp to get all the maps titles
        re_map_title = re.compile(r'([a-z]+-to-[a-z]+) map:')

        # regexp to get all the maps
        re_maps = re.compile(r'^(\d+) (\d+) (\d+)', re.MULTILINE)

        # input parsing
        log.debug("Almanac::len(lines)=%d", len(lines))
        for line in lines:
            log.debug("Almanac::line:%s", line.strip())
            if self.seeds is None:
                match = re_seeds.search(line)
                if match:
                    self.seeds = [int(x) for x in match.group(1).split()]
                    # this is the format needed for part2
                    # part2 always has even number of seeds
                    if (len(self.seeds) % 2) ==0:
                        self.seed_ranges = [(self.seeds[i], self.seeds[i+1]) for i in range(0, len(self.seeds), 2)]
                    log.debug("Almanac::seeds:%s", self.seeds)
                    continue
            match_title = re_map_title.search(line)
            if match_title:
                log.debug("Almanac::-- match_title --")
                map_title = match_title.group(1)
                log.debug("Almanac::map_title:%s", map_title)
                if map_title not in self.translators:
                    self.translators[map_title] = []
                    self.translators_boundary[map_title] = []
                continue
            match_maps = re_maps.search(line)
            if match_maps:
                log.debug("Almanac::-- match_maps --")
                destination_range = int(match_maps.group(1))
                source_range = int(match_maps.group(2))
                range_length = int(match_maps.group(3))
                log.debug("Almanac::destination_range:%s source_range:%s range_length:%s",
                      destination_range, source_range, range_length)
                self.translators[map_title].append([destination_range, source_range, range_length])
                self.translators_boundary[map_title].append(map_format_i2b([destination_range, source_range, range_length]))

    def get_translator_name(self, name, direction=True):
        """
        Giving a string as input, it looks for the translators key
        that match for it and return (<KEY_THAT_MATCH>, <NEXT_ELEMENT>)

        Let say this almanac has translators with these keys:
          - 'seed-to-soil'
          - 'soil-to-fertilizer'
          - 'fertilizer-to-water'

        almanac.get_translator_name('soil') return ('soil-to-fertilizer', 'fertilizer')

        almanac.get_translator_name('soil', False) return ('seed-to-soil', 'seed')

        almanac.get_translator_name('miocuggino', False) return None
        """
        if direction:
            re_key = re.compile(rf'{name}-to-(.*)')
        else:
            re_key = re.compile(rf'(.*)-to-{name}')
        log.debug("re_key:%s", re_key)
        for k in self.translators:
            match = re_key.search(k)
            log.debug("k:%s  match:%s", k, match)
            if match:
                return k, match.group(1)
        return None, None
    
    def is_seed(self, seed, part=1):
        """
        Determine is a seed number is a valid seed, one of them listed
        in the first line of the input.
        First line of the input is interpreted as Part1 or Part2
        """
        if part == 1:
            return seed in self.seeds
        elif part == 2:
            for r in self.seed_ranges:
                log.debug("Check if seed %s is included in range %s", seed, r)
                if seed >= r[0] and seed <= (r[0] + r[1] -1):
                    return True
            return False
        log.error("Part:%s is not valid. Only 1 and 2 supported", part)
        return False


    def reverse(self, start_element_name, start_element):
        """
        given start_element_name='something' and start_element=N, possibly return a seed id 
        starting from element N of type 'something'.
        So this function should search for translator 'somethingelse-to-something',
        and using its ranges, finds the 'somethinngelse' M that is associated to the 'something' N
        The reverse search stop at seed.
        The function returns a seed id, but does not verify if it is an existing one 
        """
        next_element_name = start_element_name
        next_element_value = start_element
        log.debug("start_element_name:%s start_element:%d", start_element_name, start_element)
        while True:
            current_key, next_element_name = self.get_translator_name(next_element_name, False)
            log.debug("current_key:%s next_element_name:%s ", current_key, next_element_name)

            if current_key is None:
                log.debug("next_element_name:%s   END OF THE WORLD", next_element_name)
                return None

            # loop through all ranges that are associated to translator where to try to jump back
            log.debug("Find a matching range in translators['%s']:%s for the next_element_value:%d",
                      current_key, self.translators[current_key], next_element_value)
            for r in self.translators[current_key]:
                log.debug("Try r:%s", r)
                if match_range(next_element_value, r, False):
                    log.debug("next_element_value:%d match in range:%s delta:%d",
                              next_element_value, r, (r[1] - r[0]))
                    next_element_value += (r[1] - r[0])
                    log.debug("New next_element_value:%d", next_element_value)
                    break
            log.debug("next_element_name:%s next_element_value:%d",
                      next_element_name, next_element_value)
            if next_element_name == 'seed':
                return next_element_value


def vertical_slices(input):
    """
    Input is a list of many [<SOURCE_START>, <SOURCE_END>, ...]

    e.g. [[3,6], [9,9], [1,5], [8,10], [5,6]]

    line1 | . . . 3 - - 6 . . . .
    line2 | . . . . . . . . . 9 .
    line3 | . 1 - - - 5 . . . . .
    line4 | . . . . . . . . 8 - 10
    line5 | . . . . . 5 6 . . . .

    Output is [1,3,5,6,8,9,10] all the different boundary
    """
    ret = set()
    log.error("vertical_slices:: input=%s", input)
    for i in input:
        ret.add(i[0])
        ret.add(i[1])
    return sorted(set(ret))


def vertical_slices_sum_gain(input):
    """
    Input is a list of multiple ranges [<SOURCE_START>, <SOURCE_END>, <DELTA>]
    """
    res = []
    log.error("vertical_slices_sum_gain:: input=%s", input)
    for this_new_range in  input:
        log.error("vertical_slices_sum_gain:: process this_new_range=%s and add it to res=%s", this_new_range, res)
        if len(res) == 0:
            res.append(this_new_range)
            continue

        if this_new_range[1] < res[0][0]:
            res.insert(0, this_new_range)
            continue

        if this_new_range[0] > res[-1][1]:
            res.append(this_new_range)
            continue
    return res


def range_in_ranges(new_range=[], ranges=[]):
    """
    Input a set of 
    """
    if len(new_range) == 0:
        log.info("range_in_ranges::Nothing to insert in new_range:%s, return the existing ranges %s", new_range, ranges)
        return ranges
    if len(ranges) == 0:
        log.info("range_in_ranges::Nothing in ranges %s. Initialize it with the new_range:%s", ranges, new_range)
        return  [new_range]
    if new_range[1] < ranges[0][0]:
        return ranges.insert(0, new_range)
    return None

def map_format_i2b(i_range):
    """
    Translate from two different ranges rappresentations, from the one used in input to another one

    [<DESTINATION>, <SOURCE>, <LENGTH>] --> [<SOURCE_START>, <SOURCE_END>, <DELTA>]
    """
    return [i_range[1], i_range[1]+i_range[2]-1, i_range[0]-i_range[1]]


def match_range(number, range_space, direction=True):
    """
    Given a number and a range using the same convention used in input file
    check if the number belong to the range.

    Some examples:
        match_range(42, [99, 42, 1])  --> True
        match_range(43, [99, 42, 1])  --> False as here starting point is 42 and range is only 1 wide
        match_range(43, [99, 42, 2])  --> True
        match_range(99, [99, 42, 1])  --> False  as 99 in range convention is the destination
        match_range(99, [99, 42, 1], False)  --> True as direction=False enable opposite range interpretation
    """
    if direction:
        start = range_space[1]
    else:
        start = range_space[0]
    return number >= start and number < (start + range_space[2])


def get_lower_range(ranges):
    """
    Given a list of ranges return the one that is about lower number range

    get_lower_range([[12, 3, 6], [1, 33, 42], [7, 0, 0], [11, 3, 6]])  --> [1,33,42]
    """
    return sorted(ranges)[0]


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
    for k in almanac:
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
        log.debug("get_list_seeds --> start:%s length:%s", start, length)
        
        # For the moment comment it as this strategy is not ok, it result in a too long list
        # ret += [seed + start for seed in range(seeds[idx_length])]

        # Just estimate how bad it is
        tot += length

    log.debug("number of seeds for the part2 --> %s", tot)
    return tot

def main():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        score = [None, 0]
        a = Almanac(f.readlines())

        log.debug("almanac:%s", a)
        locations = []
        log.info("Number of seeds for the part1 %d", len(a.seeds))

        t0 = time.time()
        for seed in a.seeds:
            current_key = 'seed'
            current_value = seed
            while current_key != 'location':
                log.debug("START --> current_key:%s current_value:%s", current_key, current_value)
                this_key, current_key = next_key(current_key, a.translators)
                log.debug("this_key:%s  current_key:%s", this_key, current_key)
                current_value = translate_to_next(current_value, a.translators[this_key])
                log.debug("END --> current_key:%s current_value:%s", current_key, current_value)
            locations.append(current_value)
        t1 = time.time()
        print(f"Time per seed:{(t1-t0)/len(a.seeds)}")
        part2_seeds_num = get_list_seeds(a.seeds)
        print(f"Estimated time for the part2 that has {part2_seeds_num} seeds --> {((t1-t0)/len(a.seeds))*part2_seeds_num}")
        #for key, value in almanac.items():
        #    print(key, len(value), sum([x[2] for x in value]), [x[0] for x in value] )
        score[0] = min(locations)

        print('-'*30)
        print(a.translators[[k for k in a.translators if 'location' in k][0]])
        lr = get_lower_range(a.translators[[k for k in a.translators if 'location' in k][0]])
        print(f"Explore before the lower location from 0 to {lr[0]}")
        for loc in range(0, lr[0]):
            rev_seed = a.reverse('location', loc)
            print(f"rev_seed:{rev_seed}")
            if rev_seed is not None and rev_seed >= 55:
                print(f"Reverse seed for location:{loc}  --> {rev_seed}")
                score[1] = rev_seed
                break

        print('-'*30)
        print(f"Lower 'location' range is {lr} and range is {[x for x in range(lr[0], lr[0] + lr[2])]}")
        for loc in range(lr[0], lr[0] + lr[2]):
            rev_seed = a.reverse('location', loc)
            print(f"rev_seed:{rev_seed}")
            if rev_seed is not None:
                print(f"Reverse seed for location:{loc}  --> {rev_seed}")
                score[1] = rev_seed
                break
        print(a.seeds)
    print("Part1:" + str(score[0]))
    print("Part2:" + str(score[1]))


if __name__ == "__main__":
    main()
