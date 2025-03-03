import random
import math
from scipy.integrate import quad
import numpy as np


random.seed(42)


class pilus_object:
    from .save_functions import SaveRealization
    from .additional_attributes import AdditionalAttributes
    from .save_helpers import HookOccurenceCounter, LengthOccurenceCounter, LengthOccurenceCounterFinalize, HookOccurenceCounterFinalize, LengthActivationOccurenceCounter, LengthActiveOccurenceCounterFinalize


    def __init__(self, params_dict):

        #What you are looking for can be in additional_attributes.py in pilus_class_folder
        self.params_dict = params_dict
        self._set_attributes(params_dict) 

        self.AdditionalAttributes()


    def _set_attributes(self, params_dict):
        for key, value in params_dict.items():
            setattr(self, key, value)
       

    def PerformOneRealization(self): 
        time = 0.0
        counter = 0
        progress_interval = int((self.total_time/self.dt)/10)  # Calculate interval for 10% increments

        while (time <= self.total_time):
            time += self.dt
            counter += 1
            if counter % progress_interval == 0:  # Check if we've hit a 10% interval
                progress = (counter / (self.total_time/self.dt)) * 100  # Calculate actual percentage
                print(f"At {int(progress)}% of the Total Time")

            if self.pilus_length > 0.0:
                self.ChangeHookState()
                self.ChangeLengthState()
                length_diff = self.LengthDifference()
                if self.hook_state == "hooked":
                    self.length_diff_record += length_diff
                else:
                    self.length_diff_record += length_diff
                    self.pilus_length = (max([self.pilus_length + self.length_diff_record, 0.0])) #size can not be smaller than 0
                    self.length_diff_record = 0.0


            elif self.pilus_length == 0.0:
                self.length_state = "inactive"
                self.hook_state = "inactive"
                self.length_diff_record = 0.0
                self.ChangeLengthState()
                if self.length_state == "extend":
                    self.hook_state = "free"
                    length_diff = self.LengthDifference()
                    self.pilus_length = (max([self.pilus_length + length_diff, 0.0])) #size can not be smaller than 0

            if self.record_length:
                if counter % self.save_resolution == 0:
                    self.length_record.append(self.pilus_length)
                    self.force_record.append(self.TensionForce())

            self.HookOccurenceCounter(self.hook_state)
            self.LengthOccurenceCounter(self.length_state)
            self.LengthActivationOccurenceCounter(self.length_state)
        
        self.LengthOccurenceCounterFinalize()
        self.HookOccurenceCounterFinalize()
        self.LengthActiveOccurenceCounterFinalize()
        self.final_time = time

    
    def TensionForce(self):
        F_tension = self.k_spring*(abs(min(0, self.length_diff_record))) #No pushing
        return F_tension
    

    def GillespieAlgorithm(self, rate_dict):
        states = rate_dict.keys()
        propensity = sum(rate_dict.values())
        probability_of_not_reacting_in_dt = 1 - math.exp(-self.dt * propensity)

        r1 = random.uniform(0,1)
        if r1 > probability_of_not_reacting_in_dt: #checking if an event happens in dt
            return (False, None) #(is the state changed, which state to move to)
        else:
            #We divide the interval (0,1) into pieces with lengths proportional
            #to the rates. We pick a random number to determine which state to go to.
            r2 = random.uniform(0,1) 
            bound = 0
            for state in states:
                rate = rate_dict[state]
                normalized_rate = rate / propensity #so that they add up to 1
                bound += normalized_rate
                if r2 < bound: 
                    return (True, state)#(is the state changed, which state to move to)
    
    def ChangeLengthState(self):
        length_prob_dict = {
            "retract":{
                "idle": self.k_r0
            },
            "extend":{
                "idle": self.k_e0
            },
            "idle": {
                "retract": self.k_0r,
                "extend": self.k_0e
            },
            "inactive": {
                "extend": self.k_on,
            }
        }
        state_changed, new_state = self.GillespieAlgorithm(length_prob_dict[self.length_state])
        if state_changed:
            self.length_state = new_state

    def ChangeHookState(self):
        unbind_rate = self.k_unbind*math.exp(self.TensionForce()/self.F_sens)
        hook_prob_dict = {
            "free": {
                "hooked": self.k_bind
            },
            "hooked": {
                "free": unbind_rate
            }
        }
        state_changed, new_state = self.GillespieAlgorithm(hook_prob_dict[self.hook_state])
        if state_changed:
            self.hook_state = new_state

                
    def LengthDifference(self):
        dt = self.dt
        retraction_speed = self.v_r*(1-(self.TensionForce())/(self.F_stall))
        if self.length_state == "extend":
            return dt*self.v_e
            
        elif self.length_state == "retract":
            return - dt*retraction_speed
        
        elif self.length_state == "idle":
            return 0
        
