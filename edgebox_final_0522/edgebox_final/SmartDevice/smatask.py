#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/6/16

import json
from celery.task import Task
from django_redis import get_redis_connection

from SmartDevice.models import SmartSns
from plugins.mqtt_pub_sub import mqtt_client_connect as client


class M5MQTTCom(Task):
    name = "M5MQTTCom"
    conn = get_redis_connection('default')

    def run(self, *arg, **kwarg):
        self.mqttclient = client(broker="127.0.0.1",
                                 port=1883,
                                 username="iot2",
                                 password="iot22",
                                 client_id="EB001_iot2")
        self.mqttclient.mqttc.on_connect = self.on_connect

        self.mqttclient.mqttc.subscribe(topic="M5base")

        self.mqttclient.mqttc.on_message = self.on_message

        while int(self.conn.hget("Agent", "settings")) == 1:
            pass
        self.mqttclient.mqttc.disconnect()

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + ":" + str(msg.payload))
        append = ": " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload) + str(client._username)
        try:
            payload = dict(json.loads(msg.payload.decode("gbk")))
            print(payload)
            # {"SN001": "SN001"}
            subdevice = SmartSns.objects.create(smart_sname=list(payload.keys())[0],
                                                smart_sns=list(payload.values())[0],
                                                )
            subdevice.save()

        except Exception as e:
            print(e)

    def on_connect(self, client, userdata, flags, rc):
        # rc为0 返回连接成功
        if rc == 0:
            print(" OnConnetc, rc: " + str(rc) + " successful " + str(client._username))
            # self.mqttclient.mqttc.subscribe(topic=self.apply_interface.get("apply_mqtt_topic"))
            # self.mqttclient.mqttc.on_message = self.on_message
        else:
            print(" OnConnetc, rc: " + str(rc) + " unsuccessful" + " " + str(client._username))


class M5MQTTCom2(Task):
    name = "M5MQTTCom2"
    conn = get_redis_connection('default')

    def run(self, *arg, **kwarg):
        self.mqttclient = client(broker="127.0.0.1",
                                 port=1883,
                                 username="iot3",
                                 password="iot33",
                                 client_id="EB001_iot3")
        self.mqttclient.mqttc.on_connect = self.on_connect

        self.now_sns = eval(str(self.conn.hget("Smart", "now_sns"), encoding="utf-8"))

        for i in self.now_sns:
            self.topics = i  # EB需要订阅的各个主题
            print(self.topics)
            self.mqttclient.mqttc.subscribe(topic=i)
            print("ok sub " + i)

        self.mqttclient.mqttc.on_message = self.on_message

            # self.mqttclient.mqttc.publish(i + "_ts", self.payload)
            # print("ok pub " + i + " _ts")


        while int(self.conn.hget(self.conn.hget("Smart", "now_sname"), "smart_enable")) == 1:
            pass
        self.mqttclient.mqttc.disconnect()

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + ":" + str(eval(msg.payload)))
        payload = str(eval(msg.payload))

        for j in self.now_sns:
            self.mqttclient.mqttc.publish(j + "_ts", payload)
            print("ok pub " + j + " _ts")

    def on_connect(self, client, userdata, flags, rc):
        # rc为0 返回连接成功
        if rc == 0:
            print(" OnConnetc, rc: " + str(rc) + " successful " + str(client._username))
            # self.mqttclient.mqttc.subscribe(topic=self.apply_interface.get("apply_mqtt_topic"))
            # self.mqttclient.mqttc.on_message = self.on_message
        else:
            print(" OnConnetc, rc: " + str(rc) + " unsuccessful" + " " + str(client._username))
