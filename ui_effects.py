import math
import random
import pygame

class Particle:
    def __init__(self, x, y, is_horror=False):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, -1)
        self.size = random.randint(3, 7)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.04)
        self.is_horror = is_horror

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.25
        self.life -= self.decay

    def draw(self, surface):
        if self.life > 0:
            color = (80, 20, 30) if self.is_horror else (220, 160, 80)
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), max(1, int(self.size * self.life)))


class FloatingText:
    def __init__(self, text, x, y, font, color=(245, 195, 65)):
        self.text = text
        self.font = font
        self.x = x + random.randint(-15, 15)
        self.y = y + random.randint(-10, 10)
        self.color = color
        self.life = 1.0
        self.decay = 0.025

    def update(self):
        self.y -= 1.2
        self.life -= self.decay

    def draw(self, surface):
        if self.life > 0:
            rendered = self.font.render(self.text, True, self.color)
            rendered.set_alpha(int(self.life * 255))
            surface.blit(rendered, (self.x, self.y))


class NotificationBanner:
    def __init__(self):
        self.active = False
        self.text = ""
        self.subtext = ""
        self.timer = 0.0
        self.duration = 6.0
        self.anim_y = -80.0

    def show(self, text, subtext=""):
        self.active = True
        self.text = text
        self.subtext = subtext
        self.timer = self.duration
        self.anim_y = -80.0

    def hide(self):
        self.active = False

    def update(self, dt):
        if not self.active:
            return

        self.timer -= dt
        if self.timer <= 0:
            self.active = False
            return

        target_y = 15.0 if self.timer > 0.6 else -90.0
        self.anim_y += (target_y - self.anim_y) * 0.15

    def draw(self, surface, font_main, font_small, screen_w):
        if not self.active or self.anim_y < -75:
            return

        banner_w = min(580, screen_w - 40)
        banner_h = 56
        bx = screen_w // 2 - banner_w // 2
        by = int(self.anim_y)

        pulse = (math.sin(self.timer * 6.0) + 1) / 2
        bg_col = (50 + int(30 * pulse), 20 + int(15 * pulse), 30)
        border_col = (245, 195, 65) if pulse > 0.4 else (200, 70, 80)

        banner_rect = pygame.Rect(bx, by, banner_w, banner_h)
        pygame.draw.rect(surface, bg_col, banner_rect, border_radius=10)
        pygame.draw.rect(surface, border_col, banner_rect, width=2, border_radius=10)

        t_surf = font_main.render(self.text, True, (255, 235, 150))
        surface.blit(t_surf, (banner_rect.centerx - t_surf.get_width() // 2, banner_rect.y + 8))

        if self.subtext:
            s_surf = font_small.render(self.subtext, True, (220, 200, 210))
            surface.blit(s_surf, (banner_rect.centerx - s_surf.get_width() // 2, banner_rect.y + 32))


class HorrorEndingSequence:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.active = False
        self.timer = 0.0
        self.horror_type = "eldritch_tentacle_maw"
        
        self.lines = [
            "ЦВІЛЬ ПОГЛИНУЛА ВСЕ БУТТЯ ЦЬОГО СВІТУ...",
            "РЕАЛЬНІСТЬ ЗГНИЛА. ХЛІБ БІЛЬШЕ НЕ НАЛЕЖИТЬ ТОБІ.",
            "ГРУ ЗАКІНЧЕНО. ПЕРЕРОДИСЯ ЧЕРЕЗ ДЕРЕВО ЕВОЛЮЦІЇ."
        ]
        self.char_index = 0
        self.line_index = 0
        self.char_delay = 0.045
        self.char_timer = 0.0
        self.text_complete = False

    def trigger(self, horror_type="eldritch_tentacle_maw"):
        if not self.active:
            self.active = True
            self.timer = 0.0
            self.horror_type = horror_type
            self.char_index = 0
            self.line_index = 0
            self.char_timer = 0.0
            self.text_complete = False

    def update(self, dt):
        if not self.active:
            return

        self.timer += dt
        if self.timer > 1.2 and not self.text_complete:
            self.char_timer += dt
            if self.char_timer >= self.char_delay:
                self.char_timer = 0.0
                if self.line_index < len(self.lines):
                    current_line = self.lines[self.line_index]
                    if self.char_index < len(current_line):
                        self.char_index += 1
                    else:
                        self.line_index += 1
                        self.char_index = 0
                else:
                    self.text_complete = True

    def draw(self, surface, font_horror, font_btn, mouse_pos):
        if not self.active:
            return None

        # Фаза 1: Унікальний процедурний скример для кожної локації
        if self.timer < 1.2:
            flash_col = (random.randint(180, 255), 0, 0) if random.random() < 0.6 else (255, 255, 255)
            surface.fill(flash_col)

            cx, cy = self.w // 2 + random.randint(-20, 20), self.h // 2 + random.randint(-20, 20)

            if "cyber" in self.horror_type:
                # Кібер-череп з неоновим глітчем
                pygame.draw.rect(surface, (0, 255, 255), (cx - 100, cy - 100, 200, 200), width=6)
                pygame.draw.rect(surface, (255, 0, 80), (cx - 70, cy - 50, 40, 40))
                pygame.draw.rect(surface, (255, 0, 80), (cx + 30, cy - 50, 40, 40))
                for _ in range(25):
                    gx = random.randint(0, self.w)
                    gy = random.randint(0, self.h)
                    pygame.draw.line(surface, (0, 255, 100), (gx, gy), (gx + random.randint(20, 150), gy), 4)

            elif "pigeon" in self.horror_type:
                # Мутантний паразитний голуб
                pygame.draw.circle(surface, (40, 40, 50), (cx, cy), 120)
                pygame.draw.polygon(surface, (220, 180, 20), [(cx, cy + 40), (cx - 30, cy + 120), (cx + 30, cy + 120)])
                pygame.draw.circle(surface, (255, 0, 0), (cx - 45, cy - 20), 28)
                pygame.draw.circle(surface, (255, 0, 0), (cx + 45, cy - 20), 28)
                pygame.draw.circle(surface, (0, 0, 0), (cx - 45, cy - 20), 10)
                pygame.draw.circle(surface, (0, 0, 0), (cx + 45, cy - 20), 10)

            elif "cosmic" in self.horror_type or "horizon" in self.horror_type:
                # Космічне Око Сингулярності
                pygame.draw.ellipse(surface, (20, 0, 30), (cx - 240, cy - 150, 480, 300))
                pygame.draw.ellipse(surface, (255, 50, 50), (cx - 140, cy - 90, 280, 180))
                pygame.draw.circle(surface, (0, 0, 0), (cx, cy), 50)
                pygame.draw.circle(surface, (255, 255, 255), (cx - 15, cy - 15), 14)

            elif "ghost" in self.horror_type or "mill" in self.horror_type:
                # Білий привид з чорними очницями
                pygame.draw.ellipse(surface, (230, 230, 240), (cx - 130, cy - 180, 260, 360))
                pygame.draw.ellipse(surface, (0, 0, 0), (cx - 50, cy - 60, 35, 65))
                pygame.draw.ellipse(surface, (0, 0, 0), (cx + 15, cy - 60, 35, 65))
                pygame.draw.ellipse(surface, (0, 0, 0), (cx - 30, cy + 40, 60, 90))

            else:
                # Елдріч-Паща з іклами
                pygame.draw.ellipse(surface, (10, 0, 5), (cx - 220, cy - 140, 440, 280))
                pygame.draw.circle(surface, (230, 20, 20), (cx - 70, cy - 20), 40)
                pygame.draw.circle(surface, (230, 20, 20), (cx + 70, cy - 20), 40)
                pygame.draw.circle(surface, (0, 0, 0), (cx - 70, cy - 20), 12)
                pygame.draw.circle(surface, (0, 0, 0), (cx + 70, cy - 20), 12)
                pygame.draw.polygon(surface, (200, 200, 200), [
                    (cx - 90, cy + 50), (cx - 60, cy + 90), (cx - 30, cy + 50),
                    (cx, cy + 100), (cx + 30, cy + 50), (cx + 60, cy + 90), (cx + 90, cy + 50)
                ])

            for _ in range(12):
                gy = random.randint(0, self.h)
                gh = random.randint(4, 25)
                pygame.draw.rect(surface, (0, 0, 0), (0, gy, self.w, gh))

            return None

        # Фаза 2: Друкарський текст
        surface.fill((8, 5, 8))
        start_y = self.h // 2 - 100
        for i in range(self.line_index):
            line_surf = font_horror.render(self.lines[i], True, (210, 40, 40) if i == 1 else (210, 190, 190))
            surface.blit(line_surf, (self.w // 2 - line_surf.get_width() // 2, start_y + i * 38))

        if self.line_index < len(self.lines):
            partial_text = self.lines[self.line_index][:self.char_index] + ("_" if int(self.timer * 6) % 2 == 0 else "")
            line_surf = font_horror.render(partial_text, True, (240, 60, 60) if self.line_index == 1 else (210, 190, 190))
            surface.blit(line_surf, (self.w // 2 - line_surf.get_width() // 2, start_y + self.line_index * 38))

        if self.text_complete:
            btn_rect = pygame.Rect(self.w // 2 - 190, start_y + len(self.lines) * 38 + 35, 380, 52)
            is_hover = btn_rect.collidepoint(mouse_pos)
            pulse = (math.sin(self.timer * 4) + 1) / 2
            bg_col = (140 + int(40 * pulse), 30, 45) if is_hover else (90 + int(30 * pulse), 20, 30)
            
            pygame.draw.rect(surface, bg_col, btn_rect, border_radius=10)
            pygame.draw.rect(surface, (245, 195, 65), btn_rect, width=2, border_radius=10)

            btn_txt = font_btn.render("ВІДКРИТИ ДЕРЕВО ПЕРЕРОДЖЕННЯ", True, (255, 240, 220))
            surface.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2, btn_rect.centery - btn_txt.get_height() // 2))

            return btn_rect

        return None