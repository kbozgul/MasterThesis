

### How to Run the Code

Run `main.py` to run the whole code and use `params.yaml` to enter the parameters.  The values on the `parameter_sweep.py` file will be replaced to `params.yaml` for each combination possible. Example usage :
If one sets `parameter_sweep.py` file to be:
```
parameter_sweep_dict  = {
"object_radius": [0.05, 0.1],
"object_initial_distance": [0.6]
}
```
then the simulation will run twice for the parameter combinations {(0.05,0.6), (0.1,0.6)} for `object_radius` and `object_initial_distance` respectively.
 
### Saving Data

#### Save Location
When run, the code will create a folder in the root directory with the name `data_for_thesis/<simulation_type>`, with a time-stamped folder for each run. Time-stamped folder will include the data of all realizations in different folders with integers. (for the example given in the previous section there will be two folders: `data_for_thesis/object_uptake_data/<time_stamp>/1` and `2`).

#### Record Data
 In each of these integer named folders, there will be a file called `record_data.csv` that includes the time series data of certain variables. This functionality can be disabled using `params.yaml/simulation/record_length` or reduced in resolution using  `save_resolution`.

#### Other Data

In the folders, there will also be a file called `other_data.yaml`, where the mean time spent in each state will be given.