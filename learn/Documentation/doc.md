# Terraform with flexible engine

This section guides you through the installation of RemoteLabz and its components on an Ubuntu system. We assume you have already installed an Ubuntu Server 20.04 LTS. We support only this Ubuntu version.

## Installation of the requirements
The first step is to install Ubuntu Server 20.04 LTS https://releases.ubuntu.com/20.04.4/ubuntu-20.04.4-live-server-amd64.iso on

- only one computer if you want to use the Front and the Worker on the same server
- one 2 computers if you want to separate your Front and your Worker.

To install both the Front and the Worker on the same device, the minimum requirement is 

- a hard disk of at least 30 Go.
- 2 Go of RAM
- 1 CPU

Depend of the number of VMs, containers, and, operating system used, you want to run simultaneously. At the end of the installation, 4 devices will be installed and configured :

- 3 containers with Debian 11.4, Alpine 3.15, Ubuntu Server 20.04 LTS
- 1 VM Alpine 3.10

The 5th device, called "Migration" is another Alpine to use to configure, at the end of the installation, a 6th container, a DHCP service.

## Provider

A remotelabz directory will be create on your home directory.
```bash
cd ~
git clone https://github.com/remotelabz/remotelabz.git --branch master
```

You have now a directory `remotelabz` created on your home directory.

!!! warning
    If you want to install a specific version, you have to do the following instructions. For version 2.4.1 for example.
    ```bash    
    git clone https://github.com/remotelabz/remotelabz.git --branch 2.4.1 --single-branch
    ```
    or for development version
    ```bash    
    git clone https://github.com/remotelabz/remotelabz.git --branch dev
    ```

### Install the requirements
```bash
cd remotelabz
sudo ./bin/install_requirement.sh
```

After this process, you have to understand the following information :

#### RabbitMQ and MySQL pre-configurations
The MySQL is configured with the root password : "RemoteLabz-2022\$", and a user "user" is created with password "Mysql-Pa33wrd\$". It is recommend to change it after your RemoteLabz works fine.

!!! Tips
    During the `install_requirement.sh` process, a `remotelabz-amqp` user is created in RabbitMQ with the password `password-amqp`. If you want to change the password of an existing user `remotelabz-amqp` of your RabbitMQ, you have to type the following command :
    ```
    sudo rabbitmqctl change_password 'remotelabz-amqp' 'new_password'
    ```
    For MySQL, to set the root password to `new_password`
    ```
    sudo mysql -u root -h localhost
    ALTER USER IF EXISTS 'root'@'localhost' IDENTIFIED BY 'new_password';
    FLUSH PRIVILEGES;
    EXITS;
    ```
    The remotelabz default user is `user` and its password `Mysql-Pa33wrd\$`. If you want to change to `new_password` for example, you have to do the following:
    ```
    ALTER USER IF EXISTS 'user'@'localhost' IDENTIFIED BY 'new_password';
    FLUSH PRIVILEGES;
    EXITS;
    ```

#### OpenVPN pre-configuration
The default passphrase used during the `install_requirement.sh` process is `R3mot3!abz-0penVPN-CA2020`. You can find this value in your `.env` file

```bash
SSL_CA_KEY_PASSPHRASE="R3mot3!abz-0penVPN-CA2020"
```
If you decide to change it, don't forget to change it in the `/opt/remotelabz/.env.local`.

!!! warning
    The last line `push "route 10.11.0.0 255.255.0.0"` in your `/etc/openvpn/server/server.conf` must be modified if you modifies, in your `.env.local` file, the parameters of the two next lines 
    ```BASE_NETWORK=10.11.0.0
    BASE_NETWORK_NETMASK=255.255.0.0```
    This network will be the network used for your laboratory. Your user must have a route on its workstation to join, via his VPN, his laboratory. Be careful, this network must have to be different of the user network at home.
