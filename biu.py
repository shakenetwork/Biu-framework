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
from requests import request

TODAY = str(datetime.datetime.today()).split(' ')[0].replace('-', '.')
GREEN = '\033[0;92m{}\033[0;29m'
RED = '\033[0;31m{}\033[0;29m'
TOO_LONG = 2097152
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
    for suffix in plugin['suffix']:
        urls.append('http://{}:{}{}'.format(target, port, suffix))


def audit_auth(url, plugin):
    for data in plugin.get('data'):
        vulnerable = False
        response = request(plugin.get('method'), url, timeout=timeout,
                           auth=(data['user'], data['pass']))
        if 'hits' not in plugin.keys():
            response_code = response.status_code
            if response_code not in [401, 403, 404]:
                vulnerable = True
                print(
                    '\033[0;92m[+] {}\t[{}--{}]\033[0;29m'.format(url, plugin['name'], data))
                content = data + '\t' + url + '\n'
                savereport(plugin, content)
        return response, vulnerable


def audit_gethead(url, plugin):
    response = request(plugin.get('method'), url, timeout=timeout,
                       headers=plugin.get('headers'), stream=True)
    if int(response.headers['content-length']) < TOO_LONG:
        content = response.content
    return response


def audit_post(url, plugin):
    if plugin.get('headers') == {"Content-Type": "application/json"}:
        response = request(plugin.get('method'), url, timeout=timeout, data=json.dumps(
            plugin.get('data')), headers=plugin.get('headers'))
    else:
        response = request(plugin.get('method'), url, timeout=timeout, data=plugin.get(
            'data'), headers=plugin.get('headers'))
    return response


def audit(url, plugin):
    try:
        vulnerable = False
        if plugin['method'] in ['AUTH']:
            response, vulnerable = audit_auth(url, plugin)
        elif plugin['method'] in ['GET', 'HEAD']:
            response = audit_gethead(url, plugin)
        elif plugin['method'] in ['POST']:
            response = audit_post(url, plugin)
        if debug:
            if response.status_code not in [403, 404]:
                pprint(response.text)
        if 'hits' in plugin.keys():
            for hit in plugin['hits']:
                if hit in hit_where(response, plugin):
                    vulnerable = True
                    print(
                        '\033[0;92m[+] {}\t[{}]\033[0;29m'.format(url, plugin['name']))
                    content = url + '\n'
                    savereport(plugin, content)

        if not vulnerable:
            print('\033[0;31m[-] \033[0;29m{}'.format(url))
    except:
        pass


def hit_where(response, plugin):
    if plugin.get('hit_where'):
        where = plugin.get('hit_where')
        if 'headers' in where:
            return response.headers.get(where.split('.')[-1])
    else:
        return response.text


def savereport(plugin, content):
    reportpath = 'reports/{}_{}.txt'.format(TODAY, plugin['name'])
    if not os.path.exists(reportpath):
        with open(reportpath, 'a+') as result_file:
            result_file.writelines(content)
            return
    with open(reportpath, 'r') as result_file:
        if content in result_file.readlines():
            return
    with open(reportpath, 'a+') as result_file:
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


def plugin_search():
    plugins = []
    for plugin in glob.glob("./plugins/*.json"):
        for p in args.p.lower().split(','):
            if p in plugin.lower():
                plugins.append(plugin)
    return plugins


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Biu~')
    parser.add_argument('-f', help='目标文件: 每行一个ip或域名')
    parser.add_argument('-t', help='目标: example.com或233.233.233.233')
    parser.add_argument('-r', help='ip范围: 233.233.233.0/24')
    parser.add_argument('-p', help='插件名称', default='plugins')
    parser.add_argument('-ps', help='插件搜索')
    parser.add_argument('-d', help='Debug', default=0)
    parser.add_argument('-T', help='超时时间', default=3)
    args = parser.parse_args()
    debug = args.d
    timeout = int(args.T)
    if not os.path.exists('reports'):
        os.mkdir('reports')
    if args.ps:
        args.p = args.ps
        plugins = plugin_search()
        print(GREEN.format('Total:{}\n{}'.format(
            len(plugins), [p.split('/')[2] for p in plugins])))
        exit(0)
    plugins = plugin_search()
    p = Pool(100)
    if args.f:
        targets_file = args.f
        tagets = handlefile(targets_file)
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
