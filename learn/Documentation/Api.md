#### API

Flexible engine can be used using its  console or terraform but it also has an API which allow us to make custom requests and to make automation
In this documentation i will present the python scripts made to use the api for flexible engine.

#### Pre-requisites

We will need several things to be able to contact the api

first we will need python but we should already have it.

We decided to use an AK / SK authentication when it is possible so we will need the file containing this information, also we use a library for python to sign our request, it is available here :

!!!tip 
    https://support.huaweicloud.com/intl/en-us/devg-apisign/api-sign-sdk-python.html

we downloaded the sdk and imported it in our python script

We will also need to use requests 

````bash
pip install requests
````

For the entirety of this doc we will refer to the official documentation provided by orange :

!!!tip API documentation
    https://docs.prod-cloud-ocb.orange-business.com/api

It is containing all the actions we can use with the API each of the following part 

Our architecture is looking like this : 
├── python
│   ├── apig_sdk
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   └── signer.cpython-310.pyc
│   │   └── signer.py
│   ├── auth_token.txt
│   ├── del_subnets_vpcs.py
│   ├── main.py
│   ├── Orange_auth.py
│   ├── __pycache__
│   │   └── main.cpython-310.pyc
│   ├── subnet_list.json
│   ├── test_signer.py
│   ├── test_use.py
│   └──  vpc_list.json


#### How to use it 

For now the scripts are meant to be used by choosing the function you want to use and calling it in a temporary python file, the final goal would be to at least have an cmd interface to display and use the functions 

I will present here a series of example of tasks using the API with the corresponding code explained

To use them you need to call the functions in a custom python file with the corrects imports and the changes of variables depending on your flexible engine domain configuration/account

we have two ways of contacting the first is by obtaining a token which is needed for actions concerning IAM the other is by using auhtentication key and secret

###### token
in order to obtain our token we use this code : 
```python
import requests
import json

def O_token_domain():
    # Set the API endpoint URL
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3/auth/tokens"

    # Set the request payload
    payload = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": "username",
                        "password": "yourpassword",
                        "domain": {
                            "name": "yourdomain"
                        }
                    }
                }
            },
            "scope": {
                "domain": {
                "name": "yourdomain"
                }
            }   
        }

    }

    print("--------------start token accquisition--------------------------------")
    # Make the API request to obtain the authentication token
    response = requests.post(api_endpoint, json=payload)
    
    # Check the response status
    if response.status_code == 201:
        # Get the authentication token from the response headers
        auth_token = response.headers.get("X-Subject-Token")
        # Store the authentication token in a file
        with open("auth_token.txt", "w") as token_file:
            token_file.write(auth_token)
            #print("Authentication token stored successfully.")
            print("--------------end token accquisition--------------------------------")
    else:
        print("Error occurred while retrieving the authentication token.")
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
    
    return auth_token

    pass
```
the goal of this function is to obtain a domain token and to write it for us to use it in other requests to the API

then we can build a request with token as following : 

```python
# obtain the token
    auth_token = O_token_domain()

    # Set the API endpoint variable
    api_endpoint = "https://iam.eu-west-0.prod-cloud-ocb.orange-business.com/v3/users"
    
    # Set the headears here the token and the content
    headers = {"content-type": "application/json",
                 "X-Auth-Token": auth_token               
                 }
    # build the request
    response = requests.get(api_endpoint, headers=headers)

```
###### AK / SK
For this we use the sdk mentionned earlier the following is showing how it looks like to make a request : 
```python
from apig_sdk import signer
sig = signer.Signer()
# Set the AK/SK to sign and authenticate the request.
sig.Key = "your key"
sig.Secret = "your secret"

def vpcs_list():
    # Set the API endpoint variables
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"
    project_id = "894ac8446e99430c994f7f392c5c8b32"

    # Construct the complete API endpoint URL
    api_endpoint = f"{endpoint}/v1/{project_id}/vpcs"

    # Specify a request method, such as GET, PUT, POST, DELETE, HEAD, and PATCH.
    r = signer.HttpRequest("GET", api_endpoint)
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    r.headers = {"content-type": "application/json"}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    r.body = ""
    sig.Sign(r)
    print(r.headers["X-Sdk-Date"])
    print(r.headers["Authorization"])
    response = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)

```

there is not a major difference between the two methods


Now i will list the  actions allowed by the scripts each part is corresponding to a entry in the API documentation, the corresponding code is provided when finished and/or commented
For more information concerning the request you can refer to the api documentation online.
#Actions
#### Users

Thanks to the API we can realize different actions on the users without the need of using the interface

###### Querying a User List
GET /v3/users
```python
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
```
This is the function we use to get the list of the users and then write it in a json file.

###### Creating a User
POST /v3/users
```python
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
```
This is the function we use to add a user 

###### Creating an IAM User
POST /v3.0/OS-USER/users
```python

def add_IAM_user():
    
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
        "domain_id": "a0fe10e2d45a42178afdff17e784041b",
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
```

###### Deleting a User
DELETE /v3/users/{user_id}
```python
def del_user(user_id):
   

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
```
This is the function we use to delete a user


######Listing User Groups

GET /v3/groups{?domain_id,name}
######Querying User Group Details
GET /v3/groups/{group_id}



######Creating a User Group

POST /v3/groups

######Querying Whether a User Belongs to a User Group
HEAD /v3/groups/{group_id}/users/{user_id}

 
###### Deleting a User Group

DELETE /v3/groups/{group_id}
##### VPC

###### Querying VPCs
GET /v1/{project_id}/vpcs
```python 
def vpcs_list():
    

    # The following example shows how to set the request URL and parameters to query a VPC list.

    # Set the API endpoint variables
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"
    project_id = "894ac8446e99430c994f7f392c5c8b32"

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
```
###### Deleting a VPC
DELETE /v1/{project_id}/vpcs/{vpc_id}
```python
def delete_vpc(vpc_id):
   

    # The following example shows how to set the request URL and parameters to query a VPC list.

    # Set the API endpoint variables
    project_id = "894ac8446e99430c994f7f392c5c8postb32"
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

```


###### Deleting a Subnet
DELETE /v1/{project_id}/vpcs/{vpc_id}/subnets/{subnet_id}
```python
def delete_subnet(vpc_id, subnet_id):
   

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
```
###### Querying Subnets
GET /v1/{project_id}/subnets
```python

def subnets_list():
   

    # The following example shows how to set the request URL and parameters to query a subnet list.

    # Set the API endpoint variables
    endpoint = "https://vpc.eu-west-0.prod-cloud-ocb.orange-business.com"
    project_id = "894ac8446e99430c994f7f392c5c8b32"

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
```

!!!warning 
    there is a lot more of actions permitted by the api that can and will be added in the python app depending on advancement on it, for instance we could manage projects, permissions, manage ECS ..... ect

    also the app should present in an interface the options it can do and an other possibility would be to prompt the user for information 
#### Use case

After all these examples of actions we can take using the API lets show an example

As a teacher After using flexible engine as a lab for my students i have remnants of their installations i could delete them using the console but it would take forever so il will use the functions described here to get rid of the all the ressources in the project, my student were nice they already deleted the virtual machines they created as it cost money now lets see how we can get rid of the private clouds remaining.

```python
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

```

In this scenario i must start by getting the list of all my subnets and all my vpc, then from the file containing all the subnets i extract the id of the subnets and their corresponding vpc, with these informations i can call the function delete subnet in a for iteration that delete all the subnets

then i will do the same for the vpcs

if i had virtual machines remaining in some subnets i would have to delete them first as i cannot delete a ressources if others are still depending on it same idea for external ip associated to elastic cloud servers
