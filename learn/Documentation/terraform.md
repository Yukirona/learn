## Terraform
This documentation guide you trough the installation and configuration of terraform for flexible engine

In order to setup the environment we need to do some things on Flexible engine 

##### Generate an AK/SK. 
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

for the two following section you will need to proceed with an installation of an elastic cloud server using the flexible console to be able to  create the needed things.
##### create a security group
when creating an ecs on the page 2 the second box is containing a field security group with the option to select one already existing and to create one, you can also view and set the inbound and outbound rules from there 

following the remote labz documention whe have these rules 

!!! example "Ports used (Summary)"

    === "Internet to RemoteLabz"
        - **TCP 80 (443)** : HTTP(S) pages
        - **TCP 8000** : WebSocket
        - **UDP 1194** : OpenVPN

    === "RemoteLabz to RemoteLabz-Worker"
        - **TCP 8080** : Remotelabz-Worker Internal API

    === "RemoteLabz Worker to RabbitMQ"
        - **TCP 5672** : AMQP

##### create a ssh key pair

On the third page during the creation of an ecs you have a field which allows you to select an create a key pair create and store the one you will want to use for later

you can now interrupt the creation of the ecs as we will not be creating manually and we have created the resources we needed

##### Installation

Now that we have the necessary key to authenticate to the flexible engine cloud we need to install terraform
```bash

wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
```
```bash
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
```
```bash
sudo apt update && sudo apt install terraform
```
then we verify the installation
```bash
terraform version
```
Now that we have terraform we need to set our working directory, here the work is done in a user folder in /home
We will have this architecture

|── terraform
    ├── main.tf
    ├── provider.tf
    ├── terraform.tfstate
    └── terraform.tfstate.backup

The documentation necessary to use terraform with 
flexible engine is available here :

!!!tip Terraform-flexible engine documentation

    https://registry.terraform.io/providers/FlexibleEngineCloud/flexibleengine/latest/docs

Following the documentation we create two files, a main.tf file and a provider.tf file and populate the provider file as following : 

!!!note provider.tf
        
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
You must be present in your working directory, where the terraform files are in order yo use the commands if not it will prompt you  this : 

```
Terraform initialized in an empty directory!

The directory has no Terraform configuration files. You may begin working
with Terraform immediately by creating Terraform configuration files.

````

you can type the following command to verify the connectivity to flexible engine
```bash
terraform init
```
 you should obtain this output


    
    
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

Now you can fill the main.tf file this will be the file used by terraform to deploy, in our case here is the example conf we will use

!!!info
    If you are using this doc for a general use of terraform with flexible engine the following main.tf may not be corresponding to the ressources you want to deploy, it can still serve as an example , for more details refer to the documentation given previously.

!!!note main.tf

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
See the help section for details about the main.tf what we are doing and why.

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


To finish the part concerning terraform we can use 
```bash
terraform apply
```
you should obtain a similair output
```bash
Apply complete! Resources: 5 added, 0 changed, 0 destroyed. as a final mesage
```
you can now verify on the flexible engine console you should have your vpc, subnet, ecs , and eip deployeor other ressourcess you added deployed.

Congratulations you have deployed an infrastructure on flexible engine using terraform