# 使用Celery
import time
import json
from http.client import HTTPConnection
import os
import django
from celery import Celery
from django.conf import settings


def send_register_active_email(mail_title=str(), content=str(), system_name=str(),
                               to_mail=str() or list(), cc_mail=str() or list(), server_host=settings.EMAIL_HOST,
                               server_port=settings.EMAIL_PORT, html="False"):
    to_mail = (not isinstance(to_mail, list) and to_mail) or ",".join(to_mail)
    cc_mail = (not isinstance(cc_mail, list) and cc_mail) or ",".join(cc_mail)
    data = {"system_name": system_name, "toMail": to_mail, "content": content, "mail_title": mail_title, "cc": cc_mail,
            "html_status": html, "errors_type": "email"}
    try:
        body = json.dumps(data)
        headers = {"Content-Type": "text/html; charset=utf-8"}
        conn = HTTPConnection(":".join((server_host, str(server_port))))
        conn.request(method="POST", url="/data_manage/", body=body, headers=headers)
        res = conn.getresponse().read().decode(encoding="utf-8")
        print(res)
        return json.loads(res)
    except Exception as err:
        print(err)
