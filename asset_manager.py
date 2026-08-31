import os
import pygame
from config import V_WIDTH, V_HEIGHT

class AssetManager:
    def __init__(self):
        self.backgrounds = {}
        self.logo_surface = None

    def load_background(self, loc_id, file_path, fallback_color):
        if os.path.exists(file_path):
            try:
                img = pygame.image.load(file_path).convert()
                self.backgrounds[loc_id] = pygame.transform.smoothscale(img, (V_WIDTH, V_HEIGHT))
                return
            except pygame.error:
                pass
        
        surf = pygame.Surface((V_WIDTH, V_HEIGHT))
        surf.fill(fallback_color)
        self.backgrounds[loc_id] = surf

    def get_background(self, loc_id):
        return self.backgrounds.get(loc_id)

    def load_or_generate_logo(self, path="assets/logo.png"):
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                self.logo_surface = pygame.transform.smoothscale(img, (400, 240))
                return self.logo_surface
            except pygame.error:
                pass

        # Процедурний мемний логотип
        surf = pygame.Surface((440, 240), pygame.SRCALPHA)
        # Аура
        pygame.draw.ellipse(surf, (245, 195, 65, 50), (20, 20, 400, 200))
        # Хлібина
        rect = pygame.Rect(70, 50, 300, 140)
        pygame.draw.rect(surf, (220, 150, 60), rect, border_radius=45)
        pygame.draw.rect(surf, (160, 95, 30), rect, width=8, border_radius=45)
        # Надрізи
        for off in [-60, 0, 60]:
            start = (220 + off - 15, 75)
            end = (220 + off + 15, 165)
            pygame.draw.line(surf, (130, 65, 20), start, end, 9)
            pygame.draw.line(surf, (250, 210, 130), (start[0]-2, start[1]), (end[0]-2, end[1]), 3)
        self.logo_surface = surf
        return surf

    @staticmethod
    def generate_icon():
        icon = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.rect(icon, (220, 150, 60), (4, 12, 56, 40), border_radius=12)
        pygame.draw.rect(icon, (150, 85, 25), (4, 12, 56, 40), width=3, border_radius=12)
        pygame.draw.line(icon, (130, 65, 20), (22, 18), (28, 46), 4)
        pygame.draw.line(icon, (130, 65, 20), (36, 18), (42, 46), 4)
        return icon

    @staticmethod
    def generate_bread_surface(width, height, curse_level=0.0):
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, width, height)

        t = min(1.0, curse_level / 80.0)
        crust_r = int(215 * (1 - t) + 40 * t)
        crust_g = int(145 * (1 - t) + 30 * t)
        crust_b = int(60 * (1 - t) + 45 * t)

        border_r = int(155 * (1 - t) + 20 * t)
        border_g = int(90 * (1 - t) + 10 * t)
        border_b = int(30 * (1 - t) + 25 * t)

        pygame.draw.rect(surf, (crust_r, crust_g, crust_b), rect, border_radius=40)
        pygame.draw.rect(surf, (border_r, border_g, border_b), rect, width=6, border_radius=40)

        for offset_x in [-50, 0, 50]:
            start = (width // 2 + offset_x - 15, height // 2 - 35)
            end = (width // 2 + offset_x + 15, height // 2 + 35)
            cut_color = (int(120 * (1 - t) + 15 * t), int(60 * (1 - t) + 5 * t), int(20 * (1 - t) + 15 * t))
            pygame.draw.line(surf, cut_color, start, end, 8)

        if curse_level > 35:
            center = (width // 2, height // 2)
            open_ratio = min(1.0, (curse_level - 35) / 40.0)
            eye_h = int(24 * open_ratio)
            if eye_h > 2:
                pygame.draw.ellipse(surf, (220, 220, 200), (center[0] - 22, center[1] - eye_h // 2, 44, eye_h))
                pygame.draw.circle(surf, (180, 20, 20), center, 5)
                pygame.draw.circle(surf, (0, 0, 0), center, 2)

        return surf