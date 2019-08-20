# coding:utf-8
# from celery import Celery,platforms

import time
from core.Subdomain_Baidu import Baidu
from core.Subdomain_Brute import Brute
from core.Subdomain_Crawl import Crawl
from core.Subdomain_Api import Api
from core.Url_Info import Get_Url_Info
from core.Host_Info import Get_Ip_Info,Get_Alive_Url
from core.Cor import Cor
import pymysql
import random
import socket
import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Other_Url,IP,URL,Show_Data,Error_Log,Cpu_Min,Domains,Setting,Content
from django.db import connections
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from multiprocessing import Pool
import threading
import multiprocessing

#Sem = multiprocessing.Manager().BoundedSemaphore(1)

def Except_Log(stat,url,error):
    print('错误代码 [{}] {}'.format(stat,str(error)))
    try:
        Error_Log.objects.create(url=url, error='错误代码 [{}] {}'.format(stat,str(error)))
    except:
        close_old_connections()
        Error_Log.objects.create(url=url, error='错误代码 [{}] {}'.format(stat,str(error)))

def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


Set = Setting.objects.all()[0]
pool_count = int(Set.Pool)
Alive_Status = eval(Set.Alive_Code)

BA = Domains.objects.all()
ALL_DOMAINS = [x.get('url') for x in BA.values()]




def Run_Cpu_Min():
    while 1:
        c = Cor()
        cpu, men, new_send, new_recv = c[0], c[1], c[2], c[3]
        try:
            Cpu_Min.objects.create(cpu=cpu,menory=men,network_send=new_send,network_recv=new_recv)
        except Exception as e:
            close_old_connections()
            Cpu_Min.objects.create(cpu=cpu,menory=men,network_send=new_send,network_recv=new_recv)
            Except_Log(stat=16,url='资源监控消耗',error=str(e))
#
# def on_done(future):
#     # 因为每一个线程都有一个 connections，所以这里可以调用 close_all()，把本线程名下的所有连接关闭。
#     connections.close_all()

def get_host(url):
    url = url.split('//')[1]
    if ':' in url:
        url = url.split(':')[0]
    try:
        s = socket.gethostbyname(url)
        return s
    except Exception as e:
        time.sleep(2)
        try:
            s = socket.gethostbyname(url)
            return s
        except Exception as e:
            Except_Log(stat=24, url=url+'|获取IP失败', error=str(e))
            return '获取失败'



