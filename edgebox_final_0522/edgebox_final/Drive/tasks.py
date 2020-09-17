#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 17:46
# @Author  : userzhang
import hashlib
import json
import shutil
import threading
import time
import struct
import psutil
from django.db.models import F
from modbus_tk import modbus_rtu, modbus_tcp
import requests
import serial

from plugins.canis_etl_hex2dc_csv import etl_hex2dc_csv
from plugins.daq_sdk import *

from celery.task import Task
import django
from django_redis import get_redis_connection
from django.db import connection
from paho.mqtt import publish
import serial.tools.list_ports

# from plugins.mqtt_pub_sub import mqtt_client_connect

django.setup()
from Log.models import get_subdevicelog_model
from remotely.models import get_settingdown_model

from Device.models import get_subdevicedata_model, get_smartdevicedata_model
from plugins.mqtt_pub_sub import mqtt_client_connect as client
import pymysql
from scipy import signal
import time
from functions import func


class DB():
    def __init__(self, host='localhost', port=3306, db='', user='root', passwd='123456', charset='utf8'):
        # 建立连接
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标，操作设置为字典类型
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()


class DriveScanfM5(Task):
    name = "DriveScanfM5"
    conn = get_redis_connection("default")

    def run(self, *arg, **kwargs):
        '''
        :param arg:
        :param kwargs:
        :return:
        # 定時掃描任務
        '''
        m5_key = "m5_*"
        redis_com_list = {"COM1", "COM2", }  # COM1 COM2 為自帶外置RS232串口
        # s搜索缓存所有可用的端口号
        m5s = self.conn.keys(m5_key)
        try:
            # 有可能在遍历m5_devices时 设备就已经拔掉 rasie KeyError
            for m5 in m5s:
                b_info = self.conn.hgetall(m5.decode())
                info = {}
                for i, value in b_info.items():
                    info[i.decode()] = value.decode("utf-8")
                # 添加至redis_com_list 集合中
                redis_com_list.add(info["com"])
        except Exception as e:
            print(str(e) + " 設備連接異常中斷!")
        # time.sleep(3)
        print("redis_com_list" + str(redis_com_list))
        self.scanfPort(redis_com_list)

    def recv(self, ser):
        while True:
            data = ser.read_all()
            if data == "":
                continue
            else:
                break
            # time.sleep(0.02)
        return data

        # 扫描有回指令的端口号

    def scanfPort(self, redis_com_list):
        portList = list(serial.tools.list_ports.comports())
        for i in portList:
            try:
                if i[0] not in redis_com_list:
                    # 判断未曾确认的端口 已经打开的端口 语句会报错
                    with serial.Serial(i[0], baudrate=9600, timeout=3) as ser:
                        if ser.isOpen():
                            print(i[0] + " is open success ")
                            # 发送握手信息
                            ser.write("REMOTE INFORMATION\r".encode())  # 查看遠程信息 身份信息 轉發信息
                            # json_str = ser.readline().decode("gb2312").strip("\r\n")
                            json_str = ser.readline().decode().strip("\r\n")
                            json_str = ser.readline().decode().strip("\r\n")
                            print("head: ", json_str)

                            if self.is_json(json_str):
                                # 确认符合
                                head = json.loads(json_str)
                                # 握手成功！！！
                                print(i[0] + " 握手成功！！！")

                                self.cache(head, i[0])  # 保存到 Redis

                                ser.write("SMART DEVICE DATA\r".encode())  # 获取智能硬件采集的数据一直发送（2秒间隔），直到接收到其他指令才停止
                                json_str = ser.readline().decode().strip("\r\n")
                                json_str = ser.readline().decode().strip("\r\n")
                                print("data: " + json_str)
                                mythread = threading.Thread(target=self.m5_open_write,
                                                            args=(i[0], 9600, head["smartDevice_name"]))
                                mythread.setDaemon(True)
                                mythread.start()

                    print(i[0] + " is close ")

                else:
                    print("no found ")
                    time.sleep(1)
            except Exception as e:
                print(i[0] + " is open fail " + str(e))
                time.sleep(1)

    def cache(self, head, com):
        m5device_name = head["smartDevice_name"]
        m5device_type = head["smartDevice_type"]
        m5device_com = com
        m5device_botelv = "9600"
        m5device_remark = head["smartDevice_remark"]
        m5device_forward = head["smartDevice_forward"]
        m5s = self.conn.keys("m5_*")
        self.no = 'm5_0' + str(len(m5s) + 1) + "_%s"

        # redis_com_list.append(i[0])
        # 握手成功 添加在redis 中
        self.conn.hset(self.no % m5device_name, "name", m5device_name)
        self.conn.hset(self.no % m5device_name, "In", m5device_type)
        self.conn.hset(self.no % m5device_name, "com", m5device_com)
        self.conn.hset(self.no % m5device_name, "botelv", m5device_botelv)
        time_local = time.localtime(int(time.time()))
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        self.conn.hset(self.no % m5device_name, "create_time", dt)
        self.conn.hset(self.no % m5device_name, "Out", [i["smartDevicePath_type"] for i in m5device_forward])
        self.conn.hset(self.no % m5device_name, "remark", m5device_remark)
        self.conn.hset(self.no % m5device_name, "device_enable", 1)
        self.conn.hset(self.no % m5device_name, "path_index", 0)

        for index, path in enumerate(m5device_forward):
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_name",
                           path["smartDevicePath_name"])
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_type",
                           path["smartDevicePath_type"])
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_host", path["smartDevicePath_ip"])
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_port",
                           path["smartDevicePath_port"])
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_username",
                           path["smartDevicePath_user"])
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_pwd",
                           path["smartDevicePath_pwd"])
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_topic",
                           path["smartDevicePath_topic"])
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_remark",
                           path["smartDevicePath_remark"])
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_createtime", dt)

            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_enable", 1)  # 默认启用
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_count", 0)  # 计数
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_index", 0)  #
            status = {
                "status_code": "1",
                "message": "路徑未開啟！"
            }
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_status", json.dumps(status))  # 状态
            self.conn.hset("m5path_%s_%d" % (m5device_name, index + 1), "path_msg", '{"init":"初始化數據"}')  # 状态
        DriveForTransmit.apply_async(kwargs={"subdevice_name": self.no % m5device_name}, queue="worker_queue")

    def m5_open_write(self, com, botelv, device):
        time.sleep(0.5)
        try:
            cls = self.createtable(device)
            # 1. 打开端口
            with serial.Serial(com, baudrate=botelv, timeout=3) as ser:
                a = b = 0
                while ser.isOpen():
                    time.sleep(.1)
                    if int(self.conn.hget(self.no % device, "device_enable")) == 0:
                        print(com + " 通道被禁用！")
                        b = 0
                        ser.readline()  # 清除此时缓冲区数据  无效
                        time.sleep(3)
                    else:
                        data = ''
                        data = data.encode()
                        n = ser.inWaiting()
                        if n:
                            # data = data+ser.read(n)
                            data = data + ser.readline()
                        # n = ser.inWaiting()
                        if len(data) > 10:
                            b = 0
                            a = a + 1
                            if a == 1:
                                print(data)
                                print("第一条消息不全丢掉")
                            else:
                                # 2. 读取数据
                                json_str = data.decode("gb2312")
                                # json_dict = json.loads(json_str)
                                print(json_str)
                                # 3. 写入设备數據表
                                if not self.insert_db(json_str, device, cls):
                                    cls = self.createtable(device)

                        else:
                            # 计数120次就默认没有消息上来 退出循环、線程
                            b = b + 1
                            if b == 120:
                                self.conn.delete(self.no % device)
                                print("设备无消息 break")
                                break
        except Exception as e:
            device_key = self.no % device
            path_key = "m5path_%s_%s" % (device, device_key.split("_")[1][1])
            print(path_key)
            self.conn.delete(device_key)
            self.conn.delete(path_key)
            cls.objects.all().delete()
            print("del " + self.no % device)
            # break

    def createtable(self, device):
        # 为设备新建一张表
        cls = get_smartdevicedata_model(self.no % device)
        if not cls.is_exists():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls)
        return cls

    def insert_db(self, data, device, cls):
        # print(str(data))
        try:
            c = cls.objects.create(data=str(data), smartdevice_name=device)
            c.save()
        except Exception as err:
            print("err: " + str(err))
            return False
        print(self.no % device + " 採集儲存成功！")
        return True

    def is_json(self, json_str):
        try:
            json.loads(json_str)
            return True
        except:
            return False


