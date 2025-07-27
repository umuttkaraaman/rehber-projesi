from django.urls import path
from . import views,api_views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('kayit/', views.kayit_ol, name='kayit'),
    path('giris/', views.giris_yap, name='giris'),
    path('bilgi/', views.bilgi_gir, name='bilgi_gir'),
    path('profil/', views.profil, name='profil'),
    path('cikis/', views.cikis_yap, name='cikis'),
    path('bilgi/guncelle/<int:id>/', views.bilgi_guncelle, name='bilgi_guncelle'),  # ✅
    path('bilgi/sil/<int:id>/', views.bilgi_sil, name='bilgi_sil'),
    path('hesap/', views.hesap_duzenle, name='hesap_duzenle'),
    path('sifre-degistir/', auth_views.PasswordChangeView.as_view(
        template_name='kullanici/sifre_degistir.html',
        success_url='/profil/'
    ), name='sifre_degistir'),
    # ✅
    path('grafik/', views.grafik_sayfasi, name='grafik'),
    path('loglar/', views.log_kayitlari, name='loglar'),
    path('mesaj-gonder/', views.mesaj_gonder, name='mesaj_gonder'),
    path('mesajlas/<int:kullanici_id>/', views.mesajlasma, name='mesajlasma'),
    path('mesajlarim/', views.mesaj_listesi, name='mesajlarim'),
    path('api/kisiler/', api_views.KisiListesiAPI.as_view(), name='api_kisiler'),
    path('api/mesajlar/', api_views.MesajListesiAPI.as_view(), name='api_mesajlar'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/yenile/', TokenRefreshView.as_view(), name='token_refresh'),



]
