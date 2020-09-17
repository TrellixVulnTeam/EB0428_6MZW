import json

from django.core import serializers
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


# apis/drive/list
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from Device.models import applyTemplateRtuInterface, applyTemplateTcpInterface, EquipmentTemplateRtu, \
    applyTemplateCanisInterface, EquipmentTemplateCanis, applyTemplateMQTTInterface, EquipmentTemplateMqtt
from Drive.models import Drive
from Drive.tasks import DriveModbusRtu, DriveModbusTcp, DriveCanisPro, DriveMQTTPro
from Log.models import get_subdevicelog_model

@csrf_exempt
def driveList(request):
    '''

    :param request:
    :return:
    '''
    if request.method == "GET":
        query_set = Drive.objects.all().order_by('-id')
        if query_set.exists():
            json_db = json.loads(serializers.serialize("json", query_set))
            db = [i.pop("fields") for i in json_db]
            # print(db)

            return JsonResponse({
                "status_code": 0,
                "db": db
            })

        else:
            return JsonResponse({
                "status_code": 1,
                "error": "not data"
            })

# apis/drive/varlist
@csrf_exempt
def varList(request):
    '''
    :param request:
    :return:
    '''
    if request.method == "GET":
        subdevice = request.GET.get("device_name")
        template_name = request.GET.get("template_name")
        conn = get_redis_connection('default')
        if template_name is None:
            return JsonResponse({
                "status_code": 1,
                "error": "请先应用模板！"
            })
        try:
            varlist = eval(conn.hget(subdevice, template_name + '_varlist').decode())
            print(varlist)
            return JsonResponse({
                "status_code": 0,
                'varlist': varlist
            })
        except:
            conn.hset(subdevice , template_name + '_varlist', [])
            return JsonResponse({
                "status_code": 0,
                'varlist': []
            })


    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        print(vue_json)
        cls_log = get_subdevicelog_model(vue_json["device_name"])

        # 新增一条log
        remark = " 设备《" + vue_json["device_name"] + "》关键字段提取成功! "+str(vue_json["var_list"])
        cls_log.objects.create(subdevice_name=vue_json["device_name"], remark=remark)
        
        conn = get_redis_connection('default')
        conn.hset(vue_json["device_name"], vue_json["template_name"]+'_varlist', vue_json["var_list"])

        return JsonResponse({
            "status_code": 0,
            "message": "操作成功！"
        })