class DriveModbusTcp(Task):
    name = "DriveModbusTcp"
    conn = get_redis_connection('default')

    def run(self, *arg, **kwarg):
        '''

        :param apply_interface:  采集驱动任务(Modbus TCP) 建立连接的条件
        :param apply_template:   采集驱动任务(Modbus TCP) 设备模板
        :return:  while 循环 break 条件驱动状态 缓存在redis
        '''
        # print("arg:", arg)
        # print("kwarg:", kwarg)
        apply_interface = kwarg["apply_interface"]
        apply_template = kwarg["apply_template"]
        self.key = apply_interface["apply_tcp_device"]
        self.cls = get_subdevicedata_model(self.key)

        print("start modbus tcp drive " + self.key)

        try:
            master = modbus_tcp.TcpMaster(host=apply_interface["apply_tcp_ip"],
                                          port=int(apply_interface["apply_tcp_port"]),
                                          timeout_in_sec=float(apply_interface["apply_tcp_timeout"]))
            # self.
            var_list = self.init_val(apply_template, eval(apply_interface["apply_tcp_slave"]))
            # print(var_list)
            self.loop_start(var_list, master, float(apply_interface["apply_tcp_cycle"]))
            print("end modbus tcp drive ", self.key)
        except Exception as e:
            print(e)
            self.conn.hset(self.key, "drive_status_msg", " Error: " + str(e))
        finally:
            if 'master' in locals().keys():
                master.close()
            self.conn.hset(self.key, "drive_enable", 0)

    def Calculator(self, *args, type=2, reverse=True):
        n, m = 0, 0
        for n, m in args:
            n, m = '%04x' % n, '%04x' % m
        # print("nm:",n,m)
        if reverse:
            v = n + m
        else:
            v = m + n

        y_bytes = bytes.fromhex(v)
        y = struct.unpack('!f', y_bytes)[0]
        y = round(y, 2)
        if type == 0:  # 2進制
            return v
        elif type == 2:  # 16進制
            return y_bytes
        elif type == 1:  # 10進制
            return y

    def loop_start(self, var_list, master, cycle):
        # print(var_list)
        print(cycle)
        while int(self.conn.hget(self.key, "drive_enable").decode()):
            try:
                data = {}
                for var in var_list:
                    # raw_ = master.execute(var[1], var[2], var[3], var[4], data_format="!f")
                    # print(var)
                    raw_ = master.execute(var[1], var[2], var[3], var[4], data_format="!f")[0]
                    # print(raw_)
                    data[var[0]] = round(raw_, 2)
                    # data[var[0]] = self.Calculator(raw_)
                    # if var[5] == 0:  # 2、16進制輸出
                    #     data[var[0]]=self.Calculator(raw_, type=0)
                    # elif var[5] == 1:  # 2、16進制輸出
                    #     data[var[0]] = self.Calculator(raw_, type=1)
                    # elif var[5] == 2:  # 2、16進制輸出
                    #     data[var[0]] = self.Calculator(raw_, type=2)
                    # b_ = master.execute(var[1], var[2], var[3], var[4])
                    # s_ = master.execute(var[1], var[2], var[3], var[4] )
                    # print(b_)

                self.insert_db(data)
                self.conn.hset(self.key, "drive_status_msg", "")
                time.sleep(cycle)

            except Exception as e:
                print(str(e) + " continue......")
                self.conn.hset(self.key, "drive_status_msg", " Error: " + str(e))
                time.sleep(.8)
            # n=n-1

    def insert_db(self, data):
        # print(str(data))
        cls = self.cls.objects.create(data=str(data), subdevice_name=self.key)
        cls.save()
        print(self.key + " 採集儲存成功！")

    def init_val(self, apply_template, slave):
        var_list = []
        for etr in apply_template:
            # for s in slave:
            var_list.append([etr["etr_param"], slave[0], int(etr["etr_code"]), int(etr["etr_register"], 16),
                             int(etr["etr_register_num"], 16), int(etr["etr_format"]),
                             etr["etr_rule_sign"], etr["etr_rule_number"]])
        return var_list


