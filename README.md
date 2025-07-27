# Rehber Projesi

Bu proje Django ile geliştirilmiş bir telefon rehberi uygulamasıdır. Kullanıcılar sisteme kayıt olabilir, giriş yapabilir, kişi bilgileri ekleyebilir ve diğer kullanıcılarla mesajlaşabilir.

## Özellikler

- Kullanıcı kayıt ve giriş sistemi
- Bilgi (Ad, Soyad, Telefon, Tarih) ekleme, güncelleme, silme
- Kategorilere göre filtreleme (Aile, İş, Acil, Diğer)
- Bootstrap ile şık tasarım
- Kullanıcı işlemlerini loglama
- Gelen kutusu ve mesajlaşma sistemi
- REST API ile mobil uyumluluk (JWT Token sistemi)
- Grafiklerle veri analizi
- Admin panelinden log görüntüleme
- GitHub'a versiyon kontrolü

KURULUM TALİMATLARI
----------------------

Bu proje, Django tabanlı bir telefon rehberi uygulamasıdır. Kayıt, giriş, mesajlaşma, loglama, grafiksel analiz ve REST API gibi birçok işlevi içerir.

Gerekli Araçlar
Python 3.9+
Git
pip (Python paket yöneticisi)
MySQL (veya varsayılan olarak SQLite)
Postman (API testleri için - opsiyonel)
1. Projeyi Klonla
git clone https://github.com/umuttkaraaman/rehber-projesi.git
cd rehber-projesi
2. Sanal Ortam Oluştur
python -m venv .venv
source .venv/bin/activate  # Windows için: .venv\Scripts\activate
3. Gereksinimleri Kur
pip install -r requirements.txt
Not: Eğer requirements.txt yoksa, aşağıdaki temel paketleri kurabilirsin:
pip install django djangorestframework djangorestframework-simplejwt mysqlclient
4. Veritabanını Ayarla
python manage.py makemigrations
python manage.py migrate
5. Süper Kullanıcı Oluştur
python manage.py createsuperuser
6. Sunucuyu Başlat
python manage.py runserver

## Geliştirici

**Umut Karaman** – Bilgisayar Programcı
