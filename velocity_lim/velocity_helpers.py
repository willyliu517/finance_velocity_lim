"""Collection of helper functions"""

from datetime import datetime
from datetime import timedelta

def pass_daily_limit(
    load_amt: float,
    daily_loaded_so_far: float,
    daily_limit: float = 5000
) -> bool: 
    
 
    """Indicates whether the attempted load transaction will be under the daily limit threshold
    
        Parameters
        ---------
        load_amt: float
            amount to load in current transaction
        daily_loaded_so_far: float
            amount loaded so far in the day 
        daily_limit: float
            daily loading limit, set to $5,000 by default
            
        Returns
        -------
        bool:
            True if under the daily limit threshold
            False otherwise   
        """
    return (load_amt + daily_loaded_so_far) <= daily_limit
  
def pass_weekly_limit(
    load_amt: float,
    weekly_loaded_so_far: float,
    weekly_limit: float = 20000
) -> bool:
    
 
    """Indicates whether the attempted load transaction will be under the weekly limit threshold
    
        Parameters
        ----------
        load_amt: float
            amount to load in current transaction
        weekly_loaded_so_far: float
            amount loaded so far in the week
        weekly_limit: float
            weekly loading limit, set to $20,000 by default
            
        Returns
        -------
        bool:
            True if under the weekly limit threshold
            False otherwise
                
        """
    return(load_amt + weekly_loaded_so_far) <= weekly_limit
    
def pass_daily_vol(
    daily_vol_so_far: int,
    daily_vol_limit: int = 3
) -> bool: 
    
    """Indicates whether the attempted load will be under the daily load volume threshold
    
        Parameters
        ----------
        daily_vol_so_far: float
            number of accepted load attempts so far in the day
        daily_vol_limit: int
            limit of the daily load volume limit, set to 3 by default
            
        Returns
        -------
        bool:
            True if under the daily volume threshold
            False otherwise
                
        """
    return (daily_vol_so_far + 1) <= daily_vol_limit
    
    
def pass_all_limits(
    load_amt: float,
    daily_loaded_so_far: float,
    weekly_loaded_so_far: float,
    daily_vol_so_far: int, 
) -> bool:

    """Indicates whether the attempt load has passed all three limit thresholds
    
    Parameters
    ----------
    load_amt: float
        amount to load in current transaction
    daily_loaded_so_far: float
        amount loaded so far in the day
    weekly_loaded_so_far: float
        amount loaded so far in the week
    daily_vol_so_far: int
        number of accepted load attempts so far in the day
        
     Returns
     -------
     bool:
        True if load attempt passes all three limit thresholds 
        False otherwise
    """
    return pass_daily_limit(load_amt, daily_loaded_so_far) & \
            pass_weekly_limit(load_amt, weekly_loaded_so_far) & \
            pass_daily_vol(daily_vol_so_far)
    

def get_start_of_day(
    date_of_load: datetime
) -> datetime:
    """Gets the time of load date at midnight
    
    Parameters
    ----------
    date_of_load: datetime.datetime
        datetime of the load attempt
       
    Returns
    -------
    datetime.datetime:
        datetime of the load attempt with the hour, minute and second reset to 0     
    """
    
    return datetime(date_of_load.year, date_of_load.month, date_of_load.day, 0, 0, 0)
    
    
def get_start_of_week(
    date_of_load: datetime
) -> datetime:
    """Gets the datetime of the most recent Monday from load date
    
    Parameters
    ----------
    date_of_load: datetime.datetime
        datetime of the load attempt
       
    Returns
    -------
    datetime.datetime:
        datetime of the most recent Monday with the hour, minute and second reset to 0     
   
    """
    
    recent_monday = date_of_load - timedelta(days=date_of_load.weekday())
    
    return datetime(recent_monday.year, recent_monday.month, recent_monday.day, 0, 0, 0)


def check_diff_start_date(
    load_date_1: datetime,
    load_date_2: datetime
) -> bool:
    
    """Checks if load_date_1 and load_date_2 are in different dates (i.e. datetime(2000, 1, 1, 1, 1, 22) and 
    datetime(2000, 2, 12, 13, 45, 18) would be on different dates but datetime.datetime(2000, 1, 1, 0, 0) and 
    datetime(2000, 1, 1, 1, 1, 22) would be in the same date)
    
    Parameters
    ----------
    load_date_1: datetime.datetime
        datetime of the load attempt 1
        
    load_date_2: datetime.datetime
        datetime of the load attempt 2
        
    Returns
    -------
    bool:
        True if load_date_1 and load_date_2 are on different dates
        False otherwise
    
    """
    
    return get_start_of_day(load_date_1) != get_start_of_day(load_date_2)


def check_diff_start_week(
    load_date_1: datetime,
    load_date_2: datetime
) -> bool:
    
    """Checks if load_date_1 and load_date_2 are in different weeks (i.e. datetime(2000, 1, 1, 1, 1, 22) and 
    datetime(2000, 1, 7, 9, 25) would be in different weeks but datetime.datetime(2000, 1, 1,  1, 1, 22) and 
    datetime.datetime(2000, 1, 2, 0, 32, 48) would be in the same week)
    
    Parameters
    ----------
    load_date_1: datetime.datetime
        datetime of the load attempt 1
        
    load_date_2: datetime.datetime
        datetime of the load attempt 2
        
    Returns
    -------
    bool:
        True if load_date_1 and load_date_2 are in different weeks
        False otherwise
    
    """
    
    return get_start_of_week(load_date_1) != get_start_of_week(load_date_2)



        
     
   
    
    
    

    