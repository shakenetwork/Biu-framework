#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: orange

import argparse
import datetime
import glob
import json
from multiprocessing import Pool

import ipaddress
import requests

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
        if plugin['method'] in ['GET']:
            http = requests.get
            response = http(url, timeout=1).text
        else:
            http = requests.post
            response = http(url, timeout=2, data=plugin['data']).text
        for hit in plugin['hits']:
            if hit not in response:
                pass
            else:
                available = True
        if available:
            with open('reports/{}_result_{}.txt'.format(today,plugin['name']),
                      'a+') as result_file:
                result_file.writelines(url + '\n')
            print('\033[0;92m[+] {}\t[{}]\033[0;29m'.format(url, plugin[
                'name']))
        else:
            print('\033[0;31m[-] \033[0;29m{}'.format(url))
    except:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Biu~')
    parser.add_argument('-f', help='目标文件: 每行一个ip或域名')
    parser.add_argument('-t', help='目标: example.com或233.233.233.233')
    parser.add_argument('-r', help='ip范围: 233.233.233.0/24')
    parser.add_argument('-p', help='插件名称', default='plugins')
    args = parser.parse_args()
    plugins = []
    for plugin in glob.glob("./plugins/*.json"):
        if args.p.lower() in plugin.lower():
            plugins.append(plugin)
    p = Pool(10)
    if args.f:
        targets_file = args.f
        with open(targets_file, 'r') as f:
            for target in f.readlines():
                target = target.strip('\n').strip('\t').strip(' ')
                if '://' in target:
                    target = target.split('://')[1].split('/')[0]
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
