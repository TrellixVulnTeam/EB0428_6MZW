import json
import time
from random import choice

import serial
import serial.tools.list_ports
# import numpy as np
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# mpl.use("Agg")
from django.core import serializers
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Log.models import get_event_model

# Create your views here.
from Agent.models import RegisterInfo
from Drive.models import Drive
from Drive.tasks import DriveForTransmit
from .models import SubDevice, EquipmentTemplateRtu, applyTemplateRtuInterface, applyTemplateTcpInterface, \
    Path, get_subdevicedata_model, get_smartdevicedata_model, EquipmentTemplateCanis, applyTemplateCanisInterface
from Log.models import get_subdevicelog_model

from django.db.models import Avg, Sum, Max, Min, Count
from django_redis import get_redis_connection
from plugins.mqtt_pub_sub import mqtt_client_connect


# /apis/device/create
@csrf_exempt
def Create(request):
    """
    用于创建一个新設備
    :param request: HttpRequest
    :return: Json
    """

    if request.method == "POST":
        try:
            print(request.GET.get("update"))
            vue_json = json.loads(request.body.decode())
            print(vue_json)
            if request.GET.get("select") is not None:
                ## 判断设备名是否重复
                try:
                    subdevice = SubDevice.objects.get(subdevice_name=vue_json.get("select_devicename"))
                    print(subdevice)
                    return JsonResponse({
                        "status_code": 1,
                        "is_indb": 1
                    })
                except:
                    return JsonResponse({
                        'status_code': 0,
                        "is_indb": 0
                    })
            elif request.GET.get("update") is not None:
                ## 设备信息修改
                try:
                    if vue_json.get("subdevice_remark"):
                        SubDevice.objects.filter(subdevice_name=vue_json["subdevice_name"]).update(
                            subdevice_type=vue_json["subdevice_type"],
                            subdevice_position=vue_json["subdevice_position"],
                            subdevice_model=vue_json["subdevice_model"],
                            subdevice_remark=vue_json["subdevice_remark"])
                    else:
                        SubDevice.objects.filter(subdevice_name=vue_json["subdevice_name"]).update(
                            subdevice_type=vue_json["subdevice_type"],
                            subdevice_position=vue_json["subdevice_position"],
                            subdevice_model=vue_json["subdevice_model"])
                    remark = " 设备《" + vue_json["subdevice_name"] + "》修改成功! "
                    event = get_event_model.objects.create(event_level="info", event_remark=remark,
                                                           event_username="admin")
                    event.save()
                    print("ok  !!")
                    return JsonResponse({
                        "status_code": 1,
                        "message": "修改成功！"
                    })
                except Exception as e:
                    remark = " 设备《" + vue_json["subdevice_name"] + "》修改失败! "
                    event = get_event_model.objects.create(event_level="error", event_remark=remark,
                                                           event_username="admin")
                    event.save()
                    return JsonResponse({
                        'status_code': 1,
                        "error": "修改失败！" + str(e)
                    })

            subdevice = SubDevice.objects.create(subdevice_name=vue_json["subdevice_name"],
                                                 subdevice_type=vue_json["subdevice_type"],
                                                 subdevice_position=vue_json["subdevice_position"],
                                                 subdevice_model=vue_json["subdevice_model"],
                                                 subdevice_remark=vue_json["subdevice_remark"])
            subdevice.save()

            # 为设备新建一张表
            cls = get_subdevicedata_model(vue_json["subdevice_name"])
            cls_log = get_subdevicelog_model(vue_json["subdevice_name"])

            if not cls.is_exists():
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(cls)
            if not cls_log.is_exists():
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(cls_log)

            # 新增一条log
            remark = " 设备《" + vue_json["subdevice_name"] + "》创建成功! "
            cls_log.objects.create(subdevice_name=vue_json["subdevice_name"], remark=remark)
            event = get_event_model.objects.create(event_level="success", event_remark=remark, event_username="admin")
            event.save()
            # get
            conn = get_redis_connection("default")
            conn.hset(vue_json["subdevice_name"], "device_enable", 1)
            conn.hset(vue_json["subdevice_name"], "drive_enable", 0)
            conn.hset(vue_json["subdevice_name"], "path_index", 0)
            return JsonResponse({
                "status_code": 0,
                "message": "创建成功"
            })

        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "error": str(e)
            })


# /apis/device/delete
@csrf_exempt
def Delete(request):
    '''
    删除设备
    :param request:
    :return:
    '''

    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        # print(vue_json)
        conn = get_redis_connection('default')
        subdevice = vue_json["subdevice_name"]
        conn.delete(subdevice)
        obj = SubDevice.objects.filter(subdevice_name=subdevice).delete()

        remark = " 设备《" + vue_json["subdevice_name"] + "》删除成功! "
        event = get_event_model.objects.create(event_level="warning", event_remark=remark, event_username="admin")
        event.save()
        return JsonResponse({
            "status_code": 0,
            "message": "删除成功"
        })


# /apis/device/enable

@csrf_exempt
def Enable(request):
    '''
    用户启用禁用设备接口
    :param request:
    :return:
    '''

    def set_disenable(subdevice=""):
        conn.hset(subdevice, "device_enable", 0)
        keys = "path_{}_*".format(subdevice)
        path_keys = conn.keys(keys)
        for path_key in path_keys:
            conn.hset(path_key.decode(), "path_enable", 0)
            obj = Path.objects.filter(subdevice_name=subdevice).update(path_enable=False)

    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        print(vue_json)
        conn = get_redis_connection('default')
        if request.GET.get("more") is not None:
            # 批量禁用启用
            subdevice_name_list = vue_json["subdevice_name_list"]
            enable = vue_json["enable"]
            obj = SubDevice.objects.filter(subdevice_name__in=subdevice_name_list).update(subdevice_enable=not enable)
            status = ""
            for subdevice_name in subdevice_name_list:
                cls_log = get_subdevicelog_model(subdevice_name)
                status = "禁用成功" if enable else "启用成功"
                remark = " 设备《" + subdevice_name + "》{0}! ".format(status)
                cls_log.objects.create(subdevice_name=subdevice_name, remark=remark)
                cache = set_disenable(subdevice=subdevice_name) if enable else conn.hset(subdevice_name,
                                                                                         "device_enable", 1)

            return JsonResponse({
                "status_code": 0,
                "message": status
            })

        subdevice = vue_json["subdevice_name"]
        enable = vue_json["enable"]
        obj = SubDevice.objects.filter(subdevice_name=subdevice).update(subdevice_enable=enable)

        cls_log = get_subdevicelog_model(subdevice)

        if enable:
            # 新增一条log
            remark = " 设备《" + subdevice + "》启用成功! "
            cls_log.objects.create(subdevice_name=subdevice, remark=remark)
            conn.hset(subdevice, "device_enable", 1)
            return JsonResponse({
                "status_code": 0,
                "message": "启用成功"
            })
        else:
            set_disenable(subdevice)
            # 新增一条log
            remark = " 设备《" + subdevice + "》禁用成功! "
            cls_log.objects.create(subdevice_name=subdevice, remark=remark)
            return JsonResponse({
                "status_code": 0,
                "message": "禁用成功"
            })


