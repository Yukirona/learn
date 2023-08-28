### Ansible
This documentation guide you trough the installation and configuration of Ansible for flexible engine



#####installation
```bash
sudo apt install ansible
```
we verify the installation
```bash
ansible --version
```
we need to create a folder to store the hosts file and the playbook, like for terraform i will create an ansible folder in my user folder

we will have this architecture :

├── ansible
│   ├── hosts
│   ├── hosts.bak
│   ├── playbook.yml
│   └── ssh-key.pem
└── terraform
    ├── main.tf
    ├── provider.tf
    ├── terraform.tfstate
    └── terraform.tfstate.backup


the hosts file conf should be populated  depending on how you want to connect to your server/s.
As we are trying to connect to the flexible engine cloud we will use the user by default cloud and the ssh key given by flexible engine.

!!!note hosts
        [remote]
        remote_test

        [remote:vars]
        ansible_host="eip of your server"
        ansible_ssh_private_key_file="path to the .pem file corresponding to your server"
        ansible_user=cloud

!!!info
    the private key should be the file you downloaded when creating an ssh key on flexible engine

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
After that we need to setup our playbook we can do a lot of things with playbooks for more information yo u can refer to the documentation of ansible.

here is provided and explained the playbook we will use to install remotelabz on flexible engine

!!!note playbook.
    ```
    - name: Preparing server
        hosts: remote
        become: true
        tasks:
        - name: Update resolv.conf
          lineinfile:
            dest: /etc/resolv.conf
            regexp: '^nameserver'
            line: 'nameserver 8.8.8.8'
            state: present
        - name: Update and upgrade apt packages
            become: true
            apt:
              upgrade: yes
              update_cache: yes
              cache_valid_time: 86400 #One day

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
            ".* Passphrase:": R3mot3!abz-0penVPN-CA2020
            "Enter pass phrase for /root/EasyRSA/pki/private/ca.key:": R3mot3!abz-0penVPN-CA2020R3mot3!abz-0penVPN-CA2020
          timeout: 36000 
        args:
          chdir: ~/remotelabz
        register: install_output

        - name: Print install output
          debug:
            var: install_output.stdout_lines
    ```

this current playbook should be able to fetch the remotelabz build on github and to make the installation of the requirements, it will display the output of the commands to follow the process for more iformation see the following help section

!!!help

  


    ```
      - name: Preparing server
        hosts: remote
        become: true
        tasks:
        - name: Update resolv.conf
          lineinfile:
            dest: /etc/resolv.conf
            regexp: '^nameserver'
            line: 'nameserver 8.8.8.8'
            state: present
        - name: Update and upgrade apt packages
            become: true
            apt:
              upgrade: yes
              update_cache: yes
              cache_valid_time: 86400 #One day
     ```
     The first step is to set the dns, as there is no correct dns set during the installation of ubuntu 20.04 and we cannot proceed with updates and downloads without it, then we make ansible update and upgrade ubuntu.
     ```
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
    ```
    
    Then we need to retrieve the repo from the git as everything we need to install remotelabz is there

     ```
       
              - name: Change to the remotelabz directory
              become: false
              shell: cd ~/remotelabz

              - name: Install requirements
                become: true
                expect:
                  command: sudo ./bin/install_requirement.sh
                  responses:
                    ".* Passphrase:": R3mot3!abz-0penVPN-CA2020
                    "Enter pass phrase for /root/EasyRSA/pki/private/ca.key:": R3mot3!abz-0penVPN-CA2020R3mot3!abz-0penVPN-CA2020
                  timeout: 36000 
                args:
                  chdir: ~/remotelabz
                register: install_output

            - name: Print install output
              debug:
                var: install_output.stdout_lines
     ```
     For the final part we go into the directory of remotelabz and start the install_requirements script, as it will ask us for passphrases we will use expect, we set up regex corresponding to the line where we wil be prompted to enter our input and then we specify the text we want here our passphrase
    

!!!warning
    currently the playbook for ansible is not fully functional pending the resolutions of the problems it only download and install the pre requisites 

When you have finished to write your playbook you can apply it by using this command  : 

```bash
ansible-playbook -i hosts playbook.yml
```
We should obtain the output of the installation script at the end which is telling us that the installation is done in our case it is looking like this : 

!!!info last lines of the output
      PLAY RECAP ************************************************************************************************************************************************
    remote_test                : ok=8    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


Congratulations you have configured a server on flexible engine using ansible.