from django.contrib import admin
from .models import KullaniciLog
from django.contrib import admin
from .models import Mesaj

admin.site.register(Mesaj)


@admin.register(KullaniciLog)
class KullaniciLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'islem', 'zaman')
    list_filter = ('user', 'zaman')
    search_fields = ('user__username', 'islem')


