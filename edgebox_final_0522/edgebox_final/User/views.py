import re
import random
import datetime
import json
from PIL import Image, ImageDraw, ImageFont
from functools import wraps
from base64 import b64encode
from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponse, Http404
from django.utils.six import BytesIO
from django.contrib.auth import login, logout
from django.views.generic import View
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from django.conf import settings
from User.models import User
from celery_tasks.tasks import send_register_active_email
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
# Create your views here
def protector(func):
    """ 确保请求来自前台 """

    @wraps(func)  # 第二种方式
    def wrapped_func(request, **kwargs):

        if request.META.get('HTTP_X_FORWARDED_HOST'):
            address = request.META.get("HTTP_X_FORWARDED_HOST")
        else:
            address = request.META.get("REMOTE_ADDR")
        # if address != "127.0.0.1:8080":  # 前台网站地址，防止外来者攻击
        #     return JsonResponse({"error_code": 1, "error_msg": "小二货还想攻击我！哼哼哼~！"})
        if request.method == "post":
            try:
                if not isinstance(json.loads(request.body), dict):
                    return JsonResponse({
                        "error_code": 1,
                        "error_msg": "数据格式错误"
                    })
            except Exception as e:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "数据格式错误"
                })
        return func(request, **kwargs)

    return wrapped_func


@csrf_exempt
def test(request):
    if request.method == "GET":
        print(request.GET.get("username"))
        return HttpResponse("ok")



class VerifyCodeApi(View):
    """验证码url和验证码获取接口"""

    @staticmethod
    @protector
    def get(request):
        return JsonResponse({
            "error_code": 0,
            "error_msg": {
                "url": "%s/%s" % (reverse("verify_code"), random.random())
            }})



class VerifyCodeView(View):
    """产生4位随机验证码"""

    @staticmethod
    # @protector
    def get(request):
        # print(request.headers)
        # 定义变量，用户画面的背景色、宽、高 RGB
        bg_color = (random.randrange(20, 100), random.randrange(20, 100), 255)
        # 创建画面对象
        image = Image.new("RGB", (settings.VERIFY_CODE_WIDTH, settings.VERIFY_CODE_HEIGHT), bg_color)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 调用画笔的point函数绘制噪点
        for i in range(0, 100):
            xy = (random.randrange(0, settings.VERIFY_CODE_WIDTH), random.randrange(0, settings.VERIFY_CODE_HEIGHT))
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            draw.point(xy, fill=fill)
        # 定义验证码备选值
        value_list_str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        # 随机选4个值作为验证码
        rand_str = ''
        for i in range(4):
            rand_str += value_list_str[random.randrange(0, len(value_list_str))]
        # 构造字体对象
        font = ImageFont.truetype("static/font/times.ttf", 23)
        # 构造字体颜色
        font_color = (255, random.randrange(0, 255), random.randrange(0, 255))
        # 绘制4个字
        width_list = [5, 25, 50, 75]
        for i in range(4):
            draw.text(xy=(width_list[i], 2), text=rand_str[i], font=font, fill=font_color)
        # 释放画笔
        del draw
        # 存入session，用于进一步验证
        request.session["verify_code"] = rand_str
        # 内存文件操作
        buffer = BytesIO()
        # 将图片保存在内存中，文件类型为png
        image.save(buffer, "png")
        # 将内存中的图片数据返回给客户端，MIME类型为图片png
        # return JsonResponse({
        #     "error_code": 0,
        #     "error_msg": {
        #         "name": "verify_code%s.png" % str(random.random()),
        #         "png": b64encode(buffer.getvalue()).decode("utf-8")
        #         # "png": str(buffer.getvalue())
        #     }})
        return HttpResponse(buffer.getvalue(), "image/png")


