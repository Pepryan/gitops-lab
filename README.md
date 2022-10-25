# lab bri
Research dan manajemen lab BRI

# DISCLAIMER
Disclaimer (updated 25-10-2022)
1. 1 ops hanya bisa membuat 1 environment, meskipun ops bisa saja punya banyak branch tetapi akan
tetap terdeteksi sebagai 1 environment pada lab7.
2. Nama VM dan IP address (harus unique) tidak boleh ada yang sama.
VM dengan nama yang sama akan terdeteksi oleh log sebagai error, nanti bisa diliat pada proses job di pipeline. 
Jika error maka harap perbaiki sendiri vm.txt lalu lakukan request ulang.
3. Ketika ada ops memakai nama VM yang sama dengan ops lain, maka terraform akan mendeteksi VM tersebut already exist, 
dan muncul error. VM dengan nama yang sudah ada (begitu pun IP address), tidak akan diproses provisioning.
4. Ketika sudah pernah buat branch sebelumnya dan sudah ada di local repository masing-masing, 
silakan simpan/ingat baik-baik file txt sebagai env. Jika ada konflik file vm.txt di repository local,
maka silakan resolve/fix sendiri dengan tetap mempertahankan config asli kepunyaan masing-masing ops.
Jika sampai ter-overwrite oleh env ops lain silakan perbaiki/revert sendiri. 
5. Gitlab menjalankan proses manajemen VM (Create, Request, Update, Delete), automation tools, dan bisa sebagai penyimpanan history,
sedangkan config env adalah kebebasan masing-masing ops, jangan sampai ada yang sama/tertukar/ter-overwrite/dsb oleh environment ops lain.
6. bagi yang mengaktifkan 2-Factor Authentication (2FA), personal access token-nya bisa buat terlebih dahulu di halaman berikut, 
lalu jika ingin melakukan push/pull sertakan token tersebut pada saat login.
https://go.btech.id/-/profile/personal_access_tokens
7. Pembuatan project (implementasi pendekatan konsep GitOps di lab BRI) ini sangat jauh dari kata sempurna. 
Semua ops Btech dipersilakan untuk berkontribusi seperti membuat fitur baru/improvement/bugfixing/dsb pada repository/labBRI ini.


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
<b>Notes: vm name must be unique.</b><br>
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
`NAME` > diisi dengan nama instance yang akan digunakan sekaligus hostname.

`KEY` > diisi dengan nama keypair yang akan digunakan instance.

`IPX` > diisi dengan Fixed / Static IP yang akan digunakan instance disesuaikan dengan network masing-masing.

`DISK{2..n}` > diisi dengan jumlah size volume secondary yang akan digunakan instance.


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
VCPUS: 4
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
VCPUS: 8
MEMORY: 8G
DISK1: 8G
DISK2: 4G
IFACE_NETWORK1: 10.10.50.0
IFACE_IP1: 10.10.50.224
IFACE_NETWORK2: 10.10.25.0
IFACE_IP2: 10.10.25.24
CONSOLE: vnc
```
2. Setelah selesai lakukan add lalu commit 
```
$ git add vm.txt
$ git commit -m "Tambah spesifikasi VM"
```

3. Lakukan push kembali 
```
$ git push
```

4. Lakukan request merge, dan tunggu approval.



### DELETE VM
1. Delete Spesifik VM

2. Delete Environment (semua VM)
