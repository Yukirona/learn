# coding=utf-8
import sys
import requests
from apig_sdk import signer
from Orange_auth import *
sig = signer.Signer()
# Set the AK/SK to sign and authenticate the request. ( asked at the launch when commented)
#sig.Key = "Z8PHOLQAJNSRNZKOHLCS"
#sig.Secret = "W9V5erMtOcNyCPc2KJHhhqGfCnz9jRfMMEuu8wid"

def vpcs_list(project_id):
    

    # The following example shows how to set the request URL and parameters to query a VPC list.

    # Set the API endpoint variables
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"

    # Construct the complete API endpoint URL
    api_endpoint = f"{endpoint}/v1/{project_id}/vpcs"
    # Set request Endpoint.
    # Specify a request method, such as GET, PUT, POST, DELETE, HEAD, and PATCH.
    # Set request URI.
    # Set parameters for the request URL.
    r = signer.HttpRequest("GET", api_endpoint)
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    r.headers = {"content-type": "application/json"}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    r.body = ""
    sig.Sign(r)
    print(r.headers["X-Sdk-Date"])
    print(r.headers["Authorization"])
    response = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
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

def subnets_list(project_id):
   

    # The following example shows how to set the request URL and parameters to query a subnet list.

    # Set the API endpoint variables
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"

    # Construct the complete API endpoint URL
    api_endpoint = f"{endpoint}/v1/{project_id}/subnets"
    # Set request Endpoint.
    # Specify a request method, such as GET, PUT, POST, DELETE, HEAD, and PATCH.
    # Set request URI.
    # Set parameters for the request URL.
    r = signer.HttpRequest("GET", api_endpoint)
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    r.headers = {"content-type": "application/json"}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    r.body = ""
    sig.Sign(r)
    print(r.headers["X-Sdk-Date"])
    print(r.headers["Authorization"])
    response = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)

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
   
    if not vpc_id:
        vpc_id = input("Enter the VPC ID: ")
    if not subnet_id:
        subnet_id = input("Enter the subnet ID: ")
    # The following example shows how to set the request URL and parameters to query a VPC list.

    # Set the API endpoint variables
    project_id = "894ac8446e99430c994f7f392c5c8b32"
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"
    resource_path = f"/v1/{project_id}/vpcs/{vpc_id}/subnets/{subnet_id}"
    api_endpoint = endpoint + resource_path

    # Set request Endpoint.
    # Specify a request method, such as GET, PUT, POST, DELETE, HEAD, and PATCH.
    # Set request URI.
    # Set parameters for the request URL.
    r = signer.HttpRequest("DELETE", api_endpoint)
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    r.headers = {"content-type": "application/json"}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    r.body = ""
    sig.Sign(r)
    print(r.headers["X-Sdk-Date"])
    print(r.headers["Authorization"])
    response = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
    
    # Check the response status
    if response.status_code == 204:
        print("Subnet deleted successfully.")
    else:
        print("Error occurred while deleting the subnet.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def delete_vpc(project_id, vpc_id):
    if not vpc_id:
        vpc_id = input("Enter the VPC ID: ")
    

    # The following example shows how to set the request URL and parameters to query a VPC list.

    # Set the API endpoint variables
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"
    resource_path = f"/v1/{project_id}/vpcs/{vpc_id}"
    api_endpoint = endpoint + resource_path


    # Set request Endpoint.
    # Specify a request method, such as GET, PUT, POST, DELETE, HEAD, and PATCH.
    # Set request URI.
    # Set parameters for the request URL.
    r = signer.HttpRequest("DELETE", api_endpoint)
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    r.headers = {"content-type": "application/json"}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    r.body = ""
    sig.Sign(r)
    print(r.headers["X-Sdk-Date"])
    print(r.headers["Authorization"])
    response = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)

    # Check the response status
    if response.status_code == 204:
        print("vpc deleted successfully.")
    else:
        print("Error occurred while deleting the subnet.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def list_users():
    
    # obtain the token
    auth_token = O_token_domain()

    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3/users"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.get(api_endpoint, headers=headers)
    # Check the response status
    if response.status_code == 200:
        print(response)
        with open("user_list.json", "w") as json_file:
            json_file.write(response.text)
            print("user list written successfully.")
    else:
        print("Error occurred while retrieving the list of users.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def user_detail(user_id):
    
    if not user_id:
        user_id = input("Enter the VPC ID: ")
    # obtain the token
    auth_token = O_token_domain()

    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3/users/"f"{user_id}"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.get(api_endpoint, headers=headers)
    # Check the response status
    if response.status_code == 200:
        print(response)
        with open("user_"f"{user_id}.json", "w") as json_file:
            json_file.write(response.text)
            print("user details written successfully.")
    else:
        print("Error occurred while retrieving the details of the user.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def add_user():
    
    # obtain the token
    auth_token = O_token_domain()
    
    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3/users"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    payload ={
    "user": {
        "default_project_id": "894ac8446e99430c994f7f392c5c8b32",
        "domain_id": "a0fe10e2d45a42178afdff17e784041b",
        "enabled": True,
        "name": "testuser2",
        "password": "Ceciestunmdp_1!"
            }
        } 
        
    
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.post(api_endpoint, headers=headers, json=payload)
    # Check the response status
    if response.status_code == 201:
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
    else:
        print("Error occurred while creating the user")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def del_user(user_id):
    if not user_id:
        user_id = input("Enter the VPC ID: ")
    

  # obtain the token
    auth_token = O_token_domain()
    endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com"
    resource_path = f"/v3/users/{user_id}"
    api_endpoint = endpoint + resource_path
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }

    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.delete(api_endpoint, headers=headers)
    # Check the response status
    if response.status_code == 204:
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
    else:
        print("Error occurred while deleting the user")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def add_IAM_user(domain_id):
    
    # obtain the token
    auth_token = O_token_domain()
    
    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3.0/OS-USER/users"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    payload ={
    "user": {
        "domain_id": domain_id,
        "name": "Utilisateurdetest",
        "password": "IAMPassword@",
        "email": "IAMEmail@example.com",
        "enabled": True,
        "pwd_status": False,
        "xuser_type": "",
        "xuser_id": "",
        "description": "TESTdescription"
    }
}
        
    
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.post(api_endpoint, headers=headers, json=payload)
    # Check the response status
    if response.status_code == 201:
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
    else:
        print("Error occurred while creating the user")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def list_groups(domain_id):
    
    # obtain the token
    auth_token = O_token_domain()

    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3/groups?"f"{domain_id}"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.get(api_endpoint, headers=headers)
    # Check the response status
    if response.status_code == 200:
        print(response)
        with open("group_list.json", "w") as json_file:
            json_file.write(response.text)
            print("user list written successfully.")
    else:
        print("Error occurred while retrieving the list of users.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def group_details(group_id):
    
    if not group_id:
        group_id = input("Enter the VPC ID: ")
  
    auth_token = O_token_domain()

    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3//v3/groups"f"{group_id}"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.get(api_endpoint, headers=headers)
    # Check the response status
    if response.status_code == 200:
        print(response)
        with open("user_list.json", "w") as json_file:
            json_file.write(response.text)
            print("user list written successfully.")
    else:
        print("Error occurred while retrieving the list of users.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def create_group():
    
    # obtain the token
    auth_token = O_token_domain()

    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3//v3/groups"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    payload = {}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.post(api_endpoint, headers=headers, json=payload)
    # Check the response status
    if response.status_code == 200:
        print(response)
        with open("user_list.json", "w") as json_file:
            json_file.write(response.text)
            print("user list written successfully.")
    else:
        print("Error occurred while retrieving the list of users.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def user_belong(group_id,user_id):
    if not group_id:
        group_id = input("Enter the VPC ID: ")
    if not user_id:
        user_id = input("Enter the subnet ID: ")
    # obtain the token
    auth_token = O_token_domain()

    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3//v3/groups/"f"{group_id}/users/{user_id}"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    payload = {}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.head(api_endpoint, headers=headers, json=payload)
    # Check the response status
    if response.status_code == 200:
        print(response)
        with open("user_list.json", "w") as json_file:
            json_file.write(response.text)
            print("user list written successfully.")
    else:
        print("Error occurred while retrieving the list of users.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def delete_group(group_id):
    
    if not group_id:
        group_id = input("Enter the subnet ID: ")
    # obtain the token
    auth_token = O_token_domain()

    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3//v3/groups/"f"{group_id}"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.delete(api_endpoint, headers=headers)
    # Check the response status
    if response.status_code == 200:
        print(response)
        with open("user_list.json", "w") as json_file:
            json_file.write(response.text)
            print("user list written successfully.")
    else:
        print("Error occurred while retrieving the list of users.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass

def add_user_to_group(group_id,user_id):
    if not group_id:
        group_id = input("Enter the VPC ID: ")
    if not user_id:
        user_id = input("Enter the subnet ID: ")
    # obtain the token
    auth_token = O_token_domain()

    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3//v3/groups/"f"{group_id}/users/{user_id}"
    
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    payload = {}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    response = requests.put(api_endpoint, headers=headers, json=payload)
    # Check the response status
    if response.status_code == 204:
        print(response)
        print("user added to group successfully.")
    else:
        print("Error occurred while adding the user to the group")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

    pass



















def display_menu():
    options = {
        '1': lambda: vpcs_list(project_id),
        '2': lambda: subnets_list(project_id),
        '3': lambda: delete_subnet(project_id, input("enter vpc id : "), input("enter subnet id : ")),
        '4': lambda: delete_vpc(project_id, input("enter vpc id : ")),
        '5': list_users,
        '6': lambda: user_detail(input("enter user id : ")),
        '7': add_user,
        '8': lambda: del_user(input("enter user id : ")),
        '9': lambda: add_IAM_user(domain_id),
        '10': lambda: list_groups(domain_id),
        '11': lambda: group_details(input("enter group id : ")),
        '12': lambda: user_belong(input("enter group id : "), input("enter user id : ")),
        '13': lambda: delete_group(input("enter group id : ")),
        '0': sys.exit
    }

    while True:
        print("Menu:")
        print("1. List VPCs")
        print("2. List Subnets")
        print("3. Delete Subnet")
        print("4. Delete VPC")
        print("5. List Users")
        print("6. User Detail")
        print("7. Add User")
        print("8. Delete User")
        print("9. Add IAM User")
        print("10. List Groups")
        print("11. Group Details")
        print("12. Check User Belong to Group")
        print("13. Delete Group")
        print("0. Exit")

        choice = input("Enter your choice: ")

        # Call the function corresponding to the user's choice
        options.get(choice, lambda: print("Invalid choice. Please try again."))()

# Entry point of the program
if __name__ == "__main__":


  # Ask the user for input variables
    domain_id = input("Enter your domain ID: ")
    project_id = input("Enter your project ID: ")
    sig.Key = input("Enter your key ")
    sig.Secret = input("Enter your secret: ")

    print(f"Domain ID: {domain_id}")
    print(f"Project ID: {project_id}")

    display_menu()