class DriveModbusRtu(Task):
    name = "DriveModbusRtu"
    conn = get_redis_connection('default')

    def run(self, *arg, **kwarg):
        '''

        :param apply_interface:  采集驱动任务(Modbus RTU) 建立连接的条件
        :param apply_template:   采集驱动任务(Modbus RTU) 设备模板
        :return:  while 循环 break 条件驱动状态 缓存在redis
        '''
        apply_interface = kwarg["apply_interface"]
        apply_template = kwarg["apply_template"]
        self.key = apply_interface["apply_rtu_device"]  # 设备名
        self.cls = get_subdevicedata_model(self.key)  # 设备绑定的数据库

        print("start modbus rtu drive ", self.key)

        try:
            # 打开Rtu
            master = modbus_rtu.RtuMaster(
                serial.Serial(apply_interface["apply_rtu_com"],
                              baudrate=int(apply_interface["apply_rtu_botelv"]),
                              bytesize=int(apply_interface["apply_rtu_databit"]),
                              parity=apply_interface["apply_rtu_parity"][0],
                              stopbits=int(apply_interface["apply_rtu_stopbit"]),
                              xonxoff=0)
            )
            master.set_timeout(float(apply_interface["apply_rtu_timeout"]), )
            master.set_verbose(True)
            # 设置参数
            var_list = self.init_val(apply_template, eval(apply_interface["apply_rtu_slave"]))
            # 循环采集数据
            self.loop_start(var_list, master, float(apply_interface["apply_rtu_cycle"]))
            # 结束采集
            print("end modbus rtu drive ", self.key)
        except Exception as e:
            print(str(e) + " break......")
            # finally:
            if 'master' in locals().keys():
                master.close()
            self.conn.hset(self.key, "drive_enable", 0)
            self.conn.hset(self.key, "drive_status_msg", " error:" + str(e))

    def convert(self, s):
        try:
            i = int(s, 16)  # convert from hex to a Python int
            cp = pointer(c_int(i))  # make this into a c integer
            fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
            return fp.contents.value  # dereference the pointer, get the float
        except:
            return "NA"

    def Calculator(self, data, size=1, type=[0]):
        try:
            if type[0] == 0:  # 2
                return bin(data)
                # return data
            elif type[0] == 1:  # 10
                # if rule
                return eval(str(data) + type[-2] + type[-1])
                # return data
            elif type[0] == 2:  # 16
                return hex(data)
                # return data
            elif type[0] == 3:  # IEEE 754
                if size == 2:
                    cp = pointer(c_int(data))  # make this into a c integer
                    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
                    return eval(str(fp.contents.value) + type[-2] + type[-1])
                return "NA"
            elif type[0] == 4:
                # data 2301
                if size == 2:
                    data_ = "%08X" % (data)
                    h, l = data_[4:], data[0:4]
                    data__ = h + l
                    return round(self.convert(data__), 2)
                # 轉16進制 8位
                # 調轉 高低四位
                return "NA"
            elif type[0] == 5:
                # 浮点型
                return "NA"
                # return data
        except Exception as e:
            self.conn.hset(self.key, "drive_status_msg", " Error: " + str(e))
            # print()
            return "NA"

    def loop_start(self, var_list, master, cycle):
        print(cycle)
        while int(self.conn.hget(self.key, "drive_enable").decode()):
            try:
                # print(master)
                data = {}
                for var in var_list:
                    raw = "NA"
                    if var[4] == 1:
                        # 1個寄存器
                        raw = master.execute(var[1], var[2], var[3], 1, data_format=">H")[0]
                        data[var[0]] = self.Calculator(raw, size=1, type=var[5:])
                    else:
                        # 2個寄存器
                        raw = master.execute(var[1], var[2], var[3], 2, data_format=">L")[0]
                        data[var[0]] = self.Calculator(raw, size=2, type=var[5:])
                    # print(raw)
                    # data[var[0]] = self.Calculator(raw_)
                    # if var[5] == 0:  # 2進制輸出
                    #     data[var[0]]=self.Calculator(raw_, var[4], type=0)
                    # elif var[5] == 1:  # 10進制輸出
                    #     data[var[0]] = self.Calculator(raw_, var[4], type=1, rule=var[6], number=var[7])
                    # elif var[5] == 2:  # 16進制輸出
                    #     data[var[0]] = self.Calculator(raw_, var[4], type=2)
                    # elif var[5] == 3:  # IEEE-754進制輸出
                    #     data[var[0]] = self.Calculator(raw_, var[4], type=3, rule=var[6], number=var[7])
                    # print(data[var[0]])
                    # print(data[var[0]][0])
                    # 输出格式
                # print(data) #采集的模板数据
                self.insert_db(data)
                self.conn.hset(self.key, "drive_status_msg", "")
                time.sleep(cycle)
            except Exception as e:
                print(str(e) + " continue......")
                self.conn.hset(self.key, "drive_status_msg", " Error: " + str(e))
                time.sleep(.8)

    def insert_db(self, data):
        # print(str(data))
        try:
            # 確保正確格式的數據到數據庫
            all_data = json.loads(str(data).replace("'", '"'))
            cls = self.cls.objects.create(data=str(data), subdevice_name=self.key)
            cls.save()
            print(self.key + " 採集儲存成功！")
        except Exception as e:
            self.conn.hset(self.key, "drive_status_msg", " Error: " + str(e))
            print(self.key + " 採集儲存失敗！" + str(e))

    def init_val(self, apply_template, slave):
        var_list = []
        # template = None if conn.hget(subdevice, "template") is None else conn.hget(subdevice, "template").decode()
        for etr in apply_template:
            # print(etr["etr_param"], etr["etr_code"], etr["etr_register"], etr["etr_register_num"])
            var_list.append([etr["etr_param"], slave[0], int(etr["etr_code"]), int(etr["etr_register"], 16),
                             int(etr["etr_register_num"], 16), int(etr["etr_format"]),
                             etr["etr_rule_sign"], etr["etr_rule_number"]])
        return var_list


