# Generated by Django 2.1.10 on 2019-08-12 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('login_username', models.CharField(max_length=16, verbose_name='登陆账号')),
                ('login_password', models.CharField(max_length=16, verbose_name='登陆密码')),
                ('login_userkey', models.CharField(max_length=16, verbose_name='登陆口令')),
                ('login_status', models.CharField(max_length=16, verbose_name='登陆状态')),
                ('login_time', models.DateTimeField(auto_now=True, verbose_name='登陆时间')),
                ('login_ip', models.CharField(max_length=16, verbose_name='登陆IP')),
            ],
            options={
                'verbose_name': '登陆日志',
                'verbose_name_plural': '登陆日志',
                'db_table': 'LoginLog',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=16, unique=True, verbose_name='用户账号')),
                ('password', models.CharField(max_length=32, verbose_name='用户密码')),
                ('userkey', models.CharField(max_length=15, verbose_name='用户口令')),
                ('last_login_ip', models.CharField(max_length=16, verbose_name='最后登陆IP')),
                ('last_login_time', models.DateTimeField(auto_now=True, verbose_name='最后登陆时间')),
                ('privileges', models.CharField(default='是', max_length=2, verbose_name='是否拥有添加资产权限')),
                ('change_time', models.DateTimeField(auto_now_add=True, verbose_name='创建用户时间')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'db_table': 'User',
            },
        ),
    ]