# /apis/device/list
@csrf_exempt
def List(request):
    """
    用于提供設備列表数据
    :param request: HttpRequest
    :return: Json
    """

    def status(row):
        conn = get_redis_connection("default")
        collect_drive = 0

        res = 0 if conn.hget(row["subdevice_name"], 'drive_enable') is None else int(
            conn.hget(row["subdevice_name"], 'drive_enable'))
        if res:
            # row["subdevice_status"] = choice(["采集驱动&传输驱动", '传输驱动', '采集驱动','暂无驱动'])
            collect_drive = 1
        keys = "path_{}_*".format(row["subdevice_name"])
        path_keys = conn.keys(keys)
        path_drive = 0
        for path_key in path_keys:
            if int(conn.hget(path_key.decode(), "path_enable")):
                path_drive = 1
        if collect_drive + path_drive == 2:
            row["subdevice_status"] = "采集驱动&传输驱动"
        elif collect_drive + path_drive == 1:
            if collect_drive:
                row["subdevice_status"] = "采集驱动"
            if path_drive:
                row["subdevice_status"] = "传输驱动"
        else:
            row["subdevice_status"] = "暂无驱动运行"

        return row

    if request.method == "GET":

        row_data = SubDevice.objects.all().order_by('-id').values("subdevice_name", "subdevice_status",
                                                                  'subdevice_online_time', "subdevice_model",
                                                                  'subdevice_enable', 'subdevice_position',
                                                                  'subdevice_type')
        db = []
        for row in row_data:
            row["subdevice_online_time"] = row["subdevice_online_time"].strftime("%Y-%m-%d %H:%M:%S")
            row = status(row)
            db.append(row)

        return JsonResponse({
            "status_code": 0,
            "db": db
        })


# apis/device/type
@csrf_exempt
def Type(request):
    '''
    用于提供添加设备的设备类型列表
    :param request: HttpRequest
    :return: Json
    '''

    if request.method == "GET":
        type_dict = ["生产设备类", "压铸设备类", "环境设备类", "机床设备类", "仪表设备类",
                     "注塑成型设备类", "包装设备类", "工控设备类", "传感器设备类", "SMT设备类",
                     "冲压设备类", "表面处理设备类", "运输设备类", "其他"]
        db = []
        for index, type_val in enumerate(type_dict):
            data = {"index": index, "value": type_val}
            db.append(data)

        return JsonResponse({
            "status_code": 0,
            "db": db
        })


# apis/device/protocollist
@csrf_exempt
def protocolList(request):
    '''
    用于提供添加设备协议的协议类型列表
    :param request: HttpRequest
    :return: Json
    '''
    if request.method == "GET":
        protocolList = []

        type_1 = {
            "value": 'RS485/RS232/USB接口',
            "label": 'RS485/RS232/USB接口',
            "children": [
                {
                    "value": 'Modbus-RTU',
                    "label": 'Modbus-RTU'
                },
            ]
        }

        type_2 = {
            "value": 'Ethernet接口',
            "label": 'Ethernet接口',
            "children": [
                {
                    "value": 'Modbus-TCP',
                    "label": 'Modbus-TCP',
                },
                {
                    "value": 'OPC-UA',
                    "label": 'OPC-UA',
                    "disabled": True,
                },
                {
                    "value": 'MQTT',
                    "label": 'MQTT',
                    # "disabled": True,
                },
                {
                    "value": 'DB',
                    "label": 'DB',
                    "children": [
                        {
                            "value": 'MySQL',
                            "label": 'MySQL',
                            "disabled": True,
                        },
                        {
                            "value": 'SQLServer',
                            "label": 'SQLServer',
                            "disabled": True,
                        }, ]
                }
            ]
        }

        type_3 = {
            "value": '专有协议接口',
            "label": '专有协议接口',
            "children": [
                {
                    "value": 'Canis Pro采集卡',
                    "label": 'Canis Pro采集卡',
                    "disabled": False,
                },
                {
                    "value": 'NI-DAQmx',
                    "label": 'NI-DAQmx',
                    "disabled": False,
                },
                {
                    "value": 'PLC',
                    "label": 'PLC',
                    "children": [
                        {
                            "value": 'S7-200',
                            "label": 'S7-200',
                            "disabled": True,
                        },
                        {
                            "value": 'FX-3U',
                            "label": 'FX-3U',
                            "disabled": True,
                        },
                        {
                            "value": 'FX-5U',
                            "label": 'FX-5U',
                            "disabled": True,
                        }, ]
                },
                {
                    "value": 'Robot',
                    "label": 'Robot',
                    "children": [
                        {
                            "value": 'Foxbot',
                            "label": 'Foxbot',
                            "disabled": True,
                        },
                        {
                            "value": 'CR750',
                            "label": 'CR750',
                            "disabled": True,
                        }, ]
                },
                {
                    "value": 'SMT',
                    "label": 'SMT',
                    "children": [
                        {
                            "value": 'TRI_7007_SPI',
                            "label": 'TRI_7007_SPI',
                            # "disabled": True,
                        },
                        {
                            "value": 'TRI_7500_II_AOI',
                            "label": 'TRI_7500_II_AOI',
                            # "disabled": True,
                        },
                        {
                            "value": 'TRI_7500_III_AOI',
                            "label": 'TRI_7500_III_AOI',
                            # "disabled": True,
                        },
                        {
                            "value": 'HITACHI_SIGMA_G5A',
                            "label": 'HITACHI_SIGMA_G5A',
                            # "disabled": True,
                        },
                        {
                            "value": 'KOH_YOUNG_SPI',
                            "label": 'KOH_YOUNG_SPI',
                            # "disabled": True,
                        },
                        {
                            "value": 'KOH_YOUNG_AOI',
                            "label": 'KOH_YOUNG_AOI',
                            # "disabled": True,
                        },
                    ]
                },
                {
                    "value": 'CNC',
                    "label": 'CNC',
                    "disabled": True,
                },

            ]
        }

        protocolList.append(type_1)
        protocolList.append(type_2)
        protocolList.append(type_3)
        # conn = get_redis_connection("default")

        return JsonResponse({
            "status_code": 0,
            "db": protocolList,
            "drive_status": True
        })


@csrf_exempt
def templateUpdate(request):
    '''
    用于修改设备模板
    :param request:
    :return:
    '''
    if request.method == "POST":
        try:
            vue_json = json.loads(request.body.decode())
            template_name = vue_json.get("template_name")
            # code_list = vue_json.get("code_list")

            etr = EquipmentTemplateRtu.objects.filter(etr_name=template_name)
            template_remark = etr[0].etr_remark
            accordname = etr[0].etr_accordname
            etr.delete()
            for row in vue_json.get("code_list"):
                if row["format"] == "2进制输出":
                    row["format"] = 0
                elif row["format"] == "10进制输出":
                    row["format"] = 1
                elif row["format"] == "16进制输出":
                    row["format"] = 2
                elif row["format"] == "IEEE-754输出":
                    row["format"] = 3
                elif row["format"] == "DATA-2301输出":
                    row["format"] = 4
                elif row["format"] == "浮点型输出":
                    row["format"] = 5
                etr = EquipmentTemplateRtu.objects.create(etr_name=template_name,
                                                          etr_remark=template_remark,
                                                          etr_accordname=accordname,
                                                          etr_code=row["function_code"],
                                                          etr_register=row["start_register"],
                                                          etr_register_num=row["register_num"],
                                                          etr_param=row["property"],
                                                          etr_format=row["format"],
                                                          etr_rule_sign=row["rule"]["sign"],
                                                          etr_rule_number=row["rule"]["number"])
                etr.save()
            remark = " 設備模板《" + template_name + "》修改成功! "
            event = get_event_model.objects.create(event_level="warning", event_remark=remark, event_username="admin")
            event.save()
            return JsonResponse({
                "status_code": 0,
                "message": "创建成功"
            })


        except Exception as e:
            print(e)
            return JsonResponse({
                "status_code": 1,
                "error": str(e)
            })


