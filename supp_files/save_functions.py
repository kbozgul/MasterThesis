import os
import datetime
import csv
import shutil
import yaml
from .save_helpers import AverageDictionary


def CheckandCreateFolder():
    # Get the parent directory of 'supp_files', which contains 'main.py'
    main_script_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))

    # Define the folder path next to 'main.py'
    data_folder_path = os.path.join(main_script_dir, 'data_for_thesis', 'surface_adhesion_data')

    # Create the folder if it doesn't exist
    os.makedirs(data_folder_path, exist_ok=True)


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
        csv_file_path = os.path.join(folder_path, "record_data.csv")
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["length", "tension_force"])
            for i in range(len(self.length_record)):
                    writer.writerow([self.length_record[i], self.force_record[i]])


    with open(metadata_file_path, 'w') as file:
        yaml.dump(self.params_dict, file)

        other_data_dict = {
            "hook_stats" : AverageDictionary(self.hook_occurence_dict, self.dt),
            "length_stats" : AverageDictionary(self.length_occurence_dict, self.dt),
            "active_time_stats": AverageDictionary(self.length_active_occurence_dict, self.dt),
            "final_time": self.final_time,
        }

        with open(yaml_file_path, 'w') as file:
            yaml.dump(other_data_dict, file)  # Write the data to the YAML file
        
    

    