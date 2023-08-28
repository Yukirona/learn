import requests
import json
from main import *


subnets_list()
vpcs_list()


# Load JSON data from file
with open('subnet_list.json') as file:
    data = json.load(file)


# Extract subnet IDs and VPC IDs
subnet_ids = [subnet['id'] for subnet in data['subnets']]
vpc_ids = [subnet['vpc_id'] for subnet in data['subnets']]


for subnet_id, vpc_id in zip(subnet_ids, vpc_ids):
    delete_subnet(vpc_id, subnet_id)
    
# Read the JSON file
with open('vpc_list.json') as f:
    data = json.load(f)

# Extract VPC IDs
vpc_ids = [vpc['id'] for vpc in data['vpcs']]

# Delete each VPC
for vpc_id in vpc_ids:
    # Call the delete_vpc function with appropriate project ID and VPC ID
    delete_vpc(vpc_id)
