#!/usr/bin/env python3
'''Create a Python script that creates a new Nornir object from inventory using the above config.yaml file. 
Nornir class
Exercise 4
8/17 BT
'''

import ipdb
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command
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

def main():
    '''Main Function'''
    nr = init_nornir()
    logging.debug(f"Got nr")
    # print(nr)
    
    # 4b. From your Nornir object in exercise4a, add a filter and select only the "eos" group.
    # 
    # Using the "netmiko_send_command" task-plugin, execute "show interface status" command 
    # against this "eos" group. Ensure that you receive structured data back from Netmiko.
    filter_ = 'eos'  # 4b select only the "eos" group.
    nr = apply_filter(nr, filter_)
    
    command = "show ip int brief"
    agg_result = netmiko_send(nr, command)
    
    # 4c. From the results in exercise4b, process the interface table for all of the devices 
    # and create a single final dictionary. The primary dictionary keys of this final dictionary 
    # should be the switch names. The switch name keys should point to an inner dictionary. 
    # The inner dictionary should have the interface names as keys and point to another 
    # internal dictionary. This last internal dictionary should have keys of "status" and "vlan". 
    
    # create a combined dictionary
    combined = {}
    # agg_result.items is all of the aggregated results from netmiko commands - one agg result per device.
    for device in agg_result.items():
        switch_name = device[0] # Getting the name of the switch to use as a key.
        inner_ints = device[1].result  # Getting the inner interfaces to use as a value of switch_name.
        # build the inner dictionary
        inner={}
        for int in inner_ints:
            interface = int['interface']
            if "Vlan" in interface or "vlan" in interface:  # check to see if the interface is a "vlan interface"
                vlan = interface[-1]  # extract the vlan number from the end of the interface (assuming its a single digit)
            status = int['status']
            last = {}  # This last internal dictionary should have keys of "status" and "vlan". 
            last['status'] = status
            last['vlan'] = vlan
            inner[interface] = last
        combined[switch_name] = inner  # The switch name keys should point to an inner dictionary.
    print()
    msg = "Printing device, Interface, Status, and VLAN ID"
    print(f"{msg}\n{'-'*(len(msg)+7)}")
    pprint(combined)
    print()

            

if __name__ == '__main__':
    main()