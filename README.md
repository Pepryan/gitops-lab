## About Lab BRI Project
This repository is used for BRI project research purposes. Furthermore, this CI/CD is applied for instance provisioning

## Build With
- <a href="https://www.terraform.io/" target="_blank">Terraform</a>
- <a href="https://www.python.org/" target="_blank">Python</a>
- <a href="https://docs.gitlab.com/runner/" target="_blank">Gitlab-Runner</a>

## Prerequisites
- You have read `isos.txt` on inventory directory for choose the OS image
- You have read `networks.txt` on inventory directory for select the network
- You have looking `vm.yaml` is existing for checking IP address had been used before

## Getting Started
### How to create instance on lab7.btech.id? ###
- Clone repository
- Create your branch
- Edit file `vm.yaml` as per your specification
  - Change vm name and specifications. Ensure you write the unique name.
    <br>The below for example :</br>

```
# ################### VM Ahsan #####################
   - name: ahs-vm1
     hostname: ahs-vm1
     nested_enabled: true
     os: ubuntu
     vcpus: 1
     memory: 2G
     console: vnc
     cloud_data:
       users:
         - name: root
           public_key:
             - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDKvMhH1eVLL1Ev98fuEujYqj/KIoJFrzu7vxj96Usc7qZp+W1n9kVTREjA6D63ko5RRD6QWl0k7oZhIfBy5vFJk+a/tzpVELb+bKutgoIgxtCZjyuVfIkw2sU40q3maA/kBAp4MEaupYxE4zQ9COpRev2Oqz+R6wchEl9FkAOVVZeWL1X0/lA6SG5VTf5vwj8FU7+yUcK+I8w/+rL+r/dJrPdXvKwSWsU0UnfVx4G1yroXcW0oaVYNplLK6IHxDuAyEsVkCy9ojyWuhBC39/w6ORDQJTRVp9njhil8TbT6EoruyvXDG6D62O5HahV10y0GIGzRc6xAHzzcscnBETjMLaOnRDg8qmlH+aXwTv0OfbLEtYQ6ZY16nTMAvoGIZ9kD7YscQdiKoYsF6tyYW4F1ezoJYCb67w30wRRdUByZ8k8wtF6wUwDZdjGJT7VlaH2KrEQsFVZkwi5NypXS5iyGjpjHsBRehGFfWqDIHWjN9+vJ5VpDEVc6Xb/5px+0Xjc= root@dwara
         - name: ubuntu
           password: ubuntu
           sudo: true
     base_image:
       storage_pool: isos
       name: ubuntu-focal.img
     disks:
       storage_pool: vms
       disk_format: qcow2
       disks:
         - name: ahs-vm1-vda.qcow2
           size: 4G
     networks:
       - name: net-10.30.13
         address: 10.30.13.171/24
         gateway: 10.30.13.1
         dns: [8.8.8.8, 8.8.4.4]
################### VM Ahsan ###################
```
- Push to your branch repository (dont push to main)
- Create merge request to main. set your reviewer to L2 and approval to TL.
- Merge request will be approve soon and vm will be created automatically.


### How to delete instance on lab7.btech.id? ###
- Clone repository
- Create your branch
- Edit file `vm.yaml` and delete your vm resource.
- Push to your branch repository (dont push to main)
- Create merge request to main. set your reviewer to L2 and approval to TL.
- Merge request will be approve soon and vm will be deleted automatically.