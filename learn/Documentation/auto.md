#### python script to do it all ?

here i will provide a python script which allows the use of commands for terraform ansible.

!!!warning 
    this is not some plug and play option you will be needing to have the install of the prerequisites for each part thus i gladly recommend to follow the doc for terraform and ansible.
     
    The goal is to centralize the way to manage our installation because it is tiresome to alternate between commands and maybe later to make it grow to take more tasks into account

Right now the script is doing several steps 

!!!summary
    - Using terraform to deploy the server
    - Retreiving the external ip associated with it
    - Creating/Updating the file hosts used by ansible
    - Using ansible to follow with the installation of remotelabz

#### Pre requisites

!!!warning
    It is recommended you already followed the doc for terraform and ansible as they are needed for this script to function

We will also need to download a library
```bash
sudo apt install python3-pip

pip install python_terraform
```
we will have this architecture
├── ansible
│   ├── hosts
│   ├── hosts.bak
│   ├── playbook.yml
│   └── ssh-key.pem
├── python
│   ├── in_remote.py
└── terraform
    ├── main.tf
    ├── provider.tf
    ├── terraform.tfstate
    └── terraform.tfstate.backup

#### The script

Here i will put the script with comments to explain the actions realized 

!!!note
    ```python
    import os
    import re
    from python_terraform import *
    import subprocess
    import fileinput


    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    # Get the parent directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    print(parent_dir)

    # Set the Terraform directory
    terraform_dir = os.path.abspath(os.path.join(parent_dir, "terraform"))
    print(terraform_dir)
    # Initialize Terraform
    terraform = Terraform(working_dir=terraform_dir)

    # Run 'terraform init'
    return_code, stdout, stderr = terraform.init(capture_output=True)
    print(return_code, stdout, stderr)

    # Run 'terraform apply'
    return_code, stdout, stderr = terraform.apply("-auto-approve", capture_output=True)

    print(return_code, stdout, stderr)

    # Extract the EIP value from the output using regular expressions
    eip_pattern = r'eip = "(.+)"'
    eip_match = re.search(eip_pattern, stdout)
    if eip_match:
        eip_value = eip_match.group(1)
        print("EIP value:", eip_value)
    else:
        print("EIP value not found in the output")

    # Extract the IP address from the output using regular expressions
    ip_pattern = r'flexibleengine_compute_floatingip_associate_v2.myip: Creation complete after \d+s \[id=([\d.]+)/'
    ip_match = re.search(ip_pattern, stdout)
    if ip_match:
        eip_value = ip_match.group(1)
        print("IP address:", eip_value)
    else:
        print("IP address not found in the output")
    # Specify the filename of the hosts file
    hosts_filename = "hosts"

    ansible_dir = os.path.join(parent_dir, "ansible")
    hosts_file_path = os.path.join(ansible_dir, hosts_filename)
    print(hosts_file_path)
    # Open the hosts file in read mode
    with fileinput.FileInput(hosts_file_path, inplace=True, backup='.bak') as file:
        # Iterate over each line in the file
        for line in file:
            # Check if the line contains the ansible_host setting
            if line.startswith("ansible_host="):
                # Replace the IP address with the new value
                line = f"ansible_host={eip_value}\n"
            # Print the modified line (which may be the same as the original line)
            print(line, end='')

    # Define the playbook file path
    playbook_path = os.path.join(ansible_dir, "playbook.yml")

    # Execute the playbook using Ansible and capture the output
    result = subprocess.run(["ansible-playbook", playbook_path], capture_output=True, text=True)

    # Get the output
    output = result.stdout

    # Display the output
    print(output)

The comments in the code should be sufficient to understand the code.

As a breif explanation we call terraform using a library and tell it to init and then apply the default main.tf we already configured,
We are capturing the integrality of the outputs of the commands, reading these outputs we extract the ip associated to our server using regex.
The ip is read differently if is it is the first installation or if you run the script with a terraform state already there.

Then the program write the ip to the ansible file containing the ip of the servers and finally it is calling ansible that should proceed with the application of the playbook you provided

the majority of the " work " is happening in terraform and ansible files as the script only call these process to tell them to do their tasks instead of us by hand

!!!warning
    currently the playbook for ansible is not fully functional

    As already stated this script is tailored to work with installing remotelabz for flexible engine
    some minor modifications would be needed to use this script with multiples ip or servers or multiples playbooks.

!!!info
    if you named some folders or files differently  you need to update it in the code for instance :
    ````
    # Specify the filename of the hosts file
    hosts_filename = "hosts"
    ````
    change hosts if you renamed the file with the servers for ansible
    ````
    # Define the playbook file path
    playbook_path = os.path.join(ansible_dir, "playbook.yml")
    ````
    change playbook.yml if you renamed the file for ansible

You have now a python script you can use and modify to automatize the use of Terraform + ansible for flexible engine.