@csrf_exempt
def driveEnable(request):
    '''

    :param request:
    :return:
    '''
    def apply_template():
        if vue_json["drive_type"] == "Canis-Pro":
            return EquipmentTemplateCanis.objects.filter(etc_name = vue_json["template_name"]).values()
        elif vue_json["drive_type"] == "MQTT":
            return EquipmentTemplateMqtt.objects.filter(etm_name = vue_json["template_name"]).values()

        template = EquipmentTemplateRtu.objects.filter(etr_name= vue_json["template_name"]).values()
        # print(template)
        return template

    def apply_interface():
        # interface = {}
        if vue_json["drive_type"] == "Modbus-RTU":
            interface = applyTemplateRtuInterface.objects.filter(apply_rtu_drive= vue_json["drive_name"],
                                                             apply_rtu_device= vue_json["device_name"]).values()[0]
            # print(interface)
            return interface
        elif vue_json["drive_type"] == "Modbus-TCP":
            interface = applyTemplateTcpInterface.objects.filter(apply_tcp_drive=vue_json["drive_name"],
                                                                 apply_tcp_device=vue_json["device_name"]).values()[0]
            return interface
        elif vue_json["drive_type"] == "Canis-Pro":
            interface = applyTemplateCanisInterface.objects.filter(apply_canis_drive=vue_json["drive_name"],
                                                                 apply_canis_device=vue_json["device_name"]).values()[0]
            return interface
        elif vue_json["drive_type"] == "MQTT":
            interface = applyTemplateMQTTInterface.objects.filter(apply_mqtt_drive=vue_json["drive_name"],
                                                                   apply_mqtt_device=vue_json["device_name"]).values()[0]
            return interface

    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        print(vue_json)
        conn = get_redis_connection('default')
        cls_log = get_subdevicelog_model(vue_json["device_name"])
        if not cls_log.is_exists():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls_log)
        status = ""
        if vue_json["drive_type"] == "Modbus-RTU":
           apply = applyTemplateRtuInterface.objects.filter(apply_rtu_drive= vue_json["drive_name"],
                                                            apply_rtu_device= vue_json["device_name"]).\
                                                     update(apply_rtu_active = vue_json["enable"])

           if vue_json["enable"]:
               conn.hset(vue_json["device_name"], "drive_enable", 1)
               result = DriveModbusRtu.apply_async(kwargs={"apply_template":apply_template(), "apply_interface":apply_interface()},
                                                   queue= "worker_queue")
               status = "设备采集驱动启动成功！"
               # 新增一条log
               remark = " 设备《" + vue_json["device_name"] + "》采集驱动 *" + vue_json["drive_name"] + "* 已启用! "
               cls_log.objects.create(subdevice_name=vue_json["device_name"], remark=remark)

           else:
               conn.hset(vue_json["device_name"], "drive_enable", 0)
               status = "设备采集驱动已停止！"
               # 新增一条log
               remark = " 设备《" + vue_json["device_name"] + "》采集驱动 *" + vue_json["drive_name"] + "* 已关闭! "
               cls_log.objects.create(subdevice_name=vue_json["device_name"], remark=remark)

           return JsonResponse({
               "status_code": 1,
               "message": status
           })
        elif vue_json["drive_type"] == "Modbus-TCP":
            apply = applyTemplateTcpInterface.objects.filter(apply_tcp_drive=vue_json["drive_name"],
                                                             apply_tcp_device=vue_json["device_name"]). \
                                                    update(apply_tcp_active=vue_json["enable"])


            if vue_json["enable"]:
                conn.hset(vue_json["device_name"], "drive_enable", 1)
                result = DriveModbusTcp.apply_async(kwargs={"apply_template": apply_template(),
                                                            "apply_interface": apply_interface()},
                                                     queue="worker_queue")
                status = "设备采集驱动启动成功！"
                # 新增一条log
                remark = " 设备《" + vue_json["device_name"] +"》采集驱动 *"+vue_json["drive_name"]+ "* 已启用! "
                cls_log.objects.create(subdevice_name=vue_json["device_name"], remark=remark)


            else:
                conn.hset(vue_json["device_name"], "drive_enable", 0)
                status = "设备采集驱动已停止！"
                # 新增一条log
                remark = " 设备《" + vue_json["device_name"] + "》采集驱动 *" + vue_json["drive_name"] + "* 已关闭! "
                cls_log.objects.create(subdevice_name=vue_json["device_name"], remark=remark)

            return JsonResponse({
                "status_code": 1,
                "message": status
            })
        elif vue_json["drive_type"] == "Canis-Pro":
            apply = applyTemplateCanisInterface.objects.filter(apply_canis_drive=vue_json["drive_name"],
                                                             apply_canis_device=vue_json["device_name"]). \
                                                    update(apply_canis_active=vue_json["enable"])


            if vue_json["enable"]:
                conn.hset(vue_json["device_name"], "drive_enable", 1)
                result = DriveCanisPro.apply_async(kwargs={"apply_template": apply_template(),
                                                            "apply_interface": apply_interface()},
                                                     queue="worker_queue")
                status = "设备采集驱动启动成功！"
                # 新增一条log
                remark = " 设备《" + vue_json["device_name"] +"》采集驱动 *"+vue_json["drive_name"]+ "* 已启用! "
                cls_log.objects.create(subdevice_name=vue_json["device_name"], remark=remark)


            else:
                conn.hset(vue_json["device_name"], "drive_enable", 0)
                status = "设备采集驱动已停止！"
                # 新增一条log
                remark = " 设备《" + vue_json["device_name"] + "》采集驱动 *" + vue_json["drive_name"] + "* 已关闭! "
                cls_log.objects.create(subdevice_name=vue_json["device_name"], remark=remark)

            return JsonResponse({
                "status_code": 1,
                "message": status
            })
        elif vue_json["drive_type"] == "MQTT":
            apply = applyTemplateMQTTInterface.objects.filter(apply_mqtt_drive=vue_json["drive_name"],
                                                             apply_mqtt_device=vue_json["device_name"]). \
                                                    update(apply_mqtt_active=vue_json["enable"])


            if vue_json["enable"]:
                conn.hset(vue_json["device_name"], "drive_enable", 1)
                result = DriveMQTTPro.apply_async(kwargs={"apply_template": apply_template(),
                                                            "apply_interface": apply_interface()},
                                                     queue="worker_queue")
                status = "设备采集驱动启动成功！"
                # 新增一条log
                remark = " 设备《" + vue_json["device_name"] +"》采集驱动 *"+vue_json["drive_name"]+ "* 已启用! "
                cls_log.objects.create(subdevice_name=vue_json["device_name"], remark=remark)


            else:
                conn.hset(vue_json["device_name"], "drive_enable", 0)
                status = "设备采集驱动已停止！"
                # 新增一条log
                remark = " 设备《" + vue_json["device_name"] + "》采集驱动 *" + vue_json["drive_name"] + "* 已关闭! "
                cls_log.objects.create(subdevice_name=vue_json["device_name"], remark=remark)

            return JsonResponse({
                "status_code": 1,
                "message": status
            })