@csrf_exempt
def templateDelete(request):
    '''
    用于刪除设备模板
    :param request:
    :return:
    '''
    if request.method == "POST":
        try:
            vue_json = json.loads(request.body.decode())
            print(vue_json)
            template_name = vue_json.get("template_name")
            #conn = get_redis_connection('default')
            #conn.delete(template_name)

            etr = EquipmentTemplateRtu.objects.filter(etr_name=template_name).delete()
            etc = EquipmentTemplateCanis.objects.filter(etc_name=template_name).delete()

            remark = " 設備模板《" + template_name + "》刪除成功! "
            event = get_event_model.objects.create(event_level="warning", event_remark=remark, event_username="admin")
            event.save()

            return JsonResponse({
                "status_code": 0,
                "message": "模板刪除成功！"
            })
        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "error": str(e)
            })


# apis/device/template/create
@csrf_exempt
def templateCreate(request):
    '''
    用于创建一个新的设备模板
    :param request:
    :return:
    '''
    if request.method == "POST":
        try:
            vue_json = json.loads(request.body.decode())
            print(vue_json)
            template_name = vue_json.get("template_name")
            template_remark = vue_json.get("template_remark")
            accordname = vue_json.get("accordname")[1]
            if vue_json.get("type") == "modbus":
                for row in vue_json.get("code_list"):
                    # print(row)
                    etr = EquipmentTemplateRtu.objects.create(etr_name=template_name,
                                                              etr_remark=template_remark,
                                                              etr_accordname=accordname,
                                                              etr_code=row["function_code"],
                                                              etr_register=row["start_register"],
                                                              etr_register_num=row["register_num"],
                                                              etr_param=row["property"],
                                                              etr_format=row["format"],
                                                              etr_rule_sign=row["rule"]["sign"],
                                                              etr_rule_number=row["rule"]["number"])
                    etr.save()
            elif vue_json.get("type") == "canispro":
                for row in vue_json.get("code_list"):
                    print(row)
                    etc = EquipmentTemplateCanis.objects.create(etc_name=template_name,
                                                                etc_remark=template_remark,
                                                                etc_accordname=accordname,
                                                                etc_pip_no=row["pip_no"],
                                                                etc_col=row["col"],
                                                                etc_format=row["dtype"],
                                                                etc_round=row["round"])
                    etc.save()
            return JsonResponse({
                "status_code": 0,
                "message": "创建成功"
            })

        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "error": str(e)
            })


# apis/device/template
@csrf_exempt
def templateList(request):
    '''
        用于提供设备模板列表
        :param request: HttpRequest
        :return: Json
        {
              name: 'HC31A电表',
              protocol: 'ModBus',
              createTime: '2019-05-25 13:52:47',
              description: 'HC31A电表配置模板',
              info: {
                row1: {
                  Aa:  ["0x000a",2],
                  Bb:  ["0x000a",2],
                  Cc:  ["0x000a",2],
                  Dd:  ["0x000a",2],
                },
                row2: {
                  Bb:  ["0x000a",2],
                  Cc:  ["0x000a",2],
                  Dd:  ["0x000a",2],
                }
              }
          }
        '''
    conn = get_redis_connection("default")

    def select(rows, dtype):
        templateList = []
        if dtype == "modbus":
            for etr in rows:
                template = EquipmentTemplateRtu.objects.filter(etr_name=etr["etr_name"])
                data = {}
                data["name"] = etr["etr_name"]
                data["protocol"] = etr["etr_accordname"]
                data["description"] = etr["etr_remark"]
                data["info"] = []
                data["info2"] = []

                row = 0
                for index, tmp in enumerate(template):
                    data["createTime"] = tmp.create_time.strftime("%Y-%m-%d %H:%M:%S")
                    if index % 4 == 0:
                        data["info"].append({})
                        row += 1
                    data["info"][row - 1][index] = {"property": tmp.etr_param,
                                                    "register": {
                                                        "startRegister": "0x" + tmp.etr_register,
                                                        "number": int(tmp.etr_register_num, 16),
                                                        "format": tmp.get_etr_format_display(),
                                                    }
                                                    }
                    data["info2"].append({
                        "function_code": tmp.etr_code,
                        "start_register": tmp.etr_register,
                        "register_num": tmp.etr_register_num,
                        "property": tmp.etr_param,
                        "format": tmp.get_etr_format_display(),
                        "remark": tmp.etr_remark,
                        "rule": {
                            "sign": tmp.etr_rule_sign,
                            "number": tmp.etr_rule_number
                        },
                    })
                templateList.append(data)
            return templateList
        elif dtype == "canis":
            for etc in rows:
                template = EquipmentTemplateCanis.objects.filter(etc_name=etc["etc_name"])
                print(template)
                data = {}
                data["name"] = etc["etc_name"]
                data["protocol"] = etc["etc_accordname"]
                data["description"] = etc["etc_remark"]
                data["info"] = []
                # data["info2"] = []
                row = 0
                for index, tmp in enumerate(template):
                    data["createTime"] = tmp.create_time.strftime("%Y-%m-%d %H:%M:%S")
                    if index % 4 == 0:
                        data["info"].append({})
                        row += 1
                    data["info"][row - 1][index] = {"Column": tmp.etc_col,
                                                    "Pip": {
                                                        "No": tmp.get_etc_pip_no_display(),
                                                        "DataType": tmp.get_etc_format_display(),
                                                        "Round": tmp.etc_round
                                                    }
                                                    }
                    # data["info2"].append({
                    #     "function_code": tmp.etr_code,
                    #     "start_register": tmp.etr_register,
                    #     "register_num": tmp.etr_register_num,
                    #     "property": tmp.etr_param,
                    #     "format": tmp.get_etr_format_display(),
                    #     "remark": tmp.etr_remark,
                    #     "rule": {
                    #         "sign": tmp.etr_rule_sign,
                    #         "number": tmp.etr_rule_number
                    #     },
                    # })
                templateList.append(data)
            return templateList

    if request.method == "GET":
        templateList = []
        # print(request.GET)
        vue_List = list(request.GET.getlist("typeSelected[]"))
        print(vue_List)
        subdevice = request.GET.get("subdevice")  # 设备列表进入设备管理
        res = 0 if conn.hget(subdevice, "drive_enable") is None else int(conn.hget(subdevice, "drive_enable"))
        drive_status = False if res == 0 else True
        if subdevice != None:
            print("设备默认模板")
            template = None if conn.hget(subdevice, "template") is None else conn.hget(subdevice, "template").decode()

            if template == "rtu":
                apply_rtu = applyTemplateRtuInterface.objects.filter(apply_rtu_device=subdevice)
                etrs = EquipmentTemplateRtu.objects.values("etr_name", "etr_accordname", "etr_remark", ) \
                    .filter(etr_name=apply_rtu[0].apply_rtu_template).annotate(num=Count("etr_name"))
                templateList = select(etrs, "modbus")
                return JsonResponse({
                    "status_code": 0,
                    "db": templateList,
                    "drive_status": drive_status
                })
            elif template == "tcp":
                apply_tcp = applyTemplateTcpInterface.objects.filter(apply_tcp_device=subdevice)
                etrs = EquipmentTemplateRtu.objects.values("etr_name", "etr_accordname", "etr_remark", ) \
                    .filter(etr_name=apply_tcp[0].apply_tcp_template).annotate(num=Count("etr_name"))
                templateList = select(etrs, "modbus")
                return JsonResponse({
                    "status_code": 0,
                    "db": templateList,
                    "drive_status": drive_status
                })
            elif template == "canis":
                apply_canis = applyTemplateCanisInterface.objects.filter(apply_canis_device=subdevice)
                etcs = EquipmentTemplateCanis.objects.values("etc_name", "etc_accordname", "etc_remark", ) \
                    .filter(etc_name=apply_canis[0].apply_canis_template).annotate(num=Count("etc_name"))
                templateList = select(etcs, "canis")
                return JsonResponse({
                    "status_code": 0,
                    "db": templateList,
                    "drive_status": drive_status
                })
            else:
                return JsonResponse({
                    "status_code": 1,
                    "db": [],
                })

        if vue_List == []:
            print("所有协议模板")
            etrs = EquipmentTemplateRtu.objects.values("etr_name", "etr_accordname", "etr_remark", ) \
                .all().annotate(num=Count("etr_name"))
            templateList1 = select(etrs, "modbus")
            etcs = EquipmentTemplateCanis.objects.values("etc_name", "etc_accordname", "etc_remark", ) \
                .all().annotate(num=Count("etc_name"))
            templateList2 = select(etcs, "canis")

            templateList = templateList1 + templateList2
            # info = [t["info2"][0] for t in templateList]

            return JsonResponse({
                "status_code": 1,
                # "info" : info,
                "db": templateList
            })

        if vue_List[1] == "Modbus-RTU" or vue_List[1] == "Modbus-TCP":
            etrs = EquipmentTemplateRtu.objects.values("etr_name", "etr_accordname", "etr_remark", ) \
                .filter(etr_accordname=vue_List[1]) \
                .annotate(num=Count("etr_name"))
            # print(etrs)
            templateList = select(etrs, "modbus")
            return JsonResponse({
                "status_code": 1,
                "db": templateList,
                "drive_status": drive_status
            })
        elif vue_List[1] == "Canis Pro采集卡":
            etcs = EquipmentTemplateCanis.objects.values("etc_name", "etc_accordname", "etc_remark", ) \
                .filter(etc_accordname=vue_List[1]) \
                .annotate(num=Count("etc_name"))
            # print(etrs)
            templateList = select(etcs, "canis")
            return JsonResponse({
                "status_code": 1,
                "db": templateList,
                "drive_status": drive_status
            })
    if request.method == "POST":
        try:
            # print(request.body.decode())
            vue_json = json.loads(request.body.decode())
            print(vue_json)
            if request.GET.get("select") is not None:
                select_templatename = vue_json.get("select_templatename")
                type = vue_json.get("type")
                if type == "Modbus-RTU" or type == "Modbus-TCP":
                    # 查看设备模板名是否存在
                    etr = EquipmentTemplateRtu.objects.filter(etr_name=select_templatename).count()
                    if etr:
                        return JsonResponse({
                            "status_code": 1,
                            "is_indb": 1
                        })
                elif type == "Canis Pro采集卡":
                    # 查看设备模板名是否存在
                    etc = EquipmentTemplateCanis.objects.filter(etc_name=select_templatename).count()
                    if etc:
                        return JsonResponse({
                            "status_code": 1,
                            "is_indb": 1
                        })

                # 此处则代表模板名不存在 可添加
                return JsonResponse({
                    'status_code': 0,
                    "is_indb": 0
                })


        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "error": str(e)
            })


