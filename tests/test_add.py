import pytest


def add_numbers(a, b):
    return a + b

def test_add_numbers():
    result = add_numbers(2, 3)
    assert result == 5
    print("wwwaasasasasassa")

def test_add_numbers_negative():
    result = add_numbers(-2, -3)
    assert result == -7

def test_add_numbers_zero():
    result = add_numbers(0, 0)
    print("aasasasasassa")
    assert result == 0