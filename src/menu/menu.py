import pygame
import sys
import os
import traceback

# Add the parent directory to the system path to make absolute imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Use absolute import
from menu.main import Menu

def main():
    """Ana program başlangıç fonksiyonu"""
    print("Program başlatılıyor...")
    # Pygame'i başlat
    pygame.init()
    pygame.mixer.init()
    
    # Menüyü oluştur ve çalıştır
    menu = Menu()
    try:
        menu.run()
    except Exception as e:
        print(f"Hata oluştu: {e}")
        print("Hata detayları:")
        traceback.print_exc()
    finally:
        # Programı düzgün şekilde sonlandır
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()