def Add_Data_To_Url(url):
    time.sleep(random.randint(5,20))
    time.sleep(random.randint(5,20))
    time.sleep(random.randint(5,20))
    close_old_connections()
    try:
        ip = get_host(url)
        if ip == '获取失败':
            return
        # print('[+ Domain UrlIP] IP解析 --> {}  IP --> {}'.format(url, ip))
       #  Sem.acquire()
        try:
            test_url = list(URL.objects.filter(url=url))
        except:
            try:
                test_url = list(URL.objects.filter(url=url))
            except:
                close_old_connections()
                test_url = list(URL.objects.filter(url=url))

        # Sem.release()
        # 如果数据库有这个网站的话，就直接退出
        if test_url != []:
            return

        try:
            Test_Other_Url = Other_Url.objects.filter(url=url)
            # 判断网络资产表是否有这个数据，如果没有的话，就添加进去
            if list(Test_Other_Url) == []:
                res = Get_Url_Info(url).get_info()
                res_url = res.get('url')
                try:
                    res_title = pymysql.escape_string(res.get('title'))
                except Exception as e:
                    res_title = 'Error'
                    Except_Log(stat=11, url=url + '|网页内容转码失败', error=str(e))
                res_power = res.get('power')
                res_server = res.get('server')
                res_status = res.get('status')
                res_ip = ip
                try:
                    Other_Url.objects.create(url=res_url, title=res_title, power=res_power, server=res_server,status=res_status,ip=res_ip)
                except Exception as e:
                    close_old_connections()
                    Except_Log(stat=17, url=url + '|标题等信息编码不符合', error=str(e))
                    Other_Url.objects.create(url=res_url, title='Error', power='Error', server=res_server,status=res_status,ip=res_ip)
        except Exception as e:
            Except_Log(stat=29, url=url + '|网络资产表错误', error=str(e))
        try:
            # res = Get_Url_Info(url).get_info()
            # res_status = res.get('status')
            # 再次获取状态码，判断是否符合入库状态，以保证数据统一
            # if int(res_status) not in Alive_Status:
            #     return

            # 接下来可以进行数据索引唯一统一
            '''
            这里添加网址资产到 索引表 和 清洗表
            '''
            test_url1 = list(URL.objects.filter(url=url))
            # 如果数据库有这个网站的话，就直接退出

            if test_url1 == []:
                URL.objects.create(url=url,ip=ip)
                # 添加 网址索引
                try:
                    try:
                        Show_contents = pymysql.escape_string(Get_Url_Info(url).Requests()[0])
                        Cont = Content()
                        Cont.url = url
                        Cont.content = Show_contents
                        IP_Res = Get_Ip_Info(ip)
                        Show_cs = IP_Res.get_cs_name(ip)
                        Cont.save()
                        Show_Data.objects.create(url=url, ip=ip,cs=Show_cs, content=Cont)
                    except Exception as e:
                        close_old_connections()
                        Except_Log(stat=4, url=url + '|外键添加错误', error=str(e))
                        Show_contents = 'Error'
                        Cont = Content()
                        Cont.url = url
                        Cont.content = Show_contents
                        IP_Res = Get_Ip_Info(ip)
                        Show_cs = IP_Res.get_cs_name(ip)
                        Cont.save()
                        Show_Data.objects.create(url=url, ip=ip,cs=Show_cs, content=Cont)
                    # 添加网页内容，数据展示
                except Exception as e:
                    Except_Log(stat=8, url=url + '|外键添加错误', error=str(e))

                This_Sub = [x for x in ALL_DOMAINS if x in url]
                # 获取到当前子域名属于的主域名
            try:
                # 尝试进行域名总数据获取检测
                if This_Sub != []:
                        Domain_Count = Domains.objects.filter(url=This_Sub[0])[0]
                        counts = Other_Url.objects.filter(url__contains=This_Sub[0])
                        Domain_Count.counts = str(len(counts))
                        # counts = int(Domain_Count.counts)+1
                        # Domain_Count.counts = counts
                        Domain_Count.save()
            except Exception as e:
                Except_Log(stat=15, url=url +'|获取归属域名失败|'+This_Sub, error=str(e))
        except Exception as e:
            Except_Log(stat=22, url=url + '|添加到网址索引表失败|', error=str(e))


        try:
            test_ip = list(IP.objects.filter(ip=ip))
        except:
            close_old_connections()
            test_ip = list(IP.objects.filter(ip=ip))
        # 开始添加ip 维护ip统一
        # 这里开始判断数据库中是否有这个ip，并且先添加然后修改(防止重复浪费资源)
        # if test_ip != []:
        #     test_ip_0 = IP.objects.filter(ip=ip)[0]
        #     # 这里判断数据中IP时候存在，如果存在并且有扫描状态，就直接中断操作
        #     if test_ip_0.get == '是' or test_ip_0.get == '中':
        #         return
        if test_ip ==[]:
            try:
                IP_Res = Get_Ip_Info(ip)
                area = IP_Res.get_ip_address(ip)
                cs_name = IP_Res.get_cs_name(ip)
                try:
                    IP.objects.create(ip=ip, servers='None', host_type='None', cs=cs_name,alive_urls='None', area=area)
                    # 这里先添加数据，异步执行获取到的数据作为结果给下个进程使用
                    # 这里本来是要扫描c段开放端口，但是这样就相当于把耗时操作加载到同步执行的线程中
                    # 于是把扫描开放端口  放在获取ip详细信息线程中处理
                except:
                    Except_Log(stat=86, url=url + '|转换IP地区编码失败|', error=str(e))
                    IP.objects.create(ip=ip, servers='None', host_type='None', cs=cs_name,alive_urls='None', area='获取失败')

            except Exception as e:
                Except_Log(stat=21, url=url + '|添加IP资源失败|', error=str(e))

    except Exception as e:
        Except_Log(stat=30, url=url + '|维护传入网址失败|', error=str(e))




