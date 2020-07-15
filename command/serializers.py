from rest_framework import serializers
from command.models import NodeInfo


class NodeInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = NodeInfo
        fields = ['id']

