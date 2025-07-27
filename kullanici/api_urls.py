from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import KisiListesiAPI, MesajListesiAPI

urlpatterns = [
    path('kisiler/', KisiListesiAPI.as_view(), name='kisi-listesi'),
    path('mesajlar/', MesajListesiAPI.as_view(), name='mesaj-listesi'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/yenile/', TokenRefreshView.as_view(), name='token_refresh'),
]
