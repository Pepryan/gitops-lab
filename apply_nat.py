#!/usr/bin/env python3
import yaml
import sys
import subprocess

def read_config(file):
    with open(file) as f:
        configs = yaml.safe_load(f)
    return configs

def create_nat(configs):
    for d in configs.values():
        command = f'sudo iptables -t nat -A PREROUTING -p tcp --dport {d["forwarding"]} -j DNAT --to-destination {d["target_ip"]}:{d["target_port"]}'
        command_add_txt= f'echo {d["forwarding"]}|tee -a list-nat-used.txt'
        subprocess.run(command, shell=True, check=True)
        subprocess.run(command_add_txt, shell=True, check=True)
        pass

args = sys.argv
if len(args) == 2:
    create_nat(read_config(args[1]))
else:
    print("Please provide valid args")

# Documentation
# https://go.btech.id/ops/lab-bri/-/issues/3
#
