#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: orange

import argparse
import datetime
import glob
import json
import os
from multiprocessing import Pool
from pprint import pprint
import ipaddress
import requests
from requests.auth import HTTPBasicAuth

today = str(datetime.datetime.today()).split(' ')[0].replace('-', '.')
targets = []


def generate_url(target):
    if target in targets:
        return
    else:
        targets.append(target)
    for plugin in plugins:
        urls = []
        with open(plugin) as f:
            plugin = json.load(f)
        if ':' in target:
            add_suffix(
                target.split(':')[0], target.split(':')[1], plugin, urls)
        elif plugin['port'] == [80]:
            add_suffix(target, 80, plugin, urls)
        else:
            for port in plugin['port']:
                add_suffix(target, port, plugin, urls)
        for url in urls:
            audit(url, plugin)

def add_suffix(target, port, plugin, urls):
    if type(plugin['suffix']) == list:
        for suffix in plugin['suffix']:
            urls.append('http://{}:{}{}'.format(target, port, suffix))
    else:
        urls.append('http://{}:{}{}'.format(target, port, plugin['suffix']))


def audit(url, plugin):
    try:
        available = False
        if plugin['method'] in ['AUTH']:
            http = requests.get
            for data in plugin['data']:
                reqresult = http(url, timeout=timeout,auth=(data['user'],data['pass']))
                if 'hits' in plugin.keys():
                    response = reqresult.text
                else:
                    httpcode = reqresult.status_code
                    if httpcode != 401:
                        available = True
                        print('\033[0;92m[+] {}\t[{}--{}]\033[0;29m'.format(url, plugin['name'],data))
                        content = data + '\t' + url + '\n'
                        savereport(plugin,content)
        elif plugin['method'] in ['GET']:
            http = requests.get
            response = http(url, timeout=timeout).text
        else:
            http = requests.post
            if 'headers' in plugin.keys():
                if plugin['headers'] == {"Content-Type": "application/json"}:
                    response = http(url, timeout=timeout, data=json.dumps(plugin['data']), headers=plugin['headers']).text
                else:
                    response = http(url, timeout=timeout, data=plugin['data'], headers=plugin['headers']).text
            else:
                response = http(url, timeout=timeout, data=plugin['data']).text
        if debug:
            pprint(response)
        if 'hits' in plugin.keys():
            for hit in plugin['hits']:
                if hit not in response:
                    pass
                else:
                    available = True
                    print('\033[0;92m[+] {}\t[{}]\033[0;29m'.format(url, plugin['name'])
                    content = url + '\n'
                    savereport(plugin,content)

        if not available:
            print('\033[0;31m[-] \033[0;29m{}'.format(url))
    except:
        pass

def savereport(plugin,content):
    reportpath = 'reports/{}_result_{}.txt'.format(today,plugin['name'])
    if not os.path.exists(reportpath):
        with open(reportpath,'a+') as result_file:
            result_file.writelines(content)
            return
    with open(reportpath,'r') as result_file:
        if content in result_file.readlines():
            return
    with open(reportpath,'a+') as result_file:
        result_file.writelines(content)

def handlefile(targets_file):
    targets = []
    with open(targets_file, 'r') as f:
        content = f.readlines()
        if 'masscan' in content[0]:
                for target in content[1:-1]:
                    ipport = target.split(' ')[2:4]
                    ipport.reverse()
                    targets.append(':'.join(ipport))
        else:
            for target in content:
                target = target.strip('\n').strip('\t').strip(' ')
                if '://' in target:
                    target = target.split('://')[1].split('/')[0]
                    targets.append(target)
                else:
                    targets.append(target)
    return targets

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Biu~')
    parser.add_argument('-f', help='目标文件: 每行一个ip或域名')
    parser.add_argument('-t', help='目标: example.com或233.233.233.233')
    parser.add_argument('-r', help='ip范围: 233.233.233.0/24')
    parser.add_argument('-p', help='插件名称', default='plugins')
    parser.add_argument('-d', help='Debug', default=0)
    parser.add_argument('-T', help='超时时间', default=3)
    args = parser.parse_args()
    debug = args.d
    timeout = args.T
    plugins = []
    if not os.path.exists('reports'):
        os.system('mkdir reports')
    for plugin in glob.glob("./plugins/*.json"):
        for p in args.p.lower().split(','):
            if p in plugin.lower():
                plugins.append(plugin)
    p = Pool(100)
    if args.f:
        targets_file = args.f
        tagets =  handlefile(targets_file)
        for target in tagets:
            p.apply_async(generate_url, (target, ))
        p.close()
        p.join()
    elif args.t:
        if '://' in args.t:
            args.t = args.t.split('://')[1].split('/')[0]
        generate_url(args.t)
    elif args.r:
        for target in ipaddress.IPv4Network(args.r):
            p.apply_async(generate_url, (str(target), ))
        p.close()
        p.join()
    else:
        pass
