from datetime import datetime, timedelta
from smtplib import SMTPException

import jwt
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view

import utils.mail
from utils import json


# Create your views here.
def hello(request):
    if request.method == 'GET':
        return HttpResponse("hello")


@api_view(['POST'])
def start_register(request):
    name = request.data.get('name', "")
    passwd = request.data.get('passwd', "")
    email = request.data.get('email', "")

    if User.objects.filter(username=name).exists():
        return json.response({'result': 1, 'message': "用户名已被注册"})

    if User.objects.filter(email=email).exists():
        return json.response({'result': 1, 'message': "邮箱已被注册"})

    code = jwt.encode(
        {
            'name': name,
            'passwd': passwd,
            'email': email,
            'expire': (datetime.now() + timedelta(hours=2)).isoformat()
        },
        settings.SECRET_KEY,
    )

    try:
        utils.mail.send_mail(
            "畅游中国用户注册",
            "请按提示完成注册验证",
            render_to_string("verify_link.html", {'url': f"{request.build_absolute_uri('/register/')}{code}"}),
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
    except SMTPException as e:
        return json.response({'result': 1, 'message': f"邮件发送失败，{e}"})

    return json.response({'result': 0, 'message': "已发送认证邮件"})


@api_view(['GET'])
def verify_register(request, code):
    info = jwt.decode(code, settings.SECRET_KEY, "HS256")

    name = info['name']
    passwd = info['passwd']
    email = info['email']
    expire = datetime.fromisoformat(info['expire'])

    if expire < datetime.now():
        HttpResponse("认证已过期")

    if User.objects.filter(email=email).exists():
        return HttpResponse("用户已被注册")

    user = User.objects.create_user(name, email, passwd)
    common_group, _ = Group.objects.get_or_create(name="Common User")
    user.groups.add(common_group)

    return HttpResponse("注册成功！")


@api_view(['POST'])
def login(request):
    name = request.data.get('name', None)
    email = request.data.get('email', None)
    passwd = request.data.get('passwd', "")

    if name is not None and User.objects.filter(username=name).exists():
        user = User.objects.get(username=name)
    elif email is not None and User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
    else:
        return json.response({'result': 1, 'message': "未找到用户，请检查邮箱或用户名是否正确"})

    if not user.check_password(passwd):
        return json.response({'result': 1, 'message': "密码不正确"})

    user_jwt = jwt.encode(
        {
            'name': user.username,
            'expire': (datetime.now() + timedelta(hours=2)).isoformat(),
        },
        settings.SECRET_KEY,
    )

    return json.response({'result': 1, 'message': "登陆成功", 'jwt': user_jwt})
