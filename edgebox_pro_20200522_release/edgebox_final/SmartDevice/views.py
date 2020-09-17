import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

# Create your views here.


# /apis/m5/pipeLine
from Device.models import get_smartdevicedata_model
from django.db import connection
from Log.models import get_event_model

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
        key = "m5_%s_*"% pip_no
        smart_device=conn.keys(key)
        smart_device = smart_device[0].decode()
        if enable:
            conn.hset(smart_device, "device_enable", 1)
            remark = "通道《"+pip_no+"》開啟成功！"
            event = get_event_model.objects.create(event_level="success", event_remark=remark, event_username="admin")
            event.save()
            return JsonResponse({
                "status_code": 0,
                "message": "通道《"+pip_no+"》開啟成功！"
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
        key = "m5_%s_*"% no
        smart_device=conn.keys(key)
        if smart_device == []:
            varlist = list()
            varlist.append(['通道名稱', no+"  << 該通道無設備連接 >>"])
            varlist.append(['設備名稱', "NA"])
            varlist.append(['啟用狀態', False])
            varlist.append(['In/Out', "NA"])
            varlist.append(['採集描述', "NA"])
            return JsonResponse({
                "status_code": 0,
                "varlist": varlist
            })
        smart_device=smart_device[0].decode()
        varlist = list()
        varlist.append(['通道名稱', no+" ( "+conn.hget(smart_device, "create_time").decode()+" )"])
        varlist.append(['設備名稱', conn.hget(smart_device, "name").decode()])
        varlist.append(['啟用狀態', True if int(conn.hget(smart_device, "device_enable")) else False])
        varlist.append(['In/Out', conn.hget(smart_device, "In").decode()+"-"
                       +conn.hget(smart_device, "com").decode()+"-"
                       +conn.hget(smart_device, "botelv").decode()+" / "+conn.hget(smart_device, "Out").decode()])
        varlist.append(['採集描述', conn.hget(smart_device, "remark").decode()])
       
        return JsonResponse({
            "status_code": 0,
            "varlist": varlist
        })