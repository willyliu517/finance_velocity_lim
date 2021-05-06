"""Helpers test module
"""
import pytest
import sys, os
from datetime import datetime

velocity_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../velocity_lim"))
sys.path.insert(1, velocity_dir)

from velocity_helpers import pass_all_limits, check_diff_start_date, check_diff_start_week


@pytest.mark.parametrize(
    "load_amt, load_amt_today, week_load_amt, num_load_today, expect",
    [
        (5000, 0, 0, 0, True),
        (5001, 0, 0, 0, False),
        (1000, 2000, 2000, 1, True),
        (1000, 4500, 4500, 2, False),
        (1000, 4500, 4500, 2, False),
        (100, 250, 20000, 1, False),
        (100, 250, 10000, 3, False),
        (100, 250, 12000, 2, True)
    ]
)
def test_pass_all_limits(load_amt, load_amt_today, week_load_amt, num_load_today, expect):
    """Test the 'pass_all_limit' helper function"""
    
    assert pass_all_limits(load_amt, load_amt_today, week_load_amt, num_load_today) == expect
    
    
@pytest.mark.parametrize(
    "load_date_1, load_date_2,expect",
    [
        (datetime(2000, 12, 1, 0, 0, 0) ,datetime(2000, 12, 1, 23,59,59), False),
        (datetime(2000, 12, 2, 5, 2, 3) ,datetime(2000, 12, 2, 10,59,59), False),
        (datetime(2000, 12, 1, 12, 1, 1), datetime(2000, 12, 2, 23,0,0), True),
        (datetime(2000, 12, 1, 23, 59, 59), datetime(2000, 12, 2, 0,0,0), True)
    ]
)
def test_check_diff_start_date(load_date_1, load_date_2, expect):
    """Test the 'check_diff_start_date' function """
    
    assert check_diff_start_date(load_date_1, load_date_2) == expect
    
    
@pytest.mark.parametrize(
    "load_date_1, load_date_2, expect",
    [
        (datetime(2021, 4, 25, 23, 59, 59), datetime(2021, 4, 26, 0, 0, 0), True),
        (datetime(2021, 4, 25, 23, 59, 59), datetime(2021, 5, 17, 1, 0, 0), True),
        (datetime(2021, 4, 20, 4, 15, 0), datetime(2021, 4, 24, 23, 0, 0), False)
    ]
)
def test_check_diff_start_week(load_date_1, load_date_2, expect):
    """Test the 'check_diff_start_date' function """
    
    assert check_diff_start_week(load_date_1, load_date_2) == expect