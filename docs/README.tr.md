# Bir web uygulamasını yükleyin, eşleştirin ve güncelleyin

## Tanıdığınız birine kontrol panelini gönderin

Örnek. Sebastian tren kalkışlarını gösteren bir web uygulaması oluşturuyor. Amcası zaten resmi Home Assistant Companion Uygulamasını kullanıyor ve kontrol paneline erişimi var. Sebastian tarayıcı bağlantısını WhatsApp aracılığıyla gönderir.

1. PWA Web-App Studio'de uygulamayı açın, Erişim'e gidin, Companion Uygulaması aracılığıyla oturum açmayı etkinleştirin ve kaydedin. Her iki uygulamanın da HTTPS üzerinden aynı Home Assistant sunucusuna ulaşması gerekir.

2. Misafiriniz tarayıcısında WhatsApp bağlantısını açar ve Companion App aracılığıyla Oturum Aç'ı seçer. Web uygulaması bir cihaz kodunu görüntüler. Konuk gerekirse kopyalayabilir.

3. Home Assistant Aç'a dokunun. Uygulamanın, hesabın ve kodun eşleştiğini doğrulayın. Eşleştirme sayfası bir kod isterse web uygulamasında gösterilen kodu yapıştırın veya girin. Daha sonra oturum açmayı onaylayın.

4. Orijinal tarayıcı sekmesine geri dönün. Otomatik olarak oturum açar. Gerekirse Onayı kontrol et'e dokunun. Kod beş dakika süreyle ve tek oturum açma işlemi için geçerlidir.

5. iPhone veya iPad'de yüklü kopyada oturum açmak için önce sayfayı Safari'deki Ana Ekrana ekleyin. Ana Ekran simgesini açın ve aynı onay sürecini orada başlatın.

## Stüdyoyu Bul

Entegrasyon donanımını kullanın, ardından Home Assistant iletişim kutusu aracılığıyla Studio'yu açın. Uygulamalar üzerinde sık sık çalışıyorsanız entegrasyon ayarlarında Kenar Çubuğu Paneli anahtar varlığını etkinleştirin ve kısayolu görünür tutmak için açın.

Bakım panosu için /pwa-app-studio'ye giden bir düğme kartı ekleyin. İsteğe bağlı PWA Tasarımcısını Aç düğmesi varlığı da onu aktif yönetici oturumunuzda açabilir. Önce bu varlığı etkinleştirin; Home Assistant bunu varsayılan olarak devre dışı bırakır.

## Misafir kontrol panelini tasarlayın ve güncelleyin

Örneğin, Wi-Fi bilgi kartı ve veranda ışığıyla ziyaretçiler için bir kontrol paneli oluşturun. İçerik altında, tek tek kartları seçin ve bir ön ayar seçin veya mevcut bir kartı içe aktarın. Görsel düzenleyiciyi kullanarak başlığı, varlığı veya Markdown'yi ayarlayın ve telefon önizlemesini kontrol edin.

Uygulama adımında Uygulama sürümünü 1.1 olarak ayarlayın ve kaydedin. Uygulamayı hâlâ açık olan bir misafir, uygulama yeni revizyonu algıladığında bir güncelleme başlığı görür. Uygulamayı güncelle öğesine dokunduğunuzda görünüm yeniden yüklenir ve ana ekran simgesi ile tarayıcı oturumu korunur. Daha sonra açılan bir uygulama, bağlandığında geçerli sürümü yükler.

## Android'den paylaş

Studio'da Bağlantı paylaşımını kullanın. Uygulama veya tarayıcı bunu sağladığında yerel iletişim kutusu açılır. Companion Uygulaması paylaşım API'si sunmuyorsa tarayıcıda paylaşım sayfasını açın. Ayrıca bağlantıyı kopyalayabilirsiniz.

[English README](../README.md) · [Deutsch](../README.de.md)
