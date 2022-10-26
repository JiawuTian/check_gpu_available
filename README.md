# Introduction
Check GPU(s) whether available under some conditions.  
Script ```check_gpu_available.py``` contains the following functions:  
```python
gpu_info(gpu_index)
```
```python
gpu_available(usage_demand: float=50.0, men_demand: float=1024.0, interval: int=20, execute: bool=False)
```
# How it works
```gpu_info(gpu_index)``` will get the GPU information with ID of ```gpu_index```, and return ```power```, ```memory```, ```total_memory```, ```percent```.  
```gpu_available(usage_demand: float=50.0, men_demand: float=1024.0, interval: int=20, execute: bool=False)``` performs checking and returns the available GPU ID (if parameter ```execute``` is ```False``` (default)) or executes your script (if parameter ```execute``` is ```True```).



# Usage
