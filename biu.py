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

GREEN = '\033[0;92m{}\033[0;29m'
RED = '\033[0;31m{}\033[0;29m'


class HandleTarget(object):
    def __init__(self, plugins, target=None, iprange=None, targets_file=None):
        self.plugins = plugins
        self.targets = []
        self.tasks = []
        if target:
            if '://' in target:
                self.targets.append(target.split('://')[1].split('/')[0])
            else:
                self.targets.append(target)
        if targets_file:
            self.targets_file = targets_file
            self.handlefile()
        if iprange:
            self.iprange = iprange
            self.hendleiprange()
        if self.targets:
            self.generate_url()

    def handlefile(self):
        with open(self.targets_file, 'r') as f:
            content = f.readlines()
            if 'masscan' in content[0]:
                for target in content[1:-1]:
                    ipport = target.split(' ')[2:4]
                    ipport.reverse()
                    self.targets.append(':'.join(ipport))
            else:
                for target in content:
                    target = target.strip('\n').strip('\t').strip(' ')
                    if '://' in target:
                        target = target.split('://')[1].split('/')[0]
                        self.targets.append(target)
                    else:
                        self.targets.append(target)

    def hendleiprange(self):
        for target in ipaddress.IPv4Network(self.iprange, strict=False):
            self.targets.append(str(target))

    def generate_url(self):
        for target in self.targets:
            for plugin in self.plugins:
                with open(plugin) as f:
                    plugin = json.load(f)
                if ':' in target:
                    self.add_suffix(
                        target.split(':')[0], target.split(':')[1], plugin)
                elif plugin['port'] == [80]:
                    self.add_suffix(target, 80, plugin)
                else:
                    for port in plugin['port']:
                        self.add_suffix(target, port, plugin)

    def add_suffix(self, target, port, plugin):
        for suffix in plugin['suffix']:
            self.tasks.append(
                {'url': 'http://{}:{}{}'.format(target, port, suffix), 'plugin': plugin})


class Aduit(object):
    def __init__(self, url, plugin, timeout=3, debug=0):
        self.url = url
        self.plugin = plugin
        self.vulnerable = False
        self.timeout = timeout
        self.debug = debug
        self.TOO_LONG = 2097152
        self.run()
        self.result = {'vulnerable':self.vulnerable,'url':self.url,'plugin':self.plugin.get('name')}

    def run(self):
        try:
            if self.plugin.get('method') in ['AUTH']:
                self.audit_auth()
            elif self.plugin.get('method') in ['GET', 'HEAD']:
                self.audit_gethead()
            elif self.plugin.get('method') in ['POST']:
                self.audit_post()
            self.stdout()
            if self.vulnerable:
                self.savereport()
        except Exception as e:
            print(e)
            pass

    def audit_auth(self):
        for data in self.plugin.get('data'):
            self.vulnerable = False
            self.response = request(self.plugin.get('method'), self.url, timeout=self.timeout,
                                    auth=(data['user'], data['pass']))
            if 'hits' not in self.plugin.keys():
                response_code = self.response.status_code
                if response_code not in [401, 403, 404]:
                    self.vulnerable = True
                    print(
                        '\033[0;92m[+] {}\t[{}--{}]\033[0;29m'.format(self.url, self.plugin.get('name'), data))
                    self.content = data + '\t' + self.url + '\n'

    def audit_gethead(self):
        try:
            self.response = request(self.plugin.get('method'), self.url, timeout=self.timeout,
                                    headers=self.plugin.get('headers'), stream=True)
        except:
            self.response = request(self.plugin.get('method'), self.url, verify=True, timeout=self.timeout,
                                    headers=self.plugin.get('headers'), stream=True)
        if self.response.headers.get('content-length'):
            if int(self.response.headers.get('content-length')) < self.TOO_LONG:
                content = self.response.content

    def audit_post(self):
        if self.plugin.get('headers') == {"Content-Type": "application/json"}:
            self.response = request(self.plugin.get('method'), self.url, timeout=self.timeout, data=json.dumps(
                self.plugin.get('data')), headers=self.plugin.get('headers'))
        else:
            self.response = request(self.plugin.get('method'), self.url, timeout=self.timeout, data=self.plugin.get(
                'data'), headers=self.plugin.get('headers'))

    def hit_where(self):
        if self.plugin.get('hit_where'):
            where = self.plugin.get('hit_where')
            if 'headers' in where:
                return self.response.headers.get(where.split('.')[-1])
        else:
            return self.response.text

    def savereport(self):
        if not os.path.exists('reports'):
            os.mkdir('reports')
        TODAY = str(datetime.datetime.today()).split(' ')[0].replace('-', '.')
        reportpath = 'reports/{}_{}.txt'.format(TODAY, self.plugin.get('name'))
        with open(reportpath, 'a+') as result_file:
            if self.content in result_file.readlines():
                return
            else:
                result_file.writelines(self.content)

    def stdout(self):
        if self.debug:
            if self.response.status_code not in [403, 404]:
                pprint(self.response.text)
                pprint(self.response.headers)
        if 'hits' in self.plugin.keys():
            for hit in self.plugin['hits']:
                if hit in self.hit_where():
                    self.vulnerable = True
                    print(
                        '\033[0;92m[+] {}\t[{}]\033[0;29m'.format(self.url, self.plugin.get('name')))
                    self.content = self.url + '\n'
        if not self.vulnerable:
            print('\033[0;31m[-] \033[0;29m{}'.format(self.url))


class BiuPlugin(object):
    def __init__(self, searchstr):
        self.plugin_path = './plugins/*.json'
        self.plugins = []
        self.searchstr = searchstr
        self.plugin_search()

    def plugin_search(self):
        for plugin in glob.glob(self.plugin_path):
            for p in self.searchstr.lower().split(','):
                if p in plugin.lower():
                    self.plugins.append(plugin)


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
    if args.ps:
        searchstr = args.ps
        plugins = BiuPlugin(searchstr=searchstr).plugins
        print(GREEN.format('Total:{}\n{}'.format(
            len(plugins), [p.split('/')[2] for p in plugins])))
        exit(0)
    searchstr = args.p
    plugins = BiuPlugin(searchstr=searchstr).plugins
    targets_file = args.f
    iprange = args.r
    target = args.t
    debug = int(args.d)
    timeout = int(args.T)
    targets = HandleTarget(plugins=plugins, target=target,
                           iprange=iprange, targets_file=targets_file)
    try:
        p = Pool(100)
        for task in targets.tasks:
            p.apply_async(Aduit, args=(task.get('url'),
                                       task.get('plugin'), timeout, debug))
        p.close()
        p.join()
    except KeyboardInterrupt as e:
        exit(0)