# apis/device/modbusrtufrom
@csrf_exempt
def modbusRtuForm(request):
    '''
    用于提供Modbus-RTU的from表单select
    :param request:
    :return:
    '''
    if request.method == "GET":
        form = {}
        port_list = list(serial.tools.list_ports.comports())
        serialList = [{"index": v[0], "value": v[1].split("(")[0]} for v in port_list]
        # serialList[0]["disabled"] = True
        # serialList[1]["disabled"] = True
        bitList = [{"index": v, "value": "bit"} for i, v in enumerate(["5", "6", "7", '8'])]
        baudRateList = [{"index": v, "value": "bps"} for i, v in
                        enumerate(["1200", "2400", "4800", '9600', "19200", "38400", "115200"])]
        parityList = [{"index": v, "value": v} for i, v in enumerate(["None,无校验", "Even,偶校验", 'Odd,奇校验'])]
        stopBitList = [{"index": v, "value": "bit"} for i, v in enumerate(["0", "1", "2"])]
        timeoutList = [{"index": v, "value": "second"} for i, v in
                       enumerate(["0.3", "0.5", "0.8", "1.0", "2.0", '3.0'])]
        cycleList = [{"index": str(v), "value": "second"} for v in range(3, 50)]
        addressList = [{"index": i, "value": i} for i in range(1, 248, 1)]
        drive_name = Drive.objects.filter(drive_type="Modbus-RTU").values("drive_name")
        driveList = [{"index": drive["drive_name"], "value": drive["drive_name"]} for drive in drive_name]
        # driveList = [{"index":"ModbusRtuDemo", "value":"ModbusRtuDemo"} for i in range(0, 1, 1)]

        form["serialList"] = serialList
        form["baudRateList"] = baudRateList
        form["stopBitList"] = stopBitList
        form["bitList"] = bitList
        form["parityList"] = parityList
        form["timeoutList"] = timeoutList
        form["cycleList"] = cycleList
        form["addressList"] = addressList
        form["driveList"] = driveList
        return JsonResponse({
            "status_code": 0,
            "db": form
        })


# apis/device/canisprofrom
@csrf_exempt
def canisproForm(request):
    '''
        用于提供Canis Pro的from表单select
        :param request:
        :return:
        '''
    if request.method == "GET":
        form = {}
        modeList = [{"index": "A", "value": "HPS_MODE(默认)"}, {"index": "B", "value": "HPS_MODE"}]
        bufferSizeList = [{"index": str(v), "value": "HPS_BUFFER_SIZE"} for v in
                          ("128K", "256K", "512K", "1M", "2M", "4M", "8M", "16M")]
        sampleRatelist = [{"index": str(v) + "K", "value": "HPS_SAMPLE_RATE"} for v in
                          (1, 2, 4, 8, 16, 32, 64, 128, 256)]
        triggerList = [{"index": "IO触发", "value": "(默认)"}]

        drive_name = Drive.objects.filter(drive_type="Canis-Pro").values("drive_name")
        driveList = [{"index": drive["drive_name"], "value": drive["drive_name"]} for drive in drive_name]
        # driveList = [{"index":"ModbusTcpDriveDemo", "value":"ModbusTcpDriveDemo"} for i in range(0, 1, 1)]
        form["modeList"] = modeList
        form["bufferSizeList"] = bufferSizeList
        form["sampleRatelist"] = sampleRatelist
        form["triggerList"] = triggerList
        form["driveList"] = driveList
        return JsonResponse({
            "status_code": 0,
            "db": form
        })


# apis/device/modbustcpfrom
@csrf_exempt
def modbusTcpForm(request):
    '''
    用于提供Modbus-Tcp的from表单select
    :param request:
    :return:
    '''
    if request.method == "GET":
        form = {}
        cycleList = [{"index": str(v), "value": "second"} for v in range(3, 50)]
        timeoutList = [{"index": v, "value": "second"} for i, v in enumerate(["1.0", "2.0", '3.0', '4.0', '5.0'])]
        addressList = [{"index": i, "value": i} for i in range(1, 248, 1)]
        drive_name = Drive.objects.filter(drive_type="Modbus-TCP").values("drive_name")
        driveList = [{"index": drive["drive_name"], "value": drive["drive_name"]} for drive in drive_name]
        # driveList = [{"index":"ModbusTcpDriveDemo", "value":"ModbusTcpDriveDemo"} for i in range(0, 1, 1)]
        form["timeoutList"] = timeoutList
        form["cycleList"] = cycleList
        form["addressList"] = addressList
        form["driveList"] = driveList
        return JsonResponse({
            "status_code": 0,
            "db": form
        })


