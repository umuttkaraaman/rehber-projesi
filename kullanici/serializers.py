from rest_framework import serializers
from .models import KisiBilgisi, Mesaj
from django.contrib.auth.models import User

class KisiBilgisiSerializer(serializers.ModelSerializer):
    class Meta:
        model = KisiBilgisi
        fields = ['id', 'ad', 'soyad', 'telefon', 'tarih']  # user'ı buraya eklemiyoruz!

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MesajSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesaj
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
