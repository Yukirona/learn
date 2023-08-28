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
result = subprocess.run(["ansible-playbook", "-i", "hosts", playbook_path], capture_output=True, text=True)

# Get the output
output = result.stdout

# Display the output
print(output)