# apis/device/auth
@csrf_exempt
def Auth(request):
    '''
    用于提供MQTT 客户端测试接口
    :param request:
    :return:
    '''

    def mqtt_auth():
        try:
            print(mqtt_ip, mqtt_port)
            mqttclient = mqtt_client_connect(broker=mqtt_ip, port=int(mqtt_port), username=mqtt_username,
                                             password=mqtt_pwd)
            if mqttclient.flag == 0:
                return 0
            elif mqttclient.flag == 1:
                mqttclient.mqttc.loop_stop()
                mqttclient.mqttc.disconnect()
                return 1
        except:
            return 0

    if request.method == "GET":

        auth_type = request.GET.get("authtype")
        if auth_type == "第三方MQTT":
            mqtt_ip = request.GET.get("host")
            mqtt_port = request.GET.get("port")
            mqtt_username = request.GET.get("username")
            mqtt_pwd = request.GET.get("pwd")
            result = mqtt_auth()
            if result == 0:
                return JsonResponse({
                    "status_code": 1,
                    "error": "连接失败！"
                })

        return JsonResponse({
            "status_code": 0,
            "message": "测试连接成功！"
        })


# apis/device/pathinfo
@csrf_exempt
def pathInfo(request):
    '''
    用于提供数据转发页面的狀態詳情
    :param request:
    :return:
    '''
    if request.method == "GET":
        subdevice = request.GET.get("subdevice")
        path_name = request.GET.get("path_name")
        path_type = request.GET.get("path_type")

        path_key = "m5path_{}_{}".format(subdevice.split("_")[2], subdevice.split("_")[1][1]) if "m5_0" == subdevice[
                                                                                                           0:4] else "path_{}_{}".format(
            subdevice, path_name)
        conn = get_redis_connection("default")
        status = json.loads(conn.hget(path_key, "path_status").decode())
        print(status)
        sub = []
        # if path_type == "第三方MQTT" or path_type == "MQTT":
        sub = [{
            "host": conn.hget(path_key, "path_host").decode(),
            "port": conn.hget(path_key, "path_port").decode(),
            "sub": conn.hget(path_key, "path_topic").decode()
        }]
        if path_type == 'DB':
            sub = [{
                "host": conn.hget(path_key, "path_host").decode(),
                "port": conn.hget(path_key, "path_port").decode(),
                "sub": conn.hget(path_key, "path_topic").decode() + ":path_" + subdevice + "_" + path_name
            }]
        # elif path_type == "DB":

        return JsonResponse({
            'status': status,
            'sub': sub
        })


# apis/device/path/delete
@csrf_exempt
def pathDelete(request):
    '''
     用于提供数据转发页面的删除转发路径的接口
    :param request:
    :return:
    '''
    if request.method == "POST":
        try:
            vue_json = json.loads(request.body.decode())
            print(vue_json)
            conn = get_redis_connection('default')
            subdevice = vue_json["subdevice_name"]
            path_name = vue_json["path_name"]
            key = "path_{}_{}".format(subdevice, path_name)
            obj = Path.objects.filter(path_name=path_name, subdevice_name=subdevice)
            obj.delete()
            conn.delete(key)
            cls_log = get_subdevicelog_model(vue_json["subdevice_name"])

            # 新增一条log
            remark = " 设备《" + vue_json["subdevice_name"] + "》转发路径 =" + vue_json["path_name"] + "= 删除成功! "
            cls_log.objects.create(subdevice_name=vue_json["subdevice_name"], remark=remark)
            return JsonResponse({
                "status_code": 0,
                "message": "操作成功！"
            })
        except Exception as e:
            return JsonResponse({
                "status_code": 1,
                "message": "操作失败！" + str(e)
            })


# apis/device/path/enable
@csrf_exempt
def pathEnable(request):
    '''
    用于提供数据转发页面的创建转发路径接口
    :param request:
    :return:
    '''

    def run_transmit_task():
        """
        判断缓存里面设备path的enable if num(enable)==1 run task
        :return:
        """
        # keys = "path_{}_*".format(subdevice)
        keys = "m5path_{}_*".format(subdevice.split("_")[2]) if "m5_0" == subdevice[:4] else "path_{}_*".format(
            subdevice)

        path_keys = conn.keys(keys)
        num = 0
        for path in path_keys:
            enable = conn.hget(path.decode(), "path_enable")
            if int(enable):
                num += 1
        # print("num:",num)
        if num == 1:
            result = DriveForTransmit.apply_async(kwargs={"subdevice_name": subdevice}, queue="worker_queue")
            print("apply async")

    def check_enable():
        # print("result:", conn.hget(subdevice, "device_enable"))
        if int(conn.hget(subdevice, "device_enable")):
            conn.hset(key, "path_enable", 1)
            return 1
        else:
            return 0

    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        print(vue_json)
        conn = get_redis_connection('default')
        subdevice = vue_json["subdevice_name"]
        path_name = vue_json["path_name"]
        enable = vue_json["enable"]
        key = "m5path_{}_{}".format(subdevice.split("_")[2], subdevice.split("_")[1][1]) if "m5_0" == subdevice[
                                                                                                      :4] else "path_{}_{}".format(
            subdevice, path_name)
        # key = "path_{}_{}".format(subdevice, path_name)
        cls_log = get_subdevicelog_model(subdevice)

        if enable:
            result = check_enable()  # 判斷設備的啟用狀態
            if result:
                run_transmit_task()
                if "m5_0" != subdevice[:4]:
                    obj = Path.objects.filter(path_name=path_name, subdevice_name=subdevice).update(path_enable=enable)
                # 新增一条log
                remark = " 设备《" + subdevice + "》转发路径 =" + path_name + "= 已启用! "
                cls_log.objects.create(subdevice_name=subdevice, remark=remark)
                return JsonResponse({
                    "status_code": 0,
                    "message": "启用成功"
                })
            else:
                return JsonResponse({
                    "status_code": 1,
                    "message": "設備被禁用, 在设备列表可重新启用该设备！"
                })
        else:
            if "m5_0" != subdevice[:4]:
                obj = Path.objects.filter(path_name=path_name, subdevice_name=subdevice).update(path_enable=enable)
            conn.hset(key, "path_enable", 0)
            # 新增一条log
            remark = " 设备《" + subdevice + "》转发路径 =" + path_name + "= 已关闭! "
            cls_log.objects.create(subdevice_name=subdevice, remark=remark)
            return JsonResponse({
                "status_code": 0,
                "message": "禁用成功"
            })