class LoginView(View):
    """登录视图"""

    @staticmethod
    @protector
    def get(request, change):
        if change == "/change":
            request.session["is_login"] = False
            request.session["username"] = ""
            return JsonResponse({
                "error_code": 0,
                "error_msg": {
                    "username": "",
                    "is_login": False
                }
            })
        username = request.session.get("username", "")
        is_login = request.session.get("is_login", False)
        return JsonResponse({
            "error_code": 0,
            "error_msg": {
                "username": username,
                "is_login": is_login
            }
        })

    @staticmethod
    @protector
    def post(request, change):
        """post请求"""
        """验证登录参数"""
        print(request.body)
        print(str(request.body))
        response = json.loads(request.body.decode())  # 获取前台回传数据
        verify_code = response.get("verify_code", None)  # 验证码
        if verify_code is None:
            # 没有传验证码
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台没有传验证码(verify_code)"
            })
        else:
            # 如果验证码存在
            if verify_code.lower() != request.session.get("verify_code").lower():
                # 用户输入验证码与后台验证码不一致，回传错误信
                # pass
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "验证码输入错误"
                })
        username = response.get("username", None)  # 登录用户名
        if username is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传用户名(username)"
            })

        password = response.get("password", None)  # 登录密码
        if password is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传密码(password)"
            })

        try:
            user = User.objects.get(username=username)  # 获取用户名
            """如果用户存在，密码正确且没有删除标记为0"""
            if not check_password(password, user.password, "pbkdf2_sha256"):
                # 密码错误
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "账户/密码错误"
                })
            if not user.is_delete:
                # 用户未删除, is_delete==0
                if user.is_active:
                    # 用户已激活, is_active==1,允许登录
                    user.last_login = datetime.datetime.now()
                    user.save()
                    request.session["username"] = username
                    remain = response.get("keep-alive", False)
                    if remain:
                        request.session["is_login"] = True
                    else:
                        request.session["is_login"] = False
                    return JsonResponse({
                        "error_code": 0,
                        "error_msg": {
                            "is_superuser": user.is_superuser
                        }
                    })
                else:
                    # 用户未激活
                    return JsonResponse({
                        "error_code": 1,
                        "error_msg": "用户未激活"
                    })
            else:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "用户已被禁用"
                })
        except User.DoesNotExist:
            # 用户不存在
            return JsonResponse({
                "error_code": 1,
                "error_msg": "账户/密码错误"
            })
        except Exception as e:
            return JsonResponse({
                "error_code": 1,
                "error_msg": str(e)
            })


class ForgetPasswordView(View):
    """忘记密码视图"""

    @staticmethod
    @protector
    def post(request):
        """post请求"""
        """以POST方式提交请求"""
        response = json.loads(request.body)
        username = response.get("username", None)  # 当前用户名
        if username is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入登录用户名(username)"
            })
        try:
            """如果用户存在"""
            user = User.objects.get(username=username)
            user_id_six = response.get("user_id_six", None)  # 身份证后六位
            if user_id_six is None:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "前台未传入用户身份后六位(user_id_six)"
                })
            if user.user_id_six != user_id_six:
                """身份证后六位错误"""
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "身份证后六位输入错误"
                })

            phone_number = response.get("phone_number", None)  # 手机号
            if phone_number is None:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "前台未传入用户身份手机号(phone_number)"
                })
            if user.phone_number != phone_number:
                """手机号错误"""
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "用户手机号输入错误"
                })

            email = response.get("email", None)  # 邮箱号
            if email is None:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "前台未传入用户邮箱号(email)"
                })
            if user.email != email:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "用户邮箱号输入错误"
                })
            return JsonResponse({
                "error_code": 0,
                "error_msg": ""
            })  # 身份信息验证成功，进入修改密码界面
        except User.DoesNotExist:
            """如果用户不存在"""
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户[%s]不存在" % username
            })
        except Exception as e:
            return JsonResponse({
                "error_code": 1,
                "error_msg": str(e)
            })


class MendPasswordView(View):
    """用户修改密码， 所有用户可修该"""

    @staticmethod
    @protector
    def post(request):
        response = json.loads(request.body)
        username = response.get("username", None)  # 获取用户名
        if username is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg":
                    "前台未传入用户名(username)"
            })
        try:
            user = User.objects.get(username=username)  # 获取用户
            new_password = response.get("new_password", None)  # 获取新密码
            if new_password is None:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "前台未传入新密码(new_password)"
                })
            if new_password == "":
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "新密码不能为空"
                })
            if not check_password(new_password, user.password, "pbkdf2_sha256"):
                # 如果密码不一致，重写密码
                user.password = make_password(new_password, username, "pbkdf2_sha256")  # 写入密码
                user.save()  # 保存修改
                if not check_password(new_password, user.password, "pbkdf2_sha256"):
                    return JsonResponse({
                        "error_code": 1,
                        "error_msg": "密码未修改成功,请重新提交或者联系管理员"
                    })
                else:
                    return JsonResponse({
                        "error_code": 0,
                        "error_msg": "密码修改成功"
                    })
            else:
                # 如果密码一致，不重新写密码
                return JsonResponse({
                    "error_code": 0,
                    "error_msg": "密码修改成功"
                })
        except User.DoesNotExist:
            """用户不存在"""
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户不存在"
            })
        except Exception as e:
            return JsonResponse({
                "error_code": 1,
                "error_msg": str(e)
            })


