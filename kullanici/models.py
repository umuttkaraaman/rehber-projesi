from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone

class Mesaj(models.Model):
    gonderen = models.ForeignKey(User, related_name='gonderilenler', on_delete=models.CASCADE)
    alici = models.ForeignKey(User, related_name='alinanlar', on_delete=models.CASCADE)
    mesaj = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)
    okundu = models.BooleanField(default=False)  # 🔴 Burayı ekle

    def __str__(self):
        return f"{self.gonderen} → {self.alici}"




KATEGORI_SECENEKLERI = [
    ('Aile', 'Aile'),
    ('İş', 'İş'),
    ('Acil', 'Acil'),
    ('Diğer', 'Diğer'),
]

class KisiBilgisi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.CharField(max_length=50)
    soyad = models.CharField(max_length=50)
    telefon = models.CharField(max_length=11)
    tarih = models.DateField()
    kategori = models.CharField(max_length=10, choices=KATEGORI_SECENEKLERI, default='Diğer')

    def __str__(self):
        return f"{self.ad} {self.soyad}"

class KullaniciLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    islem = models.CharField(max_length=255)
    zaman = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.islem} ({self.zaman.strftime('%Y-%m-%d %H:%M')})"

