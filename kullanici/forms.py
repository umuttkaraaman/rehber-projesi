from django import forms
from django.contrib.auth.models import User
from .models import KisiBilgisi, Mesaj, KATEGORI_SECENEKLERI
from datetime import date


# 📨 Yeni Mesaj Başlatma Formu
class YeniMesajForm(forms.Form):
    alici = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Kime",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mesaj = forms.CharField(
        label="Mesaj",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )


# 📨 Mesaj Gönderme (model tabanlı)
class MesajForm(forms.ModelForm):
    class Meta:
        model = Mesaj
        fields = ['mesaj']  # 'alici' kaldırıldı
        widgets = {
            'mesaj': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }



# 👤 Profil Güncelleme Formu
class KullaniciProfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# 📝 Kayıt Formu
class KullaniciKayitForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# 📇 Kişi Bilgisi Formu
class KullaniciBilgiForm(forms.ModelForm):
    kategori = forms.ChoiceField(
        choices=KATEGORI_SECENEKLERI,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = KisiBilgisi
        fields = ['ad', 'soyad', 'telefon', 'tarih', 'kategori']
        widgets = {
            'ad': forms.TextInput(attrs={'class': 'form-control'}),
            'soyad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'tarih': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': date.today().isoformat()
            }),
        }

    def clean_telefon(self):
        tel = self.cleaned_data.get('telefon')
        if not tel.isdigit():
            raise forms.ValidationError("Telefon numarası sadece rakamlardan oluşmalıdır.")
        if len(tel) > 11:
            raise forms.ValidationError("Telefon numarası en fazla 11 haneli olmalıdır.")
        return tel

    def clean_tarih(self):
        tarih = self.cleaned_data.get('tarih')
        if tarih and tarih < date.today():
            raise forms.ValidationError("Bugünden önceki bir tarih girilemez.")
        return tarih
