import pytest
from idcard_generator.id_card_utils import IdentityCard

def test_calculate_valid_id_check_digits():
    # Test cases mapping 17-digit prefix to expected check digit
    test_cases = [
        # Example 1: a common pattern, say "11010519491231002" -> 'x'
        ("11010519491231002", "x"),
        # Example 2: random valid case 1
        ("32030219800101123", "9"),
        # Example 3: known case ending in '1'
        ("44052418800101001", "4"),
    ]

    for prefix, expected_check_digit in test_cases:
        assert IdentityCard.calculate(prefix) == expected_check_digit


def test_calculate_invalid_characters():
    # Should raise ValueError when trying to int() non-numeric chars
    with pytest.raises(ValueError):
        IdentityCard.calculate("3203021980010112X") # Contains non-numeric at end of 17 chars

    with pytest.raises(ValueError):
        IdentityCard.calculate("32030A19800101123") # Contains letter in middle


def test_calculate_short_string():
    # Should raise IndexError when string is shorter than 17
    with pytest.raises(IndexError):
        IdentityCard.calculate("1234567890123456")
