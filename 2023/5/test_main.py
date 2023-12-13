import main

def test_decode_almanac():
    lines = [
        "seeds: 79 14 55 13",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "soil-to-fertilizer map:",
        "10 15 37"]
    seed, almanac = main.decode_almanac(lines)
    assert seed == [79, 14, 55, 13]
    assert 'seed-to-soil' in almanac
    assert 'soil-to-fertilizer' in almanac
    assert [[50, 98, 2], [52, 50, 48]] == almanac['seed-to-soil']
    assert [[10, 15, 37]] == almanac['soil-to-fertilizer']


def test_seed_location_one_translation():
    """
    If there's no translators that match the number to translate
    the number itself is the translated number
    """
    assert 42 == main.translate_to_next(42, [[1,1,1]])


def test_seed_location_one_translation_range_one_key():
    """
    Only one translator that has source matching the number to translate
    """
    assert 50 == main.translate_to_next(42, [[50, 42, 1]])
    assert 10 == main.translate_to_next(42, [[10, 42, 1]])


def test_seed_location_two_translation_range():
    """
    translation not directly in source but in range
    """
    assert 50 == main.translate_to_next(42, [[1, 1, 1],[50, 42, 2]])


def test_next_key():
    almanac = {'cane-to-pane': []}
    assert ('cane-to-pane', 'pane') == main.next_key('cane', almanac)


def test_get_list_seeds_one_pair():
    """
    New seed list definition for the part 2
    """
    assert [1, 2, 3, 4, 5] == main.get_list_seeds([1, 5])


def test_get_list_seeds_two_pair():
    """
    New seed list definition for the part 2
    """
    assert [1, 2, 3, 9, 10, 11, 12, 13] == main.get_list_seeds([1, 3, 9, 5])