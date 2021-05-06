"""Core module for processing incoming load attempts """

from datetime import datetime
from datetime import timedelta
from typing import Dict, List
from .velocity_helpers import pass_all_limits, check_diff_start_week, check_diff_start_date
import json

class velocity_limit_compiler:
    
    """velocity_limit_compiler baseclass.
    This class stores information for each customer that has made at least one valid load attempt
    
    Parameters
    ----------
    customer_base: Dict[str, Dict]
        Nested dictionary where the keys are the customer_id and values for each key is a  
        dictionary containing information on the remaining limits for that customer   
        
    input_txt_dir: str
        directory to the input.txt file
    """
    
    def __init__(
        self,
        input_txt_dir: str,
        customer_base: Dict = {},
    ):
        self.input_txt_dir = input_txt_dir
        self.customer_base = customer_base
        self.load_attempt_list = self.parse_text_file(self.input_txt_dir)
          
    def parse_text_file(
        self,
        text_dir: str
    ) -> List[Dict] :
        """reads in and parses through a txt file to return a list JSON payloads
        
        Parameters
        ----------
        text_dir: str
            directory to the input.txt file 
        
        Returns
        ------- 
        Dict:
            a list of dictionaries where each dictionary corresponds to a load fund attempt
        
        """
        load_attempt_list = []   
        
        with open(text_dir) as f: 
            for line in f:
                load_attempt_list.append(eval(line))
        
        #Converts the time string to the corresponding time values in datetime and load amount to float
        for item in load_attempt_list:
            item['time'] =  datetime.strptime(item['time'], "%Y-%m-%dT%H:%M:%SZ")
            item['load_amount'] = float(item['load_amount'][1:])
            
        return load_attempt_list
        
        
    def output_to_text_file(
        self,
        output_dir: str
    ):
        """writes the output of the evaluated list of load attempts into a txt file where each line will 
        be a JSON response pertaining to the status of the load attempt (accepted or ignored)
        
        Parameters
        ----------
        output_dir: str
            directory to the output txt file 
        
        Side Effects
        ------- 
        writes the responses for each load attempt in a txt file and save to the path specified in output_dir
        
        """
        
        with open(output_dir,'w') as file:
            
            for load_attempt in self.load_attempt_list: 
                load_response = self.evaluate_transaction(load_attempt)
                
                #Ensures load_response is not null; this will be the case for duplicate ids
                if load_response:
                    json.dump(load_response, file)
                    file.write('\n')
                
                
    def evaluate_transaction(
        self,
        load_attempt: Dict,
    ) -> Dict:
        """evaluates whether the load_attempt will be accepted based on input information and the
        current status of the customer's account
        
        Parameters
        ----------
        load_attempt: Dict[str, Any]
            Dictionary storing the information regarding the attempted load 
            
        Returns
        ------- 
        Dict:
            JSON output indicating whether the load attempt has been accepted or rejected
                
        Side Effects
        ------------ 
        If the load_attempt is accepted, self.customer_base will be updated with the transaction information   
        
        """
        
        #Checks if the customer id is already in the database and if the customer has made a successful transaction
        if load_attempt['customer_id'] in self.customer_base.keys():
            
            #Checks if the customer has made a successful transaction
            if self.customer_base[load_attempt['customer_id']].get('last_transaction'):
            
                #Ensure load id is not already in the list of previously used ids by the customer; else the attempt will be ignored
                if load_attempt['id'] not in self.customer_base[load_attempt['customer_id']]['load_id_list'] :

                    #Saves the load id for the given customer
                    self.save_load_id(load_attempt['customer_id'], load_attempt['id'])

                    #refreshes the daily and weekly limit if the time of incoming attempt is outside of the day or week range of the previous transaction
                    self.reset_daily_weekly_load_amt(load_attempt['customer_id'], load_attempt['time'])

                    customer_info = self.customer_base[load_attempt['customer_id']]

                    if pass_all_limits(load_attempt['load_amount'], customer_info['loaded_so_far_today'],
                                       customer_info['loaded_this_week'], customer_info['loaded_vol_today']):

                        #Updates the information of the transaction if it passes all limits
                        self.update_customer_info(load_attempt['customer_id'], load_attempt['load_amount'], load_attempt['time'])

                        return {"id":load_attempt['id'], "customer_id":load_attempt['customer_id'], "accepted": True}

                    else:     

                        return {"id":load_attempt['id'], "customer_id":load_attempt['customer_id'], "accepted": False}
            
            #If customer id is in database but has not made a successful transaction
            else:
                
                #Ensure load id is not already in the list of previously used ids by the customer; else the attempt will be ignored
                if load_attempt['id'] not in self.customer_base[load_attempt['customer_id']]['load_id_list'] :
                    
                    #Saves the load id for the given customer
                    self.save_load_id(load_attempt['customer_id'], load_attempt['id'])
                    
                    if pass_all_limits(load_attempt['load_amount'], 0, 0, 0):
                
                        #Update the information of the transaction if it passes all limits
                        self.update_customer_info(load_attempt['customer_id'], load_attempt['load_amount'], load_attempt['time'])

                        return {"id":load_attempt['id'], "customer_id":load_attempt['customer_id'], "accepted": True}

                    else: 

                        return {"id":load_attempt['id'], "customer_id":load_attempt['customer_id'], "accepted": False}
                    
            
        else: 
            
            #Saves the load id for the given customer
            self.save_load_id(load_attempt['customer_id'], load_attempt['id'])
            
            if pass_all_limits(load_attempt['load_amount'], 0, 0, 0):
                
                #Update the information of the transaction if it passes all limits
                self.update_customer_info(load_attempt['customer_id'], load_attempt['load_amount'], load_attempt['time'])
                
                return {"id":load_attempt['id'], "customer_id":load_attempt['customer_id'], "accepted": True}
    
            else: 
            
                return {"id":load_attempt['id'], "customer_id":load_attempt['customer_id'], "accepted": False}
            
    def save_load_id(
        self,
        customer_id: str,
        load_id: str,
    ):
        """saves the load_id of a load attempt regardless if it succeeds or not 
        
        Parameters
        ----------
        customer_id: str
            id of the customer
        load_id: str
            id of load attempt
            
        Side Effects
        ------------ 
        load_id will be be added to the list of attempted ids previously used for a given customer, if customer is not
        on file, a dictionary will be created with their customer_id as the key
        
        """
        
        #Initialzies new dictionary if the customer id is not the customer_base
        if customer_id not in self.customer_base.keys():

            self.customer_base[customer_id] = {}
            self.customer_base[customer_id]['load_id_list'] = []
        
        
        self.customer_base[customer_id]['load_id_list'].append(load_id)
            
    def update_customer_info(
        self,
        customer_id: str,
        load_amt: float,
        attempt_time: datetime,
    ):
        """updates the load info for the customer, if the load attempt is accepted
        
        Parameters
        ----------
        customer_id: str
            id of the customer
        
        load_amt: float
            amount loaded in the transaction
            
        attempt_time: datetime.datetime
            datetime of the transaction
            
        Side Effects
        ------------ 
        customer load info will be updated in the customer_base
        
        """
        
        customer_info = self.customer_base[customer_id]
        
        self.customer_base[customer_id]['loaded_so_far_today'] = load_amt + customer_info.get('loaded_so_far_today', 0.0)
        self.customer_base[customer_id]['loaded_this_week'] = load_amt + customer_info.get('loaded_this_week', 0.0)
        self.customer_base[customer_id]['loaded_vol_today'] = 1 + customer_info.get('loaded_vol_today', 0.0)
        self.customer_base[customer_id]['last_transaction'] = attempt_time
        
    def reset_daily_weekly_load_amt(
        self,
        customer_id: str,
        attempt_time: datetime,
    ):
        """resets the daily and weekly load amount, and daily load volume if the incoming load attempt is outside the day and week range from previous transaction
        
        Parameters
        ----------
        customer_id: str
            id of the customer
        
        attempt_time: datetime.datetime
            datetime of the transaction
            
        Side Effects
        ------------ 
        If the start of the week for the incoming load attempt is different from that of the last transaction, reset 'loaded_this_week' to 0
        If the start of day for the load attempt is different from that of the last transaction, reset 'loaded_so_far_today' and 'loaded_vol_today' to 0 
        No changes otherwise
        """
        
        if check_diff_start_week(self.customer_base[customer_id]['last_transaction'], attempt_time):
            
            self.customer_base[customer_id]['loaded_this_week'] = 0
            
        if check_diff_start_date(self.customer_base[customer_id]['last_transaction'], attempt_time):
            
            self.customer_base[customer_id]['loaded_so_far_today'] = 0
            self.customer_base[customer_id]['loaded_vol_today'] = 0
            
            
            
            