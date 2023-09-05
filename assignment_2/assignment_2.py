#!/usr/bin/env python
#### 1. Create a simple inventory that contains just a hosts.yaml file. 
'''
2. Create the following inventory in the hosts.yaml and the groups.yaml files:
    a. The hosts.yaml file should have two hosts.
    b. Each 'host' in the hosts.yaml file should have a hostname.
    c. Each 'host' in the hosts.yaml file should belong to the group 'ios'.
    d. The groups.yaml file should contain the group 'ios' and this group should have the 
        following attributes: platform, username, password, and port.
    e. Create a Python script that uses InitNornir to create a Nornir object using the newly created 
    hosts.yaml and groups.yaml files. Using a for-loop loop over the Nornir hosts in inventory and 
    print out the following attributes for each host: hostname, groups, platform, username, password, 
    and port. Do this directly from the Nornir host objects (i.e. rely on Nornir's ability to search 
    from the host object then to group object).

'''

import sys
sys.path.append('/home/taylor/VENV/py3_venv/lib/python3.9/site-packages')
from nornir import InitNornir


def init_nor():
    return InitNornir()

def main():
    nr = init_nor()
    for host_name, host_object in nr.inventory.hosts.items():
        print()
        print(f"Host: {host_name}")
        print("-"*20)
        print(f"hostname: {host_object.hostname}")
        print(f"groups: {host_object.groups}")
        print(f"platform: {host_object.platform}")
        print(f"username: {host_object.username}")
        print(f"password: {host_object.password}")
        print(f"port: {host_object.port}")
        print()
    
        




# Main

if __name__ == '__main__':
    main()