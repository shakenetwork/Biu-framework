# Biu-framework 🚀
[![GitHub issues](https://img.shields.io/github/issues/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/issues)
[![GitHub forks](https://img.shields.io/github/forks/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/network)
[![GitHub stars](https://img.shields.io/github/stars/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/stargazers)
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) 
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/0xbug/Biu-framework/master/LICENSE)

> 漏洞扫描框架

[English Doc](https://github.com/0xbug/Biu-framework/blob/master/README.md) | [中文版说明文档](https://github.com/0xbug/Biu-framework/blob/master/README_zh.md)


## 依赖

Python3.x

## 安装

```
pip install -r requirements.txt
```

## 用法

```
usage: biu.py [-h] [-f F] [-d D] [-a A]

Biu~

optional arguments:
  -h, --help  show this help message and exit
  -f F        目标文件: 每行一个ip或域名
  -d D        目标: example.com或233.233.233.233
  -a A        ip范围: 233.233.233.233/24
```

## 插件编写

### 插件格式

```
{
    "name":"", // 名字
    "method": "GET", // 发包方式
    "port": [8080], // 可能的端口
    "suffix":"", // 目标的后缀，支持list格式
    "hits":[""] // 命中规则
}
```

或者

```
{
    "name": "",
    "method": "POST",
    "port": [
        8080
    ],
    "suffix": [
        "/",
        "/maybe"
    ],
    "data": {
        "username": "admin",
        "password": "admin"
    },
    "hits": [
        "Auto-Refresh"
    ]
}
```