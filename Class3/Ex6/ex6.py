#!/usr/bin/env python3
'''6. NAPALM Getters Expanded

6a. Using the config.yaml file from exercise 4, create a new Nornir object that filters to only the "nxos" 
devices. Using the "napalm_get" task-plugin, retrieve the configuration from these devices. Print the results of this task.

6b. Filter the napalm "get" to capture only the running configuration. Print the results of the task.

6c. Modify the script to get the running configuration AND facts from the device. Once again, print the results.

6d. Finally, modify the code to capture all configurations (continue to use the "getters_options"), and the 
facts. For each device, parse the data and indicate whether the startup and running configs match and print 
out this information along with some of the basic device information. Your output should be similar to the following: 

{'nxos1': {'model': 'Nexus9000 9000v Chassis',
           'start_running_match': True,
           'uptime': 7172937,
           'vendor': 'Cisco'},
 'nxos2': {'model': 'Nexus9000 9000v Chassis',
           'start_running_match': True,
           'uptime': 7172474,
           'vendor': 'Cisco'}}

*Note* startup and running config contain timestamps--remove those timestamps before comparing the configurations!


Official answer to problem:  https://github.com/twin-bridges/nornir_course/tree/master/class3/exercises/exercise6

Nornir class
Exercise 6
8/19 BT
'''

import ipdb
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

import logging
from pprint import pprint

log_format = "%(asctime)s-%(levelname)s-%(name)s-"\
             "%(filename)s-%(funcName)20s-%(lineno)d-%(message)s"
logging.basicConfig(filename='mylogs.log', filemode='w', level='DEBUG', format=log_format)

def init_nornir():
    data = InitNornir(config_file="config.yaml")
    logging.info(f"Returning: {data}")
    return data

def apply_filter(nr, filter_:str):
    data = nr.filter(F(groups__contains=filter_))  # 4b select only the "eos" group.
    logging.info(f"Returning: {data}")
    return data

def netmiko_send(nr, command: str, use_textfsm:bool = True):
    
    data = nr.run(task=netmiko_send_command, command_string=command, use_textfsm=True)
    logging.info(f"Returning: {data}")
    return data

def func_napalm_get(nr, getters:list):
    
    data = nr.run(task=napalm_get, getters=getters)
    logging.info(f"Returning: {data}")
    return data

def main():
    '''Main Function'''
    nr = init_nornir()
    logging.debug(f"Got nr")
    # print(nr)
    
    # 4b. From your Nornir object in exercise4a, add a filter and select only the "eos" group.
    # 
    # Using the "netmiko_send_command" task-plugin, execute "show interface status" command 
    # against this "eos" group. Ensure that you receive structured data back from Netmiko.
    filter_ = 'nxos'  # 4b select only the "nxos" group.
    nr = apply_filter(nr, filter_)
    # ipdb.set_trace()
    # print(nr.inventory.hosts.items())
    
    # command = "show interface status"
    command = "show run"
    getters = ["config"]
    agg_result = func_napalm_get(nr, getters)
    
    print_result(agg_result)
    

if __name__ == '__main__':
    main()