# apis/device/path
@csrf_exempt
def pathList(request):
    '''
    用于提供数据转发页面的创建转发路径接口
    :param request:
    :return:
    '''

    def run_transmit_task(subdevice):
        """
        判断缓存里面设备path的enable if num(enable)==1 run task
        :return:
        """
        # keys = "path_{}_*".format(subdevice)
        keys = "m5path_{}_*".format(subdevice.split("_")[2]) if "m5_0" == subdevice[:4] else "path_{}_*".format(
            subdevice)

        path_keys = conn.keys(keys)
        num = 0
        for path in path_keys:
            enable = conn.hget(path.decode(), "path_enable")
            if int(enable):
                num += 1
        print("num:", num)
        if num == 1:
            result = DriveForTransmit.apply_async(kwargs={"subdevice_name": subdevice}, queue="worker_queue")

    if request.method == "GET":
        conn = get_redis_connection("default")
        subdevice_name = request.GET.get("subdevice")
        if "m5_0" == subdevice_name[:4]:
            device = subdevice_name.split("_")[2]
            key = "m5path_{}_*".format(device)
            paths = conn.keys(key)
            path_list = [{"addressName": conn.hget(path, "path_name").decode(),
                          'type': conn.hget(path, "path_type").decode(),
                          "createTime": conn.hget(path, "path_createtime").decode(),
                          "switch": True if int(conn.hget(path, "path_enable").decode()) else False,
                          "mesNumber": int(conn.hget(path, "path_count").decode()),
                          "path_msg": json.loads(conn.hget(path, "path_msg").decode())
                          } for path in paths]

            return JsonResponse({
                "status_code": 0,
                "db": path_list,
            })

        path_key = "path_{}_".format(subdevice_name)
        db = Path.objects.filter(subdevice_name=subdevice_name).order_by("-id").values()

        path_list = [{"addressName": path["path_name"],
                      'type': path["path_type"],
                      "createTime": path["create_time"].strftime("%Y-%m-%d %H:%M:%S"),
                      "switch": True if int(conn.hget(path_key + path["path_name"], "path_enable").decode()) else False,
                      # "mesNumber": 1,
                      "mesNumber": int(conn.hget(path_key + path["path_name"], "path_count")),
                      "path_msg": json.loads(conn.hget(path_key + path['path_name'], "path_msg").decode())
                      } for path in db]

        return JsonResponse({
            "status_code": 0,
            "db": path_list,
        })
    if request.method == "POST":
        vue_json = json.loads(request.body.decode())
        print(vue_json)
        conn = get_redis_connection('default')
        if request.GET.get("select") is not None:
            select_path = vue_json.get("select_path")
            # print(select_path)
            path = Path.objects.filter(path_name=select_path).count()
            if path:
                return JsonResponse({
                    "status_code": 1,
                    "is_indb": 1
                })
            return JsonResponse({
                'status_code': 0,
                "is_indb": 0
            })
        else:
            subdevice = vue_json["subdevice"]
            key = 'path_' + vue_json["subdevice"] + '_' + vue_json["params"]["name"]
            count = Path.objects.filter(subdevice_name=subdevice).count()
            print("count:", count)
            if count >= 4:
                return JsonResponse({
                    "status_code": 1,
                    "error": "每台设备四条转发路径上限！",
                })
            # print(vue_json)

            if "MQTT" in vue_json["path_type"]:
                vue_json = vue_json["params"]
                print("MQTT")
                path = Path.objects.create(path_name=vue_json["name"], path_type="第三方MQTT",
                                           subdevice_name=subdevice, path_ip=vue_json["ip"],
                                           path_port=vue_json["port"], path_sub=vue_json["pubtopic"], path_enable=True)
                path.save()

                conn.hset(key, "path_type", "第三方MQTT")
                conn.hset(key, "path_name", vue_json["name"])
                conn.hset(key, "path_host", vue_json["ip"])
                conn.hset(key, "path_port", vue_json["port"])
                conn.hset(key, "path_username", vue_json["userName"])
                conn.hset(key, "path_pwd", vue_json["pwd"])
                conn.hset(key, "path_topic", vue_json["pubtopic"])
                conn.hset(key, "path_index", 0)
                conn.hset(key, "path_count", 0)
                status = {
                    "status_code": "1",
                    "message": "路徑未開啟！"
                }
                conn.hset(key, "path_status", json.dumps(status))
                conn.hset(key, "path_msg", '{"init":"初始化數據"}')
                conn.hset(key, "path_enable", 1)

            elif vue_json["path_type"] == "CorePro Server":
                print("CorePro", vue_json)
                vue_json = vue_json["params"]
                path = Path.objects.create(path_name=vue_json["name"], path_type="CorePro Server",
                                           subdevice_name=subdevice, path_ip="",
                                           path_port="", path_sub=vue_json["datatopic"], path_enable=True)
                path.save()

                row_data = RegisterInfo.objects.last()

                conn.hset(key, "path_type", "CorePro Server")
                conn.hset(key, "path_name", vue_json["name"])
                conn.hset(key, "path_host", row_data.gateway_iothost)
                conn.hset(key, "path_port", row_data.gateway_iotport)
                conn.hset(key, "path_username", row_data.gateway_iotid)
                conn.hset(key, "path_pwd", row_data.gateway_iottoken)
                conn.hset(key, "path_topic", vue_json["datatopic"])
                conn.hset(key, "path_datatype", vue_json["datatype"])
                conn.hset(key, "path_datatypeid", vue_json["datatypeid"])
                conn.hset(key, "path_index", 0)
                conn.hset(key, "path_count", 0)
                status = {
                    "status_code": "1",
                    "message": "驅動未開啟！"
                }
                conn.hset(key, "path_status", json.dumps(status))
                conn.hset(key, "path_msg", '{"init":"初始化數據"}')
                conn.hset(key, "path_enable", 1)

            elif "DB" in vue_json["path_type"]:
                vue_json = vue_json["params"]
                print("DB")
                path = Path.objects.create(path_name=vue_json["name"], path_type="DB",
                                           subdevice_name=subdevice, path_ip=vue_json["dbip"],
                                           path_port=vue_json["dbport"], path_sub=vue_json["dbname"], path_enable=True)
                path.save()

                conn.hset(key, "path_type", "DB")
                conn.hset(key, "path_name", vue_json["name"])
                conn.hset(key, "path_host", vue_json["dbip"])
                conn.hset(key, "path_port", vue_json["dbport"])
                conn.hset(key, "path_username", vue_json["dbuserName"])
                conn.hset(key, "path_pwd", vue_json["dbpwd"])
                conn.hset(key, "path_topic", vue_json["dbname"])
                conn.hset(key, "path_index", 0)
                conn.hset(key, "path_count", 0)
                status = {
                    "status_code": "1",
                    "message": "路徑未開啟！"
                }
                conn.hset(key, "path_status", json.dumps(status))
                conn.hset(key, "path_msg", '{"init":"初始化數據"}')
                conn.hset(key, "path_enable", 1)
            cls_log = get_subdevicelog_model(subdevice)

            # 新增一条log
            remark = " 设备《" + subdevice + "》转发路径 =" + vue_json["name"] + "= 添加成功! "
            cls_log.objects.create(subdevice_name=subdevice, remark=remark)

            run_transmit_task(subdevice)
            # 新增一条log
            remark = " 设备《" + subdevice + "》转发路径 =" + vue_json["name"] + "= 已启用! "
            cls_log.objects.create(subdevice_name=subdevice, remark=remark)
            return JsonResponse({
                "status_code": 0,
                "message": "创建成功",
            })


