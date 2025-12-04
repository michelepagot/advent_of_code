import pytest
from utils import solve, find_invalids, is_invalid_part2

def test_is_invalid_part2():
    assert is_invalid_part2(11)
    assert is_invalid_part2(111)
    assert is_invalid_part2(1111)
    assert is_invalid_part2(12341234)
    assert is_invalid_part2(123123123)
    assert is_invalid_part2(1212121212)
    assert is_invalid_part2(1111111)



def test_find_invalids():
    assert ([11,22],[11,22]) == find_invalids((11,22))
    assert ([99], [99,111]) == find_invalids((95,115))
    assert ([1010], [999,1010]) == find_invalids((998,1012))
    assert ([1188511885], [1188511885]) == find_invalids((1188511880,1188511890))
    assert ([222222], [222222]) == find_invalids((222220,222224))
    assert ([], []) == find_invalids((1698522,1698528))
    assert ([446446], [446446]) == find_invalids((446443,446449))
    assert ([38593859], [38593859]) == find_invalids((38593856,38593862))
    assert ([], [565656]) == find_invalids((565653,565659))
    assert ([], [824824824]) == find_invalids((824824821,824824827))
    assert ([], [2121212121]) == find_invalids((2121212118,2121212124))

def test_solve():
    assert [1227775554,4174379265] == solve("11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124")
