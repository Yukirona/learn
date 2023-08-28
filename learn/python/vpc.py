import requests
import json
from Orange_auth import O_token

# Set the authentication token
auth_token = O_token()


# Set the headers for the API request
headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": auth_token
}


def vpc_list():
    # Set the API endpoint variables
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"
    project_id = "894ac8446e99430c994f7f392c5c8b32"

    # Construct the complete API endpoint URL
    api_endpoint = f"{endpoint}/v1/{project_id}/vpcs"

    # Make the API request to get the list of VPCs
    response = requests.get(api_endpoint, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print(response)
        with open("vpc_list.json", "w") as json_file:
            json_file.write(response.text)
            print("vpc list written successfully.")
    else:
        print("Error occurred while retrieving the list of VPCs.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
    pass

def subnet_list():
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"
    project_id = "894ac8446e99430c994f7f392c5c8b32"
    # Construct the complete API endpoint URL
    api_endpoint = f"{endpoint}/v1/{project_id}/subnets"

    # Make the API request to get the list of VPCs
    response = requests.get(api_endpoint, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print(response)
        with open("subnet_list.json", "w") as json:
            json.write(response.text)
            print("subnet list written successfully.")
    else:
        print("Error occurred while retrieving the list of VPCs.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)


    pass

def delete_subnet(project_id, vpc_id, subnet_id):

    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"
    resource_path = f"/v1/{project_id}/vpcs/{vpc_id}/subnets/{subnet_id}"
    api_endpoint = endpoint + resource_path

     # Make the DELETE request to delete the subnet
    response = requests.delete(api_endpoint, headers=headers)

    # Check the response status
    if response.status_code == 204:
        print("Subnet deleted successfully.")
    else:
        print("Error occurred while deleting the subnet.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def delete_vpc(project_id, vpc_id):
    
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"
    resource_path = f"/v1/{project_id}/vpcs/{vpc_id}"
    api_endpoint = endpoint + resource_path

     # Make the DELETE request to delete the subnet
    response = requests.delete(api_endpoint, headers=headers)

    # Check the response status
    if response.status_code == 204:
        print("vpc deleted successfully.")
    else:
        print("Error occurred while deleting the subnet.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass


