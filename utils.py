# utils.py
import pygame

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()
        self.cache = {}

    def get_image(self, frame, width, height, scale):
        key = (frame, width, height, scale)
        if key not in self.cache:
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
            image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.cache[key] = image
        return self.cache[key]

    # utils.py
    def get_animation_frames(self, frame_width, frame_height, scale, frame_count=None):
        sheet_width, sheet_height = self.sheet.get_size()
        if frame_count is None:
            frame_count = sheet_width // frame_width
        if frame_width <= 0 or frame_height <= 0 or frame_count <= 0:
            raise ValueError(f"Geçersiz boyutlar: frame_width={frame_width}, frame_height={frame_height}, frame_count={frame_count}")
        frames = []
        for i in range(frame_count):
            if i * frame_width + frame_width <= sheet_width:
                frame = self.get_image(i, frame_width, frame_height, scale)
                frames.append(frame)
            else:
                print(f"Uyarı: Sprite sheet sınırı aşıldı, kare {i} atlandı.")
        return frames


class Font:
    def __init__(self, font_path=None, size=24):
        self.font_path = font_path
        self.size = size
        self._font = None

    @property
    def font(self):
        if self._font is None:
            import pygame
            self._font = pygame.font.Font(self.font_path, self.size) if self.font_path else pygame.font.Font(None, self.size)
        return self._font

    def render(self, text, color=(255, 255, 255), background=None, shadow=False):
        if shadow:
            shadow_surface = self.font.render(text, True, (0, 0, 0))
            main_surface = self.font.render(text, True, color)
            width, height = self.font.size(text)
            final_surface = pygame.Surface((width + 2, height + 2), pygame.SRCALPHA)
            final_surface.blit(shadow_surface, (2, 2))
            final_surface.blit(main_surface, (0, 0))
            return final_surface
        elif background:
            return self.font.render(text, True, color, background)
        return self.font.render(text, True, color)

    def get_size(self, text):
        return self.font.size(text)