def Change_IP_Info():
        time.sleep(random.randint(1,20))
        time.sleep(random.randint(1,20))
        time.sleep(random.randint(1,20))

        # 首先捕获一个值，设置为扫描中状态，但是要确保是事务
        try:
            target_ip = IP.objects.filter(get='否')[0]
            ip = target_ip.ip
            target_ip.get = '中'
            # 为了防止重复获取同一个数值，这里进行修改
            # 但是有时候 数据没有正常跑出来 设置成 【是】 会导致偏差
            target_ip.save()
        except Exception as e:
            Except_Log(stat=19, url='|扫描IP资产并设置扫描状态失败|', error='数据库暂无可供扫描IP数据')
            time.sleep(360)
            # 等待并充实一次
            return

        try:
            print('[+ Host Scaner] 当前扫描主机 : {}'.format(ip))
            IP_Res = Get_Ip_Info(ip)
            servers = IP_Res.get_server_from_nmap(ip)
            # 服务与端口  字典类型
            open_port = servers.keys()
            check_alive_url = []
            for port in open_port:
                check_alive_url.append('http://{}:{}'.format(ip, port))
                check_alive_url.append('https://{}:{}'.format(ip, port))
            alive_url = Get_Alive_Url(check_alive_url)
            # 该IP上存活WEB，类型为列表，内容为多个字典
            host_type = IP_Res.get_host_type(ip)
            # windows/linux
            area = IP_Res.get_ip_address(ip)
            # 返回地址
            cs = IP_Res.get_cs_name(ip)

            IP_Obj_ip = ip
            IP_Obj_servers = str(servers)
            IP_Obj_host_type = host_type
            IP_Obj_alive_urls = str(alive_url)
            IP_Obj_area = area
            IP_Obj_cs = cs
            IP_Obj_get = '是'
            try:
                IP_Obj = IP.objects.filter(ip=ip)[0]
                IP_Obj.ip = IP_Obj_ip
                IP_Obj.host_type = IP_Obj_host_type
                IP_Obj.alive_urls = IP_Obj_alive_urls
                IP_Obj.servers = IP_Obj_servers
                IP_Obj.area = IP_Obj_area
                IP_Obj.cs = IP_Obj_cs
                IP_Obj.get = IP_Obj_get
                IP_Obj.save()
            except:
                # 这里重试的原因是有可能因为失去链接导致无法保存
                # 但是扫描ip是耗时操作，获取的数据不能轻易的舍弃，重试一次
                close_old_connections()
                IP_Obj = IP.objects.filter(ip=ip)[0]
                IP_Obj.ip = IP_Obj_ip
                IP_Obj.host_type = IP_Obj_host_type
                IP_Obj.alive_urls = IP_Obj_alive_urls
                IP_Obj.servers = IP_Obj_servers
                IP_Obj.area = IP_Obj_area
                IP_Obj.cs = IP_Obj_cs
                IP_Obj.get = IP_Obj_get
                IP_Obj.save()
        except Exception as e:
            Except_Log(stat=28, url=ip+'|清洗 IP 资产失败|', error=str(e))
            # 这里如果失败，则回退
            close_old_connections()
            IP_Obj_f = IP.objects.filter(ip=ip)[0]
            IP_Obj_f.get = '否'
            IP_Obj_f.save()
        '''
        下面的代码，是获取ip的c段存活主机，然后加载到扫描计划中，老夫先注释了
        '''
        # try:
        #     cs_ips = [str(x) for x in list(IP_Res.get_cs_ips(ip).values())[0]]
        #     cs_name = cs
        #     # 整个 C 段的数据ip
        #
        #     if ip in cs_ips:
        #         cs_ips.remove(ip)
        #
        #     Read_to_check_host = set()
        #     for cs_ip in cs_ips:
        #         indata = list(IP.objects.filter(ip=str(cs_ip)))
        #         if indata == [] and cs_ip != ip:
        #             Read_to_check_host.add(cs_ip)
        #
        #     Alive_Hosts = IP_Res.get_alive_hosts(Read_to_check_host)
        #     print('[+ CHost Scaner] {} 段存活主机 : {}台'.format(cs_name, len(Alive_Hosts)))
        #     if Alive_Hosts == []:
        #         return
        #     for alive_host in Alive_Hosts:
        #         try:
        #             checkindata = list(IP.objects.filter(ip=str(alive_host)))
        #             if checkindata == []:
        #                 # 最后一次数据判断校验
        #                 c_ip = str(alive_host)
        #                 c_cs = cs_name
        #                 c_area = IP_Res.get_ip_address(c_ip)
        #                 IP.objects.create(ip=c_ip, servers='None', host_type='None', cs=c_cs, alive_urls='None',
        #                                   area=c_area)
        #         except Exception as e:
        #             print('错误代码 [03] {}'.format(str(e)))
        #             Error_Log.objects.create(url=ip, error='错误代码 [03] {}'.format(str(e)))
        #
        # except Exception as e:
        #     print('错误代码 [38] {}'.format(str(e)))
        #     Error_Log.objects.create(url='获取 IP 失败', error='错误代码 [38] {}'.format(str(e)))



