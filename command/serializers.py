from rest_framework import serializers
from command.models import NodeInfo, ClientInfo


class NodeInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = NodeInfo
        fields = ['id', 'name']


class ClientInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ClientInfo
        fields = ['name', 'key']

