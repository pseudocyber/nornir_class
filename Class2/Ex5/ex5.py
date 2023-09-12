#!/usr/bin/env python3
'''
Brannen Taylor - 20230910
'''
from nornir import InitNornir
from nornir.core.filter import F
import pdbr
import os
from nornir_netmiko import netmiko_send_command  # used in ex. 2b.
from nornir_napalm.plugins.tasks.napalm_get import napalm_get

def pause():
    input("pausing")
    
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
    
    # print(f"type(my_result): {type(my_result)}\n")
    # print(f"my_result keys:\n{my_result.keys()}\n")
    # print(f"my_result items:\n{my_result.items()}\n")
    # print(f"my_result values:\n{my_result.values()}\n")
    
    # to get the actual output from the device, for cisco3:
    # print(f"output: {my_result['cisco3'][0].result}")
    # output: 'hostname cisco3\n path flash:cisco3-cfg'
    
    # 2c. Assign the results from "cisco3" to a new variable named "host_results". Inspect this new MultiResult 
    # object: access the zeroith element from this MultiResult object. Finally, determine if "host_results" is an iterable or not.
    host_results = my_result["cisco3"]
    # Inspecting var: {host_results} - #TODO Remove these two lines
    # print(f"VARIABLE is type ==> {type(host_results)} \n {host_results}")
    # print()
    
    # check if host_results is iterable
    # try:
    #     iter(host_results)
    #     print(f"{host_results=} len {len(host_results)}")
    #     print(f"host_results[0] = {host_results[0]}")
    #     print(f"Type of data stored in host_results[0] is: {type(host_results[0])}")
    #     print(f"{host_results=}\nIS iterable.")
    # except Exception as e:
    #     print(e)
    
    # 2d. Assign the zeroith element of the host_results object to a new variable named "task_result". 
    # What type of object is task_result? 
    # Print out the 'host', 'name', 'result', and 'failed' attributes from task_result. 
    # Which field actually contains the output from the network device?
    # print(f"\nEx. 2d\n")
    task_result = host_results[0]
    # print(f"type: {type(task_result)}")
    # print(f"host: {task_result.host}")
    # print(f"name: {task_result.name}")
    # print(f"result: {task_result.result}")
    # print(f"failed: {task_result.failed}")
    # print()
    print(f"The field that actually contains the output from the network device is:\ntaks_result.result, which is:{task_result.result}\n")
    
    # 2e. Looking back at exercises 2a - 2d: explain what Nornir result types are "my_results", "host_results", 
    # and "task_result"? What purpose does each of those three data types serve (i.e. why do we have them)?
    # print("'my_result' returns a dict like object with multiple results")
    # print("'host_results' is a list like object from one single host.  It is iterable, but may only have one item in the list.")
    # print("'task_result' is the result of the single task, on the single host.")

    # pdbr.set_trace()
    
