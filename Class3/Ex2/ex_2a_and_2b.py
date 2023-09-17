#!/usr/bin/env python3
'''Kirk Byers Nornir Class
8/16 BT

1a. Create a Python script that initializes a Nornir object. Print out the "data" attribute of the "arista3" host. 
Call the "items()" method on host "arista3". Notice that when calling the items() method that Nornir not only 
displays the "data" entries associated at the host-level, but also recurses the data for the groups (that the host belongs to).'''

from nornir import InitNornir
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
    return nr.filter(name=host)  # Use the .filter() method

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
        return nr.filter(role=role)  # Use the .filter() method
    else:
        return nr.filter(role=role).filter(port=port)

def get_hosts(nr):
    """Returns the hosts from the Nornir object.

    Args:
        nr (nornir object): nornir object

    Returns:
        list: list of hosts from the nornir object
    """
    return nr.inventory.hosts

def output(msg, hosts):
    print(f"\n{msg}\n{'-'*len(msg)}")
    for host in hosts:
        print(f"Host: {host}")
    print()

def main():
    '''Main Function'''
    logging.info(f"Entered function")
    nr = init_nornir()
    logging.info(f"set nr")
    # ipdb.set_trace()
    
    host = 'arista1'
    role = 'WAN'
    port = 22  # Set port to None not to use it.
    
    # 2a & 2b.
    nr = filter_role_and_port(nr, role, port)
    hosts = get_hosts(nr)
    # Output hosts
    if not port:
        msg = f"Hosts with role: {role}"
    else:
        msg = f"Hosts with role {role} and port {port}"
        
    output(msg, hosts)

    # ipdb.set_trace()
    
    # # 1a.1 Print out the "data" attribute of the "arista3" host.
    # data = get_data(nr, host)
    # print(data)
    
    # # 1a.2. Call the "items()" method on host "arista3". 
    
    # print(f"\nPrinting 'items' for host {host}.")
    # print("Notice that when calling the items() method that Nornir not only displays the 'data'")
    # print("entries associated at the host-level, but also recurses the data for the groups (that the host belongs to):\n")
    # print(get_items(nr, host))
    

if __name__ == '__main__':
    main()