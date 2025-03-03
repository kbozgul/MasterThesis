
from collections import defaultdict
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

def HaveSameLength(list_of_lists):
    current_length = len(list_of_lists[0])
    for listt in list_of_lists:
        if not current_length == len(listt):
            return (False, [len(x) for x in list_of_lists])
    return (True, "")

def MultiplyFloatsinDict(data, multiplier):
    """
    Recursively traverse a dictionary, multiplying all float values by a given multiplier.
    
    :param data: The dictionary to process (can be nested with dictionaries as values).
    :param multiplier: The number to multiply float values by.
    :return: The updated dictionary with floats multiplied.
    """
    if isinstance(data, dict):
        # If data is a dictionary, recursively process its values
        for key, value in data.items():
            data[key] = MultiplyFloatsinDict(value, multiplier)
    elif isinstance(data, float):
        # If data is a float, multiply it by the multiplier
        data *= multiplier
    return data



def AverageConsecutiveTimes(array):
    consecutive_dict = defaultdict(list)
    
    current_string = None
    current_count = 0
    
    for string in array:
        if string == current_string:
            current_count += 1
        else:
            if current_string is not None:
                consecutive_dict[current_string].append(current_count)
            current_string = string
            current_count = 1
    
    if current_string is not None:
        consecutive_dict[current_string].append(current_count)
    
    average_consecutive_dict = {
        key: sum(values) / len(values) for key, values in consecutive_dict.items()
    }
    
    return dict(average_consecutive_dict)


def LifeTimeLengths(array, dt):
    consecutive_counts = []
    
    current_string = None
    current_count = 0
    
    for string in array:
        if string == current_string:
            current_count += 1
        else:
            if current_string is not None and current_string != "inactive":
                consecutive_counts.append(current_count)
            current_string = string
            current_count = 1
    
    if current_string is not None and current_string != "inactive":
        consecutive_counts.append(current_count)
    
    consecutive_counts = [x*dt for x in consecutive_counts]
    filtered = [x for x in consecutive_counts if x > 1.0] #filter them not to include ones that are smaller than 1.0sec
    return filtered


def TotalCountsinPercents(arrayy):
    total_length = len(arrayy)
    count_dict = defaultdict(int)
    
    for string in arrayy:
        count_dict[string] += 1

    for key, value in count_dict.items():
        count_dict[key] = (value / total_length) * 100
    
    return dict(count_dict)


def FirstHookingtime(array, dt, search_string):
    counter = 0
    for i in array:
        if i == search_string:
            return counter*dt
        else:
            return 0.0

def AnalyzeConsequtiveOccurences(strings, dt, search_string=None):
    """
    Analyzes consecutive occurrences in an array.
    
    If `search_string` is provided, interprets the array as True/False values
    based on whether elements match `search_string`. Returns statistics for
    `search_string` and its complement.
    
    If `search_string` is not provided, analyzes consecutive occurrences of
    all unique strings in the array.

    Args:
        strings (list of str): List of strings to analyze.
        search_string (str, optional): String to consider as True; others as False.

    Returns:
        dict: If `search_string` is provided, a dictionary with keys `search_string`
              and `non_search_string`, each containing 'mean_length' and 'std'.
              Otherwise, a dictionary with statistics for all unique strings.
    """
    def convert_to_python(obj):
        """Ensure all values are standard Python types."""
        if isinstance(obj, np.generic):  # Handle NumPy scalars
            return obj.item()
        return obj

    def calculate_stats(counts):
        """Calculate mean and std, ensuring Python-native types."""
        mean_length = float(np.mean(counts)) if counts else 0
        std = float(np.std(counts, ddof=1)) if len(counts) > 1 else 0
        return {'mean_length': convert_to_python(mean_length), 'std': convert_to_python(std)}

    if search_string is not None:
        # Behavior when `search_string` is provided
        is_target = [s == search_string for s in strings]  # Convert to True/False based on search_string
        occurrences_target = []
        occurrences_non_target = []

        # Calculate consecutive occurrences
        current_value = None
        count = 0
        for val in is_target:
            if val == current_value:
                count += 1
            else:
                if current_value is not None:
                    if current_value:  # True (search_string)
                        occurrences_target.append(count)
                    else:  # False (non_search_string)
                        occurrences_non_target.append(count)
                current_value = val
                count = 1
        # Add the last streak
        if current_value is not None:
            if current_value:
                occurrences_target.append(count)
            else:
                occurrences_non_target.append(count)

        result_dict = {
            f"{search_string}": calculate_stats(occurrences_target),
            f"non_{search_string}": calculate_stats(occurrences_non_target)
        }
        
        return MultiplyFloatsinDict(result_dict, dt)
    
    else:
        # Behavior when `search_string` is not provided
        result_dict = {}
        current_string = None
        count = 0
        occurrences = {}

        # Calculate consecutive occurrences
        for s in strings:
            if s == current_string:
                count += 1
            else:
                if current_string is not None:
                    occurrences.setdefault(current_string, []).append(count)
                current_string = s
                count = 1
        # Add the last streak
        if current_string is not None:
            occurrences.setdefault(current_string, []).append(count)

        # Calculate mean and standard deviation
        for string, counts in occurrences.items():
            mean_length = float(np.mean(counts))
            std = float(np.std(counts, ddof=1)) if len(counts) > 1 else 0
            result_dict[string] = {'mean_length': convert_to_python(mean_length), 'std': convert_to_python(std)}

        return MultiplyFloatsinDict(result_dict, dt)

