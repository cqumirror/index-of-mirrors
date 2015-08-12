CQU Mirror Site back-end
===

##About back-end api
1. 数据返回格式统一使用 `json`
2. HTTP Method: `GET`
3. 返回值为单个对象:


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


####获取镜像列表
```
GET    /api/mirrors/list
```

返回列表中对象:
```
{
    "id": "archlinux",
    "name": "Arch Linux",
    "alt": "http://mirrors.cqu.edu.cn/archlinux",
    "help": "http://mirrors.cqu.edu.cn/wiki?page=archlinux",
    "comment": "",
    "last_update": "2015-08-11 12:40:00",
    "status": 200,
    "errmsg": ""
}
```

参数说明:

|参数|意义|备注|
|----|----|----|
|id||应仅包含 [a-z] 和 \_|
|name|显示名字|参见镜像官方|
|alt|镜像链接|现需完整 url|
|help|镜像使用帮助链接|现链接到相应 wiki 页|
|comment|镜像备注|新镜像标注 new, 没有则为空|
|last_update|最后更新时间||
|status|镜像更新状态|具体代码含义参加下表|
|errmsg|根据 status 给出相应信息, 没有则为空||

`status` 状态说明:

|状态码|含义|备注|
|100|Syncing|正在更新|
|200|Success|更新成功|
|300|Freeze|镜像冻结|
|400|Unknown|更新失败|


####获取镜像更新状态
用于前端轮询来刷新镜像列表中镜像更新状态
```
GET    /api/mirrors/status
```

返回列表中的对象:
```
{
    "id": "archlinux",
    "last_update": "2015-08-21 12:42:20",
    "status": 100,
    "errmsg": ""
}
```

####获取镜像站公告
```
GET    /api/mirrors/notice
```

返回列表中的对象:
```
{
    "created_at": "2015-08-21 01:02:00",
    "notice": "镜像站添了点东西"
}
```