def show_arp(nr):
    """3. Using the Nornir filter pattern shown below and the 'netmiko_send_command' task-plugin capture
    the output of 'show ip arp' from all of the Cisco-IOS and Arista-EOS devices.
    
    ios_filt = F(groups__contains="ios")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(ios_filt | eos_filt)

    NOTE: We will cover filtering inventory later in the course, but for now, add the following 
    to your script after initializing your Nornir object. This will filter the Nornir hosts to be only the IOS and EOS devices: 

    """
    print(f"\nEntered func 'show_arp\n")
    
    # set up filters
    ios_filt = F(groups__contains="ios")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(ios_filt | eos_filt)
    
    # send command to netmiko
    command = "show ip arp"
    nm_result = nr.run(task=netmiko_send_command, command_string=command)  # netmiko result
    
    # Process the "show ip arp" results such that only the default gateway is retained from the ARP table. 
    # Note, please accomplish this exercise by handling the AggregatedResult and MultiResult in your 
    # Python program instead of using a router CLI command (i.e. do not do "show ip arp | include gateway"). 
    # In other words, the purpose of this exercise is for you to gain familiarity with handling Nornir result objects.
    
    # Use pdpr.set_trace() to explore the variables, methods, and attributes.
    # using pdpr, found some of the information needed:
    # arp = list(nm_result['cisco3'].result.split('\n'))
    # (Pdbr) devices = [device for device in nm_result]
    # (Pdbr) devices
    # ['cisco3', 'cisco4', 'arista1', 'arista2', 'arista3', 'arista4']
    # (Pdbr) 
    
    output = []
    """
    (Pdbr) nm_result
    AggregatedResult (netmiko_send_command): {'cisco3': MultiResult: [Result: "netmiko_send_command"], 'cisco4': MultiResult: [Result: "netmiko_send_command"], 'arista1': MultiResult: [Result: "netmiko_send_command"], 'arista2': MultiResult: [Result: 
    "netmiko_send_command"], 'arista3': MultiResult: [Result: "netmiko_send_command"], 'arista4': MultiResult: [Result: "netmiko_send_command"]}
    (Pdbr) len(nm_result)
    6
    (Pdbr) nm_result.keys()
    dict_keys(['cisco3', 'cisco4', 'arista1', 'arista2', 'arista3', 'arista4'])
    """
    # nm_result will be a dict like object, where each key is one of the devices
    for device in nm_result:
        # result[device].result will hold the arp table as a single string.
        arp_table = list(nm_result[device].result.split('\n'))
        # for each line of the arp table analyze it for the default gateway IP, and if found, add the host and gateway line to a list.
        for line in arp_table:
            if '10.220.88.1' in line:
                output.append(f"Host: {device}, Gateway: {line}")
    
    for line in output:
        print(line)
        
    """Outputs:
    
    Entered func 'show_arp

    Host: cisco3, Gateway: Internet  10.220.88.1            25   0024.c4e9.48ae  ARPA   GigabitEthernet0/0/0
    Host: cisco4, Gateway: Internet  10.220.88.1            25   0024.c4e9.48ae  ARPA   GigabitEthernet0/0/0
    Host: arista1, Gateway: 10.220.88.1       0:00:00  0024.c4e9.48ae  Vlan1, Ethernet1
    Host: arista2, Gateway: 10.220.88.1       0:00:00  0024.c4e9.48ae  Vlan1, Ethernet1
    Host: arista3, Gateway: 10.220.88.1       0:00:00  0024.c4e9.48ae  Vlan1, Ethernet1
    Host: arista4, Gateway: 10.220.88.1       0:00:00  0024.c4e9.48ae  Vlan1, Ethernet1
    """
    # set up filters
    ios_filt = F(groups__contains="ios")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(ios_filt | eos_filt)
        


