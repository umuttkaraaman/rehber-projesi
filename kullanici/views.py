from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from datetime import datetime, date
from collections import defaultdict

from .forms import (
    KullaniciKayitForm, KullaniciBilgiForm, KullaniciProfilForm,
    MesajForm, YeniMesajForm
)
from .models import KisiBilgisi, KullaniciLog, Mesaj

@login_required
def mesaj_gonder(request):
    if request.method == 'POST':
        form = YeniMesajForm(request.POST)
        if form.is_valid():
            alici = form.cleaned_data['alici']
            mesaj_icerik = form.cleaned_data['mesaj']
            mesaj = Mesaj.objects.create(
                gonderen=request.user,
                alici=alici,
                mesaj=mesaj_icerik
            )
            return redirect('mesajlasma', kullanici_id=alici.id)
    else:
        form = YeniMesajForm()
    return render(request, 'kullanici/mesaj_gonder.html', {'form': form})


# ✔⃣ MESAJLARIM SAYFASI
@login_required
def mesaj_listesi(request):
    gonderilenler = Mesaj.objects.filter(gonderen=request.user).values_list('alici', flat=True)
    alinanlar = Mesaj.objects.filter(alici=request.user).values_list('gonderen', flat=True)
    tum_kisiler = set(list(gonderilenler) + list(alinanlar))
    kisiler = User.objects.filter(id__in=tum_kisiler).exclude(id=request.user.id)

    if request.method == 'POST':
        form = YeniMesajForm(request.POST)
        if form.is_valid():
            alici = form.cleaned_data['alici']
            mesaj_icerik = form.cleaned_data['mesaj']
            Mesaj.objects.create(gonderen=request.user, alici=alici, mesaj=mesaj_icerik)
            return redirect('mesajlasma', kullanici_id=alici.id)
    else:
        form = YeniMesajForm()

    return render(request, 'kullanici/mesaj_listesi.html', {
        'kisiler': kisiler,
        'form': form
    })


# ✔⃣ MESAJLAŞMA SAYFASI
@login_required
def mesajlasma(request, kullanici_id):
    alici = get_object_or_404(User, id=kullanici_id)
    mesajlar = Mesaj.objects.filter(
        (Q(gonderen=request.user) & Q(alici=alici)) |
        (Q(gonderen=alici) & Q(alici=request.user))
    ).order_by('tarih')

    # 👀 Okunmamış mesajları okundu olarak işaretle
    Mesaj.objects.filter(gonderen=alici, alici=request.user, okundu=False).update(okundu=True)

    if request.method == 'POST':
        form = MesajForm(request.POST)
        if form.is_valid():
            mesaj = form.save(commit=False)
            mesaj.gonderen = request.user
            mesaj.alici = alici
            mesaj.save()
            return redirect('mesajlasma', kullanici_id=alici.id)
    else:
        form = MesajForm()

    return render(request, 'kullanici/chat.html', {
        'form': form,
        'mesajlar': mesajlar,
        'alici': alici
    })




# ✔⃣ GELEN KUTUSU
@login_required
def gelen_kutusu(request):
    mesajlar = Mesaj.objects.filter(alici=request.user).order_by('-tarih')
    return render(request, 'kullanici/gelen_kutusu.html', {'mesajlar': mesajlar})


# ✔⃣ ADMİN LOG SAYFASI
@staff_member_required
def log_kayitlari(request):
    query = request.GET.get('q', '')
    start = request.GET.get('start')
    end = request.GET.get('end')

    loglar = KullaniciLog.objects.select_related('user').order_by('-zaman')

    if query:
        loglar = loglar.filter(user__username__icontains=query)

    if start and end:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            loglar = loglar.filter(zaman__range=(start_date, end_date))
        except:
            pass

    paginator = Paginator(loglar, 15)
    page = request.GET.get('page')
    loglar = paginator.get_page(page)

    return render(request, 'kullanici/loglar.html', {
        'loglar': loglar,
        'query': query,
        'start': start,
        'end': end,
    })


