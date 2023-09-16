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

def get_timezones(nr):
    """Returns list of timezones that all the hosts have.

    Args:
        nr (Nornir object): Nornir object

    Returns:
        timezones:list: A list of timezones all the hosts are in.
    """
    # Print out the timezone for each of the hosts in the inventory
    timezones = []
    # For each host, get the items for it.
    for host in nr.inventory.hosts:
        # convert the items dict_keys object to a dictionary
        data = dict(nr.inventory.hosts[host].items())
        timezones.append(data.get('timezone', 'Not set'))

    logging.info(f"Returning: {timezones=}")
    return timezones

def main():
    '''Main Function'''
    logging.info(f"Entered function")
    nr = init_nornir()
    logging.info(f"set nr")
    # ipdb.set_trace()
    
    # 1a.1 Print out the "data" attribute of the "arista3" host.
    # data = get_data(nr, 'arista3')
    # print(data)
    
    # # 1a.2. Call the "items()" method on host "arista3". 
    
    # print("\nPrinting 'items' for host 'arista3'.")
    # print("Notice that when calling the items() method that Nornir not only displays the 'data'")
    # print("entries associated at the host-level, but also recurses the data for the groups (that the host belongs to):\n")
    # print(get_items(nr, 'arista3'))
    
    # 1b. 1 In the "sea" group in groups.yaml, add a "timezone" key and set the value to "PST". 
    # Print out the timezone for each of the hosts in the inventory. 
    print(get_timezones(nr))

if __name__ == '__main__':
    main()