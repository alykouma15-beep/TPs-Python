from rest_framework import serializers
from .models import Message,Utilisateur

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Message
        fields=('source','to','body')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Utilisateur
        fields=('prenom','nom','age','mail')


