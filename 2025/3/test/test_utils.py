import pytest
from utils import solve

def test_solve():
    assert [357,0] == solve("""
987654321111111
811111111111119
234234234234278
818181911112111""")