class ActivateUserView(View):
    """用户激活"""

    @staticmethod
    @protector
    def get(request, token):
        serializer = Serializer(settings.SECRET_KEY, 1 * 60 * 60)  # 生成激活序列，超时时间为1小时
        try:
            info = serializer.loads(token)
            # 获取用户id
            user_id = info["user_id"]
            try:
                user = User.objects.get(id=user_id)
                if user.is_active:
                    return JsonResponse({
                        "error_code": 0,
                        "error_msg": "用户已激活"
                    })
                user.is_active = 1
                user.save()
                return JsonResponse({
                    "error_code": 0,
                    "error_msg": "用户激活成功"
                })
            except User.DoesNotExist:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "用户不存在,请联系管理员"
                })
        except SignatureExpired:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "激活链接已过期失效,请重新激活"
            })
        except Exception as e:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "激活链接无效:"
            })


class SendActivateEmailView(View):
    """激活链接过期，用户重新激活"""

    @staticmethod
    @protector
    def get(request, username):
        if username == "":
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户名不能为空"
            })
        try:
            user = User.objects.get(username=username)
            if user.is_delete:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "用户[%s]已禁用" % username
                })
            if user.is_active:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "用户[%s]已激活" % username
                })
            # 生成激活信息
            serializer = Serializer(settings.SECRET_KEY, 1 * 60 * 60)  # 生成激活序列，超时时间为1小时
            info = {"user_id": user.id}  # 需要加密的信息 用户名
            serialized_info = serializer.dumps(info).decode()  # 加密信息

            # 生成邮件信息
            main_title = "EdgeBox激活邮件"
            content = "<a href='http://%s:%d/user/activate_user/%s>点击激活用户</a>" % (
                "127.0.0.1", 8000, serialized_info)
            with open("a.txt", "w") as f:
                f.write(content)
            system_name = settings.EMAIL_FROM
            to_mail = user.email
            cc_mail = []

            # send_register_active_email.delay(main_title, content, system_name, to_mail, cc_mail)  # 发送激活邮件
            return JsonResponse({
                "error_code": 1,
                "error_msg": "激活邮件已经发送，请注意查收,有效期1小时....."
            })
        except User.DoesNotExist:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户[%s]不存在,请联系管理员" % username
            })


class CreateUserView(View):
    """创建用户，仅超级管理员有此权限，设置权限待补充"""

    @staticmethod
    def post(request):
        """post请求"""
        response = json.loads(request.body.decode())
        username = response.get("username", None)
        if username is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入用户名(username)"
            })
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 未获取到用户名
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户不存在"
            })
        is_superuser = user.is_superuser
        if not is_superuser:
            # 非管理员用户
            return JsonResponse({
                "error_code": 1,
                "error_msg": "非管理员用户，拒绝访问，请登录管理员账户"
            })

        new_user = response.get("new_user", None)  # 获取用户名
        if new_user is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入新的用户名(new_user)"
            })
        if len(new_user) > 20:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户名必须只能包含字母、数字和下划线且不能以数字开头，长度20个字符"
            })
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", new_user):
            # 如果用户名不满足包含只有字母数字下划线，且不以数字开头
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户名必须只能包含字母、数字和下划线且不能以数字开头，长度20个字符"
            })

        # password = response.get("password", None)  # 获取密码
        # if password is None:
        #     return JsonResponse({
        #         "error_code": 1,
        #         "error_msg": "前台未传入新用户密码(password)"
        #     })

        user_id_six = response.get("user_id_six", None)  # 获取身份证后六位
        if user_id_six is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入新用户身份证后六位(user_id_six)"
            })
        if not re.match(r"\d{5}[0-9xX]$", user_id_six):
            # 身份证后六位包含非数字
            return JsonResponse({
                "error_code": 1,
                "error_msg": "身份证后六位应该由6位数字或者5位数字加1位X/x组成"
            })

        phone_number = response.get("phone_number", None)  # 获取手机号
        if phone_number is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入新用户手机号(phone_number)"
            })
        if not re.match(r"\d{11}$", phone_number):
            return JsonResponse({
                "error_code": 1,
                "error_msg": "手机号必须由11位数字组成"
            })

        email = response.get("email", None)  # 获取邮箱号
        if email is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入新用户邮箱号(email)"
            })
        if not re.match(r".+@.*", email):
            return JsonResponse({
                "error_code": 1,
                "error_msg": "邮箱不满足规则"
            })

        try:
            """用户存在"""
            User.objects.get(username=new_user)
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户已存在"
            })
        except User.DoesNotExist:
            """用户不存在, 创建用户"""
            try:
                # 储存用户信息
                password = "admin"
                user = User.objects.create_user(new_user, email, password, user_id_six=user_id_six,
                                                phone_number=phone_number)
                user.password = make_password(password, new_user, "pbkdf2_sha256")  # 采用自己的加密方式
                user.is_active = 1
                user.save()
                # 生成激活信息
                serializer = Serializer(settings.SECRET_KEY, 1 * 60 * 60)  # 生成激活序列，超时时间为1小时
                info = {"user_id": user.id}  # 需要加密的信息 用户名
                serialized_info = serializer.dumps(info).decode()  # 加密信息

                # 生成邮件信息
                main_title = "EdgeBox激活邮件"
                content = "<a href='http://%s:%d/user/activate_user/%s>点击激活用户</a>" % (
                    "127.0.0.1", 8000, serialized_info)
                with open("a.txt", "w") as f:
                    f.write(content)
                # TODO
                system_name = settings.EMAIL_FROM
                to_mail = email
                cc_mail = []

                # send_register_active_email.delay(main_title, content, system_name, to_mail, cc_mail)  # 发送激活邮件
            except Exception as e:
                return JsonResponse({"error_code": 1, "error_msg": "用户创建失败，请重新创建" + str(e)})
            try:
                """检查写入数据库否是否成功"""
                user = User.objects.get(username=new_user)
                if check_password(password, user.password, "pbkdf2_sha256"):
                    return JsonResponse({"error_code": 0, "error_msg": "用户创建成功"})
                else:
                    return JsonResponse({"error_code": 1, "error_msg": "用户创建失败，请重新创建"})
            except User.DoesNotExist:
                return JsonResponse({"error_code": 1, "error_msg": "用户创建失败，请重新创建"})
        except Exception as e:
            return JsonResponse({"error_code": 1, "error_msg": str(e)})


