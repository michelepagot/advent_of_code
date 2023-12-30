import pytest
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


def test_almanac_decoding_class_seeds():
    lines = [
        "seeds: 79 14 55 13",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "soil-to-fertilizer map:",
        "10 15 37"]
    a = main.Almanac(lines)
    assert a.seeds == [79, 14, 55, 13]


def test_almanac_is_seed():
    lines = ["seeds: 79 10 55 13"]
    a = main.Almanac(lines)

    # For both part1 and part2 ...
    assert a.is_seed(79) == True
    assert a.is_seed(79, 2) == True

    assert a.is_seed(80) == False
    assert a.is_seed(79, 2) == True
    assert a.is_seed(88, 2) == True
    assert a.is_seed(89, 2) == False
    assert a.is_seed(55) == True
    assert a.is_seed(56) == False
    assert a.is_seed(56,2) == True


def test_almanac_decoding_class_only_care_first_seeds_line():
    """
    Not to regexp all the lines for `seeds:` string
    it is only done once
    """
    lines = [
        "seeds: 79 14 55 13",
        "seeds: 7 1 5 3"
        ]
    a = main.Almanac(lines)
    assert a.seeds == [79, 14, 55, 13]


def test_almanac_decoding_class_translators():
    lines = [
        "seeds: 79 14 55 13",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "soil-to-fertilizer map:",
        "10 15 37"]
    almanac = main.Almanac(lines)
    assert 'seed-to-soil' in almanac.translators
    assert 'soil-to-fertilizer' in almanac.translators


def test_almanac_decoding_class_translators_ranges():
    """
    File representation for ranges is
    <DESTINATION> <SOURCE> <RANGE_LENGTH>

    So for example 

    50 98 4

    means that
    98  --> 50
    99  --> 51
    100 --> 52
    101 --> 53

    Is there a better way to represent it?

    Maybe [(98,101), (50,53)] 

    It is just 4 vs 3 int long.
    """
    lines = [
        "seeds: 79 14 55 13",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "soil-to-fertilizer map:",
        "10 15 37"]
    almanac = main.Almanac(lines)
    assert [[50, 98, 2], [52, 50, 48]] == almanac.translators['seed-to-soil']
    assert [[10, 15, 37]] == almanac.translators['soil-to-fertilizer']


def test_almanac_get_translator_name():
    lines = [
        "seeds: 79 14 55 13",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "soil-to-fertilizer map:",
        "10 15 37"]
    almanac = main.Almanac(lines)
    assert almanac.get_translator_name('soil') == ('soil-to-fertilizer', 'fertilizer')
    assert almanac.get_translator_name('soil', False) == ('seed-to-soil', 'seed')
    assert almanac.get_translator_name('miocuggino') == (None, None)


def test_almanac_reverse_reading():
    """
    Go from last translator, back to 'seed'.

    For the following almanac, the forward path is:

    seed 0 --> soil 5 --> fertilizer 10 --> water 15

    Is it possible, giving water 15, get back seed 0?
    """
    lines = [
        "seeds: 0",
        "seed-to-soil map:",
        "5 0 1",
        "soil-to-fertilizer map:",
        "10 5 1",
        "fertilizer-to-water map:",
        "15 10 1"]
    almanac = main.Almanac(lines)
    assert 0 == almanac.reverse('water', 15)


def test_almanac_reverse_reading_in_range():
    """
    Go from last translator, back to 'seed'.

    For the following almanac, the forward path is:

    seed 3 --> soil 5 --> fertilizer 10 --> water 15

    Is it possible, giving water 15, get back seed 0?
    """
    lines = [
        "seeds: 0",
        "seed-to-soil map:",
        "5 0 4",
        "soil-to-fertilizer map:",
        "12 5 1",
        "fertilizer-to-water map:",
        "15 10 3"]
    almanac = main.Almanac(lines)
    assert 0 == almanac.reverse('water', 17)


def test_almanac_reverse_reading_start_from_the_middle():
    """
    Go from last translator, back to 'seed'.

    For the following almanac, the forward path is:

    seed 0 --> soil 5 --> fertilizer 10 --> water 15

    Is it possible, giving fertilizer 10, get back seed 0?
    """
    lines = [
        "seeds: 0",
        "seed-to-soil map:",
        "5 0 1",
        "soil-to-fertilizer map:",
        "10 5 1",
        "fertilizer-to-water map:",
        "15 10 1"]
    almanac = main.Almanac(lines)
    assert 0 == almanac.reverse('fertilizer', 10)


