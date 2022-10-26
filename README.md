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
1. Clone repository ke laptop masing-masing (hanya dilakukan saat pertama kali buat, jika sudah pernah lanjut ke step berikutnya)
```bash
git clone https://go.btech.id/ops/lab-bri.git
```
2. Masuk ke folder `lab-bri`
```bash
cd lab-bri
```

3. Edit vm.txt
Sesuaikan nama VM, OS, disk, dst <br>
Isi Fixed / static ip sesuaikan dengan network yang digunakan. <br>
<b>Notes: Nama VM harus unik</b><br>
<b>Notes: Nama VM harus berupa huruf(aA-zZ), angka(0-9), underscrore(_), dan dash (-)</b><br>
<b>Notes: Agar tidak terjadi kesalahan saat pembuatan ada baiknya nama vm format berikut:{inisial nama}-{nama-instance}
contoh: al-centos7</b><br>
Example configuration `vm.txt` file:
```yml
[LAB]
PUBKEY1: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDKvMhH1eVLL1Ev98fuEujYqj/KIoJFrzu7vxj96Usc7qZp+W1n9kVTREjA6D63ko5RRD6QWl0k7oZhIfBy5vFJk+a/tzpVELb+bKutgoIgxtCZjyuVfIkw2sU40q3maA/kBAp4MEaupYxE4zQ9COpRev2Oqz+R6wchEl9FkAOVVZeWL1X0/lA6SG5VTf5vwj8FU7+yUcK+I8w/+rL+r/dJrPdXvKwSWsU0UnfVx4G1yroXcW0oaVYNplLK6IHxDuAyEsVkCy9ojyWuhBC39/w6ORDQJTRVp9njhil8TbT6EoruyvXDG6D62O5HahV10y0GIGzRc6xAHzzcscnBETjMLaOnRDg8qmlH+aXwTv0OfbLEtYQ6ZY16nTMAvoGIZ9kD7YscQdiKoYsF6tyYW4F1ezoJYCb67w30wRRdUByZ8k8wtF6wUwDZdjGJT7VlaH2KrEQsFVZkwi5NypXS5iyGjpjHsBRehGFfWqDIHWjN9+vJ5VpDEVc6Xb/5px+0Xjc= root@dwara

[VM1]
NAME: {inisial nama}-{nama-instance}
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
NAME: {inisial nama}-{nama-instance}
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
`NAME` > diisi dengan nama VM/instance yang akan digunakan sekaligus hostname.

`OS` > Isi dengan iso OS yang akan digunakan.

`NESTED` > Nested virtualization. Isi `y` jika nantinya VM/Instance digunakan untuk virtualisasi di dalamnya. Isi `n` jika tidak.

`PUBKEYX` > diisi dengan nama keypair yang akan digunakan VM/instance.

`IFACE_NETWORK1` > diisi dengan Network yang akan digunakan VM/instance disesuaikan dengan network masing-masing.

`IFACE_IPX` > diisi dengan Fixed / Static IP yang akan digunakan instance disesuaikan dengan network masing-masing.

`DISK{2..n}` > diisi dengan jumlah size volume secondary yang akan digunakan VM/instance.

`CONSOLE` > isi dengan `vnc`


### UPDATE/EDIT VM

Contoh case ingin meng-upgrade vCPU's dari yang semula 4 core menjadi 8 core dan menambah disk1 menjadi 8GB.

1. Pada vm.txt edit apa yang ingin diubah, pada case ini ingin meng-upgrade vCPU's menjadi 8 core

```yml
$ nano vm.txt

Before 

[VM1]
NAME: {inisial nama}-{nama-instance}
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
NAME: {inisial nama}-{nama-instance}
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
```bash
$ git add vm.txt
$ git commit -m "Tambah spesifikasi VM"
```

3. Lakukan push kembali 
```bash
$ git push
```
### MERGE REQUEST (MRs)
1. Baik itu provisioning ataupun update VM silakan untuk melakukan request merge, dan tunggu approval.
Bisa lewat dashboard atau pilih link ketika sudah push.
![firefox_25-10-2022_074534](/uploads/e216ea6c778052fda42055215861a946/firefox_25-10-2022_074534.png)
<br>Atau<br>
![Code_25-10-2022_074520](/uploads/a9108e8909f572a43f255847f4bc02d2/Code_25-10-2022_074520.png)<br>
Jangan checklist delete branch<br>
![image](/uploads/e149a846637f1cb31d176b6d9c1915ad/image.png)

2. Contoh request menunggu approval
![firefox_24-10-2022_114806](/uploads/1c494275493dbd1072d268a410af1664/firefox_24-10-2022_114806.png)

#### Merge Conflict

Jika terjadi merge conflict:
1. Bisa pilih **Resolve Conflict** lalu cek kembali text yang diubah sudah benar atau belum.
![firefox_26-10-2022_130334](/uploads/910406fadf627d7bf435372a558323b8/firefox_26-10-2022_130334.png)
2. Lalu pilih **use ours** agar file vm.txt di branch main berubah dan bisa menjalankan provisioning/update. 
![firefox_26-10-2022_130404](/uploads/0dd729cbfd528dcfd971e7930c405ce1/firefox_26-10-2022_130404.png)
![firefox_26-10-2022_130407](/uploads/6b261a8c1b676c046bb2fe70cc5f42be/firefox_26-10-2022_130407.png)
3. Berikan keterangan, lalu pilih **Commit to Source Branch**. Contoh:
![firefox_26-10-2022_130515](/uploads/26122974fe01f6e8ed2c3528ae48049b/firefox_26-10-2022_130515.png)

### DELETE VM
1. Jika ingin Delete Spesifik VM<br>
Edit vm.txt (nano vm.txt)
```yml
[VM1]
NAME: {inisial nama}-{nama-instance}
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
NAME: {inisial nama}-{nama-instance}
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

**After**
```yml
[VM1]
NAME: {inisial nama}-{nama-instance}
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
```

2. Jika ingin Delete Environment (semua VM)<br>
Pilih Job-Destroy pada pipeline, tekan tombol play.<br>
![image](/uploads/b93fa92bd00e79bad1c2bec6891889fd/image.png)