def HookOccurenceCounter(self, string):
    # Process a single string
    if self.hook_last_string is None or self.hook_last_string == string:
        self.hook_last_count += 1
    else:
        # Store the count for the last string
        if self.hook_last_string not in self.hook_occurence_dict:
            self.hook_occurence_dict[self.hook_last_string] = []
        self.hook_occurence_dict[self.hook_last_string].append(self.hook_last_count)
        # Reset the count for the new string
        self.hook_last_count = 1
    # Update the last string to the current string
    self.hook_last_string = string

def HookOccurenceCounterFinalize(self):
    # Finalize to store the last string's occurrences
    if self.hook_last_string is not None:
        if self.hook_last_string not in self.hook_occurence_dict:
            self.hook_occurence_dict[self.hook_last_string] = []
        self.hook_occurence_dict[self.hook_last_string].append(self.hook_last_count)
    # Reset attributes for potential reuse
    self.hook_last_count = 0
    self.hook_last_string = None

def LengthOccurenceCounter(self, string):
    # Process a single string
    if self.length_last_string is None or self.length_last_string == string:
        self.length_last_count += 1
    else:
        # Store the count for the last string
        if self.length_last_string not in self.length_occurence_dict:
            self.length_occurence_dict[self.length_last_string] = []
        self.length_occurence_dict[self.length_last_string].append(self.length_last_count)
        # Reset the count for the new string
        self.length_last_count = 1
    # Update the last string to the current string
    self.length_last_string = string

def LengthOccurenceCounterFinalize(self):
    # Finalize to store the last string's occurrences
    if self.length_last_string is not None:
        if self.length_last_string not in self.length_occurence_dict:
            self.length_occurence_dict[self.length_last_string] = []
        self.length_occurence_dict[self.length_last_string].append(self.length_last_count)
    # Reset attributes for potential reuse
    self.length_last_count = 0
    self.length_last_string = None

def LengthActivationOccurenceCounter(self, string):
    if string != "inactive":
        string = "active"
    # Process a single string
    if self.length_active_last_string is None or self.length_active_last_string == string:
        self.length_active_last_count += 1
    else:
        # Store the count for the last string
        if self.length_active_last_string not in self.length_active_occurence_dict:
            self.length_active_occurence_dict[self.length_active_last_string] = []
        self.length_active_occurence_dict[self.length_active_last_string].append(self.length_active_last_count)
        # Reset the count for the new string
        self.length_active_last_count = 1
    # Update the last string to the current string
    self.length_active_last_string = string

def LengthActiveOccurenceCounterFinalize(self):
    if self.length_active_last_string is not None:
        if self.length_active_last_string not in self.length_active_occurence_dict:
            self.length_active_occurence_dict[self.length_active_last_string] = []
        self.length_active_occurence_dict[self.length_active_last_string].append(self.length_active_last_count)
    # Reset attributes for potential reuse
    self.length_active_last_count = 0
    self.length_active_last_string = None

def AverageDictionary(dictt, dt):
    def AverageList(array):
        return sum(array)/len(array)
    
    for key, value in dictt.items():
        dictt[key] = AverageList(value)*dt
    return dictt