`

### Configure the mail (Exim4)
1. Configure the /etc/aliases to redirect all mail to root to an existing user of your OS
2. Check the aliases with the command `exim -brw root`
3. Edit the file `/etc/exim4/exim4.conf.template` and locate the part "Rewrite configuration" to have, for example, the following lines :
```bash
######################################################################
#                      REWRITE CONFIGURATION                         #
######################################################################

begin rewrite

user@* myemail@domain.com FfrsTtcb
root@* myemail@domain.com FfrsTtcb
```
4. Update your exim configuration with command `sudo update-exim4.conf`, following the command `sudo service exim4 restart`
5. Check all addresses are rewritten with the command `exim -brw root`

### Install RemoteLabz application

The install process will create the directory `/opt/remotelabz`.

While you're in RemoteLabz root directory :

``` bash
cd ~/remotelabz
sudo ./bin/install
```
The install process can take 5 minutes

!!! info
    During the installation, some actions is done on the directory permission :
    ```bash
    chgrp remotelabz /etc/openvpn/server -R
    chmod g+rx /etc/openvpn/server -R
    ```

#### Configure the RemoteLabz database
Run the `remotelabz-ctl` configuration utility to setup your database :

```bash
sudo remotelabz-ctl reconfigure database
```

Don't forget to edit your `/opt/remotelabz/.env.local` :

!!! warning
    Don't forget to modify the line `PUBLIC_ADDRESS="your-url-or-ip-of-your-front"`

#### Generate API keys
At the root of your RemoteLabz directory:

```bash
cd /opt/remotelabz
sudo mkdir -p config/jwt
sudo openssl genpkey -out config/jwt/private.pem -aes256 -algorithm rsa -pkeyopt rsa_keygen_bits:4096
#Your can use as passphrase "JWTTok3n"
sudo openssl pkey -in config/jwt/private.pem -out config/jwt/public.pem -pubout
sudo chown -R www-data:www-data config/jwt
sudo chown -R www-data:www-data var
# Replace 'yourpassphrase' by your actual passphrase
echo "JWT_PASSPHRASE=\"JWTTok3n\"" | sudo tee -a .env.local
```

!!! warning
    Avoid special character in the JWT, otherwise you will have some errors

!!! tips
    In order for the app to work correctly, a key pair is created for JWT. You can find detailed configuration in [the LexikJWTAuthenticationBundle doc](https://github.com/lexik/LexikJWTAuthenticationBundle/blob/master/Resources/doc/index.md#generate-the-ssh-keys).

#### Start the RemoteLabz Front

In order to be able to control instances on [the worker](https://gitlab.remotelabz.com/crestic/remotelabz-worker), you need to start **Symfony Messenger** :

```bash
sudo systemctl enable remotelabz
sudo systemctl enable remotelabz-proxy
sudo systemctl start remotelabz
sudo systemctl start remotelabz-proxy
```

You can now test your RemoteLabz front with your internet navigator but you will just make connection until the worker is not installed.

!!! info
    The default credentials are :

    - Username : `root@localhost`
    - Password : `admin`

    You may change those values by using the web interface.


!!! warning
    When consuming messages, a timestamp is used to determine which messages the messenger worker is able to consume. Therefore, each machines needs to be time-synchronized. We recommend you to use a service like `ntp` to keep your machines synchronized.

!!! warning
    Now you have to install RemoteLabz Worker

## Installation of the Worker
### Retrieve the RemoteLabz Worker source 
A remotelabz directory will be create on your home directory.
```bash
cd ~
git clone https://github.com/remotelabz/remotelabz-worker.git --branch master
```
A `remotelabz-worker` directory is created after the previous command.

!!! tips
    If you want to install only a specific version, you have to do the following instruction, for version 2.4.1 for example.
    ```bash    
    git clone https://github.com/remotelabz/remotelabz-worker.git --branch 2.4.1 --single-branch
    ```
    ou
    ```bash    
    git clone https://github.com/remotelabz/remotelabz-worker.git --branch dev
    ```

### Installation of the RemoteLabz worker application
```bash
cd ~/remotelabz-worker
cp .env .env.local
```

You should modify the `~/remotelabz-worker/.env.local` file according to your environment before starting the worker installation.


Next, type 
```bash
sudo ./install
```
### Configuration of the worker

#### Start your RemoteLabz Worker service
Normally, the service remotelabz-worker is started during the installation phase and it will start automatically when your system boots but if you need to start the service manually :

```bash
sudo systemctl start remotelabz-worker
```

!!! tips
    To automatically start the service on boot 
    ```bash
    sudo systemctl enable remotelabz-worker
    ```
    To check the status of your service
    ```bash
    sudo service remotelabz-worker status
    ```

You can check the log of the worker in `/opt/remotelabz-worker/var/log/prod.log`

!!! warning
    When consuming messages, a timestamp is used to determine which messages the messenger worker is able to consume. Therefore, each machines needs to be time-synchronized. We recommend you to use a service like `ntp` to keep your machines synchronized.

The installation is finish and RemoteLabz application must be works. You have now to change the parameter in the `/opt/remotelabz/.env.local` to have the following

```bash
APP_MAINTENANCE=0
```
If you let the value 1, nobody can use the application.

If you have an error 500, do the following :
```bash
cd /opt/remotelabz
sudo chown -R www-data:www-data config/jwt
sudo chown -R www-data:www-data var
```

## Configure your RemoteLabz
### Add a DHCP Service for your laboratory
In the device list, you will find a device with the name "Migration". This container will be used to configure a new container, called "Service" to provide a DHCP service to your laboratory. Each laboratory has its DHCP service and its network so the RemoteLabz needs to configure this generic container to offer IP on the right network. For each lab, if you add the DHCP service container, it will be configured with the IP : IP_Gateway - 1. For example, if your attributed network is 10.10.10.0/27, your gateway will be 10.10.10.30 and you DHCP service container will have the IP 10.10.10.29 .

First : go to the sandbox menu and start the "Migration" device. Next, in the console of the started device, configure the network of the device (show the log, with "Show logs" button to know it) 
!!! tips
    Add an IP address `ip addr add X.X.X.X/M dev eth0`

    Add the default route `ip route add default via X.X.X.X`

    Add a DNS Server `echo "nameserver 1.1.1.1" > /etc/resolv.conf`

Next, type the following command :
```bash
apt-get update; apt-get -y upgrade; apt-get install -y dnsmasq;
echo "dhcp-range=RANGE_TO_DEFINED" >> /etc/dnsmasq.conf
echo "dhcp-option=3,GW_TO_DEFINED" >> /etc/dnsmasq.conf
systemctl stop systemd-resolved
systemctl disable systemd-resolved
systemctl disable systemd-networkd
systemctl enable dnsmasq
```

The last line (`systemctl disable systemd-networkd`) is mandatory otherwise your container will not have any IP.

Your "Service" device, which is a container, is now ready. You have to stop the Migration device, click on Export and type, as a New Name : Service and click on the button "Export Device"
On your lab, if you add Service device, you will have a DHCP service for all your devices of your lab.

## Secure the communication
If you want to secure all communication between the client, the Remotelabz front and the Remotelabz Worker, you have to follow the instruction of [page SSL](ubuntu-secure.md) 

# Configure RemoteLabz to use SSL

This section guides you through the configuration of SSL between all service of the RemoteLabz.

## Requirement
Your Remotelabz must work fine before to configure the SSL

- You must connect to a device of type QEMU
- You must connect to a device of type LXC

## Configure your Apache 2 with HTTPS (required if you want to use Shibboleth)

During the installation process, the file `200-remotelabz-ssl.conf` is copy in your `/etc/apache2/sites-available` directory. The certificate is defined as follow :
```bash
        SSLCertificateFile	/etc/apache2/RemoteLabz-WebServer.crt
        #SSLCertificateChainFile /etc/ssl/certs/remotelabz._INTERMEDIATE.cer
        SSLCertificateKeyFile /etc/apache2/RemoteLabz-WebServer.key
