#!/usr/bin/env python3
'''2a. Create a new configuration file named config.yaml. Using the SimpleInventory Plugin, 
point the host_file, the group_file, and the defaults_file to the respective files in 
the ~/nornir_inventory directory. This config.yaml file will be used throughout the course unless otherwise noted. 

Your config.yaml file should look similar to the following: 

---
inventory:
  plugin: SimpleInventory
  options:
    host_file: "~/nornir_inventory/hosts.yaml"
    group_file: "~/nornir_inventory/groups.yaml"
    defaults_file: "~/nornir_inventory/defaults.yaml"

Filter your inventory to select ONLY devices that belong to the "ios" group.

NOTE: We will cover inventory filtering later in the course, but for now, add the following 
to your script after initializing your Nornir object (this will filter to select only the "ios" group): 

from nornir.core.filter import F
filt = F(groups__contains="ios")
nr = nr.filter(filt)

Print out your inventory hosts after you accomplish your filtering: 

print(nr.inventory.hosts)


Brannen Taylor - 20230910
'''
from nornir import InitNornir
import pdbr
import os
from nornir_netmiko import netmiko_send_command  # used in ex. 2b.

def init_nornir():
    """Initializes norir.  Returns a nornir object.

    Returns:
        nornir_object: nornir object
    """
    nr = InitNornir(config_file="config.yaml")
    return nr

def check_workers(nr):
    """Small function to output the number or nornir workers

    Args:
        nr (nornir object): nornir object
    """
    workers = nr.runner.num_workers  # nr.runner.num_workers
    print(f"nr workers = {workers}")
    
def filter_inventory(nr, group_name):
    """2a. We will cover inventory filtering later in the course, but for now, 
    add the following to your script after initializing your Nornir object 
    (this will filter to select only the "ios" group): 

    Args:
        nr (nornir_object): nornir object
        group_name (str): the group name you want to filter on.

    Returns: filt (nornir.core.filter.F) - returns a nornir filter
    """
    
    # We will cover inventory filtering later in the course
    from nornir.core.filter import F
    filt = F(groups__contains=group_name)
    nr = nr.filter(filt)
    
        
    filter_results = nr.inventory.hosts
    print("From: func'filter_function:'")
    print(f"Inventory hosts with '{group_name}': {filter_results}\n")
    
    return filt
    
def show_hostname(nr, filt):
    """2b. Create a Python script that uses netmiko_send_command to execute "show run | inc hostname" 
    on all the "ios" devices in your inventory (once again use the filter that you created in exercise 2a). 
    Assign the result of this task to a variable named "my_results".

    Print the "type" of the my_results object. Additionally, inspect the my_results object using its 
    "keys()", "items()" and "values" methods.

    """
    print("From: func show_hostname")
    nr = nr.filter(filt)
    # filter_results = nr.inventory.hosts
    command = f'show run | inc cisco3'
    my_result = nr.run(task=netmiko_send_command, command_string=command)
    
    print(f"type(my_result): {type(my_result)}\n")
    print(f"my_result keys:\n{my_result.keys()}\n")
    print(f"my_result items:\n{my_result.items()}\n")
    print(f"my_result values:\n{my_result.values()}\n")
    
    # to get the actual output from the device, for cisco3:
    # print(f"output: {my_result['cisco3'][0].result}")
    # output: 'hostname cisco3\n path flash:cisco3-cfg'
    
    # 2c. Assign the results from "cisco3" to a new variable named "host_results". Inspect this new MultiResult 
    # object: access the zeroith element from this MultiResult object. Finally, determine if "host_results" is an iterable or not.
    host_results = my_result["cisco3"]
    # Inspecting var: {host_results} - #TODO Remove these two lines
    print(f"VARIABLE is type ==> {type(host_results)} \n {host_results}")
    print()
    
    # check if host_results is iterable
    try:
        iter(host_results)
        print(f"{host_results=} len {len(host_results)}")
        print(f"host_results[0] = {host_results[0]}")
        print(f"Type of data stored in host_results[0] is: {type(host_results[0])}")
        print(f"{host_results=}\nIS iterable.")
    except Exception as e:
        print(e)
    
    # 2d. Assign the zeroith element of the host_results object to a new variable named "task_result". 
    # What type of object is task_result? 
    # Print out the 'host', 'name', 'result', and 'failed' attributes from task_result. 
    # Which field actually contains the output from the network device?
    print(f"\nEx. 2d\n")
    task_result = host_results[0]
    print(f"type: {type(task_result)}")
    print(f"host: {task_result.host}")
    print(f"name: {task_result.name}")
    print(f"result: {task_result.result}")
    print(f"failed: {task_result.failed}")
    print()
    print(f"The field that actually contains the output from the network device is:\ntaks_result.result, which is:{task_result.result}\n")
    
    # 2e. Looking back at exercises 2a - 2d: explain what Nornir result types are "my_results", "host_results", 
    # and "task_result"? What purpose does each of those three data types serve (i.e. why do we have them)?
    print("'my_result' returns a dict like object with multiple results")
    print("'host_results' is a list like object from one single host.  It is iterable, but may only have one item in the list.")
    print("'task_result' is the result of the single task, on the single host.")

    # pdbr.set_trace()

def main():
    '''Main Function'''
    nr = init_nornir()
    check_workers(nr) # 1a
    filt = filter_inventory(nr, "ios") # 2a
    show_hostname(nr, filt) # 2b
    
    


if __name__ == '__main__':
    main()