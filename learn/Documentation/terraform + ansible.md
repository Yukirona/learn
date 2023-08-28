# Terraform with flexible engine

This document guides you through the installation of RemoteLabz and its components on an Ubuntu system hosted on flexible engine using Terraform and Ansible

it does not stand  for a representation of the project/work or the trials and errors encountered, it is there as a user guide to understand and jump start into the use of remotelabz

Att he end you should have the following structure 

!!!tip

        ├── ansible
        │   ├── hosts
        │   ├── hosts.bak
        │   ├── playbook.yml
        │   └── ssh-key.pem
        ├── python
        │   ├── apig_sdk
        │   │   ├── __init__.py
        │   │   ├── __pycache__
        │   │   │   ├── __init__.cpython-310.pyc
        │   │   │   └── signer.cpython-310.pyc
        │   │   └── signer.py
        │   ├── auth_token.txt
        │   ├── del_subnets_vpcs.py
        │   ├── in_remote.py
        │   ├── main.py
        │   ├── Orange_auth.py
        │   ├── __pycache__
        │   │   └── main.cpython-310.pyc
        │   ├── subnet_list.json
        │   ├── test_signer.py
        │   ├── test_use.py
        │   ├── vpc_list.json
        │   └── vpc.py
        └── terraform
            ├── main.tf
            ├── provider.tf
            ├── terraform.tfstate
            └── terraform.tfstate.backup


## Installation of the requirements
First we need to work in a linux environment, here we will chose a wsl of ubuntu for its ease of use

Do not forget the usual 

```bash
apt-get update
apt-get upgrade
```

## Flexible engine

In order to setup the environment we need to do some things on Flexible engine 

Generate an AK/SK. 
(If an AK/SK file has already been obtained, skip this step and locate the downloaded AK/SK file. Generally, the file name will be credentials.csv.)

Log in to the management console.

Click the username and select My Credentials from the drop-down list.

On the My Credentials page, click the Access Keys tab.

Click Add Access Key.

Enter the verification code received by email.

Click OK to download the access key.

!!! warning
    Keep the the file secure
    If you already made a key and lost the file you can always delete and recreate a key

## Terraform
Now that we have the necessary key to authenticate to the flexible engine clous we need to install and configure terraform
```bash

wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
```
```bash
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
```
```bash
sudo apt update && sudo apt install terraform
```
```bash
terraform version
```
Now that we have terraform we need to set our working directory, here /home/terrafom
The documentation necessary to use terraform with 
flexible engine is available here 

!!!tip

    https://registry.terraform.io/providers/FlexibleEngineCloud/flexibleengine/latest/docs

Following the documentation we create two files, a main.tf file and a provider.tf file and populate the provider file as following : 

!!!note
        
        terraform {
        required_providers {
        flexibleengine = {
            source = "FlexibleEngineCloud/flexibleengine"
            version = "1.38.0"
        }
        }
        }

        # Configure the FlexibleEngine Provider
        provider "flexibleengine" {
        access_key  = "you access key"
        secret_key  = "your secret key"
        domain_name = "your domain name"
        region      = "you region"
        }

        
!!!info 
    the domain name can be found on the My Credentials page 
    In the provider put information given in the credentials.csv obtained

you can type the following command to verify the connectivity to flexible engine
```bash
terraform init
```
 you should obtain this output

!!!info 
    
    
        Initializing the backend...

        Initializing provider plugins...
        - Finding flexibleenginecloud/flexibleengine versions matching "1.38.0"...
        - Installing flexibleenginecloud/flexibleengine v1.38.0...
        - Installed flexibleenginecloud/flexibleengine v1.38.0 (self-signed, key ID 0D0EDE6AC300F5EE)

        Partner and community providers are signed by their developers.
        If you'd like to know more about provider signing, you can read about it here:
        https://www.terraform.io/docs/cli/plugins/signing.html

        Terraform has created a lock file .terraform.lock.hcl to record the provider
        selections it made above. Include this file in your version control repository
        so that Terraform can guarantee to make the same selections by default when
        you run "terraform init" in the future.

        Terraform has been successfully initialized!

        You may now begin working with Terraform. Try running "terraform plan" to see
        any changes that are required for your infrastructure. All Terraform commands
        should now work.

        If you ever set or change modules or backend configuration for Terraform,
        rerun this command to reinitialize your working directory. If you forget, other
        commands will detect it and remind you to do so if necessary.

Now you can fill the main.tf file , in our case here is the example conf we will use