class DriveMQTTPro(Task):
    name = "DriveMQTTPro"
    conn = get_redis_connection('default')

    def run(self, *arg, **kwarg):
        '''

        :param apply_interface:  采集驱动任务(MQTT) 建立连接的条件
        :param apply_template:   采集驱动任务(MQTT) 设备模板
        :return:  while 循环 break 条件驱动状态 缓存在redis
        '''
        self.apply_interface = kwarg["apply_interface"]
        self.apply_template = kwarg["apply_template"]
        self.key = self.apply_interface["apply_mqtt_device"]
        self.cls = get_subdevicedata_model(self.key)
        self.obj_list = []

        print("start mqtt drive " + self.key)
        # print(self.apply_interface, self.apply_template)
        timestamp = str(round(time.time() * 1000))
        self.get_params()
        self.mqttclient = client(broker=self.apply_interface.get("apply_mqtt_ip"),
                                 port=int(self.apply_interface.get("apply_mqtt_port")),
                                 username=self.apply_interface.get("apply_mqtt_userName"),
                                 password=self.apply_interface.get("apply_mqtt_pwd"),
                                 client_id=timestamp)
        self.mqttclient.mqttc.on_connect = self.on_connect
        self.num = 0
        while int(self.conn.hget(self.key, "drive_enable").decode()):
            pass
        self.mqttclient.mqttc.disconnect()
        self.conn.hset(self.key, "drive_enable", 0)

    def get_params(self):
        self.params = [param["etm_param"] for param in self.apply_template]
        self.params_as = [param["etm_param_as"] for param in self.apply_template]
        self.params_type = [param["etm_type"] for param in self.apply_template]
        self.params_isnull = [param["etm_null"] for param in self.apply_template]

    def select_params(self, payload):
        new_dict = dict()
        for idx, param in enumerate(self.params):
            new_dict[self.params_as[idx]] = "NA"
            if self.params_type[idx] == "root":
                ## 根节点寻找
                v = payload.get(param)
                if v: new_dict[self.params_as[idx]] = v
            else:
                ## 子节点寻找
                for value in payload.values():
                    if type(value).__name__ == "dict":
                        v = value.get(param)
                        if v: new_dict[self.params_as[idx]] = v
                    elif type(value).__name__ == "list":
                        # 特殊情况[{}]
                        if type(value[0]).__name__ == "dict":
                            v = value[0].get(param)
                            if v: new_dict[self.params_as[idx]] = v
        # print(new_dict)
        return new_dict

    def insert_db(self, data, N=3):
        # print(str(data))
        try:
            # 確保正確格式的數據到數據庫
            all_data = json.loads(str(data).replace("'", '"'))
            # cls = self.cls.objects.create(data=str(data), subdevice_name=self.key)
            obj = self.cls(data=str(data), subdevice_name=self.key)

            self.obj_list.append(obj)
            if len(self.obj_list) >= N:
                self.cls.objects.bulk_create(self.obj_list)
                self.obj_list = []
                # cls.save()
                print(self.key + " 採集儲存成功！bulk=" + str(N))

        except Exception as e:
            self.conn.hset(self.key, "drive_status_msg", " Error: " + str(e))
            print(self.key + " 採集儲存失敗！" + str(e))

    def on_message(self, client, userdata, msg):
        append = ": " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + str(client._username)
        try:
            payload = json.loads(msg.payload.decode("gbk"))
            self.num += 1
            new_dict = self.select_params(payload)
            self.insert_db(new_dict)


        except Exception as e:
            print(e)

    def on_connect(self, client, userdata, flags, rc):
        # rc为0 返回连接成功
        if rc == 0:
            print(" OnConnetc, rc: " + str(rc) + " successful " + str(client._username))
            self.mqttclient.mqttc.subscribe(topic=self.apply_interface.get("apply_mqtt_topic"))
            self.mqttclient.mqttc.on_message = self.on_message
        else:
            print(" OnConnetc, rc: " + str(rc) + " unsuccessful" + " " + str(client._username))


class DriveCanisPro(Task):
    name = "DriveCanisPro"
    conn = get_redis_connection('default')

    def run(self, *arg, **kwarg):
        '''

        :param apply_interface:  采集驱动任务(Canis Pro) 建立连接的条件
        :param apply_template:   采集驱动任务(Canis Pro) 设备模板
        :return:  while 循环 break 条件驱动状态 缓存在redis
        '''
        self.apply_interface = apply_interface = kwarg["apply_interface"]
        self.apply_template = apply_template = kwarg["apply_template"]
        self.key = self.apply_interface["apply_canis_device"]
        self.cls = get_subdevicedata_model(self.key)

        print("start canis-pro drive " + self.key)

        try:
            self.sdk = sdk = DaqSDK()
            self.connect(sdk)  # 建立連接
            self.set_channel(sdk)  # 設置通道啟用

            self.collect(sdk)  # 開啟線程採集

            self.conn.hset(self.key, "drive_status_msg", "")
            while int(self.conn.hget(self.key, "drive_enable").decode()):
                ## 遍歷生成的文件 convert ac值
                # os.
                canis_files = [f for f in os.listdir() if "data_ch" in f]
                # sort timestamp
                canis_files.sort(key=lambda x: int(x[9:-4]))

                for file in canis_files:
                    full_path = os.path.join(os.path.abspath(""), file)
                    hex_path = os.path.join(os.path.abspath(r"plugins\CanisPro\HEX"), file)
                    ac_path = os.path.join(os.path.abspath(r"plugins\CanisPro\AC"), file.replace(".txt", ".pk"))
                    if self.check_file(full_path):
                        # 可以轉換和刪除
                        if self.cutmove(file):
                            # 可以移除或刪除后 convert ac
                            etl_hex2dc_csv(hex_path, ac_path)
                time.sleep(10)
            print("end modbus tcp drive ", self.key)

        except Exception as e:
            print(e)
            self.conn.hset(self.key, "drive_status_msg", " Error: " + str(e))
        finally:
            self.sdk.daq_disconnect()
            self.conn.hset(self.key, "drive_enable", 0)

    def cutmove(self, file):
        try:
            dst = os.path.join(os.path.abspath(""), r"plugins\CanisPro\HEX", file)  # dst 目的地址 絕對路徑
            src = os.path.join(os.path.abspath(""), file)  # src 原地址 絕對路徑
            shutil.move(src, dst)  # src -> dst 原文件存放地址放置在 目的地址
            return True
        except:
            return False

    def check_file(self, full_path):
        # print(full_path, end=": ")
        md5_first = hashlib.md5(open(full_path, 'rb').read()).hexdigest()
        time.sleep(.1)  # 等待100ms 判斷文件是否在更新
        md5_second = hashlib.md5(open(full_path, 'rb').read()).hexdigest()
        res = True if md5_first == md5_second else False
        # true 是未更新 false為在更新
        return res

    def collect(self, sdk):
        pip_no_list = [p["etc_pip_no"] for p in self.apply_template]
        for p in pip_no_list:
            mythread = threading.Thread(target=self.get_data_thread, args=("get_data_thread" + str(p), p, sdk))
            mythread.setDaemon(True)
            mythread.start()

    def connect(self, sdk):
        sdk.daq_set_buffer_size(50000)
        #
        ret = sdk.daq_connect(self.apply_interface.get("apply_canis_ip"),
                              int(self.apply_interface.get("apply_canis_port")),
                              self.apply_interface.get("apply_canis_userName"),
                              self.apply_interface.get("apply_canis_pwd"))
        print("Call daq_connect, ret = " + str(ret))
        self.exit_main(ret)
        # SET_HPS_SAMPLE_RATE = int(apply_interface.get("apply_canis_sampleRate")[:-1])
        SET_HPS_SAMPLE_RATE = HPS_SAMPLE_RATE_64K
        ret = sdk.daq_mode_config(SET_HPS_SAMPLE_RATE, SET_HPS_SAMPLE_RATE)
        print("Call daq_mode_config, ret = " + str(ret))
        self.exit_main(ret)
        #
        # HPS_BUFFER_SIZE = apply_interface.get("apply_canis_bufferSize")
        ret = sdk.daq_basic_config(HPS_BUFFER_SIZE_512K, HPS_MODE_A)
        print("Call daq_basic_config, ret = " + str(ret))
        self.exit_main(ret)

    def get_data_thread(self, name, channel, sdk):
        print("running... " + name)
        size = 100
        while int(self.conn.hget(self.key, "drive_enable").decode()):
            print("write data ........")
            ret, smp_data = sdk.daq_get_channel_data(channel, size)
        print("stop..." + name)

    def set_channel(self, sdk):
        # 設置通道啟用
        for i in range(6):
            ret = sdk.daq_channel_enable_config(i, 1)
            print("Call daq_channel_enable_config, ret = " + str(ret))
            self.exit_main(ret)

    def exit_main(self, ret):
        if (ret != DAQ_STATUS_GOOD):
            # exit()
            self.sdk.daq_disconnect()
            self.conn.hset(self.key, "drive_status_msg", " Error: " + str(ret))


