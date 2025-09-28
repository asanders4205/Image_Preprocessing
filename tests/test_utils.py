# tests/test_utils.py

from tests_module import add

def test_add_two_numbers():
    assert add(2, 3) == 5

def test_add_with_negatives():
    assert add(-1, 5) == 4
