#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/8/21
import ast

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
from paho.mqtt import publish
import json
import pymysql

host = "127.0.0.1"
port = 1883
client = mqtt.Client()
list_data = []


# 連接服務器
def on_connect():
    client.username_pw_set('iot', "iot123!")
    client.connect(host, port, 60)
    client.loop_start()


# 發佈消息
def on_publish(topic, payload, qos):
    client.publish(topic, payload, qos)


# 處理消息
def on_message_come(client, userdata, msg):
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(msg.topic + " " + ":" + str(msg.payload))
    ttdetails = ast.literal_eval(msg.payload.decode())
    ttpayload = ttdetails['Command'] + " : " + ttdetails["Data"]

    # {"Command":"error message","Data":"Call supervisor"}

    # on_publish("andeng_reply", m5mess, 1)
    ttype = "send"
    db = pymysql.connect(host="localhost", user="root",
                         password="16888", db="m5logweb", port=3306)

    # sql = "CREATE TABLE IF NOT EXISTS m5logs (id VARCHAR(255) NOT NULL, thingtime VARCHAR(255) NOT NULL, thingtype VARCHAR(255) NOT NULL, thingdetails INT NOT NULL, PRIMARY KEY (id))"
    # sql = "select * from m5logs order by id desc limit 10"
    sql = "INSERT INTO m5logs(thingtime, thingtype, thingdetails) values(%s, %s, %s)"
    try:
        cur = db.cursor()
        cur.execute(sql, (now_time, ttype, ttpayload))  # 第二个参数可用一个包含数据的列表
        db.commit()  # 插入数据的话需要commit
    except:
        db.rollback()
    db.close()
    print("接收成功! ")


# 訂閱消息
def on_subscribe(self):
    client.subscribe(self, 1)
    client.on_message = on_message_come


def datahandle():
    # global list_data
    db = pymysql.connect(host="localhost", user="root",
                         password="16888", db="m5logweb", port=3306)

    # sql = "CREATE TABLE IF NOT EXISTS m5logs (id VARCHAR(255) NOT NULL, thingtime VARCHAR(255) NOT NULL, thingtype VARCHAR(255) NOT NULL, thingdetails INT NOT NULL, PRIMARY KEY (id))"
    sql = "select * from m5logs order by id desc limit 10"
    cur = db.cursor()
    cur.execute(sql)

    lidata = cur.fetchall()
    db.close()
    print(lidata)
    # list_data = list(lidata)
    # print(list_data)

    # 调用fetchone()方法获得查询结果第一条数据
    # data = cur.fetchall()
    # print('Database:', data)
    # try:
    #     #     cur.execute(sql, (id, user, age))  # 第二个参数可用一个包含数据的列表
    #     #     db.commit()  # 插入数据的话需要commit
    #     # except:
    #     #     db.rollback()


def confirm_message():
    m5mess = "{\"Command\":\"message reply\", \"Data\":\"error Information is confirmed\"}"
    publish.single("m5/reply", payload=m5mess,
                   hostname="127.0.0.1",
                   port=1883,
                   auth={'username': 'iot', 'password': 'iot123!'})
    now_time2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    ttype2 = "received"
    ttpayload2 = "error Information is confirmed"
    # sql = "INSERT INTO m5logs(thingtime, thingtype, thingdetails) values(%s, %s, %s)"
    print("确认成功! ")
    db = pymysql.connect(host="localhost", user="root",
                         password="16888", db="m5logweb", port=3306)

    # sql = "CREATE TABLE IF NOT EXISTS m5logs (id VARCHAR(255) NOT NULL, thingtime VARCHAR(255) NOT NULL, thingtype VARCHAR(255) NOT NULL, thingdetails INT NOT NULL, PRIMARY KEY (id))"
    # sql = "select * from m5logs order by id desc limit 10"
    sql = "INSERT INTO m5logs(thingtime, thingtype, thingdetails) values(%s, %s, %s)"
    try:
        cur = db.cursor()
        cur.execute(sql, (now_time2, ttype2, ttpayload2))  # 第二个参数可用一个包含数据的列表
        db.commit()  # 插入数据的话需要commit
    except:
        db.rollback()
    db.close()


def main():
    on_connect()
    on_subscribe("m5")
    # confirm_message()
    while True:
        time.sleep(60)
        confirm_message()

        # on_subscribe("m5")
        # time.sleep(0.2)


if __name__ == '__main__':
    main()
