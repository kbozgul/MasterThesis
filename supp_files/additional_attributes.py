import math

def AdditionalAttributes(self):
    #additional assistant attributes
    if self.record_length:
        self.length_record = []
        self.force_record = []


    self.pilus_length = self.pilus_initial_length

    self.hook_occurence_dict = {}
    self.hook_last_count = 0
    self.hook_last_string = None

    self.length_occurence_dict = {}
    self.length_last_count = 0
    self.length_last_string = None

    self.length_active_occurence_dict = {}
    self.length_active_last_count = 0
    self.length_active_last_string = None

    self.final_time = -1000000.0 #ease to debug



def simplify_dict(dictionary):
    simplified_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            nested_simplified_dict = simplify_dict(value)
            simplified_dict.update(nested_simplified_dict)
        else:
            simplified_dict[key] = value
    return simplified_dict

