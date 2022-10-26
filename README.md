# Introduction
Check NVIDIA GPU(s) whether available under some conditions.  
Script ```check_gpu_available.py``` contains the following functions:  
```python
gpu_info(gpu_index)
```
Explanation of parameters: 
1. ```gpu_index```: The ID of GPU.

```python
gpu_available(usage_demand: float=50.0, men_demand: float=1024.0, interval: int=20, execute: bool=False)
```
Explanation of parameters: 
1. ```usage_demand```: The required percentage (%) of available GPU memory, default 50.00%.
2. ```men_demand```: The required available GPU memory, default 1024MiB. 
3. ```interval```: Sleep for interval before starting checking, default 20 seconds.
4. ```execute```: If True, execute the script. If False, do not execute the script and return the available GPU ID. Default False.


# How it works
```gpu_info()``` will get the GPU information with ID of ```gpu_index```, and return ```power```, ```memory```, ```total_memory```, ```percent```.  
```gpu_available()``` performs checking and returns the available GPU ID (if parameter ```execute``` is ```False``` (default)) or executes your script (if parameter ```execute``` is ```True```).  
```gpu_available()```  will always perform checking until ```waitting``` becomes ```False```, which determined by some conditions ```usage_demand``` or ```men_demand```.



# Usage
