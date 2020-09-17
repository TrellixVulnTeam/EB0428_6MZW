# -*- coding: utf-8 -*-
"""
Create Time: 2020/3/10 17:07
Author: userzhang
"""


import json
import time
import psutil
import os, datetime
import pymysql
import datetime
import sys
import netifaces
import serial.tools.list_ports
import socket
sys.coinit_flags = 0
# import pythoncom
# import wmi
import uuid

class systemos:
    def __init__(self):
        pass
        
    def to_time(self, number):
        hour = str(int(number / 3600))
        minute = str(int(number%3600/60))
        seconds = str(round(number % 60, 3))
        return "{0}:{1}:{2}".format(hour, minute, seconds)

    def GetMemoryInfo(self):
        memory = psutil.virtual_memory()
        total_nc = round((float(memory.total) / 1024 / 1024 / 1024), 2)  # 总内存
        used_nc = round((float(memory.used) / 1024 / 1024 / 1024), 2)  # 已用内存
        free_nc = round((float(memory.free) / 1024 / 1024 / 1024), 2)  # 空闲内存
        syl_nc = round((float(memory.used) / float(memory.total) * 100), 2)  # 内存使用率
        routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
        routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
        routingIPNetmask = ''
        for interface in netifaces.interfaces():
            if interface == routingNicName:
                routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
        return {
            "total_nc": total_nc,
            "used_nc": used_nc,
            "free_nc": free_nc,
            "syl_nc": syl_nc,
            "routingGateway": routingGateway,
            "routingIPNetmask": routingIPNetmask
        }
    # 获取CPU信息
    def GetCpuInfo(self):
        cpu_times = psutil.cpu_times()
        user_time = self.to_time(cpu_times.user) +"("+ str(psutil.cpu_times_percent().user)+"%)"  # 用户使用时间及百分比 系统启动到当前时刻
        system_time = self.to_time(cpu_times.system)+"("+ str(psutil.cpu_times_percent().system)+"%)"        # 系統使用时间
        free_time = self.to_time(cpu_times.idle)+"("+ str(psutil.cpu_times_percent().idle)+"%)"    # 用户时间
        core_num= psutil.cpu_count()
        core_threads=psutil.cpu_count(logical=False)
        use_status = psutil.cpu_percent(percpu=True)
        return {
            "user_time": user_time,
            "sys_time": system_time,
            "free_time": free_time,
            "core_num": core_num,
            "core_threads": core_threads,
            "use_status": use_status
        }
#
    def GetDiskInfo(self):
        l = psutil.disk_partitions()[0:4]  # 磁盘列表
        ilen = len(l)  # 磁盘分区个数
        i = 0
        
        retlist2 = []
        while i < ilen:
            diskinfo = psutil.disk_usage(l[i].device)
            total_disk = round((float(diskinfo.total) / 1024 / 1024 / 1024), 2)  # 总大小
            used_disk = round((float(diskinfo.used) / 1024 / 1024 / 1024), 2)  # 已用大小
            free_disk = round((float(diskinfo.free) / 1024 / 1024 / 1024), 2)  # 剩余大小
            syl_disk = diskinfo.percent

            retlist1 = [i, l[i].device, total_disk, used_disk, free_disk, syl_disk]  # 序号，磁盘名称，
            retlist2.append(retlist1)
            i = i + 1
        memory = 0
        usermemory = 0
        for i in retlist2:
            memory += i[2]
            usermemory += i[3]

        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        MAC=":".join([mac[e:e + 2] for e in range(0, 11, 2)])

        # 获取本机电脑名
        myname = socket.getfqdn(socket.gethostname())
        # 获取本机ip
        myaddr = socket.gethostbyname(myname)
   
        ser = list()
        port_list = list(serial.tools.list_ports.comports())
        for i in port_list:
            if i[0] != 'COM1' and i[0] != 'COM2':
                ser.append(i[0])
                ser = ser[0]
        if ser == []:
            ser = 0
        return {
            "sys_harddisk":round((int(usermemory) / int(memory)) * 100 ,1),
            "sys_harddisk_size":round((round(memory,2)),3),
            "sys_mac": MAC,
            "sys_ip": myaddr,
            "sys_use_usb_num": int(len(list(serial.tools.list_ports.comports()))),
            "sys_com":ser
        }
        



pass