import pytest
from idcard_generator.id_card_utils import IdentityCard

def test_identity_card_check_valid_length():
    """Test that a code with length 17 returns True."""
    # 17 characters string
    code = "12345678901234567"
    assert IdentityCard.check(code) is True

def test_identity_card_check_shorter_length():
    """Test that a code with length less than 17 returns False."""
    # 16 characters string
    code = "1234567890123456"
    assert IdentityCard.check(code) is False

def test_identity_card_check_longer_length():
    """Test that a code with length greater than 17 returns False."""
    # 18 characters string
    code = "123456789012345678"
    assert IdentityCard.check(code) is False

def test_identity_card_check_empty_string():
    """Test that an empty string returns False."""
    code = ""
    assert IdentityCard.check(code) is False

def test_identity_card_check_with_none():
    """Test that passing None raises TypeError or is handled."""
    # len(None) raises TypeError in Python, so this test should verify that
    with pytest.raises(TypeError):
        IdentityCard.check(None)
