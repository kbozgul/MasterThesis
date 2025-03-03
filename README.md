


# Questions
+ Can it be that true that $v_{0} = v_{r}$? Beacuse under the condition $F_{tension} = 0$, retraction speed should be equal to it's default value (it's value during the unhooked state).


# About the Code
Some relevant plots can be found in `plot_class_folder/plotter.ipynb`

## Important Points
+  Use `main.py` to run the whole code and use `params.yaml` to enter the paramters.
+  The code now works with small time increments instead of proper Gillespie Algorithm
+  Also new parameters were added: `F_stall`, `v_0`, `k_spring`, `exp_delta (kinetic term)`. 
+  The most important details of the code are apparent in the `PerformOneRealization(self)` function in `pilus_class_folder/pilus_class.py`.
+  There are 2 length records (inside `__init__()`), `L_list` and `L_0_list`, keeping the record of the real and rest lengths w.r.t. time. The difference between these values determines the streching force of the pilus which changes the retraction speed of the rest length and also the unhooking rate, `k_hf`.

## Notes

#### Gillespie:
How the Gillespie algorithm works can be seen from `ReturnNewState(self, rate_dict)`. It takes the information of the rates between the states via a dictionary object (from `pilus_class_folder/prob_dicts.py`). More details can be found in `pilus_class_main.py`.

#### Hook States
The pilus object has a  parameter called `hook_state`, which takes the values ` 'free' ` or ` 'hooked' `.
If the pilus is in the free state, $L$ and  $L_{\circ}$ are equal to each other and their value change with the stochastic process provided by the [paper](https://www.biorxiv.org/content/10.1101/2023.05.09.538458v1.full). However, if the pilus is hooked, then $L$ remains the same and $L_0$ changes with the same process but with changing unhooking rate and retraction speed.

#### Retraction Speed

During the hook state, the retraction speed, $v_r$, changes linearly with the tension force of the pilus.
The streching force has the following spring-like formula:
$$F_{tension} = K max(L - L_{\circ},0)$$
````
def ReturnTensionForce(self):
	return self.k_spring * (max(0, self.L_current - self.L_0_current))
````
And the retraction speed is:
$$v_{r} = v_{\circ} \Big(1- \frac{F_{tension}}{F_{stall}} \Big)$$
````
def ReturnRetractionSpeed(self):
	F_tension  =  self.ReturnTensionForce()
	v_retract  =  self.v_0*(1-(F_tension)/(self.F_stall))
	self.retraction_speed_list.append(v_retract)
	return  v_retract 
````
for some free parameters $v_{\circ}$ and $F_{stall}$.

#### Unhooking Rate
One can increase the value of unhooking rate, `k_hf` by setting the `include_kinetic_pr` parameter from `params.yaml` to `True`. Once it's turned on, the unhooking rate gets to multiplied by $e^{\Delta}$(`exp_delta` in `params.yaml`), which makes the unhooking process more frequent.

In the [paper](https://www.biorxiv.org/content/10.1101/2023.05.09.538458v1.full), the change of the unhooking rate also depends on $L - L_{\circ}$ value. However, neither in the actual paper nor in the supplementary material, is there any information about how to get the value.






