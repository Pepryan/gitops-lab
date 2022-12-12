#!/usr/bin/env python3
# https://go.btech.id/ops/lab-bri/-/issues/9
# https://go.btech.id/ops/lab-bri/-/issues/1

import yaml
import argparse
import subprocess
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', type=str, required=True)
parser.add_argument('-k','--key', type=str, required=True)
args = parser.parse_args()

def read_ip(file):
    with open(file) as f:
        ip_vm = []
        vm_counter = 0
        datas = yaml.safe_load(f)
        # print(datas)
        vms = datas['spec']
        for vm in vms:
            ip_vm_subnet = datas['spec'][vm_counter]['networks'][0]['address']
            ip_vm.append(ip_vm_subnet.split('/', 1)[0])
            print(ip_vm)
            vm_counter += 1
    return ip_vm

def scp_and_install(iface1s, key):
    for iface1 in iface1s:
        print(f'============= ssh-keyscan to {iface1} =============\n')
        cmdkeygen = f'ssh-keygen -f "/home/gitlab-runner/.ssh/known_hosts" -R {iface1}'
        # check=True: raise exit code when command failed
        subprocess.run(cmdkeygen, shell=True)

        cmdkeyscan = f'ssh-keyscan -H {iface1} >> /home/gitlab-runner/.ssh/known_hosts'
        subprocess.run(cmdkeyscan, shell=True)

        print(f'============= Checking node exporter availability at {iface1} =============\n')
        cmd = f"ssh -i dwara.pem -l root 10.30.13.171 'if [ -e /usr/local/bin/node_exporter ]; then echo \"available\"; else echo \"unavailable\"; fi'"
        output = subprocess.getoutput(cmd)

        if output == "available":
            print(f'============= Node exporter at {iface1} is available, skipping installation =============\n')
        else:
            print(f'============= Sending node exporter package to {iface1} =============\n')
            cmdscp = f'scp -i {key} /home/gitlab-runner/environment/node_exporter.tar.gz root@{iface1}:/tmp'
            subprocess.run(cmdscp, shell=True, check=True)

            print(f'============= Sending script install to {iface1} =============\n')
            cmdcd = f'cd /home/gitlab-runner/environment/scripts'
            subprocess.run(cmdcd, shell=True, check=True)
            cmdnode = f'scp -i {key} install_node_exporter.sh root@{iface1}:/root'
            subprocess.run(cmdnode, shell=True, check=True)

            print(f'============= Running script install at {iface1} =============\n')
            cmdnd = f'ssh -i {key} -l root {iface1} "./install_node_exporter.sh"'
            subprocess.run(cmdnd, shell=True, check=True)    

ip_vm = read_ip(args.file)
scp_and_install(ip_vm, args.key)