class UserInfoView(View):
    """修改用户信息， 所有用户均可在用户中心修改；修改权限仅超级管理员有此权限"""

    @staticmethod
    def get(request, username):
        """get请求"""
        if username is None:
            return JsonResponse({"error_code": 1, "error_msg": "前台未传入用户名"})
        try:
            user = User.objects.get(username=username)  # 从数据库查询用户信息
            if not user.is_superuser:
                # 非管理员
                user_id_six = user.user_id_six[:2] + "****"
                phone_number = user.phone_number[:3] + "****" + user.phone_number[7:]
                email = user.email
                username = user.username
                is_superuser = user.is_superuser
                last_login = user.last_login
                is_staff = user.is_staff
                is_active = user.is_active
                is_delete = user.is_delete
                return JsonResponse({
                    "error_code": 0,
                    "error_msg": [{
                        "username": username,
                        "user_id_six": user_id_six,
                        "phone_number": phone_number,
                        "email": email,
                        "is_superuser": is_superuser,
                        "last_login": last_login,
                        "is_staff": is_staff,
                        "is_active": is_active,
                        "is_delete": is_delete
                    }]}
                )
            else:
                # 管理员
                users = User.objects.all()
                user_info_list = []
                for user in users:
                    user_info = dict()
                    user_id_six = user.user_id_six
                    phone_number = user.phone_number
                    email = user.email
                    username = user.username
                    is_superuser = user.is_superuser
                    last_login = user.last_login
                    is_staff = user.is_staff
                    is_active = user.is_active
                    is_delete = user.is_delete
                    user_info["username"] = username
                    user_info["user_id_six"] = user_id_six
                    user_info["phone_number"] = phone_number
                    user_info["email"] = email
                    user_info["is_superuser"] = is_superuser
                    user_info["last_login"] = last_login
                    user_info["is_staff"] = is_staff
                    user_info["is_active"] = is_active
                    user_info["is_delete"] = is_delete
                    user_info_list.append(user_info)
                print(user_info_list)
                return JsonResponse({
                    "error_code": 0,
                    "error_msg": user_info_list
                })
        except User.DoesNotExist:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户不存在"
            })
        except Exception as e:
            return JsonResponse({
                "error_code": 1,
                "error_msg": str(e)
            })

    @staticmethod
    def post(request):
        """post请求"""
        response = json.loads(request.body)
        username = response.get("username", None)  # 前台获取到的用户名
        if username is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入用户名(username)"
            })
        try:
            user = User.objects.get(username=username)  # 从数据库查询用户信息
            user_id_six = response.get("user_id_six", None)  # 获取身份证后六位
            if user_id_six is None:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "前台未传入用户身份证后六位(user_id_six)"
                })
            if not re.match(r"\d{5}[0-9xX]$", user_id_six):
                # 身份证后六位包含非数字
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "身份证后六位只能是数字或五位数字加1位X/x"
                })

            phone_number = response.get("phone_number", None)  # 获取手机号
            if phone_number is None:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "前台未传入用户手机号(phone_number)"
                })
            if not re.match(r"\d{11}$", phone_number):
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "手机号只能包含11位数字"
                })

            email = response.get("email", None)  # 获取邮箱
            if email is None:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "前台未传入用户邮箱(email)"

                })

            if not re.match(r".+@.*", email):
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "邮箱不满足规则"
                })

            if user.user_id_six != user_id_six:
                # 如果用户身份证后六位变化，重写身份后六位
                user.user_id_six = user_id_six
            if user.phone_number != phone_number:
                # 如果用户手机号变化，重写手机号
                user.phone_number = phone_number
            if user.email != email:
                # 如果用户邮箱变化，重写邮箱
                user.email = email
            user.save()
            is_superuser = user.is_superuser
            if is_superuser:
                # TODO 超级管理员设置权限
                pass
            if user.user_id_six == user_id_six and user.phone_number == phone_number and user.email == email:
                return JsonResponse({
                    "error_code": 0,
                    "error_msg": "用户[%s]信息修改成功" % username
                })
            else:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "用户[%s]信息修改失败，请重新提交或联系管理员" % username
                })
        except User.DoesNotExist:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户[%s]不存在，请重新提交或联系管理员" % username
            })
        except Exception as e:
            return JsonResponse({
                "error_code": 1,
                "error_msg": str(e)
            })


