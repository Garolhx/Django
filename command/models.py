from django.db import models

# Create your models here.
# orm对应数据库的类


class NodeInfo(models.Model):
    id = models.CharField(verbose_name='节点Id', max_length=256, primary_key=True)
    name = models.CharField(verbose_name= '节点名', max_length=256)

    class Meta:
        db_table = 'node_info'


class ClientInfo(models.Model):
    name = models.CharField(verbose_name='用户名', max_length=256, primary_key=True)
    key = models.CharField(verbose_name= '用户密钥', max_length=256)

    class Meta:
        db_table = 'client_info'
