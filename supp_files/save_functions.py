import os
import datetime
import csv
import shutil
import yaml
from .save_helpers import AverageDictionary

def CheckandCreateFolder():
    data_folder_path = r'C:\Users\bozguel\data_for_thesis\2D_new'
    #data_folder_path = '/home/kaan/Documents/data/2D_spherical'

    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    timestamped_folder_path = os.path.join(data_folder_path, timestamp)
    os.makedirs(timestamped_folder_path, exist_ok=True) #check this out
    return timestamped_folder_path

def SaveRealization(self, timestamped_folder_path, realization):
    folder_path = os.path.join(timestamped_folder_path, r'data', realization)
    os.makedirs(folder_path, exist_ok=True)
    metadata_file_path = os.path.join(folder_path, "metadata.yaml")
    yaml_file_path = os.path.join(folder_path, "other_data.yaml")

    if self.record_length == True:
        csv_file_path = os.path.join(folder_path, "length_record.csv")
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["length", "object_distance", "pilus_angle", "object_angle", "tension_force"])
            for i in range(len(self.length_record)):
                    writer.writerow([self.length_record[i], self.object_dist_record[i], self.pilus_angle_record[i], self.object_angle_record[i], self.force_record[i]])


    with open(metadata_file_path, 'w') as file:
        yaml.dump(self.params_dict, file)

        other_data_dict = {
            "hook_stats" : AverageDictionary(self.hook_occurence_dict, self.dt),
            "length_stats" : AverageDictionary(self.length_occurence_dict, self.dt),
            "active_time_stats": AverageDictionary(self.length_active_occurence_dict, self.dt),
            "object_reached_cell": self.object_reached_cell,
            "final_time": self.final_time,
        }

        with open(yaml_file_path, 'w') as file:
            yaml.dump(other_data_dict, file)  # Write the data to the YAML file
        
    

    