import json

import datetime, time
import subprocess
from django.db import connection
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from plugins.systemos import systemos

from plugins.auth_corepro import AuthCorepro as agentauth
from Device.models import SubDevice, get_subdevicedata_model
from .models import RegisterInfo
from django.http import JsonResponse
from django.core import serializers
import psutil
from Drive.tasks import smatask


# /apis/agent/info
@csrf_exempt
def Info(request):
    """
    用于提供Agent数据
    :param request: HttpRequest
    :return: Json
    """

    def auth():
        result = agentauth(ProductKey=vue_json["gateway_key"],
                           DeviceName=vue_json["gateway_name"],
                           DeviceSecret=vue_json["gateway_secret"],
                           auth_url=vue_json["gateway_tokenapi"])
        return [result.username, result.password, result.mqtthost, result.mqttport]

    if request.method == "POST":
        try:
            vue_json = json.loads(request.body.decode())["params"]
            # print(vue_json)
            result = auth()
            if all(result):
                obj, created = RegisterInfo.objects.update_or_create(
                    gateway_trade_name='IoT',
                    gateway_model='IoT',
                    gateway_remark="EdgeBox边缘层网关测试版",
                    gateway_key=vue_json["gateway_key"],
                    gateway_secret=vue_json["gateway_secret"],
                    gateway_tokenapi=vue_json["gateway_tokenapi"],
                    gateway_location=vue_json["gateway_location"],
                    gateway_iotid=result[0],
                    gateway_iottoken=result[1],
                    gateway_iothost=result[2],
                    gateway_iotport=result[3],
                    gateway_registration_time=datetime.datetime.now(),
                    defaults={"gateway_name": vue_json["gateway_name"]},
                )
                status = "新建" if created else '修改'
                conn = get_redis_connection('default')
                conn.hset("Agent", "name", vue_json["gateway_name"])
                conn.hset("Agent", "id", vue_json["gateway_key"])
                conn.hset("Agent", "sercet", vue_json["gateway_secret"])
                conn.hset("Agent", "tokenapi", vue_json["gateway_tokenapi"])
                conn.hset("Agent", "location", vue_json["gateway_location"])

                return JsonResponse({
                    "status_code": 0,
                    "message": "注册成功/" + status,
                })
            else:
                return JsonResponse({
                    "status_code": 1,
                    "error": "注册修改出错: auth error",
                })
        except Exception as e:

            return JsonResponse({
                "status_code": 1,
                "error": "注册修改出错:" + str(e),
            })

    if request.method == "GET":
        # data = RegisterInfo.objects.create(gateway_name="EdgeBox003",
        #                                    gateway_key="6553791093879608705",
        #                                    gateway_secret="e3f3eeb045f0a19284ad03f64e101ce3f7fa15d135a7140e411fa29dbd269d7c",
        #                                    gateway_subdevice_num=0,
        #                                    gateway_model="IoT",
        #                                    gateway_trade_name="IoT",
        #                                    gateway_registration_time=datetime.datetime.now(),
        #                                    gateway_location="E5-4F",
        #                                    gateway_remark="EdgeBox边缘层网关测试版")
        # data.save()
        # row_data = RegisterInfo.objects.all().values()[0]
        raw_data = RegisterInfo.objects.all().order_by("-id").values()[:7]
        row_data = raw_data[0]
        row_data['gateway_registration_time'] = row_data['gateway_registration_time'].strftime("%Y-%m-%d %H:%M:%S")
        row_data["gateway_subdevice_num"] = SubDevice.objects.all().count()
        row_data["status_code"] = 0
        history_data = raw_data[:]
        history_data = [data for data in history_data]
        return JsonResponse({
            "row_data": [row_data],
            "history_data": history_data,
        })


# /apis/agent/sysinfo
@csrf_exempt
def sysInfo(request):
    """
    用于提供数据
    :param request: HttpRequest
    :return: Json
    """

    if request.method == "GET":
        data = {}
        s = systemos()
        if request.GET.get("cpu") is not None:
            data["data_for_cpu"] = s.GetCpuInfo()
        elif request.GET.get("os") is not None:
            data["data_for_sys"] = s.GetMemoryInfo()
        elif request.GET.get("interface") is not None:
            data["data_for_disk"] = s.GetDiskInfo()
        data["status_code"] = 0
        data["cpu_status"] = max(psutil.cpu_percent(interval=1, percpu=True))  # 获得cpu当前使用率
        data["memory_status"] = float(psutil.virtual_memory().percent)  # 获取当前内存使用情况
        data["disk_status"] = float(psutil.disk_usage("/").percent)  # 获取当前磁盘的使用率
        cls = get_subdevicedata_model("system")
        if not cls.is_exists():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls)
        start_time, end_time = datetime.datetime.now() + datetime.timedelta(hours=-1), datetime.datetime.now()
        row_lasthours_data = cls.objects.filter(create_time__range=(start_time, end_time)).values("create_time", "data")
        db = [json.loads(i["data"].replace("'", '"')) for i in row_lasthours_data]
        table = []
        for index, row in enumerate(db):
            add_json = {
                "id": row_lasthours_data[index]["create_time"].strftime("%m-%d %H:%M:%S")
            }
            row.update(add_json)
            table.append(row)
        data["table"] = table
        data["total"] = len(table)
        return JsonResponse(data)


# /apis/agent/sysmqtt
@csrf_exempt
def sysMqtt(request):
    """
       用于开启mqtt服务
       :param request: HttpRequest
       :return: Json
    """
    start_comm = 'emqx start'
    stop_comm = 'emqx stop'
    cwd = 'F:/EB0428/emqx-windows-v4.0.2/emqx/bin'
    mqtt_data = [
        {
            'mqtthost': '127.0.0.1',
            'mqttport': '18083',
            'mqttusername': 'admin',
            'mqttpassword': 'public',
            'mqttstatus': False,
            'mqtturl': 'http://localhost:18083/'
        }
    ]

    if request.method == "GET":
        conn = get_redis_connection('default')
        enable = conn.hget("Agent", "settings")

        if not enable:
            conn.hset("Agent", "settings", 0)
            mqtt_data[0]['mqttstatus'] = False

        else:
            if int(enable) == 1:
                mqtt_data[0]['mqttstatus'] = True
            else:
                mqtt_data[0]['mqttstatus'] = False

        return JsonResponse({
            "status_code": 0,
            "mqtt_data": mqtt_data
        })

    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        conn = get_redis_connection('default')
        try:
            enable = vue_json["enable"]
            if enable:
                p = subprocess.Popen(start_comm, cwd=cwd, shell=True, stdout=subprocess.PIPE,
                                     universal_newlines=True)
                p.wait()
                conn.hset("Agent", "settings", 1)

                return JsonResponse({
                    "status_code": 0,
                    "message": "MQTT服务啟動成功！"
                })
                ## 启动驱动
            else:
                p = subprocess.Popen(stop_comm, cwd=cwd, shell=True, stdout=subprocess.PIPE,
                                     universal_newlines=True)
                p.wait()
                conn.hset("Agent", "settings", 0)
                return JsonResponse({
                    "status_code": 0,
                    "message": "MQTT服务已禁用！"
                })
        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "message": "操作失敗！" + str(e)
            })
