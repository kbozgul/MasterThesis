import math
import os
import datetime
import itertools
import yaml
import csv
import shutil
from supp_files.pilus_class_main import pilus_object
from supp_files.additional_attributes import simplify_dict
from supp_files.save_functions import CheckandCreateFolder
from parameter_sweep import parameter_sweep_dict


def read_params_from_yaml(file_name):
    with open(file_name, 'r') as yaml_file:
        params_dict = yaml.safe_load(yaml_file)
    return params_dict
params_dict = simplify_dict(read_params_from_yaml("params.yaml"))



timestamped_folder_path = CheckandCreateFolder()

keys = list(parameter_sweep_dict.keys())
values = list(parameter_sweep_dict.values())

for realization_number, combination in enumerate(itertools.product(*values)): #writes all the combinations of the param values
    print(f"INSIDE REALIZATION: {realization_number + 1}")
    for i, key in enumerate(keys):
        if key not in params_dict:
            raise KeyError(f"Key '{key}' not found in the params dictionary.")
        params_dict[key] = combination[i]
    pilus = pilus_object(params_dict)
    print(f"PERFORMING REALIZATION")
    pilus.PerformOneRealization()

    print(f"SAVING REALIZATION")
    pilus.SaveRealization(timestamped_folder_path, str(realization_number + 1))

with open(os.path.join(timestamped_folder_path, 'parameter_sweep_dict.yaml'), 'w') as file:
    yaml.dump(parameter_sweep_dict, file)  # Write the data to the YAML file