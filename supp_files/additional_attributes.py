import math

def AdditionalAttributes(self):
    #additional assistant attributes
    if self.record_length:
        self.length_record = []
        self.object_dist_record = []
        self.object_angle_record = []
        self.pilus_angle_record = []

    self.object_theta = self.theta_range/2
    self.object_position = self.object_initial_distance
    self.object_reached_cell = False
    self.object_x = self.object_position * math.cos(math.radians(self.object_theta))
    self.object_y = self.object_position * math.sin(math.radians(self.object_theta))

    self.pilus_length = self.pilus_initial_length
    self.pilus_theta = 0.0

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

