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

        while (time <= self.total_time) and (self.object_position > self.object_radius):
            time += self.dt
            counter += 1
            if counter % progress_interval == 0:  # Check if we've hit a 10% interval
                progress = (counter / (self.total_time/self.dt)) * 100  # Calculate actual percentage
                print(f"At {int(progress)}% of the Total Time")

            if self.pilus_length > 0.0:
                if self.IsEligibleForHook():
                    self.ChangeHookState()
                else:
                    self.hook_state = "free"
                self.ChangeLengthState()
                length_diff = self.LengthDifference()
                self.pilus_length = (max([self.pilus_length + length_diff, 0.0]))
                if self.hook_state == "hooked":
                    self.MoveObject(length_diff)

            elif self.pilus_length == 0.0:
                self.length_state = "inactive"
                self.hook_state = "inactive"
                self.length_diff_record = 0.0
                self.ChangeLengthState()
                if self.length_state == "extend":
                    self.hook_state = "free"
                    self.pilus_theta = random.uniform(0, self.theta_range)
                    length_diff = self.LengthDifference()
                    self.pilus_length = (max([self.pilus_length + length_diff, 0.0])) #size can not be smaller than 0

            if self.record_length:
                if counter % self.save_resolution == 0:
                    self.length_record.append(self.pilus_length)
                    self.object_dist_record.append(self.object_position)
                    self.pilus_angle_record.append(self.pilus_theta)
                    self.object_angle_record.append(self.object_theta)

            self.HookOccurenceCounter(self.hook_state)
            self.LengthOccurenceCounter(self.length_state)
            self.LengthActivationOccurenceCounter(self.length_state)
        
        self.LengthOccurenceCounterFinalize()
        self.HookOccurenceCounterFinalize()
        self.LengthActiveOccurenceCounterFinalize()
        if self.object_position <=  self.object_radius:
            self.object_reached_cell = True
        self.final_time = time

           
    def IsEligibleForHook(self): #check if the object is in the right region to be hooked
        psi = abs(math.radians(self.pilus_theta - self.object_theta))
        if self.object_position*math.sin(psi) > self.object_radius:
            return False
        a = math.sqrt((self.object_radius)**2 - (self.object_position*math.sin(psi))**2)
        pilus_is_too_short = self.pilus_length < self.object_position*math.cos(psi) - a
        pilus_is_too_long = self.pilus_length - self.L_hook_region > self.object_position*math.cos(psi) + a
        if pilus_is_too_short or pilus_is_too_long:
            return False
        return True


    def MoveObject(self, length_diff):
        if self.hook_state == "hooked":
            delta_x = length_diff*math.cos(math.radians(self.pilus_theta)) #important that it is pilus theta
            delta_y = length_diff*math.sin(math.radians(self.pilus_theta)) #important that it is pilus theta
            self.object_x = self.object_x + delta_x
            self.object_y = self.object_y + delta_y
            self.object_position = math.sqrt(((self.object_x)**2)+((self.object_y)**2))
            self.object_theta = math.degrees(math.atan(self.object_y/self.object_x))
        else:
            pass
    

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
        hook_prob_dict = {
            "free": {
                "hooked": self.k_bind
            },
            "hooked": {
                "free": self.k_unbind
            }
        }
        state_changed, new_state = self.GillespieAlgorithm(hook_prob_dict[self.hook_state])
        if state_changed:
            self.hook_state = new_state

                
    def LengthDifference(self):
        dt = self.dt

        if self.length_state == "extend":
            return dt*self.v_e
            
        elif self.length_state == "retract":
            return - dt*self.v_r
        
        elif self.length_state == "idle":
            return 0
        
