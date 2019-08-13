# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/7 18:01
@file: Cor.py
"""

import psutil,time
def network():
    p = psutil
    before_recv = p.net_io_counters().bytes_recv
    before_send = p.net_io_counters().bytes_sent
    cpu_1 = psutil.virtual_memory().percent
    men_1 = psutil.cpu_percent(True)
    time.sleep(1200)
    cpu_2 = psutil.virtual_memory().percent
    men_2 = psutil.cpu_percent(True)
    time.sleep(1200)
    cpu_3 = psutil.virtual_memory().percent
    men_3 = psutil.cpu_percent(True)
    time.sleep(1200)
    # 每个小时
    cpu = ((cpu_1+cpu_2+cpu_3)/3)
    men = ((men_1+men_2+men_3)/3)
    now_recv = p.net_io_counters().bytes_recv
    now_send = p.net_io_counters().bytes_sent

    delta_send = (now_send - before_send) / 102400
    delta_recv = (now_recv - before_recv) / 102400
    return (str(cpu).split('.')[0],str(men).split('.')[0],int(delta_send),int(delta_recv))

def Cor():
    # 返回一个小时内，CPU/内存 使用率% 和使用的宽带 上传/下载量 M
    new = network()
    # 返回 ('25.7%', '2.3%', '0Mb', '0Mb')
    return (str(new[0])+'%',str(new[1])+'%',str(new[2])+'Mb',str(new[3])+'Mb')

if __name__ == '__main__':
    print('内存使用率:{}%'.format(psutil.virtual_memory().percent))
    print('CPU使用率:{}%'.format(psutil.cpu_percent(True)))
    new = network()
    print('宽带上传量:{}MB'.format(new[0]))
    print('宽带下载量:{}MB'.format(new[1]))
