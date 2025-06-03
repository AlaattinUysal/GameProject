# GameProject

## 🎮 Proje Hakkında

GameProject, Python ve Pygame kullanılarak geliştirilmiş, modüler yapıda bir 2D oyun projesidir. Oyunda karakter, düşmanlar, haritalar, envanter ve ses yönetimi gibi birçok temel oyun mekaniği bulunmaktadır. Proje, kolayca genişletilebilir ve özelleştirilebilir şekilde tasarlanmıştır.

## 🚀 Özellikler

- Modüler ve okunabilir kod yapısı
- Farklı düşman tipleri ve yapay zekâ
- Harita ve seviye yönetimi
- Menü arayüzü ve kullanıcı etkileşimi
- Ses ve müzik yönetimi
- Envanter ve eşya sistemi
- Kolayca yeni içerik eklenebilir

## 🛠️ Kurulum

### Gereksinimler

- Python 3.8+
- [Pygame](https://www.pygame.org/) kütüphanesi
- Numpy kütüphanesi

### Kurulum Adımları

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/AlaattinUysal/GameProject.git
   cd GameProject
   ```
2. Gerekli paketleri yükleyin:
   ```bash
   pip install pygame
   pip install numpy
   ```
3. Oyunu başlatmak için:
   ```bash
   python game.py
   ```
   veya menüden başlatmak için:
   ```bash
   python menu/menu.py
   ```

## 📁 Proje Yapısı

```
GameProject/
│
├── game.py              # Ana oyun dosyası
├── menu/                # Menü ve arayüz dosyaları
├── player.py            # Oyuncu karakteri
├── enemy.py             # Düşmanlar ve tipleri
├── map.py               # Harita yönetimi
├── items.py             # Eşyalar ve envanter
├── soundmanager.py      # Ses yönetimi
├── utils.py             # Yardımcı fonksiyonlar
├── ...                  # Diğer modüller ve varlıklar
```

## 👾 Kullanım

- Oyunu başlatın ve menüden yeni oyun veya devam et seçeneklerini kullanın.
- Karakterinizi yön tuşlarıyla hareket ettirin.
- Düşmanlarla savaşın, eşyaları toplayın ve haritayı keşfedin.
- Oyun içi sesler ve müzikler otomatik olarak yönetilir.

## 🧑‍💻 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz! Lütfen büyük değişiklikler için önce bir issue açarak neyi değiştirmek istediğinizi tartışın.

1. Projeyi fork'layın
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniozellik`)
3. Değişikliklerinizi commit'leyin (`git commit -m 'Açıklama'`)
4. Branch'i push'layın (`git push origin feature/yeniozellik`)
5. Bir Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakabilirsiniz.

## 📬 İletişim

Her türlü soru ve öneriniz için mail: alaaddinuysal9@gmail.com
