from unittest.mock import patch
from idcard_generator.name_utils import random_name

def test_random_name_structure():
    result = random_name()
    assert isinstance(result, dict)
    assert "name_full" in result
    assert "name_xing" in result
    assert "name_ming" in result
    assert "sex" in result
    assert "sex_text" in result

    assert isinstance(result["name_full"], str)
    assert isinstance(result["name_xing"], str)
    assert isinstance(result["name_ming"], str)
    assert isinstance(result["sex"], int)
    assert isinstance(result["sex_text"], str)

def test_random_name_logic():
    result = random_name()
    assert result["name_full"] == result["name_xing"] + result["name_ming"]
    assert result["sex"] in [0, 1]
    assert result["sex_text"] in ["男", "女"]
    if result["sex"] == 0:
        assert result["sex_text"] == "女"
    else:
        assert result["sex_text"] == "男"

@patch('idcard_generator.name_utils.secure_random.choice')
def test_random_name_male(mock_choice):
    # Mocking choice to return a specific surname, gender, and male name
    mock_choice.side_effect = ['张', 1, '伟']
    result = random_name()
    assert result["name_full"] == "张伟"
    assert result["name_xing"] == "张"
    assert result["name_ming"] == "伟"
    assert result["sex"] == 1
    assert result["sex_text"] == "男"

@patch('idcard_generator.name_utils.secure_random.choice')
def test_random_name_female(mock_choice):
    # Mocking choice to return a specific surname, gender, and female name
    mock_choice.side_effect = ['李', 0, '娜']
    result = random_name()
    assert result["name_full"] == "李娜"
    assert result["name_xing"] == "李"
    assert result["name_ming"] == "娜"
    assert result["sex"] == 0
    assert result["sex_text"] == "女"