# apis/device/data
@csrf_exempt
def Data(request):
    '''
    用于提供特征提取页面表格数据
    :param request:
    :return:
    '''
    if request.method == "GET":
        subdevice = request.GET.get("subdevice")
        template_name = request.GET.get("template_name")
        if template_name is None:
            return JsonResponse({
                "status_code": 1,
                'message': "应用模板不能为空！"
            })
        conn = get_redis_connection("default")
        varlist = []
        try:
            varlist = eval(conn.hget(subdevice, template_name + '_varlist').decode())
        except:
            conn.hset(subdevice, template_name + '_varlist', [])

        row = int(request.GET.get("row"))

        cls = get_smartdevicedata_model(subdevice) if "m5_0" == subdevice[:4] else get_subdevicedata_model(subdevice)
        if row:
            # 用于提供特征提取页面的设备URI 最近n条数据
            print("row:", row)
            row_last_data = cls.objects.values("data", "id", 'create_time').order_by("-id")[:row]
            db = [json.loads(i["data"].replace("'", '"')) for i in row_last_data]
            print(db)
            for index, row in enumerate(db):
                add_json = {
                    "id": row_last_data[index]["id"],
                    "create_time": row_last_data[index]["create_time"].strftime("%Y-%m-%d %H:%M:%S")
                }
                row.update(add_json)
            print(db)
            data_db = []
            for row in db:
                data = {}
                if varlist == []:
                    for i in row:
                        data[i] = row[i]
                else:
                    for i in row:
                        if i in varlist:
                            data[i] = row[i]
                data_db.append(data)
            # db = [ {i: row[i]}  for i in row for row in db if i in varlist]
            # print(db)

            Total = cls.objects.count()

            return JsonResponse({
                "status_code": 0,
                "subdevice": subdevice,
                "Total": Total,
                "db": data_db,
            })

        else:
            # 默认 row=0 选最后一条
            # print(request.META)
            # header = '{}://{}:{}'.format(request.scheme, request.META["HTTP_X_FORWARDED_FOR"],
            #                              request.META["SERVER_PORT"])
            header = '{}://{}'.format(request.scheme, request.META["HTTP_X_FORWARDED_HOST"])
            # try:
            # header = '{}://{}'.format(request.scheme, request.META["HTTP_HOST"])[:-5]
            # except:
            #     header = 'http://127.0.0.1'
            try:
                print("row:", row)
                row_last_data = cls.objects.values("data", "create_time").last()
                row_last_data["create_time"] = row_last_data["create_time"].strftime("%Y-%m-%d %H:%M:%S")
                # print(row_last_data["create_time"])
                data = json.loads(row_last_data["data"].replace("'", '"'))
                if varlist == []:
                    tablaData = [{"property": i, "value": v, "create_time": row_last_data["create_time"]} for i, v in
                                 data.items()]
                else:
                    tablaData = [{"property": i, "value": v, "create_time": row_last_data["create_time"]} for i, v in
                                 data.items() if i in varlist]
                Total = cls.objects.count()

                key_list = []
                for key in data:
                    key_list.append({
                        "key": key,
                        "label": key,
                        "disabled": False
                    })
                return JsonResponse({
                    "status_code": 0,
                    "tableData": tablaData,
                    "formatData": data,
                    "Total": Total,
                    "URI": "{header}/apis/device/data?subdevice={subdevice}&template_name={template_name}&row=30".format(
                        header=header, subdevice=subdevice, template_name=template_name),
                    "key": key_list,
                })
            except Exception as e:
                print(str(e))
                return JsonResponse({
                    "status_code": 0,
                    "tableData": [],
                    "formatData": {},
                    "Total": 0,
                    "URI": "null",
                    "key": [],
                })


# apis/device/apply
@csrf_exempt
def showApply(request):
    '''
    用于提供特征提取页面模板接口数据
    :param request:
    :return:
    '''

    def rtu(apply_rtu, res):
        active = False if res == 0 else True
        apply_interface = []
        apply_interface.append(["驱动名称", apply_rtu[0].apply_rtu_drive])
        apply_interface.append(["驱动类型", "Modbus-RTU"])

        apply_interface.append(["驱动状态", active])
        apply_interface.append(["串口号", apply_rtu[0].apply_rtu_com])
        apply_interface.append(["Slave地址", apply_rtu[0].apply_rtu_slave])
        apply_interface.append(["波特率", apply_rtu[0].apply_rtu_botelv])
        apply_interface.append(["奇偶校验", apply_rtu[0].apply_rtu_parity])
        apply_interface.append(["数据位", apply_rtu[0].apply_rtu_databit])
        apply_interface.append(["停止位", apply_rtu[0].apply_rtu_stopbit])
        apply_interface.append(["回复超时", apply_rtu[0].apply_rtu_timeout])
        apply_interface.append(["读写周期", apply_rtu[0].apply_rtu_cycle])
        return apply_interface

    def tcp(apply_tcp, res):
        active = False if res == 0 else True

        apply_interface = []
        apply_interface.append(["驱动名称", apply_tcp[0].apply_tcp_drive])
        apply_interface.append(["驱动类型", "Modbus-TCP"])
        apply_interface.append(["驱动状态", active])
        apply_interface.append(["Slave地址", apply_tcp[0].apply_tcp_slave])
        apply_interface.append(["IP地址", apply_tcp[0].apply_tcp_ip])
        apply_interface.append(["端口号", apply_tcp[0].apply_tcp_port])
        apply_interface.append(["回复超时", apply_tcp[0].apply_tcp_timeout])
        apply_interface.append(["读写周期", apply_tcp[0].apply_tcp_cycle])
        return apply_interface

    def canis(apply_canis, res):
        active = False if res == 0 else True

        apply_interface = []
        apply_interface.append(["驱动名称", apply_canis[0].apply_canis_drive])
        apply_interface.append(["驱动类型", "Canis-Pro"])
        apply_interface.append(["驱动状态", active])
        apply_interface.append(["IP地址", apply_canis[0].apply_canis_ip])
        apply_interface.append(["端口号", apply_canis[0].apply_canis_port])
        apply_interface.append(["采集模式", apply_canis[0].apply_canis_mode])
        apply_interface.append(["采集频率", apply_canis[0].apply_canis_sampleRate])
        apply_interface.append(["缓存区大小", apply_canis[0].apply_canis_bufferSize])
        apply_interface.append(["觸發方式", apply_canis[0].apply_canis_trigger])
        return apply_interface

    if request.method == "GET":
        subdevice = request.GET.get("subdevice")
        # print(subdevice)
        conn = get_redis_connection("default")

        if "m5_0" == subdevice[:4]:
            smart_device = subdevice
            varlist = list()
            varlist.append(['通道序號', smart_device.split("_")[1]])
            varlist.append(['設備名稱', conn.hget(smart_device, "name").decode()])
            varlist.append(['採集狀態', "驅動採集正常" if int(conn.hget(smart_device, "device_enable")) else "驅動採集異常"])
            varlist.append(['串口号', conn.hget(smart_device, "com").decode()])
            varlist.append(['波特率', conn.hget(smart_device, "botelv").decode()])
            varlist.append(['In', conn.hget(smart_device, "In").decode()])
            varlist.append(["Out", conn.hget(smart_device, "Out").decode()])
            varlist.append(['握手時間', conn.hget(smart_device, "create_time").decode()])
            varlist.append(['採集描述', conn.hget(smart_device, "remark").decode()])
            return JsonResponse({
                "status_code": 1,
                "db": varlist,
                "template_name": "System"

            })
        res = 0 if conn.hget(subdevice, "drive_enable") is None else int(conn.hget(subdevice, "drive_enable"))

        template = None if conn.hget(subdevice, "template") is None else conn.hget(subdevice, "template").decode()
        drive_status_msg = '' if conn.hget(subdevice, "drive_status_msg") is None else conn.hget(subdevice,
                                                                                                 "drive_status_msg").decode()
        if template == "rtu":
            apply_rtu = applyTemplateRtuInterface.objects.filter(apply_rtu_device=subdevice)
            com, botelv = apply_rtu[0].apply_rtu_com, apply_rtu[0].apply_rtu_botelv
            status = ""
            try:
                with serial.Serial(com, baudrate=botelv, timeout=.3) as ser:
                    if ser.isOpen():
                        # print(com + " is open success ")
                        status = True
            except:
                status = False
            return JsonResponse({
                "status_code": 1,
                "db": rtu(apply_rtu, res),
                "template_name": apply_rtu[0].apply_rtu_template,
                "status": status,
                "drive_status": res,
                "drive_status_msg": drive_status_msg
            })
        elif template == "tcp":
            apply_tcp = applyTemplateTcpInterface.objects.filter(apply_tcp_device=subdevice)
            return JsonResponse({
                "status_code": 1,
                "db": tcp(apply_tcp, res),
                "template_name": apply_tcp[0].apply_tcp_template,
                "drive_status_msg": drive_status_msg

            })
        elif template == "canis":
            apply_canis = applyTemplateCanisInterface.objects.filter(apply_canis_device=subdevice)
            return JsonResponse({
                "status_code": 1,
                "db": canis(apply_canis, res),
                "template_name": apply_canis[0].apply_canis_template,
                "drive_status_msg": drive_status_msg

            })
        else:
            return JsonResponse({
                "status_code": 1,
                "db": []
            })


