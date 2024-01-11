from os import popen, system
import sys
from time import sleep
from random import shuffle


cmd = 'python3 your_script.py' # Script which you want to execute.



def get_gpu_ids():
    gpu_ids = popen("nvidia-smi -L | cut -d ' ' -f 2 | cut -c 1").read().split('\n')
    while '' in gpu_ids:
        gpu_ids.remove('')
    return gpu_ids



def gpu_info(gpu_index):
    # Explanation of parameters: 
    # 1. gpu_index: The ID of GPU.
    cmd_ = 'nvidia-smi -q -i ' + str(gpu_index)
    gpu_status = popen(cmd_).read().split('\n')
    for i in range(len(gpu_status)):
        if 'FB Memory Usage' in gpu_status[i]:
            total_memory = float(gpu_status[i+1].split(' ')[-2])
            memory = float(gpu_status[i+2].split(' ')[-2])
        if 'Utilization' in gpu_status[i]:
            gpu_utli = float(gpu_status[i+1].split(' ')[-2])
        if 'Power Draw' in gpu_status[i]:
            power = float(gpu_status[i].split(' ')[-2])
        if 'Power Limit' in gpu_status[i]:
            limit_power = float(gpu_status[i].split(' ')[-2])
    men_percent = (memory / total_memory) * 100.0
    # gpu_info_dict = {'GPU ID': gpu_index, 'Power': power, 'Limited Power': limit_power, 
    #                'Memory': memory, 'Total Memory': total_memory, 'Memory Percent': men_percent,
    #                'GPU Utilization': gpu_utli}
    # return gpu_info_dict
    return power, limit_power, memory, total_memory, men_percent, gpu_utli



def gpu_available(gpu_usage_demand:float=50.0, men_usage_demand:float=50.0, men_demand:float=1024.0, 
                  least_mem_usage:float=20.0, interval:int=20, execute:bool=False, 
                  reversed_ids:bool=False, random_ids:bool=True):
    ## Explanation of parameters: ##
    # 1. gpu_usage_demand: The required percentage (%) of available GPU-Utilization, default 50.00%.
    # 2. men_usage_demand: The required percentage (%) of available GPU memory, default 50.00%.
    #                      This parameter will be ingored if "gpu_usage_demand" is NOT 0.
    # 3. men_demand: The required available GPU memory, default 1024MiB. 
    #                This parameter will be ingored if "gpu_usage_demand" or "men_usage_demand" is NOT 0.
    # 4. least_mem_usage: The minimum ratio of available memory. Default 20.00%.
    #                     This parameter can avoid memory overflow.
    # 5. interval: Sleep for interval before starting checking, default 20 seconds.
    # 6. execute: If True, execute the script. If False, do NOT execute the script 
    #             and return the available GPU ID. Default False.
    # 7. reversed_ids: If True, reverse the GPU ID list checked. Default False.
    if not 0.0 <= gpu_usage_demand <= 100.0:
        raise ValueError("Invalid gpu_usage_demand value: {:.2f}%.".format(gpu_usage_demand))
    if not 0.0 <= men_usage_demand <= 100.0:
        raise ValueError("Invalid men_usage_demand value: {:.2f}%.".format(men_usage_demand))
    if not 0.0 < least_mem_usage < 100.0:
        raise ValueError("Invalid least_mem_usage value: {:.2f}%.".format(least_mem_usage))
    if gpu_usage_demand:
        print('\nThe required percentage of available GPU-Utilization is {:.2f}%.'.format(gpu_usage_demand))
    elif men_usage_demand:
        print('\nThe required percentage of available GPU memory is {:.2f}%.'.format(men_usage_demand))
    else:
        print('\nThe required available GPU memory is {:.0f} MiB.'.format(men_demand))
    
    print('\nSleep for {:.0f} seconds before starting checking GPUs.'.format(interval))

    ids = get_gpu_ids()
    if random_ids:
        shuffle(ids)
    elif reversed_ids:
        ids.reverse()
        
    max_total_men = 0
    waitting = True
    print_counter = -1
    first_check = True
    while waitting:
        print_counter += 1
        sleep(interval)
        for gpu_id in ids:
            if first_check and not gpu_usage_demand and not men_usage_demand:
                gpu_power, limit_power, gpu_memory, toal_memory, men_percent, gpu_utli = gpu_info(gpu_id)
                if toal_memory > max_total_men:
                    max_total_men = toal_memory
                if gpu_id == ids[-1] and max_total_men < men_demand:
                    raise Exception("Invalid men_demand value: {} MiB. Max GPU memory is {:.0f} MiB.".format(men_demand,max_total_men))

            for i in range(5): # Check GPU[gpu_id] for 5 seconds.
                gpu_power, limit_power, gpu_memory, toal_memory, men_percent, gpu_utli = gpu_info(gpu_id)
                available_gpu_utli = 100.0 - gpu_utli
                available_mem_usage = 100.0 - men_percent
                available_men = toal_memory - gpu_memory
                if gpu_usage_demand and gpu_usage_demand <= available_gpu_utli and least_mem_usage <= available_mem_usage:
                    waitting = False
                    print('\nNow GPU[ID {}] available GPU-Utilization: {:.2f}%.'.format(gpu_id,available_gpu_utli))
                    break
                elif not gpu_usage_demand and men_usage_demand and men_usage_demand <= available_mem_usage and least_mem_usage <= available_mem_usage:
                    waitting = False
                    print('\nNow GPU[ID {}] available memory usage: {:.2f}%.'.format(gpu_id,available_mem_usage))
                    break
                elif not gpu_usage_demand and not men_usage_demand and men_demand <= available_men and least_mem_usage <= available_mem_usage:
                    waitting = False
                    print('\nNow GPU[ID {}] available memory: {:.0f} MiB.'.format(gpu_id,available_men))
                    break
                if print_counter % 60 == 0:
                    # after monitoring all GPUs every 60 times, print monitoring logs.
                    # the interval between the printing is about 60*(interval+5*len(ids)) seconds.
                    # so if you have 6(=len(ids)) GPUs and set ```interval``` as default, it will take about 50 minutes.
                    print_counter = 0
                    symbol = 'Monitoring: ' + '>' * (i+1) + ' ' * (4 - i) + '|'
                    gpu = '[GPU:{}]'.format(gpu_id)
                    gpu_utli_str = 'GPU-Utilization {:.2f}% |'.format(gpu_utli)
                    gpu_memory_str = 'Memory in use: %dMiB / %dMiB |' % (gpu_memory,toal_memory)
                    gpu_memory_per_str = 'Memory Usage: {:.2f}% |'.format(men_percent)
                    gpu_power_str = 'Power: {:.2f}W / {:.2f}W |'.format(gpu_power,limit_power)
                    sys.stdout.write('\r' + gpu + ' '+ gpu_utli_str +' ' + gpu_memory_str + ' ' + gpu_memory_per_str+ ' '+ gpu_power_str+ ' ' + symbol)
                    sys.stdout.flush()
                sleep(1)
            if not waitting:
                break
        first_check = False
    if execute:
        system(cmd)
    else:
        return gpu_id



if __name__ == '__main__':
    print(gpu_available(gpu_usage_demand=50, men_usage_demand=78, men_demand=24382, 
                        interval=1, reversed_ids=True, random_ids=False))