```

Two case, either you have an official certificate or you have to generate your own certificate.
### Official certificate

If you have an official certificate, you have to copy it in your `/etc/apache2` directory and rename it to `RemoteLabz-WebServer.crt` and `RemoteLabz-WebServer.key`. Next, you have to activate this site:
```bash
sudo a2ensite 200-remotelabz-ssl.conf
sudo a2enmod ssl
sudo service apache2 reload
```

### Self-signed certificate
Execute the script 
```bash
cd ~
sudo remotelabz/bin/install_ssl.sh
```

## Redirection to https
Verify your application is now available with HTTPS and if it works fine, you can modify the `/etc/apache2/sites-available/100-remotelabz.conf` to redirect all HTTP request to HTTPS. 
Activate the rewrite module
```bash
sudo a2enmod rewrite
```

Uncomment the following lines in the file `/etc/apache2/sites-available/100-remotelabz.conf`:
```bash
#<IfModule mod_rewrite.c>
#    RewriteEngine On
#    RewriteCond %{HTTPS} !=on
#    RewriteRule ^/?(.*) https://%{SERVER_NAME}/$1 [R,L]
#</IfModule>
```
Now, if you go to the your application's url with http, you should be redirected to HTTTS.

!!! tips
    You can verify your certificate with the following command : 
    ```bash
    openssl x509 -noout -text -in /etc/apache2/RemoteLabz-WebServer.crt
    ```

!!! warning 
    Don't forget to reload the Apache 2 service
    ```bash
    sudo service apache2 reload
    ```

### Copy certificate files to the worker
Copy the two files `~/EasyRSA/RemoteLabz-WebServer.crt` and `~/EasyRSA/RemoteLabz-WebServer.key` to your **worker** in directory `/opt/remotelabz-worker/config/certs`

```bash
cd ~/EasyRSA
source /opt/remotelabz/.env.local
scp ~/EasyRSA/RemoteLabz-WebServer.crt user@${WORKER_SERVER}:~
sudo scp ~/EasyRSA/RemoteLabz-WebServer.key user@${WORKER_SERVER}:~
```

On the **worker**
```bash
cd ~
sudo mv RemoteLabz-WebServer.* /opt/remotelabz-worker/config/certs/
sudo sed -i "s/REMOTELABZ_PROXY_USE_WSS=0/REMOTELABZ_PROXY_USE_WSS=1/g" /opt/remotelabz-worker/.env.local
sudo service remotelabz-worker restart
```

!!! warning
    You need to use the same certificate between your front and the worker. Don't forget to copy them and to change it automatically if your certificate expired.


## Shibboleth (optional - You have to be registered by Renater)

!!!warning
    You have to activate HTTPS to use Shibboleth authentication method

```bash
cd ~
curl --fail --remote-name https://pkg.switch.ch/switchaai/ubuntu/dists/focal/main/binary-all/misc/switchaai-apt-source_1.0.0~ubuntu20.04.1_all.deb
sudo apt install ./switchaai-apt-source_1.0.0~ubuntu20.04.1_all.deb
sudo apt update
sudo apt install --install-recommends shibboleth
sudo a2enconf shib
sudo a2enmod shib
sudo service apache2 restart
```

Next step, to finish to configure your Shibboleth Service Provider (SP), you have to modify your `/etc/shibboleth/shibboleth2.xml` file, following the guide from Paragraph 4, depend of your Shibboleth Identity Provider (IdP):

 - [SWITCH Shibboleth Service Provider (SP) 3.1 Configuration Guide](https://www.switch.ch/aai/guides/sp/configuration/){target=_blank}
 - [RENATER Shibboleth Service Provider (SP) Configuration Guide](https://services.renater.fr/federation/documentation/guides-installation/sp3/chap04){target=_blank}

You can find all the configuration guides on the following site :

- [On Ubuntu 20.04 LTS](https://www.switch.ch/aai/guides/sp/installation/?os=ubuntu20){target=_blank}

To enable Shibboleth site-wide, you need to change the value of `ENABLE_SHIBBOLETH` environment variable :

```bash
# .env.local
ENABLE_SHIBBOLETH=1
```