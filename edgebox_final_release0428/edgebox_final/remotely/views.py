import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Drive.tasks import DriveForSettingDown
from .models import get_settingdown_model
from Agent.models import RegisterInfo
from django_redis import get_redis_connection


# Create your views here.

# /apis/remotely/setting/enable
@csrf_exempt
def settingEnable(request):
    """
       用于提供設備列表数据
       :param request: HttpRequest
       :return: Json
       """
    if request.method == "POST":
        # db = [{"content":i["create_time"].strftime("%H:%M:%S  ")+i["remark"], "timestamp":i["create_time"].strftime("%Y-%m-%d")} for i in row_last_data]
        vue_json = json.loads(request.body.decode())
        conn = get_redis_connection('default')
        try:
            enable = vue_json["enable"]
            if enable:
                obj = get_settingdown_model.objects.all().values()
                last_data = RegisterInfo.objects.all().order_by("-id").values()[0]
                topic = []
                for i in obj:
                    down_topic = i["down_topic"].format(gateway=last_data["gateway_name"],
                                                        gateway_id=last_data["gateway_key"])
                    topic.append(down_topic)
                result = DriveForSettingDown.apply_async(kwargs={"down_topic": topic}, queue="worker_queue")
                print("apply async")
                conn.hset("Agent", "setting", 1)
                return JsonResponse({
                    "status_code": 0,
                    "message": "配置下發接口啟動成功！"
                })
                ## 啟動驅動
            else:
                conn.hset("Agent", "setting", 0)
                return JsonResponse({
                    "status_code": 0,
                    "message": "配置下發接口已禁用！"
                })
        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "message": "操作失敗！" + str(e)
            })


# /apis/remotely/list
@csrf_exempt
def List(request):
    """
    用于提供設備列表数据
    :param request: HttpRequest
    :return: Json
    """
    if request.method == "GET":
        # db = [{"content":i["create_time"].strftime("%H:%M:%S  ")+i["remark"], "timestamp":i["create_time"].strftime("%Y-%m-%d")} for i in row_last_data]
        obj = get_settingdown_model.objects.all().values()
        conn = get_redis_connection('default')
        enable = conn.hget("Agent", "setting")
        if not enable:
            conn.hset("Agent", "setting", 0)
            enable = False
        else:
            enable = True if int(enable) == 1 else False

        last_data = RegisterInfo.objects.all().order_by("-id").values()[0]
        db = []

        for i in obj:
            i["down_topic"] = i["down_topic"].format(gateway=last_data["gateway_name"],
                                                     gateway_id=last_data["gateway_key"])
            i["down_param"] = json.loads(i["down_param"])
            db.append(i)
        # print(db)
        return JsonResponse({
            "status_code": 0,
            "db": db,
            "enable": enable,
        })
