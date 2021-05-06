"""Velocity Complie test module
"""
import pytest
import sys, os
from datetime import datetime

home_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(1, home_dir)
from velocity_lim.velocity_compile import velocity_limit_compiler


#Expected response output of the "input_all_attempts_accepted.txt" test case
all_attempts_accepted = [
    {"id":"15881","customer_id":"527" , "accepted": True},
    {"id":"15882","customer_id":"527" , "accepted": True},
    {"id":"15883","customer_id":"527" , "accepted": True},
    {"id":"15884","customer_id":"527" , "accepted": True},
    {"id":"15885","customer_id":"527" , "accepted": True},
    {"id":"15886","customer_id":"527" , "accepted": True},
    {"id":"15887","customer_id":"527" , "accepted": True},
    {"id":"15888","customer_id":"527" , "accepted": True},
    {"id":"15889","customer_id":"527" , "accepted": True},
    {"id":"15890","customer_id":"527" , "accepted": True},
    
]


#Expected parse and reponse output of the "input_duplicated_id_first_instance_accepted.txt" test case
duplicate_first_instance_accepted = {
    
    'parse_output': [
        {"id":"15887","customer_id":"528", "load_amount": 3318.47, "time":datetime(2021, 4, 23, 12, 0, 0)},
        {"id":"15887","customer_id":"528", "load_amount": 200.00, "time":datetime(2021, 4, 23, 13, 0, 0)},
        {"id":"15888","customer_id":"528", "load_amount": 150.00, "time":datetime(2021, 4, 23, 14, 0, 0)},
        {"id":"15889","customer_id":"528", "load_amount": 1000.00, "time":datetime(2021, 4, 23, 15, 0, 0)}
    ],
    
    'evaluated_ouput': [
        {"id":"15887","customer_id":"528" , "accepted": True},
        None,
        {"id":"15888","customer_id":"528" , "accepted": True},
        {"id":"15889","customer_id":"528" , "accepted": True}
    ]
    
}

#Expected parse and reponse output of the "input_duplicated_id_first_instance_rejected.txt" test case
duplicate_first_instance_rejected = {
    
    'parse_output': [
        {"id":"15899","customer_id":"529", "load_amount": 6000.47, "time":datetime(2021, 4, 23, 12, 0, 0)},
        {"id":"15899","customer_id":"529", "load_amount": 200.00, "time":datetime(2021, 4, 23, 13, 0, 0)},
        {"id":"15900","customer_id":"529", "load_amount": 150.00, "time":datetime(2021, 4, 23, 14, 0, 0)},
        {"id":"15901","customer_id":"529", "load_amount": 150.00, "time":datetime(2021, 4, 23, 15, 0, 0)},
        {"id":"15902","customer_id":"529", "load_amount": 150.00, "time":datetime(2021, 4, 23, 16, 0, 0)}
    ],
    
    'evaluated_ouput': [
        {"id":"15899","customer_id":"529" , "accepted": False},
        None,
        {"id":"15900","customer_id":"529" , "accepted": True},
        {"id":"15901","customer_id":"529" , "accepted": True},
        {"id":"15902","customer_id":"529" , "accepted": True},
        
    ]
    
}

#Expected response output of the "input_not_accepted_over_daily_amt.txt" test case
over_daily_load_amt = [
    {"id":"15887","customer_id":"530" , "accepted": True},
    {"id":"15888","customer_id":"530" , "accepted": False},
]

#Expected response output of the "input_not_accepted_over_daily_attempt_vol.txt" test case
over_daily_attempt_volume = [
    {"id":"15887","customer_id":"531" , "accepted": True},
    {"id":"15888","customer_id":"531" , "accepted": True},
    {"id":"15889","customer_id":"531" , "accepted": True},
    {"id":"15890","customer_id":"531" , "accepted": False},
]

#Expected response output of the "input_not_accepted_over_daily_attempt_vol.txt" test case
over_weekly_attempt_volume = [
    {"id":"15881","customer_id":"532" , "accepted": True},
    {"id":"15882","customer_id":"532" , "accepted": True},
    {"id":"15883","customer_id":"532" , "accepted": True},
    {"id":"15884","customer_id":"532" , "accepted": True},
    {"id":"15885","customer_id":"532" , "accepted": True},
    {"id":"15886","customer_id":"532" , "accepted": True},
    {"id":"15887","customer_id":"532" , "accepted": True},
    {"id":"15888","customer_id":"532" , "accepted": True},
    {"id":"15889","customer_id":"532" , "accepted": True},
    {"id":"15890","customer_id":"532" , "accepted": False},
]



@pytest.mark.parametrize(
    "txt_dir, expect",
    [
       ('./tests/test_inputs/input_duplicated_id_first_instance_rejected.txt',
        duplicate_first_instance_rejected['parse_output']),
       ('./tests/test_inputs/input_duplicated_id_first_instance_accepted.txt',
        duplicate_first_instance_accepted['parse_output'])
    ]
)
def test_parse_text_file(txt_dir, expect):
    """Test the 'parse_text_file function' within the velocity_limit_compiler class"""
    
    test_compiler = velocity_limit_compiler(input_txt_dir = txt_dir)
    
    for i in range(0, len(test_compiler.load_attempt_list)): 
        
        assert(test_compiler.load_attempt_list[i] == expect[i])
        
@pytest.mark.parametrize(
    "txt_dir, expect",
    [
       ('./tests/test_inputs/input_all_attempts_accepted.txt',
         all_attempts_accepted),
        
        ('./tests/test_inputs/input_duplicated_id_first_instance_accepted.txt',
        duplicate_first_instance_accepted['evaluated_ouput']), 
        
       ('./tests/test_inputs/input_duplicated_id_first_instance_rejected.txt',
        duplicate_first_instance_rejected['evaluated_ouput']),
        
       ('./tests/test_inputs/input_not_accepted_over_daily_amt.txt',
        over_daily_load_amt),
        
       ('./tests/test_inputs/input_not_accepted_over_daily_attempt_vol.txt',
        over_daily_attempt_volume),
        
       ('./tests/test_inputs/input_not_accepted_over_weekly_amt.txt',
        over_weekly_attempt_volume),          
    ]
)
def test_evaluate_file(txt_dir, expect):
    """Test the 'evaluate_transaction' within the velocity_limit_compiler class"""
    test_compiler = velocity_limit_compiler(input_txt_dir = txt_dir)
    
    for i in range(0, len(test_compiler.load_attempt_list)): 
        
        assert(test_compiler.evaluate_transaction(test_compiler.load_attempt_list[i]) == expect[i])
        

        
