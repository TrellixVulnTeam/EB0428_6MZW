#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/8/24


import sqlite3

conn = sqlite3.connect('test.db')
# 建立连接，如果不存在将会创建
print("Open database successfully")
cursor = conn.cursor()
# 创建cursor

# cursor.execute(
#     "CREATE TABLE IF NOT EXISTS m5logs (id INTEGER PRIMARY KEY, thingtime VARCHAR(255) NOT NULL, thingtype VARCHAR(255) NOT NULL, thingdetails VARCHAR(255) NOT NULL)")
#
# # cursor.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 );")
# cursor.execute(
#     "INSERT INTO m5logs(thingtime, thingtype, thingdetails) values('2020-08-21 16:38:10', 'send', 'error message : Call supervisor')")
cursor.execute("select * from m5logs order by id desc limit 10")

results = cursor.fetchall()
for row in results:
    print(row)

cursor.close()
# 关闭cursor
conn.commit()
# 提交事务
conn.close()
# 关闭连接