# apis/device/template/apply/
@csrf_exempt
def templateApply(request):
    '''
    用于提供Modbus-Tcp的from表单select
    :param request:
    :return:
    '''
    if request.method == "POST":
        # print(request.body.decode())
        vue_json = json.loads(request.body.decode())
        print(vue_json)
        conn = get_redis_connection("default")
        # print(vue_json)
        if vue_json.get("type") == "rtu":
            update_content = {
                "apply_rtu_template": vue_json["template_name"],
                "apply_rtu_com": vue_json["serial"],
                "apply_rtu_botelv": vue_json["baudRate"],
                "apply_rtu_databit": vue_json["databit"],
                "apply_rtu_parity": vue_json["parity"],
                "apply_rtu_stopbit": vue_json["stopBit"],
                "apply_rtu_timeout": vue_json["timeout"],
                "apply_rtu_cycle": vue_json["cycle"],
                "apply_rtu_slave": vue_json["address"],
                "apply_rtu_drive": vue_json["drive"],
                "apply_rtu_active": False
            }
            applyTemplateRtuInterface.objects.update_or_create(apply_rtu_device=vue_json["subdevice_name"],
                                                               defaults=update_content)
            conn.hset(vue_json["subdevice_name"], "template", "rtu")
            conn.hset(vue_json["subdevice_name"], "template_name", vue_json["template_name"])
        elif vue_json.get("type") == "tcp":
            update_content = {
                "apply_tcp_template": vue_json["template_name"],
                "apply_tcp_ip": vue_json["ip"],
                "apply_tcp_port": vue_json["port"],
                "apply_tcp_timeout": vue_json["timeout"],
                "apply_tcp_slave": vue_json["address"],
                "apply_tcp_drive": vue_json["drive"],
                "apply_tcp_cycle": vue_json["cycle"],
                "apply_tcp_active": False
            }
            applyTemplateTcpInterface.objects.update_or_create(apply_tcp_device=vue_json["subdevice_name"],
                                                               defaults=update_content)
            conn.hset(vue_json["subdevice_name"], "template", "tcp")
            conn.hset(vue_json["subdevice_name"], "template_name", vue_json["template_name"])
        elif vue_json.get("type") == "canis":
            update_content = {
                "apply_canis_template": vue_json["template_name"],
                "apply_canis_ip": vue_json.get("content")["ip"],
                "apply_canis_port": vue_json.get("content")["port"],
                "apply_canis_userName": vue_json.get("content")["userName"],
                "apply_canis_pwd": vue_json.get("content")["pwd"],
                "apply_canis_mode": vue_json.get("content")["mode"],
                "apply_canis_bufferSize": vue_json.get("content")["bufferSize"],
                "apply_canis_sampleRate": vue_json.get("content")["sampleRate"],
                "apply_canis_trigger": vue_json.get("content")["trigger"][0],
                "apply_canis_drive": vue_json.get("content")["drive"],
                "apply_canis_active": False
            }
            applyTemplateCanisInterface.objects.update_or_create(apply_canis_device=vue_json["subdevice_name"],
                                                                 defaults=update_content)
            conn.hset(vue_json["subdevice_name"], "template", "canis")
            conn.hset(vue_json["subdevice_name"], "template_name", vue_json["template_name"])

        cls_log = get_subdevicelog_model(vue_json["subdevice_name"])
        # 新增一条log
        remark = " 设备《" + vue_json["subdevice_name"] + "》应用模板 *" + vue_json["template_name"] + "* 成功! "
        cls_log.objects.create(subdevice_name=vue_json["subdevice_name"], remark=remark)

        return JsonResponse({
            "status_code": 0,
            "message": "模板应用成功"
        })


# apis/device/plot

# def plot(request):
#     '''
#
#     :param request:
#     :return:
#     '''
#     if request.method == "GET":
#         row =1000
#         subdevice = request.GET.get("subdevice")
#         param = request.GET.get("param")
#         param = param.split(")")[1] if param else ""
#         cls = get_smartdevicedata_model(subdevice) if "m5_0" == subdevice[:4] else get_subdevicedata_model(subdevice)
#         row_last_data = cls.objects.values("data", "id", 'create_time').order_by("-id")[:row]
#         db = [json.loads(i["data"].replace("'", '"')) for i in row_last_data]
#         for index, row in enumerate(db):
#             add_json = {
#                 "id": row_last_data[index]["id"],
#                 "create_time": row_last_data[index]["create_time"].strftime("%m-%d %H:%M:%S")
#             }
#             row.update(add_json)
#         db = [ {"create_time":i.get("create_time"), "value": i.get(param)} for i in db]
#
#         # plt.ion()
#         arr = np.array([ i.get("value") for i in db])
#         plt.figure(figsize=(8,4))
#         plt.title(param+" with TimeArea")
#         plt.xlabel("Time")
#         plt.ylabel(param)
#         plt.plot(arr)
#         plt.savefig(r"G:\edgebox_pro\vue_edgebox\src\assets\device\\"+ subdevice+r"_trend.png")
#         plt.figure(figsize=(8, 4))
#         plt.title(param + " with Xbar-s")
#         plt.xlabel("Time")
#         plt.ylabel(param)
#         plt.plot(arr)
#         plt.savefig(r"G:\edgebox_pro\vue_edgebox\src\assets\device\\" + subdevice + r"_control.png")
#         plt.figure(figsize=(8, 4))
#         plt.title(param + " with corr")
#         plt.xlabel("Time")
#         plt.ylabel(param)
#         plt.plot(arr)
#         plt.savefig(r"G:\edgebox_pro\vue_edgebox\src\assets\device\\" + subdevice + r"_corr.png")
#         print(arr.shape)
#         return JsonResponse({
#             "status_code": 1,
#             "db": db,
#             "img_list": [r"assets/device/"+subdevice+"_trend.png",
#                          r"assets/device/"+subdevice+"_control.png",
#                          r"assets/device/"+subdevice+"_corr.png",]
#         })
#         # print(db)

# apis/device/status_img
@csrf_exempt
def device_status(request):
    '''
    用于返回圖片
    :param request:
    :return:  img, attribute
    '''
    if request.method == "GET":
        subdevice = request.GET.get("subdevice")
        print(request.GET)
        conn = get_redis_connection("default")
        img_url = r"../../../assets/m5.png"
        cls = get_smartdevicedata_model(subdevice) if "m5_0" == subdevice[:4] else get_subdevicedata_model(subdevice)
        row_last_data = cls.objects.values("data", "create_time").last()
        attribute = []
        # {index: 0, value: 'None'},
        if row_last_data:
            for p, v in eval(row_last_data["data"]).items():
                if type(v).__name__ == "int" or type(v).__name__ == "float":
                    attribute.append("(float)" + p)
                else:
                    attribute.append("(str)" + p)
            attribute = [{"index": i, "value": a} for i, a in enumerate(attribute)]
            return JsonResponse({
                "status_code": 1,
                "img": img_url,
                "attribute": attribute

            })
        return JsonResponse({
            "status_code": 1,
            "img": img_url,
            "attribute": [{"index": 0, "value": 'None'}]

        })
