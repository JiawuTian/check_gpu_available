# Introduction
Check NVIDIA GPU(s) whether available under some conditions.  
Script ```check_gpu_available.py``` contains the following functions:  
```python
gpu_info(gpu_index)
```
Explanation of parameters for ```gpu_info```: 
1. ```gpu_index```: The ID of GPU.

```python
gpu_available(gpu_usage_demand:float=50.0, men_usage_demand:float=50.0, men_demand:float=1024.0,
              least_mem_usage:float=20.0, interval: int=20, execute: bool=False,
              reversed_ids:bool=False, random_ids:bool=True)
```
Explanation of parameters for ```gpu_available```: 
1. ```gpu_usage_demand```: The required percentage (%) of available GPU-Utilization, default 50.00%.
2. ```men_usage_demand```: The required percentage (%) of available GPU memory, default 50.00%. This parameter will be ingored if ```gpu_usage_demand``` is NOT 0.
3. ```men_demand```: The required available GPU memory, default 1024MiB. This parameter will be ingored if ```gpu_usage_demand``` or ```men_usage_demand``` is NOT 0.
4. ```least_mem_usage```: The least percentage (%) of available GPU memory, default 20.00%.
5. ```interval```: Sleep for interval before starting checking, default 20 seconds.
6. ```execute```: If True, execute the script. If False, do not execute the script and return the available GPU ID. Default False.
7. ```reversed_ids```: Reverse the GPU ID list. Default False.
8. ```random_ids```: Shuffle the GPU ID list. Default True.

# Requirements
Require ```torch``` installed. Installation guide can be found [here](https://pytorch.org/get-started/locally/).


# How it works
```gpu_info()``` will get the GPU information with ID of ```gpu_index```, and return ```power```, ```memory```, ```total_memory```, ```percent```.  
```gpu_available()``` performs checking and returns the available GPU ID (if parameter ```execute``` is ```False``` (default)) or executes your script (if parameter ```execute``` is ```True```).  
```gpu_available()```  will always perform checking until ```waitting``` becomes ```False```, which is determined by some conditions ```gpu_usage_demand``` or ```men_usage_demand``` or ```men_demand```.
It checks all GPU(s) by GPU ID and sleeps for ```interval``` before starting checking (default 20 seconds) to avoid one GPU FALSE AVAILABE which means in some cases such as asynchronization the GPU is loading data or is preparing for other program but meet your demand condition for this GPU at the same time.  
For checking every GPU, it checks no more than 5 seconds (also be called 5 times) either meeting your demand or turning to next GPU and keeping checking.

# Usage
There are two applications as following:
1. Set ```execute``` ```True``` and change ```cmd``` variable, then run the following code in your SSH terminal:
```shell
nohup ./check_gpu_available.py > ./nohup_output.log 2>&1 &
```
2. See [an asynchronous training example](https://github.com/EpicTian/async_train).

# Outputs
![图片](https://github.com/EpicTian/check_gpu_available/blob/main/output.png)

# Change logs
```2024-01-11```
1. Remove ```reverse``` parameter of ```gpu_available()```.
2. Add ```least_mem_usage```, ```reversed_ids``` and ```random_ids``` parameter to ```gpu_available()```.


```2022-12-21```
1. Improve ```gpu_info()``` getting GPU ID list.
2. Add ```reverse``` parameter to ```gpu_available()```.


```2022-11-05```
1. Fix ```gpu_info()``` getting memory information bug.
2. Add getting ```gpu_utli``` information to ```gpu_info()```.
3. Add ```gpu_usage_demand``` condition to ```gpu_available()```.
4. Update explanation of parameters of ```gpu_available()```.
