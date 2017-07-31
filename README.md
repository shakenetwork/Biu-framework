# Biu-framework 🚀
[![GitHub issues](https://img.shields.io/github/issues/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/issues)
[![GitHub forks](https://img.shields.io/github/forks/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/network)
[![GitHub stars](https://img.shields.io/github/stars/0xbug/Biu-framework.svg)](https://github.com/0xbug/Biu-framework/stargazers)
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) 
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/0xbug/Biu-framework/master/LICENSE)

> Security Scan Framework For Enterprise Intranet Based Services

[English Doc](https://github.com/0xbug/Biu-framework/blob/master/README.md) | [中文版说明文档](https://github.com/0xbug/Biu-framework/blob/master/README_zh.md)

## Dependencies

Python3.x

## INSTALL

```
pip install -r requirements.txt
```

## Usage

```
usage: biu.py [-h] [-f F] [-t T] [-r R] [-p P] [-d D] [-T T]

Biu~

optional arguments:
  -h, --help  show this help message and exit
  -f F        target file: ip\n or host\n
  -t T        target: host or ip
  -r R        ipaddress range: <ADDRESS>/<NETMASK>
  -p P        plugin: plugins to scan
  -ps PS      plugins search
  -d D        Debug
  -T T        Timeout

```
✨🍰✨Below are a series of example usages:

```
python biu.py -p elasticsearch -f target/elasticsearch.txt
python biu.py -p elastic -t 1.1.1.1:9200
python biu.py -p elastic -t 1.1.1.1
python biu.py -p elastic -r 1.1.1.0/24
python biu.py -p elastic,kibana -r 1.1.1.0/24
python biu.py -p elastic -t 1.1.1.1:9200 -d 1
```

## Quick scan with masscan 🚀

Biu-framework `-f` argument support scan results of [masscan](https://github.com/robertdavidgraham/masscan) via `-oL`

```
masscan -p9200,5601 --rate=1000 10.10.0.0/16 -oL targets.txt
python biu.py -p elasticsearch,kibana -f targets.txt

```

## Report

The scan report is in the `./reports` directory, formate: `today_pluginname.txt`

## Plugin

### Just like this 🚀

### Template
```
{
    "name":"",
    "author": "",
    "method": "GET",
    "port": [],
    "suffix":[""],
    "hits":[""],
    "document": [""]
}
```


```
{
    "name": "Cacti_default_account_authentication",
    "author": "0xbug",
    "method": "POST",
    "port": [
        80
    ],
    "suffix": [
        "/index.php",
        "/cacti/index.php"
    ],
    "headers": {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    "data": {
        "action": "login",
        "login_username": "admin",
        "login_password": "admin"
    },
    "hits": [
        "graph_view.php"
    ]
}
```



```
{
    "name": "RabbitMQManagement_guest",
    "author": "0xbug",
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



```
{
    "name": "CompressedBackupFile_undelete",
    "author": "0xbug",
    "method": "HEAD",
    "port": [
        80,
        8080
    ],
    "suffix": [
        "/web.zip",
        "/www.zip",
        "/backup.zip",
        "/old.zip",
        "/bak.zip",
        "/code.zip"
    ],
    "hit_where": "headers.Content-Type",
    "hits": [
        "application/x-zip-compressed"
    ]
}
```