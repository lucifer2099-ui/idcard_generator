import pytest
from idcard_generator.id_card_utils import random_card_no, IdentityCard, XUZHOU_AREA_CODES

def test_random_card_no_default():
    """Test the default generation of ID card numbers."""
    code = random_card_no()

    # Check length
    assert len(code) == 18

    # Check valid prefix (should default to one of XUZHOU_AREA_CODES if not specified)
    assert code[:6] in XUZHOU_AREA_CODES

    # Check parity bit
    assert IdentityCard.check(code[:17])
    expected_vi_code = IdentityCard.calculate(code[:17])
    assert code[-1] == expected_vi_code

def test_random_card_no_specific_prefix():
    """Test generating ID card with a specific prefix."""
    prefix = '110105'
    code = random_card_no(prefix=prefix)

    assert code[:6] == prefix
    assert len(code) == 18

def test_random_card_no_specific_year_month_day():
    """Test generating ID card with specific year, month, and day."""
    year = '1990'
    month = '5'
    day = '9'

    code = random_card_no(year=year, month=month, day=day)

    assert code[6:10] == '1990'
    assert code[10:12] == '05'
    assert code[12:14] == '09'

def test_random_card_no_year_before_1980():
    """Test generating ID card with a year before 1980."""
    year = '1970'

    code = random_card_no(year=year)

    assert code[6:10] == '1980'

def test_random_card_no_sex_female():
    """Test generating ID card for a female."""
    code = random_card_no(sex=0)

    seq_last = int(code[16])
    assert seq_last % 2 == 0

def test_random_card_no_sex_male():
    """Test generating ID card for a male."""
    code = random_card_no(sex=1)

    seq_last = int(code[16])
    assert seq_last % 2 != 0

def test_random_card_no_all_parameters():
    """Test generating ID card with all specific parameters."""
    prefix = '110101'
    year = '2000'
    month = '12'
    day = '31'
    sex = 1

    code = random_card_no(prefix=prefix, year=year, month=month, day=day, sex=sex)

    assert code[:6] == prefix
    assert code[6:10] == year
    assert code[10:12] == month
    assert code[12:14] == day

    seq_last = int(code[16])
    assert seq_last % 2 != 0

    # Parity bit check
    expected_vi_code = IdentityCard.calculate(code[:17])
    assert code[-1] == expected_vi_code
