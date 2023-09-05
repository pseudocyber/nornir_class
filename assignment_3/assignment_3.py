#!/usr/bin/env python
#### 1. Create a simple inventory that contains just a hosts.yaml file. 
'''
3. Expand on your inventory from exercises to include a defaults.yaml file.
    a. Move both the username and password attributes from the groups.yaml file to the defaults.yaml file.
    b. Re-execute your exercise2e Python script against this new inventory. In other words, verify that your 
    Python for-loop on the Nornir Host Objects properly searches from host, to group, to defaults and prints 
    out the attributes specified in exercise 2e.


'''

import sys
sys.path.append('/home/taylor/VENV/py3_venv/lib/python3.9/site-packages')
from nornir import InitNornir


def init_nor():
    return InitNornir(config_file="config.yaml")

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