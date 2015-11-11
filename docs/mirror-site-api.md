API
===

##Schema
1. 数据返回格式统一使用 `json`
2. HTTP Method: `GET`
3. 时间格式: yyyy-MM-dd HH:mm:ss
4. 返回值为单个对象:


```
{
    "count": 10,
    "targets": []
}
```

参数说明:

|参数|意义|备注|
|----|----|----|
|count|对象个数||
|targets|对象列表||


##获取镜像列表
```
GET    /api/mirrors/list
```

返回列表中对象:
```
{
    "name": "archlinux",
    "fullname": "Arch Linux",
    "url": "http://b.mirrors.lanunion.org/archlinux",
    "help": "http://mirrors.cqu.edu.cn/wiki?page=archlinux",
    "comment": "",
    "last_sync": "2015-08-11 12:40:00",
    "size": "120G",
    "status": 200,
    "message": ""
}
```

参数说明:

|参数|意义|备注|
|----|----|----|
|name||应仅包含 [a-z] 和 -|
|fullname|显示名字|参见镜像官方|
|url|镜像链接|现需完整 url|
|help|镜像使用帮助链接|现链接到相应 wiki 页|
|comment|镜像备注|新镜像标注 new, 没有则为空|
|last_sync|最后同步时间||
|size|镜像大小||
|status|镜像更新状态|具体代码含义参加下表|
|message|根据 status 给出相应信息, 没有则为空||

`status` 状态说明:

|状态码|含义|备注|
|----|----|----|
|100|Syncing|正在更新|
|200|Success|更新成功|
|300|Freeze|镜像冻结|
|400|Failed|更新失败|
|500|Unknown|状态不明|



##获取镜像更新状态
用于前端轮询来刷新镜像列表中镜像更新状态
```
GET    /api/mirrors/status
```

返回列表中的对象:
```
{
    "name": "archlinux",
    "last_sync": "2015-08-21 12:42:20",
    "size": "120G",
    "status": 100,
    "message": ""
}
```

##获取镜像站公告
```
GET    /api/mirrors/notices
```

返回列表中的对象:
```
{
    "created_at": "2015-08-21 01:02:00",
    "notice": "镜像站添了点东西",
    "level": "normal"
}
```

##获取快速获取中的操作系统列表
```
GET    /api/mirrors/oses
```

返回列表中的对象:
```
{
    "name": "archlinux",
    "fullname": "Arch Linux",
    "url": "http://b.mirrors.lanunion.org/archlinux",
    "type": "os",
    "count": 3,
    "versions": [{"version": "2015.08.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.08.01/archlinux-2015.08.01-dual.iso"},
                 {"version": "2015.07.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso"},
                 {"version": "2015.06.01", "url": "http://b.mirrors.lanunion.org/archlinux/iso/2015.07.01/archlinux-2015.07.01-dual.iso"}]
}
```

##获取快速获取中的软件列表
```
GET    /api/mirrors/osses
```

返回列表中的对象:
```
{
    "name": "tomcat",
    "fullname": "Apache Tomcat",
    "url": "http://mirrors.cqu.edu.cn/apache",
    "type": "oss",
    "count": 3,
    "versions": [{"version": "8.0", "url": "http://mirrors.cqu.edu.cn/apache/tomcat/tomcat-8/"},
                 {"version": "7.0", "url": "http://mirrors.cqu.edu.cn/apache/tomcat/tomcat-7/"},
                 {"version": "6.0", "url": "http://mirrors.cqu.edu.cn/apache/tomcat/tomcat-6/"}]
}
```
