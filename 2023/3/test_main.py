import main

def test_schematic_single_dot():
    schematic = main.Schematic()
    schematic.add_line('.')
    assert [] == schematic.find_numbers()


def test_schematic_only_dot_matrix():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('...')
    schematic.add_line('...')
    assert [] == schematic.find_numbers()


def test_schematic_single_digit_number_center():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('.3.')
    schematic.add_line('...')
    assert [{'start': (1,1), 'end': (1,1)}] == schematic.find_numbers()


def test_schematic_single_digit_number_right_corner():
    schematic = main.Schematic()
    schematic.add_line('1..')
    schematic.add_line('...')
    schematic.add_line('...')
    assert [{'start': (0,0), 'end': (0,0)}] == schematic.find_numbers()


def test_schematic_single_digit_number_left_corner():
    schematic = main.Schematic()
    schematic.add_line('..7')
    schematic.add_line('...')
    schematic.add_line('...')
    assert [{'start': (2,0), 'end': (2,0)}] == schematic.find_numbers()


def test_schematic_single_digit_number_left_corner_last_line():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('...')
    schematic.add_line('..0')
    assert [{'start': (2,2), 'end': (2,2)}] == schematic.find_numbers()


def test_schematic_multiple_digit_number_center():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('.33')
    schematic.add_line('...')
    assert [{'start': (1,1), 'end': (2,1)}] == schematic.find_numbers()


def test_schematic_multiple_digit_number_right_corner():
    schematic = main.Schematic()
    schematic.add_line('11.')
    schematic.add_line('...')
    schematic.add_line('...')
    assert [{'start': (0,0), 'end': (1,0)}] == schematic.find_numbers()


def test_schematic_multiple_digit_number_left_corner():
    schematic = main.Schematic()
    schematic.add_line('.77')
    schematic.add_line('...')
    schematic.add_line('...')
    assert [{'start': (1,0), 'end': (2,0)}] == schematic.find_numbers()


def test_schematic_multiple_digit_number_left_corner_last_line():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('...')
    schematic.add_line('.00')
    assert [{'start': (1,2), 'end': (2,2)}] == schematic.find_numbers()


def test_schematic_full_line_digit_number():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('...')
    schematic.add_line('000')
    assert [{'start': (0,2), 'end': (2,2)}] == schematic.find_numbers()


def test_schematic_two_numbers_same_line():
    schematic = main.Schematic()
    schematic.add_line('1.1')
    schematic.add_line('...')
    schematic.add_line('...')
    assert 2 == len(schematic.find_numbers())


def test_schematic_two_numbers_different_line():
    schematic = main.Schematic()
    schematic.add_line('1..')
    schematic.add_line('...')
    schematic.add_line('1..')
    assert 2 == len(schematic.find_numbers())


def test_sorrunging_only_dots():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('.1.')
    schematic.add_line('...')
    number_pos = schematic.find_numbers()
    assert False == schematic.is_part(number_pos[0])


def test_sorrunging_one_sym_same_line():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('#1.')
    schematic.add_line('...')
    number_pos = schematic.find_numbers()
    assert True == schematic.is_part(number_pos[0])


def test_sorrunging_one_sym_other_line():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('.1.')
    schematic.add_line('.#.')
    number_pos = schematic.find_numbers()
    assert True == schematic.is_part(number_pos[0])


def test_sorrunging_one_sym_diagonal():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('.1.')
    schematic.add_line('..#')
    number_pos = schematic.find_numbers()
    assert True == schematic.is_part(number_pos[0])


def test_sorrunging_sym_surrounded():
    schematic = main.Schematic()
    schematic.add_line('###')
    schematic.add_line('#1#')
    schematic.add_line('###')
    number_pos = schematic.find_numbers()
    assert True == schematic.is_part(number_pos[0])


def test_sorrunging_one_sym_touch_only_another_numbers():
    schematic = main.Schematic()
    schematic.add_line('.1.')
    schematic.add_line('.1.')
    schematic.add_line('...')
    assert False == schematic.is_part({'start': (1,1), 'end': (1,1)})


def test_sorrunging_multidigits_only_dots():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('.11')
    schematic.add_line('...')
    number_pos = schematic.find_numbers()
    assert False == schematic.is_part(number_pos[0])


def test_sorrunging_fullinedigits_only_dots():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('111')
    schematic.add_line('...')
    number_pos = schematic.find_numbers()
    assert False == schematic.is_part(number_pos[0])


def test_sorrunging_fullinedigits_only_dots_lastline():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('...')
    schematic.add_line('111')
    number_pos = schematic.find_numbers()
    assert False == schematic.is_part(number_pos[0])


def test_sorrunging_multidigits_sym_same_line():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('#11')
    schematic.add_line('...')
    number_pos = schematic.find_numbers()
    assert True == schematic.is_part(number_pos[0])


def test_sorrunging_multidigits_sym_touch_below_line():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('11')
    schematic.add_line('.#.')
    number_pos = schematic.find_numbers()
    assert True == schematic.is_part(number_pos[0])


def test_sorrunging_multidigits_sym_touch_above_line():
    schematic = main.Schematic()
    schematic.add_line('...')    
    schematic.add_line('.#.')
    schematic.add_line('111')
    number_pos = schematic.find_numbers()
    assert True == schematic.is_part(number_pos[0])


def test_sorrunging_multidigits_sym_diagonal():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('11.')
    schematic.add_line('..#')
    number_pos = schematic.find_numbers()
    assert True == schematic.is_part(number_pos[0])


def test_get_one_digit_number_from_center():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('.1.')
    schematic.add_line('...')
    number_pos = schematic.find_numbers()
    assert 1 == schematic.get_number(number_pos[0])


def test_get_one_digit_number_from_last_column():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('..1')
    schematic.add_line('...')
    number_pos = schematic.find_numbers()
    assert 1 == schematic.get_number(number_pos[0])


def test_get_one_digit_number_from_first_line():
    schematic = main.Schematic()
    schematic.add_line('.1.')
    schematic.add_line('...')
    schematic.add_line('...')
    number_pos = schematic.find_numbers()
    assert 1 == schematic.get_number(number_pos[0])


def test_get_one_digit_number_from_last_line():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('...')
    schematic.add_line('.1.')
    number_pos = schematic.find_numbers()
    assert 1 == schematic.get_number(number_pos[0])


def test_get_multiple_digit_number_from_center():
    schematic = main.Schematic()
    schematic.add_line('...')
    schematic.add_line('.11')
    schematic.add_line('...')
    number_pos = schematic.find_numbers()
    assert 11 == schematic.get_number(number_pos[0])