#!/usr/bin/env python3
'''Exercise1

1a. Create a simple 'hosts.yaml' file that contains a single entry for localhost. 
Your hosts.yaml file should look similar to the following: 

---
localhost:
  hostname: localhost

Now create a Python script that uses InitNornir to initialize a Nornir object. 
Using this Nornir object print out the number of workers currently configured. 
This value should be 20 at this point.

1b. Create a Nornir config.yaml file that sets the number of workers to 5. 
Modify the Python script from exercise 1a to load this config.yaml file. 
Print out and verify the new number of workers.

1c. Use:

export NORNIR_RUNNER_OPTIONS='{"num_workers": 100}' 
in the bash shell to modify the number of workers using an environment variable. 
Keep your Python script exactly the same as exercise1a (in other words, you should 
NOT have any 'runner' section in your config.yaml). Re-run your script to validate 
the environment variable setting is now being used.

1d. Finally, modify the python script to set the number of workers to 15 using 
inline Python. Your inline Python should be similar to the following: 

    nr = InitNornir(
        config_file="config.yaml",
        runner={"plugin": "threaded", "options": {"num_workers": 15}},
    )
Re-run the script and confirm the number of workers is now 15.

From the above exercises, you should observe that the configuration order of 
preference was: inline python > config.yaml file > environment variable.

Brannen Taylor - 20230910
'''
from nornir import InitNornir
import pdbr

def init_nornir():
    # 1b. Create a Nornir config.yaml file that sets the number of workers to 5. 
    # Modify the Python script from exercise 1a to load this config.yaml file. Print out and verify the new number of workers.
    
    # nr = InitNornir(config_file="config.yaml")  # Uses a config.yaml.  Commenting to use .env var's instead. 
    # 1c. Use: - export NORNIR_RUNNER_OPTIONS='{"num_workers": 100}' 
    # in the bash shell to modify the number of workers using an environment variable. 
    # Keep your Python script exactly the same as exercise1a (in other words, you should NOT 
    # have any 'runner' section in your config.yaml). Re-run your script to validate the 
    # environment variable setting is now being used.
    # output correct: nr workers = 100
    
    # 1d. Finally, modify the python script to set the number of workers to 15 using inline Python. 
    # output correct - nr workers = 15 - the inline py over wrode the yaml.
    
    # From the above exercises, you should observe that the configuration order of preference was: 
    # inline python > config.yaml file > environment variable.
    # nr = InitNornir(
    #     config_file="config.yaml",
    #     runner={"plugin": "threaded", "options": {"num_workers": 15}}
    # )
    
    # returning init to use the config.yaml file as the preferred method.
    nr = InitNornir(config_file="config.yaml")
    return nr

def main():
    '''Main Function'''
    # 1.a Now create a Python script that uses InitNornir to initialize a Nornir object. 
    # Using this Nornir object print out the number of workers currently configured. This value should be 20 at this point.
    workers = init_nornir().runner.num_workers  # nr.runner.num_workers
    print(f"nr workers = {workers}") 
    # pdbr.set_trace()


if __name__ == '__main__':
    main()