import pytest
from utils import rotate, solve

def test_rotate_no_move():
    # Starting from 0 and not moving
    # end in 0 crossing 0 for 0 times
    assert (0,0) == rotate(10, 0, 0)
    # Starting from 2 and not moving
    # end in 2 not crossing the 0
    assert (2,0) == rotate(10, 2, 0)

def test_rotate_start_from_zero_right():
    # Starting from 0 and move 1 to the right
    # end in 1 crossing 0 for 0 times
    assert (1,0) == rotate(10, 0, 1)
    assert (9,0) == rotate(10, 0, 9)
    assert (0,1) == rotate(10, 0, 10)
    assert (0,2) == rotate(10, 0, 20)

def test_rotate_start_from_zero_left():
    # Starting from 0 and move 1 to the left
    # end in 9 not crossing the 0
    assert (9,0) == rotate(10, 0, -1)
    assert (9,1) == rotate(10, 0, -11)
    assert (9,10) == rotate(10, 0, -101)

def test_rotate_right_multiple_round():
    # starting from 2 moving 10 times on the right
    # end in 2 doing a full rotation,
    # so crossing the 0 once
    assert (2,1) == rotate(10, 2, 10)
    assert (2,10) == rotate(10, 2, 100)

def test_rotate_left_multiple_round():
    assert (2,1) == rotate(10, 2, -10)
    assert (2,10) == rotate(10, 2, -100)

def test_rotate_right_no_cross():
    assert (3,0) == rotate(10, 2, 1)
    assert (9,0) == rotate(10, 2, 7)

def test_rotate_left_no_cross():
    assert (1,0) == rotate(10, 2, -1)
    assert (2,0) == rotate(10, 9, -7)

def test_rotate_right_cross():
    # Starting from 2 and doing 9 click on the right
    # end in 1 crossing the 0 once
    assert (1,1) == rotate(10, 2, 9)
    assert (1,2) == rotate(10, 2, 19)
    assert (1,11) == rotate(10, 2, 109)

def test_rotate_right_cross_once_landing_zero():
    # Starting from 9 and doing one click on the right
    # end in 0. It land on zero but never cross it
    assert (0,0) == rotate(10, 9, 1)
    # Starting from 2 moving right for 8 clicks
    # end in 0. It land on zero but never cross it
    assert (0,0) == rotate(10, 2, 8)

def test_rotate_right_cross_landing_zero():
    # Starting from 2 moving right for 18 clicks
    # end in 0. It land on zero crossing once before landing
    assert (0,1) == rotate(10, 2, 18)
    assert (0,10) == rotate(10, 2, 108)

def test_rotate_left_cross_landing_zero():
    assert (0,0) == rotate(10, 1, -1)
    assert (0,0) == rotate(10, 2, -2)
    assert (0,1) == rotate(10, 2, -12)
    assert (0,10) == rotate(10, 2, -102)

def test_rotate_left_cross():
    assert (9,1) == rotate(10, 2, -3)
    assert (9,1) == rotate(10, 9, -10)
    assert (9,2) == rotate(10, 2, -13)
    assert (9,11) == rotate(10, 2, -103)

def test_solve_no_move():
    assert [0,0] == solve("R0", 0)
    assert [0,0] == solve("L0", 0)

def test_solve_start_zero():
    assert [0,0] == solve("R1", 0)
    assert [0,0] == solve("L1", 0)

def test_solve_right_zero():
    assert [1,1] == solve("R1", 99)
    assert [1,1] == solve("R11", 89)
    assert [1,1] == solve("R99", 1)

def test_solve_left_zero():
    assert [1,1] == solve("L1", 1)
    assert [1,1] == solve("L10", 10)
    assert [1,1] == solve("L99", 99)

def test_solve_many_zero_from_rigth():
    assert [2,2] == solve("""R1
R5
L5""", 99)

def test_solve_many_zero_from_left():
    assert [2,2] == solve("""L1
L5
R5""", 1)

def test_solve_right_no_cross():
    assert [0,0] == solve("R5", 0)
    assert [0,0] == solve("""R5
R5
R5""", 0)

def test_solve_left_no_cross():
    assert [0,0] == solve("L5", 99)
    assert [0,0] == solve("""L5
L5
L5""", 99)

def test_solve_right_one_cross():
    assert [0,1] == solve("R5", 99)

def test_solve_left_one_cross():
    assert [0,1] == solve("L5", 1)

def test_solve_right_multi_cross():
    assert [0,2] == solve("R105", 99)

def test_solve_left_multi_cross():
    assert [0,1] == solve("L105", 0)
    assert [0,2] == solve("L105", 1)