def get_napalm_arp(nr):
    """
    4. Using a NAPALM getter instead of Netmiko, capture the ARP table output from all of the EOS and IOS devices. 
    The NAPALM "arp_table" getter will return a list of dictionaries. In this list of dictionaries each inner-dictionary 
    will correspond to one entry in the ARP table.

    Post-process the data retrieved from this NAPALM getter and print out the "host" name 
    (for example, "cisco3", "cisco4") and the NAPALM inner dictionary corresponding to the 
    MAC address of the default gateway. For both exercise3 and exercise4, you can just hard-code the 
    gateway value into your code. In other words, you do not need to dynamically determine the default gateway.

    Your printed output should be similar to the following (note, the default gateway and MAC address in your lab environment might be different). 

    Host: cisco3, Gateway: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 5.0}
    Host: cisco4, Gateway: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 5.0}
    Host: arista1, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}
    Host: arista2, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}
    Host: arista3, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}
    Host: arista4, Gateway: {'interface': 'Vlan1, Ethernet1', 'mac': '00:62:EC:29:70:FE', 'ip': '10.220.88.1', 'age': 0.0}

    """
    # set up filters
    ios_filt = F(groups__contains="ios")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(ios_filt | eos_filt)
        

    results = nr.run(
        task=napalm_get,
        getters=["get_arp_table"]
    )
   
    """
    (Pdbr) results.keys()
    dict_keys(['cisco3', 'cisco4', 'arista1', 'arista2', 'arista3', 'arista4'])

    (results['cisco3']) returns a list like object.
    
    (Pdbr) results['cisco3'].result - is a dictionary, where the key is the command, and then the value is a list of dictionaries, like below.
{
    'get_arp_table': [
        {'interface': 'GigabitEthernet0/0/0', 'mac': '00:24:C4:E9:48:AE', 'ip': '10.220.88.1', 'age': 0.0},
        {'interface': 'GigabitEthernet0/0/0', 'mac': 'C8:9C:1D:EA:0E:B6', 'ip': '10.220.88.20', 'age': 183.0},
        {'interface': 'GigabitEthernet0/0/0', 'mac': '1C:6A:7A:AF:57:6C', 'ip': '10.220.88.21', 'age': 21.0},
    """
    
    devices = list(results.keys())
    output = []
    for device in devices:
        device_dict = results[device].result
        arp_table = device_dict['get_arp_table']
        for line in arp_table:
            if line['ip'] == '10.220.88.1':
                output_line = f'Host: {device}: {line}'
                output.append(output_line)
    for line in output:
        print(line)
        
    """
    Output:
    
    Host: cisco3: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:24:C4:E9:48:AE', 'ip': '10.220.88.1', 'age': 31.0}
    Host: cisco4: {'interface': 'GigabitEthernet0/0/0', 'mac': '00:24:C4:E9:48:AE', 'ip': '10.220.88.1', 'age': 31.0}
    Host: arista1: {'interface': 'Vlan1, Ethernet1', 'mac': '00:24:C4:E9:48:AE', 'ip': '10.220.88.1', 'age': 0.0}
    Host: arista2: {'interface': 'Vlan1, Ethernet1', 'mac': '00:24:C4:E9:48:AE', 'ip': '10.220.88.1', 'age': 0.0}
    Host: arista3: {'interface': 'Vlan1, Ethernet1', 'mac': '00:24:C4:E9:48:AE', 'ip': '10.220.88.1', 'age': 0.0}
    Host: arista4: {'interface': 'Vlan1, Ethernet1', 'mac': '00:24:C4:E9:48:AE', 'ip': '10.220.88.1', 'age': 0.0}
    """
        
    
    # pdbr.set_trace()

def print_out(data:list):
    """Print function - looks to see if incoming data is in a list, and each item in the list is a dictionary

    Args:
        data (list): a list of dictionaries
    """
    if isinstance(data, list):
        for line in data:
            if isinstance(line, dict):
                for key in line.keys():
                    print(f"Host: {key}")
                    print(line[key])
                    print()
            else:
                print(f"Not a dict, printing whatever: {type(data)}")
        
    else:
        print(f"data is not a list.  it's: {type(data)}")
    
        
