import pygame

class SoundManager:
    def __init__(self):
        # Mixer'ı başlat
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        
        # Ses dosyalarını yükle
        self.sounds = {}
        self.channels = {}
        self.load_sounds()
        self.assign_channels()
        
    def load_sounds(self):
        """Tüm ses dosyalarını yükler."""
        sound_files = {
            "hit": "sounds/hit.wav",
            "potion": "sounds/potion.wav",
            "click": "sounds/click.wav",
            "arrow_hit": "sounds/arrow_hit.wav",
            "blacksmith_hammer": "sounds/blacksmith_hammer.wav"
        }
        
        for sound_name, sound_path in sound_files.items():
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                print(f"Ses yüklendi: {sound_name} ({sound_path})")
            except FileNotFoundError:
                print(f"Uyarı: Ses dosyası bulunamadı: {sound_path}")
                self.sounds[sound_name] = None
        
    def assign_channels(self):
        """Sesler için özel kanallar atar."""
        self.channels = {
            "hit": pygame.mixer.Channel(0),        # Oyuncu ve düşman vuruşları
            "potion": pygame.mixer.Channel(1),     # İksir toplama
            "click": pygame.mixer.Channel(2),      # NPC diyalog tıklamaları
            "arrow_hit": pygame.mixer.Channel(3),  # Ok çarpması
            "blacksmith_hammer": pygame.mixer.Channel(4)  # Demircinin çekici
        }
        
    def play_sound(self, sound_name, volume=1.0, loops=0):
        """Belirtilen sesi çalar."""
        if sound_name not in self.sounds or self.sounds[sound_name] is None:
            print(f"Uyarı: {sound_name} sesi yüklü değil!")
            return
        
        channel = self.channels.get(sound_name, pygame.mixer.Channel(5))  # Varsayılan kanal
        channel.set_volume(volume)
        channel.play(self.sounds[sound_name], loops=loops)
        print(f"Ses çalınıyor: {sound_name}, Ses seviyesi: {volume}, Döngü: {loops}")
        
    def stop_sound(self, sound_name):
        """Belirtilen sesin çalmasını durdurur."""
        if sound_name in self.channels:
            self.channels[sound_name].stop()
            print(f"Ses durduruldu: {sound_name}")
        
    def set_volume(self, sound_name, volume):
        """Belirtilen ses için ses seviyesini ayarlar."""
        if sound_name in self.channels:
            self.channels[sound_name].set_volume(volume)
            print(f"Ses seviyesi güncellendi: {sound_name}, Yeni seviye: {volume}")

# SoundManager örneğini oluştur
sound_manager = SoundManager()
