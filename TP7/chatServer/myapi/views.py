from rest_framework import viewsets 
from .serializers import MessageSerializer,UserSerializer
from .models import Message,Utilisateur

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('source')
    serializer_class = MessageSerializer
class Users(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all().order_by('prenom')
    serializer_class = UserSerializer
# Create your views here.
