from idcard_generator.time_check import check_time_limit

def test_check_time_limit():
    assert check_time_limit() is True
