# lab bri
Research dan manajemen lab BRI

# Automation Terraform VM for KVM/QEMU in lab7.btech.id
### PROVISIONING VM/INSTANCE
1. Clone repository ke laptop masing-masing
```git
git clone https://go.btech.id/ops/lab-bri.git
```
2. Masuk ke folder `lab-bri`
```bash
cd lab-bri
```

3. Edit vm.txt
Sesuaikan nama VM, OS, disk, dst <br>
Isi Fixed / static ip sesuaikan dengan network yang digunakan. <br>
`Notes: vm name must be unique.`<br>
Example configuration `vm.txt` file:
```bash
[LAB]
PUBKEY1: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDKvMhH1eVLL1Ev98fuEujYqj/KIoJFrzu7vxj96Usc7qZp+W1n9kVTREjA6D63ko5RRD6QWl0k7oZhIfBy5vFJk+a/tzpVELb+bKutgoIgxtCZjyuVfIkw2sU40q3maA/kBAp4MEaupYxE4zQ9COpRev2Oqz+R6wchEl9FkAOVVZeWL1X0/lA6SG5VTf5vwj8FU7+yUcK+I8w/+rL+r/dJrPdXvKwSWsU0UnfVx4G1yroXcW0oaVYNplLK6IHxDuAyEsVkCy9ojyWuhBC39/w6ORDQJTRVp9njhil8TbT6EoruyvXDG6D62O5HahV10y0GIGzRc6xAHzzcscnBETjMLaOnRDg8qmlH+aXwTv0OfbLEtYQ6ZY16nTMAvoGIZ9kD7YscQdiKoYsF6tyYW4F1ezoJYCb67w30wRRdUByZ8k8wtF6wUwDZdjGJT7VlaH2KrEQsFVZkwi5NypXS5iyGjpjHsBRehGFfWqDIHWjN9+vJ5VpDEVc6Xb/5px+0Xjc= root@dwara

[VM1]
NAME: instance-1
OS: ubuntu-focal.img
NESTED: y
VCPUS: 4
MEMORY: 8G
DISK1: 4G
DISK2: 4G
IFACE_NETWORK1: 10.10.50.0
IFACE_IP1: 10.10.50.224
IFACE_NETWORK2: 10.10.25.0
IFACE_IP2: 10.10.25.24
CONSOLE: vnc

[VM2]
NAME: instance-2
OS: ubuntu-focal.img
NESTED: n
VCPUS: 4
MEMORY: 8G
DISK1: 4G
DISK2: 4G
IFACE_NETWORK1: 10.10.50.0
IFACE_IP1: 10.10.50.225
IFACE_NETWORK2: 10.10.25.0
IFACE_IP2: 10.10.25.25
CONSOLE: vnc
```

#### Keterangan :
`PROJECT` > diisi dengan nama project dimana instance akan dibuat.

`NAME` > diisi dengan nama instance yang akan digunakan sekaligus hostname.

`KEY` > diisi dengan nama keypair yang akan digunakan instance.

`IPX` > diisi dengan Fixed / Static IP yang akan digunakan instance disesuaikan dengan network masing-masing.

`DISK{2..n}` > diisi dengan jumlah size volume secondary yang akan digunakan instance.

ON PROGRESS

### UPDATE/EDIT VM

Contoh case ingin meng-upgrade vCPU's dari yang semula 4 core menjadi 8 core dan menambah disk1 menjadi 8GB.

1. Pada vm.txt edit apa yang ingin diubah, pada case ini ingin meng-upgrade vCPU's menjadi 8 core

```
$ nano vm.txt

Before 

[VM1]
NAME: instance-1
OS: ubuntu-focal.img
NESTED: y
VCPUS: 8
MEMORY: 8G
DISK1: 4G
DISK2: 4G
IFACE_NETWORK1: 10.10.50.0
IFACE_IP1: 10.10.50.224
IFACE_NETWORK2: 10.10.25.0
IFACE_IP2: 10.10.25.24
CONSOLE: vnc

After 

[VM1]
NAME: instance-1
OS: ubuntu-focal.img
NESTED: y
VCPUS: 
MEMORY: 8G
DISK1: 8G
DISK2: 4G
IFACE_NETWORK1: 10.10.50.0
IFACE_IP1: 10.10.50.224
IFACE_NETWORK2: 10.10.25.0
IFACE_IP2: 10.10.25.24
CONSOLE: vnc
```
2. Setelah selesai lakukan commit 
```
$ git commit -m "Tambah spesifikasi VM"
```

3. Lakukan push kembali 
```
$ git push origin main
```




### DELETE VM
.....

