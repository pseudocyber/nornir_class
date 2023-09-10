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

    Returns: no returns
    """
    
    # We will cover inventory filtering later in the course
    from nornir.core.filter import F
    filt = F(groups__contains=group_name)
    nr = nr.filter(filt)
    
    filter_results = nr.inventory.hosts
    print(f"Inventory hosts with '{group_name}': {filter_results}")
    


def main():
    '''Main Function'''
    nr = init_nornir()
    check_workers(nr) # 1a
    filter_inventory(nr, "ios") # 2a
    
    
    # pdbr.set_trace()


if __name__ == '__main__':
    main()