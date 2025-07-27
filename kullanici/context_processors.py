from .models import Mesaj

def okunmamis_mesaj_sayisi(request):
    if request.user.is_authenticated:
        sayi = Mesaj.objects.filter(alici=request.user, okundu=False).count()
        return {'okunmamis_mesaj_sayisi': sayi}
    return {}
