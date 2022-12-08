#!/usr/bin/env python3

# this script work to compare lab7 configs and nat.yaml
# if there is difference, nat.yaml will be applied.
# based on what forwarding port is used or not used
# NOTES: it only compare the "forwarding" port,
# no matter what destination forward is applied (at --to-destination value)

import yaml
import subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', type=str, required=True)
args = parser.parse_args()

lab7_forward_ports = []
file_forward_ports = []

def read_config(file):
    with open(file) as f:
        configs = yaml.safe_load(f)
    return configs

def get_file_ports(configs):
    for conf in configs:
        file_forward_ports.append(conf['forwarding'])
        
def get_lab7_ports():
    output = subprocess.getoutput("sudo iptables -t nat -v -L PREROUTING -n --line-number | grep DNAT | awk '{print $12}'")
    for i in output.splitlines():
        # split, then get second value at dpt:<port>
        lab7_forward_ports.append(int(i.split(':', 1)[1]))
    
# add if there are no applied configs from nat.yaml
def apply_changes(file, lab7, file_cfg):
    for port in file:
        if port in lab7:
            pass
        else:
            print(f'there are unapplied port: {port}, its entry will be added')
            e = get_nat_entry(port, file_cfg)
            subprocess.getoutput(f'sudo iptables -t nat -A PREROUTING -p tcp --dport {e["forwarding"]} -j DNAT --to-destination {e["target_ip"]}:{e["target_port"]}')
            print(f'entry: {e} successfully applied')

# delete if there are port forwarding but no more used (not listed in nat.yaml)
def delete_unlisted_lab7_port(file, lab7):
    for port in lab7:
        if port in file:
            pass
        else:
            print(f'there are unlisted entry port: {port}, its iptables entry will be deleted')
            rule_number, cmd_port = get_rule_number(port)
            subprocess.getoutput(f'sudo iptables -t nat -D PREROUTING {rule_number}')
            print(f'entry: {rule_number} with port {cmd_port} successfully deleted')

def get_nat_entry(port, configs):
    e = {}
    for entry in configs:
        if entry['forwarding'] == port:
            e['forwarding'] = entry['forwarding']
            e['target_ip'] = entry['target_ip']
            e['target_port'] = entry['target_port']
    return e

def get_rule_number(port):
    # parse to get rule number and only forwarding port value
    output = subprocess.getoutput("sudo iptables -t nat -v -L PREROUTING -n --line-number | grep DNAT | awk '{print substr($1, 1), substr($12, 5)}'")
    for e in output.splitlines():
        num, applied_port = e.split(" ", 1)
        if int(applied_port) == port:
            return num, applied_port

file_cfg = read_config(args.file)
get_file_ports(file_cfg)
get_lab7_ports()

apply_changes(file_forward_ports, lab7_forward_ports, file_cfg)
delete_unlisted_lab7_port(file_forward_ports, lab7_forward_ports)
