# coding:utf-8
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
from app.models import IP
i = IP()
i.ip = '118.24.11.2'
i.servers = '666'
i.host_type = '111'
i.alive_urls = '123'
i.area ='1132'
i.save()