# ✔⃣ GRAFİK SAYFASI
@staff_member_required
def grafik_sayfasi(request):
    veriler = KisiBilgisi.objects.all()
    sayac = defaultdict(int)

    for bilgi in veriler:
        gun = bilgi.tarih if isinstance(bilgi.tarih, date) else bilgi.tarih.date()
        sayac[str(gun)] += 1

    labels = list(sayac.keys())
    values = list(sayac.values())

    return render(request, "kullanici/grafik.html", {
        "labels": labels,
        "values": values
    })


# ✔⃣ KAYIT OL
def kayit_ol(request):
    if request.method == 'POST':
        form = KullaniciKayitForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('giris')
    else:
        form = KullaniciKayitForm()
    return render(request, 'kullanici/kayit.html', {'form': form})


# ✔⃣ GİRİŞ
def giris_yap(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            KullaniciLog.objects.create(user=user, islem="Giriş yaptı")
            return redirect('bilgi_gir')
        else:
            return render(request, 'kullanici/giris.html', {'hata': 'Geçersiz bilgiler'})
    return render(request, 'kullanici/giris.html')


# ✔⃣ BİLGİ GİRİŞİ
@login_required
def bilgi_gir(request):
    if request.method == 'POST':
        form = KullaniciBilgiForm(request.POST)
        if form.is_valid():
            bilgi = form.save(commit=False)
            bilgi.user = request.user
            bilgi.save()
            KullaniciLog.objects.create(user=request.user, islem="Yeni bilgi ekledi")
            return redirect('profil')
    else:
        form = KullaniciBilgiForm()

    return render(request, 'kullanici/bilgi_gir.html', {
        'form': form,
        'today': date.today().isoformat()
    })


# ✔⃣ PROFİL GÖRÜNTÜLEME
@login_required
def profil(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    kategori = request.GET.get('kategori')

    if request.user.is_staff:
        bilgiler = KisiBilgisi.objects.all()
    else:
        bilgiler = KisiBilgisi.objects.filter(user=request.user)

    if query:
        bilgiler = bilgiler.filter(
            Q(ad__icontains=query) |
            Q(soyad__icontains=query) |
            Q(telefon__icontains=query)
        )

    if kategori:
        bilgiler = bilgiler.filter(kategori=kategori)

    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            bilgiler = bilgiler.filter(tarih__range=[start, end])
        except ValueError:
            pass

    paginator = Paginator(bilgiler, 10)
    page = request.GET.get('page')
    bilgiler = paginator.get_page(page)

    return render(request, 'kullanici/profil.html', {
        'bilgiler': bilgiler,
        'query': query,
        'start': start_date,
        'end': end_date,
        'kategori': kategori,
    })


# ✔⃣ GÜNCELLEME
@login_required
def bilgi_guncelle(request, id):
    bilgi = get_object_or_404(KisiBilgisi, id=id, user=request.user)
    if request.method == 'POST':
        form = KullaniciBilgiForm(request.POST, instance=bilgi)
        if form.is_valid():
            KullaniciLog.objects.create(user=request.user, islem=f"{bilgi.ad} bilgisini güncelledi")
            form.save()
            return redirect('profil')
    else:
        form = KullaniciBilgiForm(instance=bilgi)
    return render(request, 'kullanici/bilgi_gir.html', {'form': form})


# ✔⃣ SİLME
@login_required
def bilgi_sil(request, id):
    bilgi = get_object_or_404(KisiBilgisi, id=id, user=request.user)
    if request.method == 'POST':
        KullaniciLog.objects.create(user=request.user, islem=f"{bilgi.ad} bilgisi silindi")
        bilgi.delete()
        return redirect('profil')
    return render(request, 'kullanici/bilgi_sil.html', {'bilgi': bilgi})


# ✔⃣ HESAP GÜNCELLEME
@login_required
def hesap_duzenle(request):
    if request.method == 'POST':
        form = KullaniciProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = KullaniciProfilForm(instance=request.user)
    return render(request, 'kullanici/hesap_duzenle.html', {'form': form})


# ✔⃣ ÇIKIŞ
def cikis_yap(request):
    logout(request)
    return redirect('giris')