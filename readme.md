# 前言

LangSrcCurise资产监控系统是一套实现对指定域名进行持续性信息收集整理的自动化资产监控管理系统，基于Django开发。

趁下班休息时间抽空学了点Django，看了25小时左右文档，基础薄弱，以至于有些地方处理的很粗糙，不过会在后期慢慢完善，前端基于之前学过的的一点点Bootstrap，数据可视化基于pyecharts。

个人以为，类似于WEB服务的系统，最好的打包方案就是把所有需要的库保存在本地，每次在迁移环境和配置使用都可以非常简便，并且WEB应用依赖的第三方库有时如果更新了可能会导致不匹配，所以该项目安装环境分两种，第一种是将所有需要的库都打包在本地文件，无需再安装其他相关库，但是**这种方法只通用于windows**。第二种方法是自行安装相关库，适配Windows/Linux。

# 项目进度

目前完成后端60%功能，前端已经完成40%功能，不过核心可以开始运作，剩下的会在后期慢慢更新。

# 第一种安装方法

最好是在一个全新的环境安装

1. 安装软件  python3.6     注意必须为 3.6
2. 执行命令  python3 -m pip install django==2.1.1,或者在本地 Need_Packages 解压django后执行命令python3 setup.py install
3. Windows  安装Nmap 并添加到系统环境变量,windows安装nmap可能需要安装目录下 Need_Packages/WinPcap_4_1_3.exe 


**注意：即下方执行python3 run_tasks.py的时候，必须右键以管理员身份启动CMD，然后CMD移动路径到LangSrc资产监控目录下，然后在执行命令 python3 run_tasks.py**

# 第二种安装方法

将当前目录下的 LangSrcCuriseOnLinux 文件夹单独保存到其他目录下


## Linux 用户

依次执行以下命令：

1. sudo apt-get install python3.6
2. sudo apt-get install nmap
3. sudo python3 -m pip install -r requirement.txt

**注意：在linux下执行任何生成数据库，启动任何服务命令前都需要加上 sudo**

## Windows 用户

依次执行如下操作：

1. 安装python3.6
2. 安装nmap并添加到环境变量
3. python3 -m pip install -r requirement.txt

注意第二种安装方法可能会因为网络宽带等原因，安装相关库失败。

# 开始使用

## 初始化数据库

在 LangSrcCurise 文件夹下依次执行如下命令：

1. python3 manage.py makemigrations
2. python3 manage.py migrate
3. python3 manage.py createsuperuser # 按照提示注册生成管理员账号密码

## 初始化监控域名

编辑域名：在 initialize 文件夹 编辑 domains.list 文件

执行命令：在 initialize 文件夹 执行代码 python3 Update_Domains.py

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

1. python3 Run_Tasks.py

需要管理员权限

## 后续

如果需要删除所有的数据库，然后重新开始扫描，执行如下步骤：

1. 删除 LangSrcCurise 文件夹下方的 db.sqlite3
1. 执行命令 python3 manage.py makemigrations
2. 执行命令 python3 manage.py migrate
3. 执行命令 python3 manage.py createsuperuser # 按照提示注册生成管理员账号密码


前面步骤设置完毕后，每次如果需要启动，可以如下步骤：

启动WEB：python3 manage.py runserver 0:8888

启动扫描程序：python3 Run_Tasks.py

访问地址：http://ip:8888  前台

访问地址：http://ip:8888/lsrc

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

部署在服务器，数据可以给小弟小妹们用，给他们生成几个用户账号让他们happy。

自己使用超级管理员账号，如果只是想要简单的检索数据，在后端直接操作搜索即可，还可以导出各种格式的数据文件。

在服务器不建议开启扫描任务，开个WEB服务即可，扫描结果数据库可以本地扫后迁移到服务器，即直接复制sqlite3替换到服务即可。

