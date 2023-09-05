#!/usr/bin/env python
#### 1. Create a simple inventory that contains just a hosts.yaml file. 
'''
In this hosts.yaml file add just one device entry.  Additionally, for the device entry device just one field 'hostname: localhost'.

Using the Python interpreter shell and the hosts.yaml file that you just created:
1. Create a Nornir object using InitNornir
2. Look at nr.inventory
3. Look at nr.inventory.hosts
4. Look at nr.inventory.hosts['name'] where 'name' is the name of the entry you created in hosts.yaml.
5. Look at nr.inventory.hosts['name'].hostname
'''

import sys
sys.path.append('/home/taylor/VENV/py3_venv/lib/python3.9/site-packages')
from nornir import InitNornir

def print_inventory(nr):
    """Look at nr.inventory

    Args:
        nr (nornir object): prints out nornir.inventory
    """
    print("Printing the nr.inventory:")
    print(nr.inventory)
    print()
    
    
def print_hosts(nr):
    """Look at nr.inventory.hosts

    Args:
        nr (nornir object): Nornir.inventory.hosts looks like a dictionary.
    """
    print("Printing the nr.inventory.hosts")
    print(nr.inventory.hosts)
    print()
    
    
def print_hosts_name(nr, name=str):
    """4. Look at nr.inventory.hosts['name'] where 'name' is the name of the entry you created in hosts.yaml.

    Args:
        nr (nornir object): nornir object
        name (str, optional): name of the entry created in hosts.yaml. Defaults to str.
    """
    print("Printing the hostname")
    print(f"The key, 'my_host' is: {nr.inventory.hosts[name]}")
    print()
    
    
def print_hosts_name_hostname(nr, name):
    """5. Look at nr.inventory.hosts['name'].hostname

    Args:
        nr (nornir object): hosts['name'].hostname
    """
    print(nr.inventory.hosts[name].hostname)
        
    
def init_nor():
    """1. Create a Nornir object using InitNornir

    Returns:
        nornir object: nornir object
    """
    nr = InitNornir()
    return nr

def main():
    nr = init_nor()
    print_inventory(nr)
    print_hosts(nr)
    print_hosts_name(nr, "my_host")
    print_hosts_name_hostname(nr, "my_host")

if __name__ == '__main__':
    main()