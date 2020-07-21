import subprocess

from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser

from command.models import NodeInfo, ClientInfo
from command.serializers import NodeInfoSerializer, ClientInfoSerializer


def index(request):
    return render(request, 'index.html')


def execute_command(command):
    print(command)

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
    out, error = p.communicate()
    print(out)
    content = {'msg': 'SUCCESS', 'context': out}
    return content


@csrf_exempt
def general_command(request):
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
            function_name = data['function']
            print(function_name)
            # if data['args']:
            result = globals()[function_name](data['args'])
            # else:
            #     result = globals()[function_name]()
            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=result, status=status.HTTP_200_OK)
    # 如果不是post 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['POST'])


#查询磁盘状态
def query_disk_status(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'lsblk --json')
    return result


#添加osd节点
def add_osd(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'ceph-deploy osd create --data' + ' ' + args['device'] + ' ' + args['new-ceph-nodes'])
    return result


#把管理密钥发给新节点
def send_admin_key(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'ceph-deploy admin' + ' ' + args['new-ceph-nodes'])
    return result


#添加mon节点
def add_mon(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'ceph-deploy --overwrite-conf  mon add' + ' ' + args['new-ceph-nodes'])
    return result


#查看Mon仲裁状态
def query_quorum_status(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo ceph quorum_status --format json-pretty')
    return result


#添加mds节点
def add_mds(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'ceph-deploy mds create' + ' ' + args['new-ceph-nodes'])
    return result


#创建osd池
def build_osd_pool(args):
    execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo ceph osd pool create cephfs_data 128')
    execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo ceph osd pool create cephfs_metadata 128')
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo ceph fs new' + ' ' + args['cephfs-name'] + ' ' + 'cephfs_metadata cephfs_data')
    return result


#创建用户
def bulid_user(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + "sudo ceph auth get-or-create client." + args['client-name'] + ' ' + "mon 'allow r' mds 'allow r,allow rw path=/' osd 'allow rw pool=cephfs_data' -o ceph.client." + args['cephfs-name'] + ".keyring")
    return result


#获取用户密钥
def query_user_key(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo ceph auth get-key client.' + args['client-name'])
    return result


#目录操作
def control_dir(args):
    ifdir = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo find' + ' ' + args['path'] + ' ' + '-type d -name "' + args['dir-name'] + '"')
    if ifdir is None:
        execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo mkdir' + ' ' + args['path'])

    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo mount -t ceph' + ' ' + args['ip'] + ':/ ' + ' ' + args['path'] + ' ' +
                             '-o name=' + args['client-name'] + ',secret=' + args['key'])
    return result


#查询集群状态
def query_cluster_status(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo ceph -s --format json-pretty')
    return result


#查询故障Osd节点
def query_osd_status(args):
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo ceph osd tree --format json-pretty')
    return result


#移除故障osd
def remove_osd(args):
    execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo ceph osd down' + ' ' + args['osd-id'])
    result = execute_command('ssh' + ' ' + args['ceph-node'] + ' ' + 'sudo ceph osd out' + ' ' + args['osd-id'])
    return result


class ClientInfoViewSet(viewsets.ModelViewSet):
    queryset = ClientInfo.objects.all()
    serializer_class = ClientInfoSerializer


class NodeInfoViewSet(viewsets.ModelViewSet):
    queryset = NodeInfo.objects.all()
    serializer_class = NodeInfoSerializer


