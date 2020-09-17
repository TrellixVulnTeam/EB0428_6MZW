# -*- coding: utf-8 -*-
"""
Create Time: 2020/5/16 10:31
Author: Liuqing Zhang
"""

class Router(object):
    def db_for_read(self, model, **hints):
        ## 返回讀操作的數據庫 select
        # print("SELECT")
        return "default"
    def db_for_write(self, model, **hints):
        ## 返回寫操作的數據庫
        # print("INSERT-CREATE-UPDATE")
        return "default"
        # return ["slave1", "default"]
