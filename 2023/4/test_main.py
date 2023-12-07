import main

def test_parse_line():
    data = main.parse_line('Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53')
    assert data['id'] == 1
    assert data['winning_numbers'] == [41, 48, 83, 86, 17]
    assert data['your_numbers'] == [83, 86,  6, 31, 17,  9, 48, 53]

def test_parse_line_1():
    data = main.parse_line('Card   1: 99 71 95 70 36 79 78 84 31 10 |  5 45 54 83  3 38 89 35 80 49 76 15 63 20 21 94 65 55 44  4 75 56 85 92 90')
    assert data['id'] == 1
    assert data['winning_numbers'] == [99, 71, 95, 70, 36, 79, 78, 84, 31, 10]
    assert data['your_numbers'] == [5, 45, 54, 83, 3, 38, 89, 35, 80, 49, 76, 15, 63, 20, 21, 94, 65, 55, 44, 4, 75, 56, 85, 92, 90]

def test_winning_numbers():
    data = {}
    data['id'] = 1
    data['winning_numbers'] = [41, 48, 83, 86, 17]
    data['your_numbers'] = [83, 86,  6, 31, 17,  9, 48, 53]
    assert 4 == main.winning_numbers(data)