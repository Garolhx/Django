import ast
import json
import os
import subprocess

from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from command.models import NodeInfo
from command.serializers import NodeInfoSerializer


def index(request):
    return render(request, 'index.html')


def execute_command(command):
    print(command)

    p = subprocess.Popen(command['command'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
    out, error = p.communicate()
    print(out)
    content = {'msg': 'SUCCESS', 'context': out}
    return content


@csrf_exempt
def normal_command(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    # 判断是否为post 请求
    if request.method == 'POST':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            content = execute_command(data)
            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])


class NodeInfoViewSet(viewsets.ModelViewSet):
    queryset = NodeInfo.objects.all()
    serializer_class = NodeInfoSerializer