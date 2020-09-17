import json

import pymysql
from django.core import serializers

from django.shortcuts import render, render_to_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from SmartDevice import mqtttest

# Create your views here.


# /apis/m5/pipeLine
from Device.models import get_smartdevicedata_model
from django.db import connection
from Log.models import get_event_model
from .models import SmartCommunicate, SmartSns
import paho.mqtt.client as mqtt
from paho.mqtt import publish
from Drive.tasks import smatask

client = mqtt.Client()


@csrf_exempt
def Enable(request):
    """
    用於控制管道數據通道
    :param request: HttpRequest
    :return: Json
    """
    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        # print(vue_json)
        conn = get_redis_connection('default')
        pip_no = vue_json["pip_no"]
        enable = vue_json["enable"]
        key = "m5_%s_*" % pip_no
        smart_device = conn.keys(key)
        smart_device = smart_device[0].decode()
        if enable:
            conn.hset(smart_device, "device_enable", 1)
            remark = "通道《" + pip_no + "》開啟成功！"
            event = get_event_model.objects.create(event_level="success", event_remark=remark, event_username="admin")
            event.save()
            return JsonResponse({
                "status_code": 0,
                "message": "通道《" + pip_no + "》開啟成功！"
            })
        else:
            conn.hset(smart_device, "device_enable", 0)
            remark = "通道《" + pip_no + "》關閉成功！"
            event = get_event_model.objects.create(event_level="warning", event_remark=remark, event_username="admin")
            event.save()
            return JsonResponse({
                "status_code": 0,
                "message": "通道《" + pip_no + "》關閉成功！"
            })


@csrf_exempt
def pipeLine(request):
    """
    用于提供智能設備管道数据
    :param request: HttpRequest
    :return: Json
    """

    if request.method == "GET":
        conn = get_redis_connection('default')
        no = request.GET.get("pipe_no")
        key = "m5_%s_*" % no
        smart_device = conn.keys(key)
        if smart_device == []:
            varlist = list()
            varlist.append(['通道名稱', no + "  << 該通道無設備連接 >>"])
            varlist.append(['設備名稱', "NA"])
            varlist.append(['啟用狀態', False])
            varlist.append(['In/Out', "NA"])
            varlist.append(['採集描述', "NA"])
            return JsonResponse({
                "status_code": 0,
                "varlist": varlist
            })
        smart_device = smart_device[0].decode()
        varlist = list()
        varlist.append(['通道名稱', no + " ( " + conn.hget(smart_device, "create_time").decode() + " )"])
        varlist.append(['設備名稱', conn.hget(smart_device, "name").decode()])
        varlist.append(['啟用狀態', True if int(conn.hget(smart_device, "device_enable")) else False])
        varlist.append(['In/Out', conn.hget(smart_device, "In").decode() + "-"
                        + conn.hget(smart_device, "com").decode() + "-"
                        + conn.hget(smart_device, "botelv").decode() + " / " + conn.hget(smart_device, "Out").decode()])
        varlist.append(['採集描述', conn.hget(smart_device, "remark").decode()])

        return JsonResponse({
            "status_code": 0,
            "varlist": varlist
        })


@csrf_exempt
def apptest(request):
    if request.method == "GET":
        conn = get_redis_connection('default')
        cls = get_smartdevicedata_model("gateway_mpumpu")
        row_last_data = cls.objects.values("data", "id").order_by("-id")[0:1035]

        d_list = []
        for i in row_last_data:
            d_dict = json.loads(i["data"].replace("'", '"'))
            # print(d_dict)
            d_list.append(d_dict)

        return JsonResponse({
            "status_code": 0,
            "data": d_list
        })


@csrf_exempt
def smartList(request):
    conn = get_redis_connection('default')
    db2 = []
    if request.method == "GET":
        query_set = SmartCommunicate.objects.all().order_by('-id')
        if query_set.exists():
            json_db = json.loads(serializers.serialize("json", query_set))
            db = [i.pop("fields") for i in json_db]

            for i in db:
                i["smart_sns"] = i["smart_sns"].replace("'", "").replace("[", "").replace("]", "")
            # 要改
            print(db)
            sns_list = list(SmartSns.objects.values_list('smart_sname', flat=True))
            print(sns_list)
            # now_sns = eval(str(conn.hget("Smart", "now_sns"), encoding="utf-8"))
            # obj = SmartCommunicate.objects.filter(smart_name=smart_name).values("smart_sns")
            # sns_list = list(obj)[0]["smart_sns"]

            return JsonResponse({
                "status_code": 0,
                "db": db,
                "sns": sns_list
            })

        else:
            return JsonResponse({
                "status_code": 1,
                "error": "not data"
            })


