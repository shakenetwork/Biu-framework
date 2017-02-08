# Biu-framework 🚀
[![GitHub issues](https://img.shields.io/github/issues/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/issues)
[![GitHub forks](https://img.shields.io/github/forks/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/network)
[![GitHub stars](https://img.shields.io/github/stars/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/stargazers)
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) 
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/0xbug/Biu-framework/master/LICENSE)

> 企业内网基础服务安全扫描框架

[English Doc](https://github.com/0xbug/Biu-framework/blob/master/README.md) | [中文版说明文档](https://github.com/0xbug/Biu-framework/blob/master/README_zh.md)


## 依赖

Python3.x

## 安装

```
pip install -r requirements.txt
```

## 用法

```
usage: biu.py [-h] [-f F] [-t T] [-r R] [-p P] [-ps PS] [-d D] [-T T]

Biu~

optional arguments:
  -h, --help  show this help message and exit
  -f F        目标文件: 每行一个ip或域名
  -t T        目标: example.com或233.233.233.233
  -r R        ip范围: 233.233.233.0/24
  -p P        插件名称
  -ps PS      插件搜索
  -d D        Debug
  -T T        超时时间

```

✨🍰✨支持扫描方式:

```
python biu.py -p elasticsearch -f target/elasticsearch.txt
python biu.py -p elastic -t 1.1.1.1:9200
python biu.py -p elastic -t 1.1.1.1
python biu.py -p elastic -r 1.1.1.0/24
python biu.py -p elastic,kibana -r 1.1.1.0/24
python biu.py -p elastic -t 1.1.1.1:9200 -d 1
```

## 快速扫描 🚀

Biu-framework `-f` 参数支持 [masscan](https://github.com/robertdavidgraham/masscan) 结果文件(`-oL`)

```
masscan -p9200,5601 --rate=1000 10.10.0.0/16 -oL targets.txt
python biu.py -p elasticsearch,kibana -f targets.txt
```
## 扫描结果

扫描结果保存在 `./reports` 目录下，格式: `2017.01.01_插件名称.txt`

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
        "success"
    ]
}
```

或者

```
{
    "name": "RabbitMQManagement_guest",
    "method": "AUTH",
    "port": [
        80,
        8080
    ],
    "suffix": [
        "/api/whoami"
    ],
    "data": [
        {
            "user": "guest",
            "pass": "guest"
        }
    ],
    "hits": [
        "\"tags\":\"administrator\""
    ]
}

```