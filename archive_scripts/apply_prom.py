#!/usr/bin/env python3
import yaml
import argparse
import subprocess
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', type=str, required=True)
parser.add_argument('-fp','--file_prome', type=str, required=True)
args = parser.parse_args()

def read_config(file):
    with open(file) as f:
        configs = yaml.safe_load(f)
    return configs

def get_ip_vm(configs):
    ip_vm = []
    for vm in configs['spec']:
        # get only the first interface network defined
        ip_vm.append(vm['networks'][0]['address'].split("/", 1)[0])
    return ip_vm

def add_port_9100(ip_vm):
    added = []
    for ip in ip_vm:
        added.append(f'{ip}:9100')
    return added

def replace_all_targets(configs, ip_vm):
    for job in configs['scrape_configs']:
        if job['job_name'] == 'instances':
            # clear entry
            job['static_configs'][0]['targets'].clear()
            # apply new entry
            job['static_configs'][0]['targets'].extend(add_port_9100(ip_vm))
    return configs

def write_config(final_config):
    with open(args.file_prome, 'w') as fp:
        yaml.dump(final_config, fp)

ip_vm = get_ip_vm(read_config(args.file))
prome_conf = read_config(args.file_prome)
final_config = replace_all_targets(prome_conf, ip_vm)
write_config(final_config)
subprocess.getoutput("curl -X POST localhost:9090/-/reload")