@csrf_exempt
def smartEnable(request):
    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        print(vue_json)
        conn = get_redis_connection('default')

        smart_name = vue_json["smart_name"]
        enable = vue_json["enable"]
        obj = SmartCommunicate.objects.filter(smart_name=smart_name).update(smart_enable=enable)
        obj = SmartCommunicate.objects.filter(smart_name=smart_name).values("smart_sns")
        sns_list = list(obj)[0]["smart_sns"]
        conn.hset("Smart", "now_sns", str(sns_list))
        conn.hset("Smart", "now_sname", str(smart_name))

        if enable:
            conn.hset(smart_name, "smart_enable", 1)
            result = smatask.M5MQTTCom2.apply_async(kwargs={}, queue="worker_queue")
            print("m5 apply async 22")
            return JsonResponse({
                "status_code": 0,
                "message": "启用成功"
            })
        else:
            result = smatask.M5MQTTCom.apply_async(kwargs={}, queue="worker_queue")
            print("m5 apply async 11")
            conn.hset(smart_name, "smart_enable", 0)
            return JsonResponse({
                "status_code": 0,
                "message": "禁用成功"
            })


# apis/m5/smartcreate/
def smartCreate(request):
    """
     用于创建一个新設備
     :param request: HttpRequest
     :return: Json
     """

    if request.method == "POST":
        try:

            vue_json = json.loads(request.body.decode())
            print(vue_json["smart_type"])
            print(type(vue_json["smart_type"]))

            subdevice = SmartCommunicate.objects.create(smart_name=vue_json["smart_name"],
                                                        smart_sns=vue_json["smart_type"],
                                                        smart_area=vue_json["smart_region"],
                                                        smart_remark=vue_json["smart_remark"])
            subdevice.save()
            print("save ok")
            # get
            conn = get_redis_connection("default")
            conn.hset(vue_json["smart_name"], "smart_enable", 0)

            return JsonResponse({
                "status_code": 0,
                "message": "创建成功"
            })

        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "error": str(e)
            })


@csrf_exempt
def smartDelete(request):
    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        print(vue_json)
        conn = get_redis_connection('default')
        smartd = vue_json["smart_name"]
        conn.delete(smartd)
        obj = SmartCommunicate.objects.filter(smart_name=smartd).delete()
        print("del ok")
        return JsonResponse({
            "status_code": 0,
            "message": "删除成功"
        })


# apis/m5/smartorder/
def smartOrder(request):
    if request.method == "POST":
        try:

            vue_json = json.loads(request.body.decode())
            print(vue_json["smart_order"])
            print(type(vue_json["smart_orderpython "]))

            publish.single("M5_clight", payload=str(vue_json["smart_order"]),
                           hostname="127.0.0.1",
                           port=1883,
                           auth={'username': 'admin', 'password': 'public'})

            return JsonResponse({
                "status_code": 0,
                "message": "下发成功"
            })

        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "error": str(e)
            })


# apis/m5/logweb/
def logWeb(request):
    if request.method == "GET":
        try:
            import sqlite3
            db = sqlite3.connect('SmartDevice/test.db')
            # 建立连接，如果不存在将会创建
            print("Open database successfully")

            # sql = "CREATE TABLE IF NOT EXISTS m5logs (id VARCHAR(255) NOT NULL, thingtime VARCHAR(255) NOT NULL, thingtype VARCHAR(255) NOT NULL, thingdetails INT NOT NULL, PRIMARY KEY (id))"
            sql = "select * from m5logs order by id desc limit 10"
            cur = db.cursor()
            cur.execute(sql)

            desc = cur.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
            lidata = [dict(zip([col[0] for col in desc], row)) for row in cur.fetchall()]  # 列表表达式把数据组装起来

            cur.close()
            db.commit()
            db.close()
            # lidata = dict(lidata[0])
            print(lidata)
            # list_data = list(lidata[0])
            # print(list_data)
            return render(request, 'm5log.html', {'current_date': lidata})

        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "error": str(e)
            })
