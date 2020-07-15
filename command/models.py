from django.db import models

# Create your models here.
# orm对应数据库的类


class NodeInfo(models.Model):
    id = models.CharField(verbose_name='节点Id', max_length=256, primary_key=True)

    class Meta:
        db_table = 'node_info'