def test_almanac_reverse_reading_no_in_any_range():
    """
    Go from last translator, back to 'seed'

    for the following almanac the FW path is

    seed 0 --> soil 0 --> fertilizer 0 --> water 0

    Is it possible, giving fertilizer 0 get back seed 0?
    """
    lines = [
        "seeds: 0",
        "seed-to-soil map:",
        "5 42 1",
        "soil-to-fertilizer map:",
        "10 5 1",
        "fertilizer-to-water map:",
        "15 10 1"]
    almanac = main.Almanac(lines)
    assert 0 == almanac.reverse('water', 0)


def test_almanac_reverse_reading_no_first_range():
    """
    Go from last translator, back to 'seed'.

    For the following almanac, the forward path is:

    seed 0 --> soil 0 --> fertilizer 10 --> water 15

    Is it possible, giving water 15, get back seed 0?
    """
    lines = [
        "seeds: 0",
        "seed-to-soil map:",
        "5 42 1",
        "soil-to-fertilizer map:",
        "10 0 1",
        "fertilizer-to-water map:",
        "15 10 1"]
    almanac = main.Almanac(lines)
    assert 0 == almanac.reverse('water', 15)


def test_almanac_reverse_reading_no_last_range():
    """
    Go from last translator, back to 'seed'.

    For the following almanac, the forward path is:

    seed 0 --> soil 5 --> fertilizer 10 --> water 10

    Is it possible, giving water 10, get back seed 0?
    """
    lines = [
        "seeds: 0",
        "seed-to-soil map:",
        "5 0 1",
        "soil-to-fertilizer map:",
        "10 5 1",
        "fertilizer-to-water map:",
        "15 42 1"]
    almanac = main.Almanac(lines)
    assert 0 == almanac.reverse('water', 10)


def test_almanac_reverse_reading_not_existing_starting_point():
    """
    Go from last translator, back to 'seed'

    for the following almanac the FW path is

    seed 0 --> soil 5 --> fertilizer 10

    Is it possible, giving fertilizer 10 get back seed 0?
    """
    lines = [
        "seeds: 0",
        "seed-to-soil map:",
        "5 0 1",
        "soil-to-fertilizer map:",
        "10 5 1"]
    almanac = main.Almanac(lines)
    assert None == almanac.reverse('miocuggino', 10)


def test_match_range_source():
    assert main.match_range(42, [99, 42, 1]) == True


def test_match_range_source_fail():
    assert main.match_range(43, [99, 42, 1]) == False


def test_match_range_source_match_in_the_tail():
    assert main.match_range(43, [99, 42, 3]) == True
    assert main.match_range(44, [99, 42, 3]) == True
    assert main.match_range(45, [99, 42, 3]) == False


def test_match_range_source_reverse():
    assert main.match_range(99, [99, 42, 1]) == False
    assert main.match_range(99, [99, 42, 1], False) == True


def test_match_range_source_reverse_in_the_tail():
    assert main.match_range(99, [99, 42, 3], False) == True
    assert main.match_range(100, [99, 42, 3], False) == True
    assert main.match_range(101, [99, 42, 3], False) == True
    assert main.match_range(102, [99, 42, 3], False) == False


def test_get_lower_range():
    assert main.get_lower_range([[12, 3, 6], [1, 33, 42], [7, 0, 0], [11, 3, 6]]) == [1,33,42]


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


@pytest.mark.skip(reason="Temporary the impleemntation has been changed to evaluate performance")
def test_get_list_seeds_one_pair():
    """
    New seed list definition for the part 2
    """
    assert [1, 2, 3, 4, 5] == main.get_list_seeds([1, 5])

@pytest.mark.skip(reason="Temporary the impleemntation has been changed to evaluate performance")
def test_get_list_seeds_two_pair():
    """
    New seed list definition for the part 2
    """
    assert [1, 2, 3, 9, 10, 11, 12, 13] == main.get_list_seeds([1, 3, 9, 5])

def test_map_format_i2b():
    """
    [<DESTINATION>, <SOURCE>, <LENGTH>] --> [<SOURCE_START>, <SOURCE_END>, <DELTA>]
    """
    assert main.map_format_i2b([10, 0, 1]) == [0, 0, 10]
    assert main.map_format_i2b([0, 10, 1]) == [10, 10, -10]
    assert main.map_format_i2b([10, 0, 5]) == [0, 4, 10]