def get_ip_brief(nr):
    """This function filters the host file for cisco and arista routers.
    Then it will use netmiko to issue "show ip int brief" on each router.

    Args:
        nr (nornir object): a nornir object.
    """
    print("Entered get_ip_brief")
    
    # set up filters
    ios_filt = F(groups__contains="ios")
    eos_filt = F(groups__contains="eos")
    nr = nr.filter(ios_filt | eos_filt)
    
    # send command to netmiko
    command = "show ip int brief"
    try:
        nm_result = nr.run(task=netmiko_send_command, command_string=command)  # netmiko result
        print("Ran the netmiko_send_command")
        
        # 5b
        # print(nm_result.keys()) # this is an aggresult object, dict like obj.
        for key in nm_result.keys():
            if nm_result[key].failed:  # this is looking at a multi-result object, failed attrib. List like
                # look at the list of the nm_result[key] to see the list of items in it.  The items
                # will have attribs.
                print("results object (results.failed_hosts):")
                print(f"The netmiko command failed on: {nm_result[key].host}")  # result object attrib
        
        # if the nornir object has some failed hosts, output the failed hosts.
        if nr.data.failed_hosts:
            print(f"Nornir object (nr.data.failed_hosts): {nr.data.failed_hosts}")

       


        
    except Exception as e:
        print(e)
        input('Error, pausing.')
        
        
    # Exercise 5a
    # 5a. Create a Nornir script that uses the netmiko_send_command task-plugin to execute "show ip int brief" 
    # on each of the devices in the "ios" group. Use the inventory filtering pattern that we used in earlier 
    # exercises. Print the output from this task using the print_results function.
    
    ip_int_brief = []
    for device in nm_result.keys():
        ip_ints = (nm_result[device].result)
        temp_dict = {device:ip_ints}
        ip_int_brief.append(temp_dict)
    
    print_out(ip_int_brief)
    
    """
    Output:
    
    cisco3
    Interface              IP-Address      OK? Method Status                Protocol
    GigabitEthernet0/0/0   10.220.88.22    YES NVRAM  up                    up      
    GigabitEthernet0/0/1   unassigned      YES unset  administratively down down    
    GigabitEthernet0/1/0   unassigned      YES unset  down                  down    
    GigabitEthernet0/1/1   unassigned      YES unset  down                  down    
    GigabitEthernet0/1/2   unassigned      YES unset  down                  down    
    GigabitEthernet0/1/3   unassigned      YES unset  down                  down    
    Vlan1                  unassigned      YES manual up                    down    

    cisco4
    Interface              IP-Address      OK? Method Status                Protocol
    GigabitEthernet0/0/0   10.220.88.23    YES NVRAM  up                    up      
    GigabitEthernet0/0/1   unassigned      YES unset  administratively down down    
    GigabitEthernet0/1/0   unassigned      YES unset  down                  down    
    GigabitEthernet0/1/1   unassigned      YES unset  down                  down    
    GigabitEthernet0/1/2   unassigned      YES unset  down                  down    
    GigabitEthernet0/1/3   unassigned      YES unset  down                  down    
    Vlan1                  unassigned      YES unset  up                    down    

    arista1
                                                                                    Address
    Interface         IP Address            Status           Protocol           MTU    Owner  
    ----------------- --------------------- ---------------- -------------- ---------- -------
    Management1       unassigned            admin down       down              1500           
    Vlan1             10.220.88.28/24       up               up                1500           


    arista2
                                                                                    Address
    Interface         IP Address            Status           Protocol           MTU    Owner  
    ----------------- --------------------- ---------------- -------------- ---------- -------
    Management1       unassigned            admin down       down              1500           
    Vlan1             10.220.88.29/24       up               up                1500           


    arista3
                                                                                    Address
    Interface         IP Address            Status           Protocol           MTU    Owner  
    ----------------- --------------------- ---------------- -------------- ---------- -------
    Management1       unassigned            admin down       down              1500           
    Vlan1             10.220.88.30/24       up               up                1500           


    arista4
                                                                                    Address
    Interface         IP Address            Status           Protocol           MTU    Owner  
    ----------------- --------------------- ---------------- -------------- ---------- -------
    Management1       unassigned            admin down       down              1500           
    Vlan1             10.220.88.31/24       up               up                1500           


    """
def change_password(nr, password=str):
    """5b. Expanding on exercise 5a, set the 'cisco3' password attribute to an invalid value. The code to do this would be similar to the following: 
    nr.inventory.hosts["cisco3"].password = 'bogus'
    
    username pyclass privilege 15 secret bogus
    
    Re-run your Nornir task and print out the "failed_hosts" using both the results object (results.failed_hosts) and the Nornir object (nr.data.failed_hosts)
    Args:
        nr (nornir object): nornir object
        password (str, optional): the password you want to use. Defaults to str.
    """
    print("Changing password")
    # command = f"username pyclass privilege 15 secret {password}"
    try:
        nr.inventory.hosts["cisco3"].password = password
        print("Password changed.")
    except Exception as e:
        print(e)
    

def main():
    '''Main Function'''
    nr = init_nornir()
    # check_workers(nr) # 1a
    # filt = filter_inventory(nr, "ios") # 2a
    # show_hostname(nr, filt) # 2b
    # show_arp(nr)  # 3
    # get_napalm_arp(nr) # 4
    # get_ip_brief(nr) # 5a
    
    change_password(nr, "bogus") # 5b.
    
    get_ip_brief(nr) #5b part 2.
    
    


if __name__ == '__main__':
    main()