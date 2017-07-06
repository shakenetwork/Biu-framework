### Just like this 🚀

### Template
```
{
    "name":"",
    "method": "GET",
    "port": [],
    "suffix":[""],
    "hits":[""]
}
```


```
{
    "name": "Cacti_default_account_authentication",
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