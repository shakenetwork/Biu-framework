# Biu-framework 🚀
[![GitHub issues](https://img.shields.io/github/issues/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/issues)
[![GitHub forks](https://img.shields.io/github/forks/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/network)
[![GitHub stars](https://img.shields.io/github/stars/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/stargazers)
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) 
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/0xbug/Biu-framework/master/LICENSE)


[English Doc](https://github.com/0xbug/Biu-framework/blob/master/README.md) | [中文版说明文档](https://github.com/0xbug/Biu-framework/blob/master/README_zh.md)

## Dependencies

Python3.x

## INSTALL

```
pip install -r requirements.txt
```

## Usage

```
usage: biu.py [-h] [-f F] [-t T] [-r R] [-p P]

Biu~

optional arguments:
  -h, --help  show this help message and exit
  -f F        target file: ip\n or host\n
  -t T        target: host or ip
  -r R        ipaddress range: <ADDRESS>/<NETMASK>
  -p P        plugin: plugins to scan
```

## Plugin

### Just like this 🚀

```
{
    "name":"",
    "method": "GET",
    "port": [8080],
    "suffix":"",
    "hits":[""]
}
```
OR

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

OR

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