!!!note

        resource "flexibleengine_vpc_v1" "example_vpc" {
        name        = "example-vpc"
        cidr        = "192.168.24.0/24"
        description = "Example VPC"
        }

        resource "flexibleengine_vpc_subnet_v1" "example_subnet" {
        name       = "example-subnet"
        cidr       = "192.168.24.0/24"
        gateway_ip = "192.168.24.1"
        vpc_id     = flexibleengine_vpc_v1.example_vpc.id
        }

        resource "flexibleengine_compute_instance_v2" "example_ecs" {
        name            = "example-ecs"
        image_name      = "OBS Ubuntu 20.04"
        flavor_id       = "s6.small.1"
        key_pair        = "KeyPair-ericbonnet1"
        security_groups = ["sg-eric.bonnet-2"]

        network {
            uuid = flexibleengine_vpc_subnet_v1.example_subnet.id
        }
        }

        resource "flexibleengine_vpc_eip" "eip_example" {
        publicip {
            type = "5_bgp"
        }
        bandwidth {
            name       = "test"
            size       = 10
            share_type = "PER"
        }
        }


        resource "flexibleengine_compute_floatingip_associate_v2" "myip" {
        floating_ip = flexibleengine_vpc_eip.eip_example.publicip.0.ip_address
        instance_id = flexibleengine_compute_instance_v2.example_ecs.id
        }

        output "eip" {
        value = flexibleengine_compute_instance_v2.example_ecs.floating_ip
        }
See the help section for details about the main.tf

!!!help
    here is help concerning some fields of the conf  according to the file order:

        name        = "example-vpc"
        cidr        = "192.168.24.0/24"
    replace by the name you want to give to your vpc and the network you want/can use

        name       = "example-subnet"
        cidr       = "192.168.24.0/24"

    same idea for the subnet

        name            = "example-ecs"
        image_name      = "OBS Ubuntu 20.04"
        flavor_id       = "s6.small.1"
        key_pair        = "KeyPair-ericbonnet1"
        security_groups = ["sg-eric.bonnet-2"]
     fill with the name you want to give to the server,the image should be Ubuntu 20.04 as presented flavor_id is depending on the performance you want for your server recommended 
      hard disk of at least 30 Go.
    2 Go of RAM
    1 CPU
    we put the smallest build possible because of demonstration purpose
    the key_pair should be corresponding to the name of one of the ssh key pairs you created

    !!!warning
        not the same thing as the key used for terraform authentication
    security groups here you should put your security group created on flexible engine that allow needed ports, should permit Internet to RemoteLabz

    !!!summary
        TCP 80 (443) : HTTP(S) pages
        TCP 8000 : WebSocket
        UDP 1194 : OpenVPN  

To finish the part concerning terraform we can use 
```bash
terraform apply
```
you should obtain 
```bash
Apply complete! Resources: 5 added, 0 changed, 0 destroyed. as a final mesage
```
you can now verify on the flexible engine console you should have you vpc, subnet, ecs , and eip deployed



### Ansible
Now that we have our infrastructure deployed we need to use ansible  in order to deploy remotelabz.

To to this we will nee to install Ansible but before we have again a file to retreive from flexible engine, we need our key pair associated with the server we created.

when creating the key pair we were given a .pem file we will need it.
```bash

sudo apt install python3-pip

sudo apt intsall ansible

ansible --version
```
we need to create a folder to store the hosts file and the playbook, we will put them in the same folder this time

the hosts file conf

!!!note
    [remote]
    remote_test

    [remote:vars]
    ansible_host="eip of your server"
    ansible_ssh_private_key_file="path to the .pem file corresponding to your server"
    ansible_user=cloud

this done you can verify the connectivity using
```bash
ansible -i hosts remote -m ping
```
you should obtain the following 
```ansible
remote_test | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```
After that we need to setup our playbook to follow with the installation of remotelabz we will just proceedwith the installation of the requirements for now

!!!note
        ---
        - name: Install RemoteLabz Front
        hosts: remote
        become: true
        become_user: cloud
        tasks:
            - name: Retrieve RemoteLabz Front source
            git:
                repo: https://github.com/remotelabz/remotelabz.git
                dest: ~/remotelabz
                version: master
                accept_hostkey: yes
            become: false

            - name: Change to the remotelabz directory
            become: false
            shell: cd ~/remotelabz

            - name: Install requirements
            become: true
            expect:
                command: sudo ./bin/install_requirement.sh
                responses:
                - "Enter passphrase for /path/to/private/key1:": passphrase1
                - "Enter passphrase for /path/to/private/key2:": passphrase2
                - "Enter passphrase for /path/to/private/key3:": passphrase3
            args:
                chdir: ~/remotelabz
            register: install_output

            - name: Print install output
            debug:
                var: install_output.stdout_lines

this current playbook should be able to fetch the remotelabz build on github and to make the installation of the requirements, it will display the output of the commands to follow the process for more iformation see the following help section

!!!help
        - name: Install RemoteLabz Front
        hosts: remote
        become: true
        become_user: cloud
    we start by telling wich host in our hosts file is concerned by the playbook, then we are becoming the cloud user used to log into the server

        tasks:
            - name: Retrieve RemoteLabz Front source
            git:
                repo: https://github.com/remotelabz/remotelabz.git
                dest: ~/remotelabz
                version: master
                accept_hostkey: yes
            become: false
    Here is the task that is retrreiving the github repo containing remotelabz files

            - name: Change to the remotelabz directory
            become: false
            shell: cd ~/remotelabz
    We go inside the remotelabz folder

            - name: Install requirements
            become: true
            expect:
                command: sudo ./bin/install_requirement.sh
                responses:
                - "Enter passphrase for /path/to/private/key1:": passphrase1
                - "Enter passphrase for /path/to/private/key2:": passphrase2
                - "Enter passphrase for /path/to/private/key3:": passphrase3
            args:
                chdir: ~/remotelabz
            register: install_output
    This part launch the script for the installation of the requirements, as we are prompted to enter passphrases it is expect to receive them and will tell you so

            - name: Print install output
            debug:
                var: install_output.stdout_lines
    at the end we ask ansible to print the output of the installation to verify the execution


