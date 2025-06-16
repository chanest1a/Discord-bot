Discord Bot Yönetim Aracı

Bu araç, birden fazla Discord botunu yönetmek için tasarlanmıştır. Botlar, ses kanalına bağlanma, metin mesajı gönderme, kullanıcı banlama, susturma, atma ve DM gönderme gibi işlemleri gerçekleştirebilir.
Kurulum

Python Kurulumu: Python 3.8 veya üstü bir sürümün yüklü olduğundan emin olun.
Gerekli Kütüphaneler: setup.bat dosyasını çalıştırarak gerekli kütüphaneleri yükleyin:setup.bat


Token Dosyası: 
Proje klasöründe bir tokens.txt dosyası oluşturun ve her satıra bir Discord bot token'ı ekleyin. Örnek:
BOT_TOKEN_1

BOT_TOKEN_2



Kullanım

Botu Başlatma: Botu başlatmak için start.bat dosyasını çalıştırın:
start.bat


Menü Seçenekleri:

1. Ses kanalına bağlan: Botları belirtilen ses kanalına bağlar.
2. Metin kanalına mesaj gönder: Botlar belirtilen metin kanalına mesaj gönderir.
3. Kullanıcıyı banla: Belirtilen kullanıcıyı sunucudan banlar.
4. Kullanıcıyı sustur: Belirtilen kullanıcıyı susturur.
5. Kullanıcıyı at: Belirtilen kullanıcıyı sunucudan atar.
6. Kullanıcıya DM gönder: Belirtilen kullanıcıya özel mesaj gönderir.
7. Çıkış: Programı sonlandırır.


Girdiler:

Sunucu ID'si: İşlem yapılacak Discord sunucusunun ID'si.
Kanal ID'si: Ses veya metin kanalının ID'si.
Kullanıcı ID'si: İşlem yapılacak kullanıcının ID'si (ban, sustur, at veya DM için).
Mesaj: Gönderilecek mesaj içeriği (metin kanalı veya DM için).



Notlar

Botun çalışması için tokens.txt dosyasında en az bir geçerli Discord bot token'ı olmalıdır.
Botun sunucuda uygun yetkilere (ban, kick, mute vb.) sahip olduğundan emin olun.
Hata mesajları konsolda görüntülenir. Sorun giderme için bu mesajları kontrol edin.
Programı durdurmak için Ctrl+C kullanabilirsiniz.

Gereksinimler

Python 3.8+
discord.py kütüphanesi
Geçerli Discord bot token'ları

Dosyalar

enhanced_discord_bot.py: Ana bot scripti.
start.bat: Botu başlatır.
setup.bat: Gerekli kütüphaneleri yükler.
tokens.txt: Bot token'larınızı saklayacağınız dosya (kendi oluşturmanız gerekir).
README.md: Bu dosya, kullanım kılavuzu.

