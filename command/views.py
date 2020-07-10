import ast
import json
import os
import subprocess

from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed

#视图
#视图处理函数
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

@csrf_exempt
def run_job(request):
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
            print(data)

            # result = os.popen(data['command'])
            # out = result.readlines()

            p = subprocess.Popen(data['command'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out, error = p.communicate()

            content = {'msg': 'SUCCESS', 'context': out.decode('gbk')}
            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])