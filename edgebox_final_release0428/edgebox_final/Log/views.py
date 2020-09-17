import json
import time

import datetime
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from .models import get_subdevicelog_model
from django.db import connection
from django.http import JsonResponse
from .models import get_event_model
# /apis/log/list
@csrf_exempt
def List(request):
    """
    用于事件列表数据
    :param request: HttpRequest
    :return: Json
    """
    if request.method == "GET":
        subdevice = request.GET.get("device_name")
        cls_log = get_subdevicelog_model(subdevice)
        if not cls_log.is_exists():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls_log)
        row_last_data = cls_log.objects.values("remark", 'create_time').order_by("-id")[:10]
        db = [{"content":i["create_time"].strftime("%H:%M:%S  ")+i["remark"], "timestamp":i["create_time"].strftime("%Y-%m-%d")} for i in row_last_data]

        return JsonResponse({
            "status_code": 0,
            "db": db
        })


# /apis/log/delete
@csrf_exempt
def Delete(request):
    """
    用于刪除事件列表
    :param request: HttpRequest
    :return: Json
    """
    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        event_no = vue_json["event_no"]
        obj = get_event_model.objects.filter(id=event_no).delete()
        # obj.save()
        return JsonResponse({
            "status_code": 0,
            "message": "删除成功"
        })


# /apis/event/list
@csrf_exempt
def Event(request):
    """
    用于提供网关事件
    :param request: HttpRequest
    :return: Json
    """
    if request.method == "GET":
       
        
        row_last_data = get_event_model.objects.all().order_by("-id").values()[:30]
        # print(db)
        # db = [{"content": i["create_time"].strftime("%H:%M:%S  ") + i["remark"],
        #        "timestamp": i["create_time"].strftime("%Y-%m-%d")} for i in row_last_data]
        event = [ i for i in row_last_data ]
        
        return JsonResponse({
            "status_code": 0,
            "event": event
        })


# /apis/log/list
@csrf_exempt
def Select(request):
    """
    用于提供設備列表数据
    :param request: HttpRequest
    :return: Json
    """
    if request.method == "GET":
        subdevice = request.GET.get("device_name")
        start_time = datetime.datetime.fromtimestamp(int(request.GET.get("start"))//1000)
        end_time = datetime.datetime.fromtimestamp(int(request.GET.get("end"))//1000)
        cls_log = get_subdevicelog_model(subdevice)
        if not cls_log.is_exists():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls_log)

        row_last_data = cls_log.objects.filter(create_time__range=(start_time, end_time)).values("remark", 'create_time').order_by("-id")
        # print(db)
        db = [{"content":i["create_time"].strftime("%H:%M:%S  ")+i["remark"], "timestamp":i["create_time"].strftime("%Y-%m-%d")} for i in row_last_data]

        return JsonResponse({
            "status_code": 0,
            "db": db
        })