def test_vertical_slices():
    """
    Input is a list of many [<SOURCE_START>, <SOURCE_END>]

    e.g. [[3,6], [9,9], [1,5], [8,10], [5,6]]

    line1 | . . . 3 - - 6 . . . .
    line2 | . . . . . . . . . 9 .
    line3 | . 1 - - - 5 . . . . .
    line4 | . . . . . . . . 8 - 10
    line5 | . . . . . 5 6 . . . .

    Output is [1,3,5,6,8,9,10]
    """
    assert main.vertical_slices([[3,6], [9,9], [1,5], [8,10], [5,6]]) == [1,3,5,6,8,9,10]

def test_vertical_slices_sum_gain_detached_two():
    """
    Input [[3,6,10], [9,9,-7]]

    line1 | . . . 3 - - 6 . . . .
    line2 | . . . . . . . . . 9 .
    
    Output is [[3,6,10], [9,9,-7]]
    """
    assert main.vertical_slices_sum_gain([[3,6,10], [9,9,-7]]) == [[3,6,10], [9,9,-7]]

def test_vertical_slices_sum_gain_detached_three_order():
    """
    Input [[1,2,10], [3,5,-7], [7,9,2]]

    line1 | . 1 2 . . . . . . . .
    line2 | . . . . 3 - 5 . . . .
    line3 | . . . . . . . . 7 - 9
    
    Output is [[1,2,10], [3,5,-7], [7,9,2]]
    """
    assert main.vertical_slices_sum_gain([[1,2,10], [3,5,-7], [7,9,2]]) == [[1,2,10], [3,5,-7], [7,9,2]]

def test_vertical_slices_sum_gain_detached_three_inverted_order():
    """
    Input [[7,9,2], [3,5,-7], [1,2,10]]

    line1 | . . . . . . . . 7 - 9
    line2 | . . . . 3 - 5 . . . .
    line3 | . 1 2 . . . . . . . .
    
    Output is [[1,2,10], [3,5,-7], [7,9,2]]
    """
    assert main.vertical_slices_sum_gain([[7,9,2], [3,5,-7], [1,2,10]]) == [[1,2,10], [3,5,-7], [7,9,2]]

def test_vertical_slices_sum_gain_detached_three_interleaved_order():
    """
    Input [[1,2,10], [7,9,2], [3,5,-7]]

    line1 | . 1 2 . . . . . . . .
    line2 | . . . . . . . . 7 - 9
    line3 | . . . . 3 - 5 . . . .
    
    Output is [[1,2,10], [3,5,-7], [7,9,2]]
    """
    assert main.vertical_slices_sum_gain([[1,2,10], [7,9,2], [3,5,-7]]) == [[1,2,10], [3,5,-7], [7,9,2]]

def test_vertical_slices_sum_gain_consecutive():
    """
    Input [[3,6,10], [7,9,-7]]

    line1 | . . . 3 - - 6 . . . .
    line2 | . . . . . . . 7 - 9 .
    
    Output is [[3,6,10], [7,9,-7]]
    """
    assert main.vertical_slices_sum_gain([[3,6,10], [7,9,-7]]) == [[3,6,10], [7,9,-7]]


def test_vertical_slices_sum_gain_overlapping():
    """
    Input [[3,6,10], [6,9,-7]]

    line1 | . . . 3 - - 6 . . . .
    line2 | . . . . . . 6 - - 9 .
    
    Output is [[3,5,10], [6, 6, 3], [7,9,-7]]
    """
    assert main.vertical_slices_sum_gain([[3,6,10], [6,9,-7]]) == [[3,5,10], [6, 6, 3], [7,9,-7]]


def test_vertical_slices_sum_gain_contained():
    """
    Input [[3,6,10], [2,9,-7]]

    line1 | . . . 3 - - 6 . . . .
    line2 | . . 2 - - - - - - 9 .
    
    Output is [[0,1,1], [2,2,-7], [3 ,6, 3], [7, 9, -7], [10,10,1]]
    """
    pass


def test_range_in_ranges_empty():
   assert main.range_in_ranges(new_range=[], ranges=[]) == []
   assert main.range_in_ranges(new_range=[], ranges=[[1,2,42]]) == [[1,2,42]]
   assert main.range_in_ranges(new_range=[1,2,42], ranges=[]) == [[1,2,42]]

def test_range_in_ranges_before():
    assert main.range_in_ranges(new_range=[1,2,42], ranges=[[4,5,7]]) == [[1,2,42], [4,5,7]]

def test_range_in_ranges_after():
    assert main.range_in_ranges(new_range=[4,5,7], ranges=[[4,5,7]]) == [[1,2,42], [4,5,7]]