def Change_ShowData_Info(Sub_Domains):
    while 1:
        time.sleep(random.randint(1, 20))
        time.sleep(random.randint(1, 20))
        time.sleep(random.randint(1, 20))
        # 线程同步
        try:
            target_info = Show_Data.objects.filter(success='否')[0]
            ip = target_info.ip
            url = target_info.url
            Data_IP = IP.objects.filter(ip=ip)[0]
            if Data_IP.get == '否' or Data_IP.get == '中':
                # 如果收集整理的数据还没有获取完成,但是一定要保证扫描IP线程数据库连接安全
                time.sleep(300)
                return
            else:
                target_info.get = '中'
                target_info.save()
        except Exception as e:
            Except_Log(stat=35, url='|清洗数据并设置扫描状态失败|', error='数据库暂无可清洗数据')
            time.sleep(300)
            # 等待并充实一次
            return
        print('[+ DataInfo Collection] 数据整理清洗 : {} --> {}'.format(url,ip))

        try:
            Data_IP = IP.objects.filter(ip=ip)[0]
            try:
                Data_URL = Other_Url.objects.filter(url=url)[0]
                Show_title = Data_URL.title
                Show_power = Data_URL.power
                Show_server = Data_URL.server
                # 该网站使用的web容器
                Show_status = Data_URL.status
            except Exception as e:
                Show_title = 'None'
                Show_power = 'None'
                Show_server = 'None'
                # 该网站使用的web容器
                Show_status = '404'
                Except_Log(stat=12, url=url + '|清洗数据流程获取数据失败|', error=str(e))

            Show_servers = Data_IP.servers
            # 开放的端口和服务，字典类型
            Show_alive_urls = Data_IP.alive_urls
            # 旁站
            Show_host_type = Data_IP.host_type
            Show_area = Data_IP.area
            Show_cs = Data_IP.cs
            # IP_Res = Get_Ip_Info(ip)
            # Show_cs = IP_Res.get_cs_name(ip)

            Show_belong_domain = [x for x in Sub_Domains if x in url]
            if Show_belong_domain == []:
                Show_belong_domain = 'None'
            else:
                Show_belong_domain = Show_belong_domain[0]
            Show_success = '是'
            # 可以设置为获取成功

            ShowS_DataD = Show_Data.objects.filter(url=url)[0]
            ShowS_DataD.title = Show_title
            ShowS_DataD.power = Show_power
            ShowS_DataD.server = Show_server
            ShowS_DataD.status = Show_status
            # ShowS_DataD.content = Cont
            ShowS_DataD.servers = Show_servers
            ShowS_DataD.cs = Show_cs
            ShowS_DataD.alive_urls = Show_alive_urls
            ShowS_DataD.host_type = Show_host_type
            ShowS_DataD.area = Show_area
            ShowS_DataD.belong_domain = Show_belong_domain
            ShowS_DataD.success = Show_success
            ShowS_DataD.save()
        except Exception as e:
            Except_Log(stat=43, url=url + '|'+ip+'|清洗数据流程获取数据失败|', error=str(e))
            close_old_connections()
            ShowS_DataD_f = Show_Data.objects.filter(url=url)[0]
            ShowS_DataD_f.success = '否'
            ShowS_DataD_f.save()
# def Run_Baidu(url):
#     # 这里对传入Baidu进行重写，该函数接受一个参数域名，返回参数对应的网址，列表格式
#





