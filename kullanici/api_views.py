from rest_framework import generics
from .models import KisiBilgisi, Mesaj
from .serializers import KisiBilgisiSerializer, MesajSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

class KisiListesiAPI(generics.ListCreateAPIView):
    queryset = KisiBilgisi.objects.all()
    serializer_class = KisiBilgisiSerializer
    permission_classes = [AllowAny]  # ✅ Şu anlık test için


    def get_serializer_context(self):
        return {'request': self.request}

class MesajListesiAPI(generics.ListCreateAPIView):
    queryset = Mesaj.objects.all()
    serializer_class = MesajSerializer
    permission_classes = [IsAuthenticated]