class DriveForTransmit(Task):
    name = "DriveForTransmit"
    conn = get_redis_connection('default')
    mqttclient = ""

    def run(self, *arg, **kwarg):
        '''

        :param arg:
        :param kwarg: subdevice设备名 data_format 数据格式
        redis subdevice: device_enable 设备启用禁用
              path_subdevice_pathname: path_enable  设备路径启用禁用
        :return:
        '''
        # 获取设备名
        # 获取设备路径名称
        self.subdevice = kwarg["subdevice_name"]
        self.cls_log = get_subdevicelog_model(self.subdevice)

        print("start  drive transmit " + self.subdevice)
        # self.keys = "path_{}_*".format(self.subdevice)
        self.keys = "m5path_{}_*".format(self.subdevice.split("_")[2]) if "m5_0" == self.subdevice[
                                                                                    :4] else "path_{}_*".format(
            self.subdevice)
        self.path_keys = self.conn.keys(self.keys)

        # cls = get_subdevicedata_model(self.subdevice)
        cls = get_smartdevicedata_model(self.subdevice) if "m5_0" == self.subdevice[:4] else get_subdevicedata_model(
            self.subdevice)

        while True:
            # 大條件 設備是否禁用
            enable = self.conn.hget(self.subdevice, "device_enable")
            if not enable:
                break
            index = int(self.conn.hget(self.subdevice, "path_index"))
            result = self.transmit(index, cls)

            if result:  # 所有路徑被禁用的情況 驅動停止
                break

            index = int(self.conn.hget(self.subdevice, "path_index"))
            self.conn.hset(self.subdevice, "path_index", index + 1)
            time.sleep(3)

        self.close_tip()
        print("end for drive transmit " + self.subdevice)

    def close_tip(self):
        status = {
                     "status_code": "1",
                     "message": "路徑未開啟！"
                 },
        self.path_keys = self.conn.keys(self.keys)
        for path_key in self.path_keys:
            key = path_key.decode()
            self.conn.hset(key, 'path_status', json.dumps(status))
            self.conn.hset(key, 'path_index', 0)

    def transmit(self, index, cls):
        # 路徑是否禁用
        n = 0
        self.path_keys = self.conn.keys(self.keys)
        path_length = len(self.path_keys)
        for path_key in self.path_keys:
            key = path_key.decode()
            # print(key, "0310312031203122")
            type = self.conn.hget(key, "path_type").decode()
            if int(self.conn.hget(key, "path_enable")):  # 判斷路徑是否被禁用
                if type == "第三方MQTT" or type == "MQTT":
                    result = self.transmitformqtt(key, index, cls)
                    print("result:", result)
                    if result["status_code"] == "1":
                        print(self.subdevice + " " + result["error"] + str(index))
                        self.conn.hset(self.subdevice, "path_index", index - 1)

                if type == "Result Down":
                    result = self.downformqtt(key, index, cls)
                    print("result:", result)
                    if result["status_code"] == "1":
                        print(self.subdevice + " " + result["error"] + str(index))
                        self.conn.hset(self.subdevice, "path_index", index - 1)

                elif self.conn.hget(key, "path_type").decode() == "CorePro Server":
                    self.transmitforcorepro(key, index, cls)
                elif self.conn.hget(key, "path_type").decode() == "DB":
                    self.transmitfordb(key, index, cls)
            else:
                print(self.subdevice + " " + key + " 禁用")
                n += 1
                if n == path_length:
                    return True

    def transmitfordb(self, key, index, cls):
        # 路徑名稱key, 設備名稱subdevice, Django 數據objects接口 cls
        dbname = self.conn.hget(key, "path_topic").decode()
        dbip = self.conn.hget(key, "path_host").decode()
        dbport = int(self.conn.hget(key, "path_port").decode())
        dbusername = self.conn.hget(key, "path_username").decode()
        dbpwd = self.conn.hget(key, "path_pwd").decode()
        db = [dbip, dbport, dbusername, dbpwd, dbname]
        return self.dbcore(key, index, cls, db)

    def transmitformqtt(self, key, index, cls):
        # 路徑名稱key, 設備名稱subdevice, Django 數據objects接口 cls
        mqtt_topic = self.conn.hget(key, "path_topic").decode()
        mqtt_host = self.conn.hget(key, "path_host").decode()
        mqtt_port = int(self.conn.hget(key, "path_port").decode())
        mqtt_username = self.conn.hget(key, "path_username").decode()
        mqtt_pwd = self.conn.hget(key, "path_pwd").decode()
        mqtt = [mqtt_host, mqtt_port, mqtt_username, mqtt_pwd, mqtt_topic]
        return self.mqttcore(key, index, cls, mqtt)

    def downformqtt(self, key, index, cls):
        # 路徑名稱key, 設備名稱subdevice, Django 數據objects接口 cls
        mqtt_topic = self.conn.hget(key, "path_topic").decode()
        mqtt_host = self.conn.hget(key, "path_host").decode()
        mqtt_port = int(self.conn.hget(key, "path_port").decode())
        mqtt_username = self.conn.hget(key, "path_username").decode()
        mqtt_pwd = self.conn.hget(key, "path_pwd").decode()
        mqtt = [mqtt_host, mqtt_port, mqtt_username, mqtt_pwd, mqtt_topic]
        return self.mqttdown(key, index, cls, mqtt)

    def transmitforcorepro(self, key, index, cls):
        iot_topic = self.conn.hget(key, "path_topic").decode()
        iot_host = self.conn.hget(key, "path_host").decode()
        iot_port = int(self.conn.hget(key, "path_port").decode())
        iot_username = self.conn.hget(key, "path_username").decode()
        iot_pwd = self.conn.hget(key, "path_pwd").decode()
        iot = [iot_host, iot_port, iot_username, iot_pwd, iot_topic]
        if int(self.conn.hget(key, 'path_index')) == 0:
            # 路径的index 用来看是否 corepro 模组连接初始化
            timestamp = str(round(time.time() * 1000))
            self.mqttclient = client(broker=iot_host,
                                     port=iot_port,
                                     username=iot_username,
                                     password=iot_pwd,
                                     client_id=timestamp)

            self.mqttclient.mqttc.subscribe(topic=iot_topic + "/reply")
            self.conn.hset(key, 'path_index', 1)  # 初始化成功

        return self.iotcore(key, index, cls, self.mqttclient, iot)

    def dbcore(self, key, index, cls, db):
        obj = cls.objects.filter(id=index).values("data", "id", "smartdevice_name", "create_time") if "m5path" == key[
                                                                                                                  :6] else cls.objects.filter(
            id=index).values("data", "id", "subdevice_name", "create_time")
        if obj.count() == 0:
            last_row = cls.objects.last()
            if last_row is None:
                status_msg = {
                    "status_code": "1",
                    "error": "设备无数据！"
                }
                return status_msg
            if last_row.id > index:
                # 行缺失
                status_msg = {
                    "status_code": "0",
                    "error": "行缺失！"
                }
                return status_msg

            else:
                # 傳輸數據索引大於總行數
                status = {
                             "status_code": "1",
                             "error": "无数据更新！"
                         },
                self.conn.hset(key, 'path_status', json.dumps(status))
                return status
        else:
            obj = obj[0]
            # obj["create_time"]=obj["create_time"].strftime("%Y-%m-%d %H:%M:%S")
            obj["data"] = json.loads(obj["data"].replace("'", '"'))
            obj["data"]["collect_time"] = obj["create_time"].strftime("%Y-%m-%d %H:%M:%S")
            all_data = obj["data"]
            # data = json.dumps(obj)

            sql = "create table {0}("
            # d = ()
            for c, v in all_data.items():
                if type(v).__name__ == "str":
                    row = c + " char(50),"
                else:
                    row = c + " " + type(v).__name__ + ","
                sql += row
            sql = sql[:-1] + ")"
            template_name = self.conn.hget(self.subdevice, "template_name").decode()
            var_ = self.conn.hget(self.subdevice, template_name + "_varlist")
            var__ = [] if var_ is None else eval(var_.decode())
            obj = {data: all_data[data] for data in all_data.keys() if data in var__ + ["collect_time"]}
            d_ = [v for c, v in obj.items()]
            c_ = [c for c, v in obj.items()]

            print(sql)
            # 有客戶端連接會報錯
            try:
                # publish.single(mqtt[-1] , payload=data,
                #                hostname=mqtt[0],
                #                port=mqtt[1],
                #                auth={'username':mqtt[2], 'password':mqtt[3]})
                try:
                    with DB(host=db[0], port=db[1], user=db[2], passwd=db[3], db=db[-1]) as dbs:
                        # 使用预处理语句创建表
                        create_sql = sql.format(key)
                        dbs.execute(create_sql)
                except Exception as e:
                    print(str(e))
                    with DB(host=db[0], port=db[1], user=db[2], passwd=db[3], db=db[-1]) as dbs:

                        sql = "insert into {0}{1} values {2}".format(key, str(c_).replace("[", "(").replace("]",
                                                                                                            ")").replace(
                            "'", "")
                                                                     , str(d_).replace("[", "(").replace("]", ")"))
                        print(sql)
                        dbs.execute(sql)

                print(self.subdevice + " " + key + " " + "传输成功! " + str(index))
                count = int(self.conn.hget(key, "path_count"))
                # self.conn.hset(key, 'path_msg', data)
                self.conn.hset(key, 'path_count', count + 1)

                status_msg = {
                    "status_code": "0",
                    "message": "路徑运行正常！"
                }
                return status_msg
            except Exception as e:
                status_msg = {
                    "status_code": "1",
                    "error": "網絡連接失敗！"
                }
                print(status_msg.get("error") + str(e))
                return status_msg
            finally:
                self.conn.hset(key, 'path_status', json.dumps(status_msg))

    def iotcore(self, key, index, cls, mqttclient, iot):
        if self.mqttclient == "":
            self.conn.hset(key, 'path_index', 0)
            return False

        obj = cls.objects.filter(id=index).values("data")
        if obj.count() == 0:
            last_row = cls.objects.last()
            if last_row.id > index:
                # 行缺失
                status_msg = {
                    "status_code": "0",
                    "error": "行缺失！"
                }
                self.conn.hset(key, 'path_status', json.dumps(status_msg))
                # remark = " 设备《" + self.subdevice + "》" + json.dumps(status_msg)
                # self.cls_log.objects.create(subdevice_name=self.subdevice, remark=remark)
                return True

            else:
                # 傳輸數據索引大於總行數
                status_msg = {
                    "status_code": "1",
                    "message": "設備無數據！"
                }
                # remark = " 设备《" + self.subdevice + "》" + json.dumps(status_msg)
                # self.cls_log.objects.create(subdevice_name=self.subdevice, remark=remark)
                self.conn.hset(key, 'path_status', json.dumps(status_msg))
                return False
        else:
            obj = obj[0]
            all_data = json.loads(obj["data"].replace("'", '"'))
            template_name = self.conn.hget(self.subdevice, "template_name").decode()
            var_ = self.conn.hget(self.subdevice, template_name + "_varlist")
            var__ = [] if var_ is None else eval(var_.decode())
            obj = {data: all_data[data] for data in all_data.keys() if data in var__}

            data = self.corePro_format(key)
            data["app_params"][0].update(obj)
            data = json.dumps(data)

            mqttclient.mqttc.publish(topic=iot[-1], payload=data, qos=1)

            print(self.subdevice + " " + key + " " + "發佈成功! " + str(index))

            count = int(self.conn.hget(key, "path_count"))
            status_msg = {
                             "status_code": "0",
                             "message": "路徑运行正常！"
                         },
            self.conn.hset(key, 'path_status', json.dumps(status_msg))
            self.conn.hset(key, 'path_msg', data)
            self.conn.hset(key, 'path_count', count + 1)
            return True

    def mqttcore(self, key, index, cls, mqtt):
        obj = cls.objects.filter(id=index).values("data", "id", "smartdevice_name", "create_time") if "m5path" == key[
                                                                                                                  :6] \
            else cls.objects.filter(id=index).values("data", "id", "subdevice_name", "create_time")
        # print(obj.count())
        if obj.count() == 0:
            last_row = cls.objects.last()
            if last_row is None:
                status_msg = {
                    "status_code": "1",
                    "error": "设备无数据！"
                }
                self.conn.hset(key, 'path_status', json.dumps(status_msg))
                # remark = " 设备《" + self.subdevice + "》" +json.dumps(status_msg)
                # self.cls_log.objects.create(subdevice_name=self.subdevice, remark=remark)

                return status_msg
            if last_row.id > index:
                # 行缺失
                status_msg = {
                    "status_code": "0",
                    "error": "行缺失！"
                }
                self.conn.hset(key, 'path_status', json.dumps(status_msg))
                # remark = " 设备《" + self.subdevice + "》" + json.dumps(status_msg)
                # self.cls_log.objects.create(subdevice_name=self.subdevice, remark=remark)
                return status_msg

            else:
                # 傳輸數據索引大於總行數
                status = {
                    "status_code": "1",
                    "error": "无数据更新！"
                }
                self.conn.hset(key, 'path_status', json.dumps(status))
                # remark = " 设备《" + self.subdevice + "》" + json.dumps(status)
                # self.cls_log.objects.create(subdevice_name=self.subdevice, remark=remark)
                return status
        else:
            obj = obj[0]
            obj["create_time"] = obj["create_time"].strftime("%Y-%m-%d %H:%M:%S")
            all_data = json.loads(obj["data"].replace("'", '"'))
            template_name = self.conn.hget(self.subdevice, "template_name").decode()
            var_ = self.conn.hget(self.subdevice, template_name + "_varlist")
            var__ = [] if var_ is None else eval(var_.decode())
            obj["data"] = {data: all_data[data] for data in all_data.keys() if data in var__}

            data = json.dumps(obj)

            # 有客戶端連接會報錯
            try:
                publish.single(mqtt[-1], payload=data,
                               hostname=mqtt[0],
                               port=mqtt[1],
                               auth={'username': mqtt[2], 'password': mqtt[3]})
                print(self.subdevice + " " + key + " " + "發佈成功! " + str(index))
                count = int(self.conn.hget(key, "path_count"))
                self.conn.hset(key, 'path_msg', data)
                self.conn.hset(key, 'path_count', count + 1)

                status_msg = {
                    "status_code": "0",
                    "message": "路徑运行正常！"
                }
                self.conn.hset(key, 'path_status', json.dumps(status_msg))
                return status_msg

            except:
                status_msg = {
                    "status_code": "1",
                    "error": "網絡連接失敗！"
                }
                print(status_msg.get("error"))
                self.conn.hset(key, 'path_status', json.dumps(status_msg))
                # remark = " 设备《" + self.subdevice + "》" + json.dumps(status_msg)
                # self.cls_log.objects.create(subdevice_name=self.subdevice, remark=remark)
                return status_msg

    def mqttdown(self, key, index, cls, mqtt):

        num = cls.objects.values("id").order_by("-id")[0:1][0]['id']
        row_last_data = cls.objects.values("data", "id").order_by("-id")[1000 * (num // 1000):num]
        g_list = []
        for i in row_last_data:
            d_dict = json.loads(i["data"].replace("'", '"'))
            # il = list((ast.literal_eval(i["data"].replace("'", '"'))).values())
            il = list(d_dict.values())

            if 'NA' not in il:
                g = round(((float(il[0])) ** 2 + (float(il[1])) ** 2 + (float(il[2])) ** 2) ** 0.5, 2)
                g_list.append(g)

        height = round(sum(g_list) / len(g_list), 2)
        g_list = func.ArithmeticAverage(g_list, 10)
        peakind = signal.find_peaks(g_list, height=height, width=1.3)

        spd_count = len(peakind[0])
        if spd_count >= (int(self.conn.hget(key, 'spd_count'))):
            self.conn.hset(key, 'spd_count', spd_count)
        # python manage.py celeryd -l info

        if int(self.conn.hget(key, 'path_N_5')) != (num // 500):
            self.conn.hset(key, 'path_bpd_count',
                           int(self.conn.hget(key, 'path_bpd_count')) + int(self.conn.hget(key, 'spd_count')))

            self.conn.hset(key, 'spd_count', spd_count)
            self.conn.hset(key, 'path_N_5', (num // 500))
        data = json.dumps({'Command': 1, "Data": int(self.conn.hget(key, 'path_bpd_count')) + spd_count})
        print("data:" + str(int(self.conn.hget(key, 'path_bpd_count')) + spd_count))
        # 有客戶端連接會報錯
        try:
            publish.single(mqtt[-1], payload=data,
                           hostname=mqtt[0],
                           port=mqtt[1],
                           auth={'username': mqtt[2], 'password': mqtt[3]})
            time.sleep(.2)
            print(self.subdevice + " " + key + " " + "發佈成功! " + str(index))
            count = int(self.conn.hget(key, "path_count"))
            self.conn.hset(key, 'path_msg', data)
            self.conn.hset(key, 'path_count', count + 1)

            status_msg = {
                "status_code": "0",
                "message": "路徑运行正常！"
            }
            self.conn.hset(key, 'path_status', json.dumps(status_msg))
            return status_msg

        except:
            status_msg = {
                "status_code": "1",
                "error": "網絡連接失敗！"
            }
            print(status_msg.get("error"))
            self.conn.hset(key, 'path_status', json.dumps(status_msg))
            return status_msg

    def corePro_format(self, key):
        # 返回發佈在CorePro的數據格式
        return {
            "system_params": {
                "type": "",
                "token": "",
                "timestamp": str(time.time()),
                "appid": self.conn.hget(key, "path_datatypeid").decode(),
                "sign": "",
                "messageid": str(time.time())
            },
            "app_params": [
                {
                    "device_name": self.subdevice,
                    # "U0": 230,
                    # "I0": 120,
                    # "Mod": 123,
                    # "Ver": 3312,
                    # "Ur": 50,
                    # "Ir": 260,
                    # "Temp": 25
                }
            ]
        }


# ToDO 1. 定时任务 采集设备系统状态 cpu memory disk interface 使用率 频率2min
class DriveCollectSys(Task):
    name = "DriveCollectSys"
    conn = get_redis_connection('default')

    def run(self, *arg, **kwarg):

        cls = get_subdevicedata_model("system")
        if not cls.is_exists():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls)
        # time.time()
        cpu_status = max(psutil.cpu_percent(interval=1, percpu=True))  # 获得cpu当前使用率
        memory_status = float(psutil.virtual_memory().percent)  # 获取当前内存使用情况
        disk_status = float(psutil.disk_usage("/").percent)  # 获取当前磁盘的使用率
        port_list = list(serial.tools.list_ports.comports())
        serialList = [v[0] for v in port_list]
        num = 0
        for s in serialList:
            try:
                with serial.Serial(s, baudrate=9600, timeout=3) as ser:
                    if ser.isOpen():
                        pass
            except:
                num += 1
        data = {
            "cpu": cpu_status,
            "memory": memory_status,
            "disk": disk_status,
            "num": num
        }
        try:
            c = cls.objects.create(data=str(data), subdevice_name="system")
            c.save()
            print("系统数据采集成功！")
        except Exception as err:
            print("err: " + str(err))
            # return False


# ToDo 2. 定时任务 判断设备采集任务 转发任务 是否终止 启动因意外停止的任务   频率15min

# TODO 3. 轉發驅動任務 DriveForTransmit 重構
class DriveForTransmitV1(Task):
    name = "DriveForTransmitV1"
    conn = get_redis_connection('default')

    def run(self, *arg, **kwarg):
        pass


# TODO 4. 配置下發任務 連接10.129.7.199MQTT服務器用於測試
class DriveForSettingDown(Task):
    name = "DriveForSettingDown"
    conn = get_redis_connection('default')
    header = "http://127.0.0.1:8002"

    def run(self, *arg, **kwarg):
        self.down_topic = kwarg["down_topic"]
        # print(down_topic)
        self.mqttclient = client(broker="127.0.0.1", port=1883, username="iot", password="iot123!",
                                 client_id="iot_edgebox")
        self.mqttclient.mqttc.on_connect = self.on_connect
        while int(self.conn.hget("Agent", "setting")):
            pass
        self.mqttclient.mqttc.disconnect()
        self.conn.hset("Agent", "setting", 0)

    def post_api(self, url, json_data):
        proxies = {"http": None, "https": None}
        res = requests.post(url=url, data=json.dumps(json_data),
                            proxies=proxies,
                            headers={'Content-Type': 'application/json;charset=UTF-8', 'Accept': '*/*',
                                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
                                     })
        return res

    def success_res(self, topic, msg="Success"):
        get_settingdown_model.objects.filter(down_topic__contains=self.topic).update(
            down_num=F('down_num') + 1,
        )
        pyload = {"status_code": 200, "message": msg}
        self.mqttclient.mqttc.publish(topic=topic + "/reply",
                                      payload=json.dumps(pyload))

    def fail_res(self, topic, msg="ds"):
        get_settingdown_model.objects.filter(down_topic__contains=self.topic).update(
            # down_num=F('down_num') + 1,
            down_num2=F('down_num2') + 1,
        )
        pyload = {"status_code": 400, "message": "Fail:" + msg}
        self.mqttclient.mqttc.publish(topic=topic + "/reply",
                                      payload=json.dumps(pyload))

    def on_message(self, client, userdata, msg):
        append = ": " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + str(client._username)
        # if msg.topic == ""
        topic = msg.topic.split("/")[-2] + "/" + msg.topic.split("/")[-1]
        self.topic = topic
        obj = get_settingdown_model.objects.filter(down_topic__contains=topic).values()
        res = None
        try:
            payload = json.loads(msg.payload.decode("gbk"))
            if topic == "device/create" and payload.get("func_name") == "create_update_device":
                res = self.post_api(url=self.header + "/apis/device/create", json_data=payload.get("param"))
                # res = self.post_api(url=self.header + "/apis/device/create?update=1",
                #                     json_data=payload.get("param"))
                # print(res.status_code, res.json())

            if topic == "device/delete" and payload.get("func_name") == "delete_device":
                res = self.post_api(url=self.header + "/apis/device/delete",
                                    json_data=payload.get("param"))

            if topic == "device/enable" and payload.get("func_name") == "enable_device":
                res = self.post_api(url=self.header + "/apis/device/enable",
                                    json_data=payload.get("param"))

            if topic == "template/create" and payload.get("func_name") == "create_template":
                res = self.post_api(url=self.header + "/apis/device/template/create/",
                                    json_data=payload.get("param"))

            if topic == "template/delete" and payload.get("func_name") == "delete_template":
                res = self.post_api(url=self.header + "/apis/device/template/delete/",
                                    json_data=payload.get("param"))

            if topic == "template/apply" and payload.get("func_name") == "apply_template":
                res = self.post_api(url=self.header + "/apis/device/template/apply/",
                                    json_data=payload.get("param"))

            if topic == "drive/enable" and payload.get("func_name") == "enable_drive":
                res = self.post_api(url=self.header + "/apis/drive/enable/",
                                    json_data=payload.get("param"))

            if topic == "path/create" and payload.get("func_name") == "create_path":
                res = self.post_api(url=self.header + "/apis/device/path",
                                    json_data=payload.get("param"))

            if topic == "path/delete" and payload.get("func_name") == "delete_path":
                res = self.post_api(url=self.header + "/apis/device/path/delete",
                                    json_data=payload.get("param"))

            if res.status_code == 200:
                r = res.json()
                print("222222222222")
                if r.get("status_code") == 0:
                    self.success_res(msg.topic)
                else:
                    self.fail_res(msg.topic, r.get("error"))
            else:
                self.fail_res(msg.topic, msg=str(res.status_code))

            # else:
            #     print("1111111111111", msg.topic)
            #     self.fail_res(msg.topic, msg="Fail: 格式不正確或功能未開放!")

        except Exception as e:
            self.fail_res(msg.topic, msg=str(e))

        # self.deviceinfo["textEdit"].append(">>>" + append)
        # print("--------------")

    def on_connect(self, client, userdata, flags, rc):
        # rc为0 返回连接成功
        if rc == 0:
            # self.deviceinfo["textEdit"].append(">>>"+strcurtime+" OnConnetc, rc: "+str(rc)+" successful "+str(client._username))
            print(" OnConnetc, rc: " + str(rc) + " successful " + str(client._username))
            for topic in self.down_topic:
                self.mqttclient.mqttc.subscribe(topic=topic)
            self.mqttclient.mqttc.on_message = self.on_message
        else:
            print(" OnConnetc, rc: " + str(rc) + " unsuccessful" + " " + str(client._username))


# TODO 5. M5任務 連接本地MQTT服務器用於測試
from SmartDevice import smatask
