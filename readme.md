# 前言

LangSrcCurise资产监控系统是一套实现对指定域名进行持续性信息收集整理的自动化资产监控管理系统，基于Django开发。


# 项目进度

目前完成后端60%功能，前端已经完成45%功能，不过核心可以开始运作，剩下的会在后期慢慢更新。

# 需要环境

1. python==3.6
2. mysql==8.0
3. nmap==7.8
4. django==2.1.1

# 安装环境

## Linux 用户

**在linux无法完美兼容**

依次执行以下命令：

1. sudo apt-get install python3.6
2. sudo apt-get install nmap
3. sudo python3 -m pip install -r requirement.txt
4. 安装MySQL8.0，步骤较多，自行百度

**注意：在linux下执行任何生成数据库，启动任何服务命令前都需要加上 sudo**


## Windows 用户

依次执行如下操作：

1. 安装python3.6
2. 安装nmap并添加到环境变量
3. python3 -m pip install -r requirement.txt
4. 建议安装最新版phpstudy，自带MySQL8.0


# 开始使用

## 开启mysql服务

1. 第一步先开启mysql服务，并且允许用户连接
2. 设置MySQL最大连接数为128，最大可插入数据为32M

## 配置数据库信息

在主目录下的 config.ini 文件中修改相关mysql登陆信息

	[Server]
	host = 127.0.0.1 # mysql登陆的ip，linux下设置为localhost
	port = 3306		# mysql 端口
	username = root
	password = root
	dbname = LangSrcCurise # 你要是用的数据库名字，数据库自动创建


## 初始化数据库

在 LangSrcCurise 文件夹下依次执行如下命令：

1. python3 manage.py makemigrations
2. python3 manage.py migrate
3. python3 manage.py createsuperuser # 按照提示注册生成管理员账号密码

## 初始化监控域名

编辑域名：在 initialize 文件夹 编辑 domains.list 文件

执行命令：在 主目录 LangSrcCurise 文件夹下依次执行如下命令：

1. python3 manage.py initial

完成将监控域名初始化到数据库


## 配置网址过滤黑名单

	Auxiliary/Black_Url.list

其下的网址都会被自动过滤，请勿修改文件名

## 配置子域名爆破字典

	Auxiliary/SubDomainDict.list

请勿修改文件名

## 启动服务

在 LangSrcCurise 文件夹下依次执行如下命令：

1. python3 manage.py runserver 0:8888


## 添加用户

添加的用户可以在前端获取数据，并且能够在前端添加查询数据

访问网址：http://127.0.0.1:8888/lsrc/

![](/static/image/20190811211936.png)

可供选项：

**是否拥有添加资产权限：是/否**

如果设置成否，则该账号无法在前端添加资产数据。

## 扫描设置

设置扫描策略，线程数进程数以及运行入库状态码

![](/static/image/20190811212243.png)

这张表只能存在一列数据，其中配置方案名称随便填写，允许入库状态码即该网址返回的状态码，如果符合这个表的内容，则保存到数据库，实际上是一个过滤规则，注意其中的数据格式参考python的列表，并且是英文输入法下的,和[]。

比如：

	配置方案：随便取个名字
	允许入库状态码：[200,301,302,404]
	

因为数据任务都是同时在跑，所以比较吃资源，建议线程等数量都设置在4或者以下

## 开启扫描

在 LangSrcCurise 文件夹下依次执行如下命令：

1. python3 manage.py startscan

需要管理员权限

## 后续

如果需要删除所有的数据库，然后重新开始扫描，执行如下步骤：

1. 直接在数据库中删除，或者在config.ini将数据库名修改成一个新的名字
1. 执行命令 python3 manage.py makemigrations
2. 执行命令 python3 manage.py migrate
3. 执行命令 python3 manage.py createsuperuser # 按照提示注册生成管理员账号密码


前面步骤设置完毕后，每次如果需要启动，可以如下步骤：

启动mysql：sudo service mysql start

启动WEB：python3 manage.py runserver 0:8888

启动扫描程序：python3 manage.py startscan

访问地址：http://ip:8888  前台

访问地址：http://ip:8888/lsrc  后台管理

# 前端-快速入门

## 登陆

![](/static/image/20190811212820.png)

这里登陆的账号密码口令是上文中生成的用户

## 查看

![](/static/image/20190811212729.png)

右上角负责添加资产，前提是该账户拥有权限

右边则是数据搜索，返回的数据结果如下，可以查看详细情况

![](/static/image/20190811213203.png)

## 标识

![](/static/image/20190811213313.png)

这里的数据可以进行标识，设置为已经进行渗透测试。

红色的说明已经手动进行过测试

![](/static/image/20190811214312.png)

# 后端-快速入门

## 主机端口表

主机端口表存储监控域名对应的IP开放服务信息

![](/static/image/20190809223353.png)

## 资源消耗表

定期检测历史资源消耗，每个小时盯控一次

![](/static/image/20190809223429.png)

## 网络资产表

网络资产表存储所有的网址(不仅仅是监控域名内)

![](/static/image/20190809223109.png)

可以用来做资产管理，搜索标题/网页关键词等信息

## 监控域名表

监控表负责监控域名

![](/static/image/20190809222638.png)

主要数据是主域名

## 网址索引表

网址索引表负责对所有监控域名网址做数据统一

![](/static/image/20190809223507.png)

# 监控流程

通过导入的监控域名表，持续循环执行如下任务：

1. 通过  baidu          进行子域名采集
2. 通过  bing           进行子域名采集
3. 通过  sougou         进行子域名采集
4. 通过  ssl证书         进行子域名采集
5. 通过  子域名爆破       进行子域名采集
6. 通过  对资产网址爬行   进行子域名采集
7. 通过  域名服务器      进行端口扫描，服务探测
8. 通过  域名服务器      进行探测是否部署web服务
9. 通过  域名服务器      进行其他数据清洗管理



# 演示案例

	http://www.langzi.fun:8888

	test/test/123456

# 总结

部署在服务器，数据可以给小弟小妹们用，给他们生成几个用户账号。

**不建议使用服务器扫描资产**

自己使用超级管理员账号，如果只是想要简单的检索数据，在后端直接操作搜索即可，还可以导出各种格式的数据文件。

在服务器不建议开启扫描任务，开个WEB服务即可，扫描结果数据库可以本地扫后迁移到服务器.

# 历史版本

当前版本使用的数据库为mysql8.0，以后更新将长期使用MySQL8.0版本，如需使用本地数据库sqlite3，可以下载

[最后一个sqlite3版本 不在维护](https://github.com/LangziFun/LangSrcCurise/tree/41d2848b7c59ea0e97e94e38618abd61a7cbaea4)


[最后一个免安装相关库版本 不在维护](https://github.com/LangziFun/LangSrcCurise/tree/00bc66c5e763b88136a5f3d187ffc1190e0ffeba)