#### python script to do it all

here i will provide a python script which allows the use of commands for terraform ansible and later the use of the api app that complete the actions that terraform or ansible cannot automatize

!!!warning 
    this is not some plug and play option there will still be need to install the prerequisites for each part thus i gladly recommend to follow the entierty of the guide but the goal is to centralize the way to manage our installation because it is tiresome to alternate between commands and maybe later to make it grow to take more task into account

Right now the script is doing severals steps 

!!!summary
    - Using terraform to deploy the server
    - Retreiving the external ip associated with it
    - Creating/Updating the file hosts useb by ansible
    - Using ansible to follow with the installation of remotelabz

```bash
pip install python_terraform
```

#### API

I have mentionned an api, flexible engine provide an extensive documentation on its api, some actions like creating ressources are better done and managed by terraform but for some cases there is no other possibility than the api, for instance as the terraform provider lack data sources it allow us to deploy a complete infrastructure but it cannot fetch data to verify or deleting the existence of  existing vpcs , subnets , ecs , ect .....

Also the api allows us to do account , user groups management and much more

the python files for the api are provided in the same folder as the rest of our installation and are fully commented for anyone to work with them but here is some comparaison between the python commands and the flexible engine api documentation

for example here is the python code that allow us to get the list of all the vpcs existing on the project and its api documentation source

!!!note

        Querying VPCs
        Function
        This API is used to query VPCs using search criteria and to display the VPCs in a list.

        URI
        GET /v1/{project_id}/vpcs

        Example:
        GET https://{Endpoint}/v1/{project_id}/vpcs?limit=10&marker=13551d6b-755d-4757-b956-536f674975c0
        Table 1 describes the parameters.
        Table 1 Parameter description
        Name

        Mandatory

        Type

        Description

        project_id

        Yes

        String

        Specifies the project ID. For details about how to obtain a project ID, see Obtaining a Project ID.

        marker

        No

        String

        Specifies a resource ID for pagination query, indicating that the query starts from the next record of the specified resource ID.

        This parameter can work together with the parameter limit.

        If parameters marker and limit are not passed, resource records on the first page will be returned.
        If the parameter marker is not passed and the value of parameter limit is set to 10, the first 10 resource records will be returned.
        If the value of the parameter marker is set to the resource ID of the 10th record and the value of parameter limit is set to 10, the 11th to 20th resource records will be returned.
        If the value of the parameter marker is set to the resource ID of the 10th record and the parameter limit is not passed, resource records starting from the 11th records (including 11th) will be returned.
        limit

        No

        Integer

        Specifies the number of records that will be returned on each page. The value is from 0 to intmax.

        limit can be used together with marker. For details, see the parameter description of marker.

        Request Message
        Request parameter
        None

        Example request
        GET https://{Endpoint}/v1/{project_id}/vpcs
        Response Message
        Response parameter
        Table 2 Response parameter
        Name

        Type

        Description

        vpcs

        Array of vpcs objects

        Specifies the VPCs.

        Table 3 Description of the vpcs field
        Name

        Type

        Description

        id

        String

        Specifies a resource ID in UUID format.

        name

        String

        Specifies the VPC name.
        The value can contain no more than 64 characters, including letters, digits, underscores (_), hyphens (-), and periods (.).
        Each VPC name of a tenant must be unique if the VPC name is not left blank.
        description

        String

        Provides supplementary information about the VPC.
        The value can contain no more than 255 characters and cannot contain angle brackets (< or >).
        cidr

        String

        Specifies the available IP address ranges for subnets in the VPC.
        Possible values are as follows:
        10.0.0.0/8-24
        172.16.0.0/12-24
        192.168.0.0/16-24
        If cidr is not specified, the default value is left blank.
        The value must be in CIDR format, for example, 192.168.0.0/16.
        status

        String

        Specifies the VPC status.
        Possible values are as follows:
        CREATING: The VPC is being created.
        OK: The VPC is created successfully.

        Example response
        {
            "vpcs": [
                {
                    "id": "13551d6b-755d-4757-b956-536f674975c0",
                    "name": "default",
                    "description": "test",
                    "cidr": "172.16.0.0/16",
                    "status": "OK"
                },
                {
                    "id": "3ec3b33f-ac1c-4630-ad1c-7dba1ed79d85",
                    "name": "222",
                    "description": "test",
                    "cidr": "192.168.0.0/16",
                    "status": "OK"
                },
                {
                    "id": "99d9d709-8478-4b46-9f3f-2206b1023fd3",
                    "name": "vpc",
                    "description": "test",
                    "cidr": "192.168.0.0/16",
                    "status": "OK"
                }
            ]
        }

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