class DeleteUserView(View):
    """删除用户，仅超级管理员由此权限"""

    @staticmethod
    def get(request, username):
        """get请求"""
        if username is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入用户名"
            })
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                # 判断是否是超级用户
                try:
                    # 获取非管理员用户
                    user = User.objects.filter(is_superuser=0)
                    user_list = [user[0] for user in user.values_list("username")]
                except User.DoesNotExist:
                    user_list = []
                return JsonResponse({
                    "error_code": 0,
                    "error_msg": {"user_list": user_list}
                })
            else:
                # 非管理员用户
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "非管理员用户，拒绝访问, 请登录管理员账户"
                })
        except User.DoesNotExist:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "用户名不存在"
            })

    @staticmethod
    def post(request):
        """post请求"""
        response = json.loads(request.body)
        username = response.get("username", None)  # 获取当前用户用户名
        if username is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入当前用户名(username)"
            })
        try:
            user = User.objects.get(username=username)  # 查询当前账户是否存在
            if not user.is_superuser:
                return JsonResponse({
                    "error_code": 1,
                    "error_msg": "非管理员用户，拒绝访问"
                })
        except User.DoesNotExist:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "当前用户不存在"
            })
        delete_user = response.get("delete_user", None)  # 获取需要删除的用户名
        if delete_user is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台没有传入需要删除用户名(delete_user)"
            })
        try:
            User.objects.get(username=delete_user)
        except User.DoesNotExist:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "需要删除的用户不存在"
            })
        except Exception as e:
            return JsonResponse({
                "error_code": 1,
                "error_msg": str(e)
            })

        super_password = response.get("super_password", None)  # 获取超级管理员密码
        if super_password is None:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "前台未传入超级管理员密码(super_password)"
            })
        try:
            super_user = User.objects.get(is_superuser=1)  # 获取超级用户
        except User.DoesNotExist:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "超级用户不存在"
            })
        except Exception as e:
            return JsonResponse({
                "error_code": 0,
                "error_msg": str(e)
            })

        if check_password(super_password, super_user.password, "pbkdf2_sha256"):
            # 超级管理密码正确，删除用户
            for i in range(5):
                # 尝试五次
                try:
                    # 删除用户
                    user = User.objects.get(username=delete_user)
                    user.delete()  # 用户存在删除用户
                except User.DoesNotExist:
                    # 如果删除用户不存在，刷新页面
                    # 获取普通用户
                    return JsonResponse({
                        "error_code": 0,
                        "error_msg": "删除用户[%s]成功" % delete_user
                    })

            return JsonResponse({
                "error_code": 1,
                "error_msg": "删除用户[%s]失败,请联系管理员,检查后台数据库" % delete_user
            })
        else:
            return JsonResponse({
                "error_code": 1,
                "error_msg": "超级管理员密码错误"
            })
