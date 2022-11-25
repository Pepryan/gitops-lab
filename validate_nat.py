#!/usr/bin/env python3
import yaml
import sys

def read_config(file):
    ports = []
    with open(file) as f:
        dictionary_data = yaml.safe_load(f)
    for d in dictionary_data.values():
        ports.append(str(d['forwarding']))
    return ports

def read_used_nat(file):
    with open(file) as f:
        ports = [line.rstrip('\n') for line in f]
    return ports

def compare(forwards, used):
    for port in forwards:
        if port in used:
            sys.exit(f'Port {port} is used, please use another port number')
    print('Validate OK')

args = sys.argv
if len(args) == 3:
    list_used_nat = read_used_nat(args[1]) # argument list_nat_used.txt
    list_forwarding = read_config(args[2]) # argument konfigurasi_nat.yaml
    compare(list_forwarding, list_used_nat)
else:
    print("Please provide valid args")
