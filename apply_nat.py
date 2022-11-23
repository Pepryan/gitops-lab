#!/usr/bin/env python3
import yaml
import sys
import subprocess

def read_config(file):
    with open(file) as f:
        configs = yaml.safe_load(f)
    return configs

def delete_nat():
    subprocess.getoutput("sudo iptables -t nat -v -L PREROUTING -n --line-number | grep DNAT | awk '{print $12}' | cut -d ':' -f 2 >list-nat-used.txt")
    ports = subprocess.getoutput("cat list-nat-used.txt")
    for port in ports:
        id_port = subprocess.getoutput("sudo iptables -t nat -v -L PREROUTING -n --line-number | grep DNAT | grep " + port + " | awk \'{print $1}\' | cut -d \':\' -f 2")
        subprocess.getoutput("sudo iptables -t nat -D PREROUTING " + id_port)
    pass

def create_nat(configs):
    for d in configs.values():
        command = f'sudo iptables -t nat -A PREROUTING -p tcp --dport {d["forwarding"]} -j DNAT --to-destination {d["target_ip"]}:{d["target_port"]}'
        # command_add_txt= f'echo {d["forwarding"]}|tee -a list-nat-used.txt'
        subprocess.run(command, shell=True, check=True)
        # subprocess.run(command_add_txt, shell=True, check=True)
        # print("Rules added for port : " + d["forwarding"]) 
        print("Rules added = Port " + str(d["forwarding"]) + " to " + str(d["target_ip"]) + ":" + str(d["target_port"]))
        pass

args = sys.argv
if len(args) == 2:
    delete_nat()
    create_nat(read_config(args[1]))
else:
    print("Please provide valid args")

# Documentation
# https://go.btech.id/ops/lab-bri/-/issues/3
#
