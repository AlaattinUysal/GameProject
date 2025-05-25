import pygame
import os

class SoundManager:
    def __init__(self):
        # Mixer'ı başlat
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        
        # Ses dosyalarını yükle
        self.sounds = {}
        self.ambiance_sounds = {}
        self.boss_sounds = {}
        self.boss_songs = [
            "sounds/ambiance/boss0.wav",
            "sounds/ambiance/boss1.wav",
            "sounds/ambiance/boss2.wav",
            "sounds/ambiance/boss3.wav",
            "sounds/ambiance/boss4.wav"
        ]
        self.channels = {}
        self.ambiance_channel = pygame.mixer.Channel(6)  # Ambians için özel kanal
        self.boss_music_channel = pygame.mixer.Channel(7)  # Boss müziği için özel kanal
        self.current_ambiance = None  # Şu an çalan ambiyans müziği
        self.current_boss_song_index = -1
        self.is_boss_music_playing = False
        self.transition_delay = 0  # Ses geçişi için gecikme (milisaniye cinsinden)
        
        self.load_sounds()
        self.load_ambiance_sounds()
        self.load_boss_sounds()
        self.assign_channels()
        
    def load_sounds(self):
        """Efekt ses dosyalarını yükler."""
        sound_files = {
            "hit": "sounds/others/hit.wav",
            "potion": "sounds/others/potion.wav",
            "click": "sounds/others/click.wav",
            "arrow_hit": "sounds/others/arrow_hit.wav",
            "blacksmith_hammer": "sounds/others/blacksmith_hammer.wav"
        }
        
        for sound_name, sound_path in sound_files.items():
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                print(f"Ses yüklendi: {sound_name} ({sound_path})")
            except FileNotFoundError:
                print(f"Uyarı: Ses dosyası bulunamadı: {sound_path}")
                self.sounds[sound_name] = None
        
    def load_ambiance_sounds(self):
        """Ambians müzik dosyalarını yükler."""
        ambiance_files = {
            "village": "sounds/ambiance/village.wav",
            "frozen_cave": "sounds/ambiance/frozen_cave.wav",
            "cyberpunk": "sounds/ambiance/cyberpunk.wav",
            "lab": "sounds/ambiance/lab.wav",
            "castle": "sounds/ambiance/castle.wav"
        }
        
        for map_name, sound_path in ambiance_files.items():
            try:
                self.ambiance_sounds[map_name] = pygame.mixer.Sound(sound_path)
                print(f"Ambians müziği yüklendi: {map_name} ({sound_path})")
            except FileNotFoundError:
                print(f"Uyarı: Ambians müziği bulunamadı: {sound_path}")
                self.ambiance_sounds[map_name] = None

    def load_boss_sounds(self):
        """Boss müzik dosyalarını yükler."""
        for i, song_path in enumerate(self.boss_songs):
            try:
                if os.path.exists(song_path):
                    self.boss_sounds[f"boss_{i}"] = pygame.mixer.Sound(song_path)
                    print(f"Boss müziği yüklendi: {song_path}")
                else:
                    print(f"Uyarı: Boss müzik dosyası bulunamadı: {song_path}")
                    self.boss_sounds[f"boss_{i}"] = None
            except Exception as e:
                print(f"Boss müziği yüklenirken hata: {song_path}, {e}")
                self.boss_sounds[f"boss_{i}"] = None
        
    def assign_channels(self):
        """Sesler için özel kanallar atar."""
        self.channels = {
            "hit": pygame.mixer.Channel(0),
            "potion": pygame.mixer.Channel(1),
            "click": pygame.mixer.Channel(2),
            "arrow_hit": pygame.mixer.Channel(3),
            "blacksmith_hammer": pygame.mixer.Channel(4)
        }
        
    def play_sound(self, sound_name, volume=1.0, loops=0):
        """Belirtilen sesi çalar."""
        if sound_name not in self.sounds or self.sounds[sound_name] is None:
            print(f"Uyarı: {sound_name} sesi yüklü değil!")
            return
        
        channel = self.channels.get(sound_name, pygame.mixer.Channel(5))
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
    
    def play_ambiance(self, map_name, volume=0.3):
        """Belirtilen harita için ambiyans müziğini çalar, castle için boss müzikleri oynatılır."""
        if map_name == "castle":
            if not self.is_boss_music_playing:
                self.stop_ambiance()  # Ambians müziğini durdur
                self.transition_delay = 2000  # 2 saniye gecikme
                print("castle haritasına geçildi, boss müziği başlatılmak için sıraya alındı")
            return
        if map_name not in self.ambiance_sounds or self.ambiance_sounds[map_name] is None:
            print(f"Uyarı: {map_name} için ambiyans müziği yüklü değil!")
            self.stop_ambiance()
            return
        if self.current_ambiance != map_name:
            self.stop_ambiance()
            if self.is_boss_music_playing:
                self.stop_boss_music()
            self.ambiance_channel.set_volume(volume)
            self.ambiance_channel.play(self.ambiance_sounds[map_name], loops=-1, fade_ms=1500)
            self.current_ambiance = map_name
            print(f"Ambians müziği çalınıyor: {map_name}, Ses seviyesi: {volume}")
        
    def stop_ambiance(self):
        """Mevcut ambiyans müziğini durdurur."""
        if self.current_ambiance:
            self.ambiance_channel.fadeout(2000)  # 2 saniyelik fade-out
            print(f"Ambians müziği durduruldu: {self.current_ambiance}")
            self.current_ambiance = None

    def play_boss_music(self):
        """Boss müziğini sırayla çalar."""
        if not self.boss_sounds or self.is_boss_music_playing:
            print("Boss şarkıları yok veya zaten çalıyor")
            return
        max_attempts = len(self.boss_songs)
        for _ in range(max_attempts):
            self.current_boss_song_index = (self.current_boss_song_index + 1) % len(self.boss_songs)
            song_key = f"boss_{self.current_boss_song_index}"
            if song_key in self.boss_sounds and self.boss_sounds[song_key] is not None:
                try:
                    self.stop_ambiance()
                    self.boss_music_channel.set_volume(0.5)
                    self.boss_music_channel.play(self.boss_sounds[song_key], loops=0, fade_ms=1500)  # 1.5 saniyelik fade-in
                    self.is_boss_music_playing = True
                    print(f"Boss şarkısı oynatılıyor: {self.boss_songs[self.current_boss_song_index]}")
                    return
                except Exception as e:
                    print(f"Boss şarkısı oynatılırken hata: {self.boss_songs[self.current_boss_song_index]}, {e}")
                    self.boss_sounds[song_key] = None
                    continue
            else:
                print(f"Uyarı: Boss şarkısı yüklü değil: {song_key}")
        self.is_boss_music_playing = False
        self.current_boss_song_index = -1
        print("Hata: Hiçbir boss şarkısı oynatılamadı!")

    def stop_boss_music(self):
        """Boss müziğini durdurur."""
        if self.is_boss_music_playing:
            self.boss_music_channel.fadeout(2000)  # 2 saniyelik fade-out
            self.is_boss_music_playing = False
            self.current_boss_song_index = -1
            print("Boss müziği durduruldu")

    def update_boss_music(self):
        """Boss müziğinin bitip bitmediğini kontrol eder ve bir sonraki şarkıya geçer."""
        if self.is_boss_music_playing and not self.boss_music_channel.get_busy():
            print("Boss şarkısı bitti, bir sonrakine geçiliyor")
            self.is_boss_music_playing = False
            self.play_boss_music()
        elif self.transition_delay > 0:
            self.transition_delay -= 16.67  # Yaklaşık 60 FPS için milisaniye cinsinden azalma
            if self.transition_delay <= 0:
                self.play_boss_music()

# SoundManager örneğini oluştur
sound_manager = SoundManager()