def Run_Crawl(Domains):
    Domains = ['.'+str(x) for x in Domains]
    time.sleep(random.randint(1, 20))
    time.sleep(random.randint(1, 20))
    time.sleep(random.randint(1, 20))
    try:
        target_url = URL.objects.filter(get='否')[0]
        url = target_url.url
        target_url.get = '是'
        target_url.save()
        # 这里需要提前设置的原因是，防止下一个进程启动重复 使用 同一个数据
    except Exception as e:
        time.sleep(300)
        Except_Log(stat=31, url='|获取URL并设置扫描状态失败|', error='数据库暂无可供爬行网址数据')
        # 在获取失败（数据库没数据存入），重试一次
        return

    try:
        All_Urls = Crawl(url)
        if All_Urls == []:
            return
        All_Urls = set(All_Urls)
        Other_Domains = []
        if list(All_Urls) != [] and All_Urls != None:
            try:
                Sub_Domains1 = set([y for x in Domains for y in All_Urls if x in y])
                if list(Sub_Domains1) != []:
                    with ThreadPoolExecutor(max_workers=pool_count) as pool1:
                        result = pool1.map(Add_Data_To_Url, list(Sub_Domains1))
                Other_Domains = list(All_Urls-Sub_Domains1)
            except Exception as e:
                Except_Log(stat=11, url='|获取URL失败|', error=str(e))

            if Other_Domains != [] and Other_Domains != None:
                try:
                    for urle in Other_Domains:
                        try:
                            try:
                                Test_Other_Url = list(Other_Url.objects.filter(url=urle))
                            except:
                                close_old_connections()
                                Test_Other_Url = list(Other_Url.objects.filter(url=urle))
                            if Test_Other_Url == []:
                                ip = get_host(urle)
                                res = Get_Url_Info(urle).get_info()
                                res_url = res.get('url')
                                try:
                                    res_title = pymysql.escape_string(res.get('title'))
                                except:
                                    res_title = 'Error'
                                res_power = res.get('power')
                                res_server = res.get('server')
                                status = res.get('status')
                                res_ip = ip
                                #if int(status) in Alive_Status:
                                try:
                                    Other_Url.objects.create(url=res_url, title=res_title, power=res_power, server=res_server,status=status,ip=res_ip)
                                except Exception as e:
                                    Except_Log(stat=33, url=url+'|资产爬行错误|', error=str(e))
                                    close_old_connections()
                                    Other_Url.objects.create(url=res_url, title='Error', power=res_power, server=res_server,status=status,ip=res_ip)
                        except Exception as e:
                            Except_Log(stat=37, url=url + '|资产爬行错误|', error=str(e))
                except Exception as e:
                    Except_Log(stat=36, url=url + '|资产爬行错误|', error=str(e))
    except Exception as e:
        Except_Log(stat=32, url=url + '|网址爬行错误|', error=str(e))


def Heartbeat():
    while 1:
        try:
            heartcheck = list(URL.objects.all())
            if heartcheck == []:
                time.sleep(60)
            else:
                time.sleep(3)
            # 维持 3 S 发送一次心跳包检测连接，如果失败则清洗连接
        except:
            print('[+ HeartBeat] 维持心跳包失败，清洗失败链接')
            close_old_connections()



def Sub_Api(Sub_Domains):
    while 1:
        res = []
        for sub_domain in Sub_Domains:
            res = Api(sub_domain)
            if res != [] and res != None:
                with ThreadPoolExecutor(max_workers=pool_count) as pool4:
                    result = pool4.map(Add_Data_To_Url, list(set(res)))
            time.sleep(60)
            # 每次扫完一个域名等待一小会儿
        time.sleep(3600 * 36)

def Sub_Baidu(Sub_Domains):
    while 1:
        close_old_connections()
        res = []
        for sub_domain in Sub_Domains:
            res = Baidu(sub_domain)
            if res != []:
                with ThreadPoolExecutor(max_workers=pool_count) as pool3:
                    result = pool3.map(Add_Data_To_Url, list(set(res)))
            time.sleep(60)
            # 每次扫完一个域名等待一小会儿
        time.sleep(3600*12)

def Sub_Brute(Sub_Domains):
    while 1:
        for domain in Sub_Domains:
            res = []
            Br = Brute(domain)
            res = Br.start()
            res = list(set(res))
            if res != []:
                with ThreadPoolExecutor(max_workers=pool_count) as pool4:
                    result = pool4.map(Add_Data_To_Url, res)
            # 每爆破一个子域名，歇会儿
            time.sleep(60)
        time.sleep(3600*24)



def Start_Crawl_Run(Sub_Domains):
    while 1:
        Run_Crawl(Sub_Domains)
def Start_ChangeIp_Run():
    while 1:
        Change_IP_Info()
def Start_ChangeInf_Run(Sub_Domains):
    while 1:
        Change_ShowData_Info(Sub_Domains)



def Sub_Crawl(pax,Sub_Domains):
    p = Pool(processes=pool_count)
    for i in range(pool_count):
        p.apply_async(Start_Crawl_Run,args=(Sub_Domains,))
    p.close()
    p.join()
def Sub_ChangeIp(pax):
    p0 = Pool(processes=pool_count)
    for i in range(pool_count):
        p0.apply_async(Start_ChangeIp_Run)
    p0.close()
    p0.join()

def Sub_ChangeInf(Sub_Domains):
    p2 = Pool(processes=pool_count)
    for i in range(pool_count):
        p2.apply_async(Start_ChangeInf_Run,args=(Sub_Domains,))
    p2.close()
    p2.join()



if __name__ == '__main__':
    pass
    #Domains = list(set([x.strip() for x in open('domains.list', 'r', encoding='utf-8').readlines()]))
    Domains = ['baidu.com','qq.com','jd.com','iqiyi.com','kuaishou.com','sina.com']
    res = Sub_Brute(Domains)

    # Sub_Baidu(Domains)
    # Sub_Crawl(range(20),Domains)