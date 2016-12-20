# Biu-framework

## Usage

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

```json
{
    "name":"", //名字
    "method": "GET", //发包方式
    "suffix":"", // 目标的后缀
    "hits":[""] // 命中规则
}
```