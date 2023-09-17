#!/usr/bin/env python3
'''Kirk Byers Nornir Class
8/17 BT

2. Filtering using the ".filter()" Method

2a. Using the inventory files from the previous exercise, create a Nornir object that is filtered to only "arista1". 
Use the .filter() method to accomplish this. Print the hosts that are contained in this new Nornir object.

2b. Using the filter method, create a Nornir object that is filtered to all devices using the role "WAN". 
Print the hosts that are contained in this new Nornir object. Further filter on this newly created Nornir 
object to capture only hosts using port 22. Once again, print the hosts in this new Nornir object.

2c. Using an F-filter, create a new Nornir object that contains all the hosts that belong to the "sfo" group. 
Print the hosts that are contained in this new Nornir object.

'''

from nornir import InitNornir
from nornir.core.filter import F  # useing "F"ilter Object - commonly used for group memebership - 2c.
import ipdb

import logging
log_format = "%(asctime)s-%(levelname)s-%(name)s-"\
             "%(filename)s-%(funcName)20s-%(lineno)d-%(message)s"
logging.basicConfig(filename='mylogs.log', filemode='w', level='INFO', format=log_format)


def init_nornir():
    logging.info(f"Entered function")
    return InitNornir(config_file="config.yaml")

def get_data(nr, host="str"):
    """
    1.a - Returns out the "data" attribute of the parameter host.
    Args:
        nr (a nornir object): nornir object
        host (str) : the host you want to look up in the inventory.
    """
    data = nr.inventory.hosts[host]
    logging.info(f"Returning: {data=}")
    return data

def get_items(nr, host:"str"):
    """Gets the items() method on host(host).
    
    Print out the "data" attribute of the "arista3" host. Call the "items()" method on host "arista3". 
    Notice that when calling the items() method that Nornir not only displays the "data" entries 
    associated at the host-level, but also recurses the data for the groups (that the host belongs to).

    Args:
        nr (nornir object): nornir object
        host (str): Hostname to call items() on.
    """
    data = nr.inventory.hosts[host].items()
    logging.info(f"Returning: {data=}")
    return data

def filter_single_host(nr, host: str):
    """2a. Using the inventory files from the previous exercise, create a Nornir object that is filtered to only "arista1". 
    Use the .filter() method to accomplish this. Print the hosts that are contained in this new Nornir object.

    Args:
        nr (Nornir object): Nornir object
        host (str): hostname to filter on

    Returns:
        Nornir Object: Filtered nornir object
    """
    data = nr.filter(name=host)  # Use the .filter() method
    logging.info(f"Returning: {data=}")
    return data

def filter_role_and_port(nr, role: str, port: int = None):
    """2b. Using the filter method, create a Nornir object that is filtered to all devices using the role "WAN". 
    Print the hosts that are contained in this new Nornir object. Further filter on this newly created 
    Nornir object to capture only hosts using port 22. Once again, print the hosts in this new Nornir object.

    Args:
        nr (Nornir object): Nornir object
        role (str): role to filter on

    Returns:
        Nornir Object: Filtered nornir object
    """
    if not port:
        data = nr.filter(role=role)  # Use the .filter() method
    else:
        data = nr.filter(role=role).filter(port=port)
    logging.info(f"Returning: {data=}")
    return data

def get_hosts(nr):
    """Returns the hosts from the Nornir object.

    Args:
        nr (nornir object): nornir object

    Returns:
        list: list of hosts from the nornir object
    """
    data = nr.inventory.hosts
    logging.info(f"Returning: {data=}")
    return data

def output(msg, hosts):
    print(f"\n{msg}\n{'-'*len(msg)}")
    for host in hosts:
        print(f"Host: {host}")
    print()
    
def get_group(nr, group:str):
    """Filtering hosts for group membership.

    Args:
        nr (nornir object): nornir object
        group (str): Group name to filter on

    Returns:
        nornir object: filtered nornir object
    """
    data = nr.filter(F(groups__contains=group))  # 2c.
    logging.info(f"Returning: {data=}")
    return data

def main():
    '''Main Function'''
    logging.info(f"Entered function")
    nr = init_nornir()
    logging.info(f"set nr")
    # ipdb.set_trace()
    
    # Applying Filters
    ##############################################
    # Set variables below to None not to use them.
    host = 'arista1'  # 2a
    role = 'WAN'  # WAN 2b
    port = 22  # 22 2b part 2
    group = 'sfo' # 'sfo' 2c.
    
    # 2a, 2b, 2c
    if group:  # filter the hosts based on a group. 2c.
        nr = get_group(nr, group)  # filter the nr object with "F"ilter.
        hosts = get_hosts(nr)  # Get the hosts from the filtered nornir object.
        msg = f"Hosts with group {group}"
    elif role and port and not group:
        nr = filter_role_and_port(nr, role, port)
        hosts = get_hosts(nr)
        msg = f"Hosts with role {role} and port {port}"
    elif role and not group and not port:
        hosts = get_hosts(nr)
        msg = f"Hosts with role: {role}"
    elif host and not role and not port and not group:
        nr = filter_single_host(nr, host)
        hosts = get_hosts(nr)
        msg = f"Host {host}"
        
    output(msg, hosts)


if __name__ == '__main__':
    main()