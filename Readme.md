Discord Bot Yönetim Aracı
Bu araç, birden fazla Discord botunu yönetmek için tasarlanmıştır. Botlar, ses kanalına bağlanma, metin mesajı gönderme, kullanıcı banlama, susturma, atma, DM gönderme, çekiliş başlatma ve destek talebi (ticket) sistemi kurma gibi işlemleri gerçekleştirebilir.
Kurulum

Python Kurulumu: Python 3.8 veya üstü bir sürümün yüklü olduğundan emin olun.
Gerekli Kütüphaneler: setup.bat dosyasını çalıştırarak gerekli kütüphaneleri yükleyin:setup.bat


Token Dosyası: Proje klasöründe bir tokens.txt dosyası oluşturun ve her satıra bir Discord bot token'ı ekleyin. Örnek:
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
7. Çekiliş başlat: Belirtilen metin kanalında bir çekiliş başlatır. Katılımcılar 🎉 emojisine tıklayarak katılır, süre sonunda belirtilen sayıda kazanan rastgele seçilir. Çekiliş, botun adıyla düzenlenir (örneğin, "Çekiliş BotAdı tarafından düzenleniyor.").
8. Ticket sistemi kur: Belirtilen metin kanalında bir destek talebi sistemi kurar. Kullanıcılar 📩 emojisine tıklayarak ticket oluşturabilir. Ticket kanalı, yalnızca kullanıcı, bot ve yönetici rolleri için görünür olur. Ticket'ı kapatmak için ticket kanalındaki "Ticket'ı Kapat" butonuna tıklayın.
9. Çıkış: Programı sonlandırır.


Girdiler:

Sunucu ID'si: İşlem yapılacak Discord sunucusunun ID'si.
Kanal ID'si: Ses veya metin kanalının ID'si.
Kullanıcı ID'si: İşlem yapılacak kullanıcının ID'si (ban, sustur, at veya DM için).
Mesaj: Gönderilecek mesaj içeriği (metin kanalı veya DM için).
Çekiliş süresi: Çekilişin dakika cinsinden süresi (pozitif bir sayı).
Çekiliş ödülü: Çekilişte verilecek ödülün tanımı.
Kazanan sayısı: Çekilişte seçilecek kazanan sayısı (varsayılan 1).
Kategori ID'si: Ticket kanallarının oluşturulacağı kategori ID'si (isteğe bağlı).



Notlar

Botun çalışması için tokens.txt dosyasında en az bir geçerli Discord bot token'ı olmalıdır.
Botun sunucuda uygun yetkilere (ban, kick, mute, mesaj gönderme, tepki okuma, kanal oluşturma, buton kullanımı vb.) sahip olduğundan emin olun.
Çekiliş için botun tepki okuma, mesaj gönderme ve embed gönderme izinleri olmalıdır.
Ticket sistemi için botun kanal oluşturma, tepki okuma, mesaj gönderme, embed gönderme ve buton kullanımı izinleri olmalıdır.
Çekiliş süresi ve kazanan sayısı pozitif tam sayılar olmalıdır, aksi takdirde hata mesajı gönderilir.
Hata mesajları konsolda ve (mümkünse) Discord kanalında görüntülenir. Sorun giderme için bu mesajları kontrol edin.
Programı durdurmak için Ctrl+C kullanabilirsiniz.

Gereksinimler

Python 3.8+
discord.py kütüphanesi (2.0 veya üstü, buton desteği için)
Geçerli Discord bot token'ları

Starlarınızı atmayı unutmayın güncellenecektir

By Hype discord kullanıcı adım = forcces_41093