import math
import sys
import random
import pygame

from config import (
    LOCATIONS_DATA, ACHIEVEMENTS_DATA, MEDAL_ARTIFACTS, PANEL_BG, PANEL_BORDER, 
    TEXT_WHITE, ACCENT_GOLD, BUTTON_BG, BUTTON_HOVER, BUTTON_DISABLED
)
from asset_manager import AssetManager
from game_state import GameState
from save_manager import SaveManager
from sound_manager import SoundManager
from ui_effects import Particle, FloatingText, HorrorEndingSequence, NotificationBanner

pygame.init()

# Роздільні здатності
RESOLUTIONS = [
    (1280, 720),
    (1600, 900),
    (1920, 1080)
]

display_info = pygame.display.Info()
native_w, native_h = display_info.current_w, display_info.current_h

is_fullscreen = True
selected_res_idx = 0
cur_w, cur_h = native_w, native_h

pygame.display.set_icon(AssetManager.generate_icon())
screen = pygame.display.set_mode((cur_w, cur_h), pygame.FULLSCREEN | pygame.RESIZABLE)
pygame.display.set_caption("Bread Simulator: 12 Realms & Artifacts Edition")
clock = pygame.time.Clock()

def format_number(num):
    val = float(num)
    if val < 1000:
        return f"{int(val)}" if val == int(val) else f"{val:.1f}"
    
    suffixes = [
        (1e18, "Qi"),
        (1e15, "Qa"),
        (1e12, "T"),
        (1e9, "B"),
        (1e6, "M"),
        (1e3, "K")
    ]
    for threshold, suffix in suffixes:
        if val >= threshold:
            formatted = f"{val / threshold:.2f}"
            if formatted.endswith(".00"):
                formatted = formatted[:-3]
            elif formatted.endswith("0"):
                formatted = formatted[:-1]
            return f"{formatted}{suffix}"
    return f"{int(val)}"

def get_fonts(h):
    scale = max(0.85, min(1.25, h / 800.0))
    font_name = "Segoe UI, Arial, sans-serif"
    return {
        "splash_title": pygame.font.SysFont(font_name, int(38 * scale), bold=True),
        "title": pygame.font.SysFont(font_name, int(18 * scale), bold=True),
        "main": pygame.font.SysFont(font_name, int(14 * scale), bold=True),
        "small": pygame.font.SysFont(font_name, int(11 * scale)),
        "desc": pygame.font.SysFont(font_name, int(12 * scale)),
        "horror": pygame.font.SysFont("Courier New, monospace", int(17 * scale), bold=True)
    }

fonts = get_fonts(cur_h)

assets = AssetManager()
for loc in LOCATIONS_DATA:
    assets.load_background(loc["id"], loc["image_file"], loc["fallback_color"])
logo_surf = assets.load_or_generate_logo("assets/logo.png")

audio = SoundManager()
game = GameState()
SaveManager.load_game(game)

horror_ending = HorrorEndingSequence(cur_w, cur_h)
notification_banner = NotificationBanner()

particles = []
floating_texts = []
scale_factor = 1.0
click_anim_timer = 0.0
scroll_y = 0
ach_scroll_y = 0
loc_scroll_y = 0
art_scroll_y = 0

# Стани меню
game_state_mode = "SPLASH"
show_prestige_menu = False
show_locations_hub = False
show_achievements_hub = False
show_artifacts_hub = False
reset_confirm_timer = 0.0

temp_fullscreen = is_fullscreen
temp_res_idx = selected_res_idx

selected_perk_id = "core_seed"
tree_pan_x = 0.0
tree_pan_y = 0.0
is_dragging_tree = False
drag_start_mouse = (0, 0)
drag_start_pan = (0.0, 0.0)
has_dragged = False
splash_timer = 0.0
auto_save_timer = 0.0

def get_max_ach_scroll(view_height):
    total_content_h = len(ACHIEVEMENTS_DATA) * 76 + 20
    return min(0, -(total_content_h - view_height))

def get_max_loc_scroll(view_height):
    total_content_h = len(game.locations) * 76 + 20
    return min(0, -(total_content_h - view_height))

def get_max_art_scroll(view_height):
    total_content_h = len(MEDAL_ARTIFACTS) * 76 + 20
    return min(0, -(total_content_h - view_height))

def apply_display_settings():
    global screen, is_fullscreen, selected_res_idx, cur_w, cur_h, fonts, horror_ending
    is_fullscreen = temp_fullscreen
    selected_res_idx = temp_res_idx

    if is_fullscreen:
        cur_w, cur_h = native_w, native_h
        screen = pygame.display.set_mode((cur_w, cur_h), pygame.FULLSCREEN | pygame.RESIZABLE)
    else:
        cur_w, cur_h = RESOLUTIONS[selected_res_idx]
        screen = pygame.display.set_mode((cur_w, cur_h), pygame.RESIZABLE)

    fonts = get_fonts(cur_h)
    horror_ending = HorrorEndingSequence(cur_w, cur_h)

def trigger_achievement_check():
    newly_unlocked = game.check_achievements()
    for ach in newly_unlocked:
        notification_banner.show(f"ДОСЯГНЕННЯ: {ach['name']}!", "Заберіть Медалі у вікні досягнень!")
        audio.play("buy")

# --- 1. Окреме Меню: Скарбниця Артефактів за Медалі ---
def draw_artifacts_hub(surface, mouse_pos):
    overlay = pygame.Surface((cur_w, cur_h), pygame.SRCALPHA)
    overlay.fill((10, 8, 12, 240))
    surface.blit(overlay, (0, 0))

    box_w = min(840, cur_w - 60)
    box_h = min(620, cur_h - 60)
    box_rect = pygame.Rect(cur_w // 2 - box_w // 2, cur_h // 2 - box_h // 2, box_w, box_h)
    pygame.draw.rect(surface, (28, 22, 26), box_rect, border_radius=16)
    pygame.draw.rect(surface, (140, 90, 110), box_rect, width=2, border_radius=16)

    title = fonts["title"].render("Скарбниця Артефактів (Постійні бонуси за Медалі)", True, ACCENT_GOLD)
    surface.blit(title, (box_rect.x + 30, box_rect.y + 18))

    medal_stat = f"Ваші Медалі: {format_number(game.medals)} мед."
    m_txt = fonts["main"].render(medal_stat, True, (255, 230, 120))
    surface.blit(m_txt, (box_rect.right - 230, box_rect.y + 20))

    scroll_top = box_rect.y + 55
    scroll_bottom = box_rect.bottom - 120
    view_h = scroll_bottom - scroll_top
    view_clip = pygame.Rect(box_rect.x + 15, scroll_top, box_rect.w - 30, view_h)
    surface.set_clip(view_clip)

    hovered_artifact = None
    card_y = scroll_top + 5 + art_scroll_y
    for art_key, art in MEDAL_ARTIFACTS.items():
        c_rect = pygame.Rect(box_rect.x + 25, card_y, box_w - 60, 68)
        is_bought = art_key in game.unlocked_artifacts
        can_buy = (game.medals >= art["cost"]) and not is_bought

        is_hover = view_clip.collidepoint(mouse_pos) and c_rect.collidepoint(mouse_pos)
        if is_hover:
            hovered_artifact = art

        if is_bought:
            bg_col = (35, 50, 38)
            border_col = (110, 200, 130)
        elif can_buy:
            bg_col = (70, 52, 30)
            border_col = ACCENT_GOLD
        else:
            bg_col = (28, 22, 26)
            border_col = (60, 50, 55)

        pygame.draw.rect(surface, bg_col, c_rect, border_radius=8)
        pygame.draw.rect(surface, border_col, c_rect, width=2 if (can_buy or is_bought) else 1, border_radius=8)

        status_prefix = "[АКТИВОВАНО] " if is_bought else "[АРТЕФАКТ] "
        n_txt = fonts["main"].render(status_prefix + art["name"], True, (255, 235, 140) if (can_buy or is_bought) else (160, 150, 155))
        surface.blit(n_txt, (c_rect.x + 15, c_rect.y + 12))

        d_txt = fonts["small"].render(art["desc"], True, (220, 220, 220) if is_bought else (175, 165, 170))
        surface.blit(d_txt, (c_rect.x + 15, c_rect.y + 38))

        btn_rect = pygame.Rect(c_rect.right - 145, c_rect.y + 16, 130, 36)
        if is_bought:
            pygame.draw.rect(surface, (45, 65, 48), btn_rect, border_radius=6)
            pygame.draw.rect(surface, (110, 200, 130), btn_rect, width=1, border_radius=6)
            b_txt = fonts["small"].render("КУПЛЕНО", True, (170, 240, 170))
        elif can_buy:
            pulse = (math.sin(pygame.time.get_ticks() * 0.008) + 1) / 2
            btn_col = (95 + int(35 * pulse), 70 + int(20 * pulse), 25)
            pygame.draw.rect(surface, btn_col, btn_rect, border_radius=6)
            pygame.draw.rect(surface, ACCENT_GOLD, btn_rect, width=2, border_radius=6)
            b_txt = fonts["small"].render(f"КУПИТИ ({art['cost']} мед.)", True, TEXT_WHITE)
        else:
            pygame.draw.rect(surface, (35, 28, 32), btn_rect, border_radius=6)
            pygame.draw.rect(surface, (55, 45, 50), btn_rect, width=1, border_radius=6)
            b_txt = fonts["small"].render(f"{art['cost']} мед.", True, (130, 120, 125))

        surface.blit(b_txt, (btn_rect.centerx - b_txt.get_width() // 2, btn_rect.centery - b_txt.get_height() // 2))

        card_y += 76

    surface.set_clip(None)

    # Скролбар
    max_s = get_max_art_scroll(view_h)
    if max_s < 0:
        bar_track = pygame.Rect(box_rect.right - 22, scroll_top, 6, view_h)
        pygame.draw.rect(surface, (40, 32, 36), bar_track, border_radius=3)
        thumb_h = max(25, int(view_h * (view_h / (len(MEDAL_ARTIFACTS) * 76 + 20))))
        thumb_prog = art_scroll_y / max_s
        thumb_y = scroll_top + int(thumb_prog * (view_h - thumb_h))
        pygame.draw.rect(surface, ACCENT_GOLD, (box_rect.right - 22, thumb_y, 6, thumb_h), border_radius=3)

    # Tooltip / Інформаційний блок опису
    info_box = pygame.Rect(box_rect.x + 25, box_rect.bottom - 105, box_w - 180, 52)
    pygame.draw.rect(surface, (18, 14, 16), info_box, border_radius=8)
    pygame.draw.rect(surface, (70, 55, 60), info_box, width=1, border_radius=8)

    if hovered_artifact:
        tip_title = fonts["main"].render(f"{hovered_artifact['name']} — {hovered_artifact['cost']} Медалей", True, ACCENT_GOLD)
        tip_desc = fonts["small"].render(f"Властивість: {hovered_artifact['desc']} (зберігається назавжди після скидань)", True, TEXT_WHITE)
        surface.blit(tip_title, (info_box.x + 12, info_box.y + 6))
        surface.blit(tip_desc, (info_box.x + 12, info_box.y + 28))
    else:
        tip_hint = fonts["small"].render("Наведіть курсор на будь-який артефакт для перегляду деталей.", True, (150, 140, 145))
        surface.blit(tip_hint, (info_box.x + 12, info_box.y + 18))

    close_btn = pygame.Rect(box_rect.right - 135, box_rect.bottom - 98, 110, 38)
    pygame.draw.rect(surface, BUTTON_BG, close_btn, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORDER, close_btn, width=2, border_radius=8)
    c_btn_txt = fonts["main"].render("Закрити", True, TEXT_WHITE)
    surface.blit(c_btn_txt, (close_btn.centerx - c_btn_txt.get_width() // 2, close_btn.centery - c_btn_txt.get_height() // 2))

# --- 2. Меню Досягнень ---
def draw_achievements_hub(surface, mouse_pos):
    overlay = pygame.Surface((cur_w, cur_h), pygame.SRCALPHA)
    overlay.fill((10, 8, 12, 240))
    surface.blit(overlay, (0, 0))

    box_w = min(840, cur_w - 60)
    box_h = min(620, cur_h - 60)
    box_rect = pygame.Rect(cur_w // 2 - box_w // 2, cur_h // 2 - box_h // 2, box_w, box_h)
    pygame.draw.rect(surface, (28, 22, 26), box_rect, border_radius=16)
    pygame.draw.rect(surface, (140, 90, 110), box_rect, width=2, border_radius=16)

    title = fonts["title"].render("Список Досягнень Пекаря", True, ACCENT_GOLD)
    surface.blit(title, (box_rect.x + 30, box_rect.y + 18))

    medal_stat = f"Ваші Медалі: {format_number(game.medals)} мед."
    m_txt = fonts["main"].render(medal_stat, True, (255, 230, 120))
    surface.blit(m_txt, (box_rect.right - 230, box_rect.y + 20))

    scroll_top = box_rect.y + 55
    scroll_bottom = box_rect.bottom - 55
    view_h = scroll_bottom - scroll_top
    view_clip = pygame.Rect(box_rect.x + 15, scroll_top, box_rect.w - 30, view_h)
    surface.set_clip(view_clip)

    card_y = scroll_top + 5 + ach_scroll_y
    for ach in ACHIEVEMENTS_DATA:
        c_rect = pygame.Rect(box_rect.x + 25, card_y, box_w - 60, 68)
        is_unlocked = ach["id"] in game.unlocked_achievements
        is_claimed = ach["id"] in game.claimed_achievements

        if is_claimed:
            bg_col = (35, 45, 35)
            border_col = (80, 140, 90)
        elif is_unlocked:
            bg_col = (75, 55, 30)
            border_col = ACCENT_GOLD
        else:
            bg_col = (25, 20, 24)
            border_col = (55, 45, 50)

        pygame.draw.rect(surface, bg_col, c_rect, border_radius=8)
        pygame.draw.rect(surface, border_col, c_rect, width=2 if (is_unlocked and not is_claimed) else 1, border_radius=8)

        status_prefix = "[ВІДКРИТО] " if is_unlocked else "[ЗАБЛОКОВАНО] "
        n_txt = fonts["main"].render(status_prefix + ach["name"], True, (255, 235, 140) if is_unlocked else (150, 140, 145))
        surface.blit(n_txt, (c_rect.x + 15, c_rect.y + 10))

        rew_medals = ach.get("reward_medals", 1)
        reward_desc = f"Нагорода: +{format_number(rew_medals)} Медалей"
        d_txt = fonts["small"].render(f"{ach['desc']} ({reward_desc})", True, (210, 210, 210) if is_unlocked else (105, 100, 105))
        surface.blit(d_txt, (c_rect.x + 15, c_rect.y + 36))

        btn_rect = pygame.Rect(c_rect.right - 145, c_rect.y + 16, 130, 36)
        if is_claimed:
            pygame.draw.rect(surface, (45, 55, 45), btn_rect, border_radius=6)
            pygame.draw.rect(surface, (70, 90, 70), btn_rect, width=1, border_radius=6)
            b_txt = fonts["small"].render("ОТРИМАНО", True, (160, 200, 160))
            surface.blit(b_txt, (btn_rect.centerx - b_txt.get_width() // 2, btn_rect.centery - b_txt.get_height() // 2))
        elif is_unlocked:
            pulse = (math.sin(pygame.time.get_ticks() * 0.008) + 1) / 2
            btn_col = (90 + int(40 * pulse), 65 + int(20 * pulse), 20)
            pygame.draw.rect(surface, btn_col, btn_rect, border_radius=6)
            pygame.draw.rect(surface, ACCENT_GOLD, btn_rect, width=2, border_radius=6)
            b_txt = fonts["small"].render("ЗАБРАТИ", True, TEXT_WHITE)
            surface.blit(b_txt, (btn_rect.centerx - b_txt.get_width() // 2, btn_rect.centery - b_txt.get_height() // 2))
        else:
            pygame.draw.rect(surface, (35, 28, 32), btn_rect, border_radius=6)
            pygame.draw.rect(surface, (55, 45, 50), btn_rect, width=1, border_radius=6)
            b_txt = fonts["small"].render("Недоступно", True, (100, 95, 100))
            surface.blit(b_txt, (btn_rect.centerx - b_txt.get_width() // 2, btn_rect.centery - b_txt.get_height() // 2))

        card_y += 76

    surface.set_clip(None)

    max_s = get_max_ach_scroll(view_h)
    if max_s < 0:
        bar_track = pygame.Rect(box_rect.right - 22, scroll_top, 6, view_h)
        pygame.draw.rect(surface, (40, 32, 36), bar_track, border_radius=3)
        thumb_h = max(25, int(view_h * (view_h / (len(ACHIEVEMENTS_DATA) * 76 + 20))))
        thumb_prog = ach_scroll_y / max_s
        thumb_y = scroll_top + int(thumb_prog * (view_h - thumb_h))
        pygame.draw.rect(surface, ACCENT_GOLD, (box_rect.right - 22, thumb_y, 6, thumb_h), border_radius=3)

    close_btn = pygame.Rect(box_rect.right - 135, box_rect.bottom - 46, 110, 36)
    pygame.draw.rect(surface, BUTTON_BG, close_btn, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORDER, close_btn, width=2, border_radius=8)
    c_btn_txt = fonts["main"].render("Закрити", True, TEXT_WHITE)
    surface.blit(c_btn_txt, (close_btn.centerx - c_btn_txt.get_width() // 2, close_btn.centery - c_btn_txt.get_height() // 2))

# --- 3. Меню Карти Локацій ---
def draw_locations_hub(surface, mouse_pos):
    overlay = pygame.Surface((cur_w, cur_h), pygame.SRCALPHA)
    overlay.fill((10, 8, 12, 240))
    surface.blit(overlay, (0, 0))

    box_w = min(780, cur_w - 60)
    box_h = min(580, cur_h - 60)
    box_rect = pygame.Rect(cur_w // 2 - box_w // 2, cur_h // 2 - box_h // 2, box_w, box_h)
    pygame.draw.rect(surface, (28, 22, 26), box_rect, border_radius=16)
    pygame.draw.rect(surface, (140, 90, 110), box_rect, width=2, border_radius=16)

    title = fonts["title"].render("Карта 12 Світів (4 Тіри)", True, ACCENT_GOLD)
    surface.blit(title, (box_rect.x + 35, box_rect.y + 18))

    view_h = box_rect.h - 105
    view_clip = pygame.Rect(box_rect.x + 15, box_rect.y + 50, box_rect.w - 30, view_h)
    surface.set_clip(view_clip)

    card_y = box_rect.y + 55 + loc_scroll_y
    for i, loc in enumerate(game.locations):
        c_rect = pygame.Rect(box_rect.x + 25, card_y, box_w - 50, 68)
        is_current = (game.current_location_idx == i)
        can_unlock = game.can_unlock_location(i)

        if is_current:
            bg_col = (65, 50, 60)
            border_col = ACCENT_GOLD
        elif loc.unlocked:
            bg_col = (45, 36, 42)
            border_col = (110, 90, 100)
        else:
            bg_col = (25, 20, 24)
            border_col = (55, 45, 50)

        pygame.draw.rect(surface, bg_col, c_rect, border_radius=8)
        pygame.draw.rect(surface, border_col, c_rect, width=2, border_radius=8)

        tier_lbl = f"[Тір {loc.tier}] "
        n_txt = fonts["main"].render(tier_lbl + loc.name, True, TEXT_WHITE if loc.unlocked else (130, 120, 125))
        surface.blit(n_txt, (c_rect.x + 15, c_rect.y + 8))

        amb_txt = fonts["small"].render(loc.ambient, True, (170, 160, 165))
        surface.blit(amb_txt, (c_rect.x + 15, c_rect.y + 28))

        if loc.unlocked:
            pass_val = game.get_location_passive(loc)
            curse_str = "Без цвілі" if loc.curse_rate == 0 else f"Цвіль: {int(loc.curse_level)}%"
            stat_txt = fonts["small"].render(f"Пасив: {format_number(pass_val)}/с | {curse_str}", True, (190, 240, 190))
            surface.blit(stat_txt, (c_rect.x + 15, c_rect.y + 46))

            btn_rect = pygame.Rect(c_rect.right - 135, c_rect.y + 16, 120, 36)
            btn_col = (85, 60, 40) if is_current else (60, 48, 55)
            pygame.draw.rect(surface, btn_col, btn_rect, border_radius=6)
            pygame.draw.rect(surface, ACCENT_GOLD if is_current else PANEL_BORDER, btn_rect, width=1, border_radius=6)
            b_lbl = fonts["small"].render("АКТИВНА" if is_current else "Перейти ->", True, TEXT_WHITE)
            surface.blit(b_lbl, (btn_rect.centerx - b_lbl.get_width() // 2, btn_rect.centery - b_lbl.get_height() // 2))
        else:
            can_buy = (game.crumbs >= loc.cost) and can_unlock
            btn_rect = pygame.Rect(c_rect.right - 185, c_rect.y + 16, 170, 36)
            
            if not can_unlock:
                btn_col = (35, 28, 32)
                border_col = (55, 45, 50)
                b_lbl_str = f"[!] Відкрийте світ {i}"
                lbl_color = (130, 110, 115)
            else:
                btn_col = (95, 65, 30) if can_buy else (45, 35, 40)
                border_col = ACCENT_GOLD if can_buy else (70, 60, 65)
                b_lbl_str = f"Купити ({format_number(loc.cost)} кр.)"
                lbl_color = TEXT_WHITE if can_buy else (130, 120, 125)

            pygame.draw.rect(surface, btn_col, btn_rect, border_radius=6)
            pygame.draw.rect(surface, border_col, btn_rect, width=2, border_radius=8)
            b_lbl = fonts["small"].render(b_lbl_str, True, lbl_color)
            surface.blit(b_lbl, (btn_rect.centerx - b_lbl.get_width() // 2, btn_rect.centery - b_lbl.get_height() // 2))

        card_y += 76

    surface.set_clip(None)

    close_btn = pygame.Rect(box_rect.right - 135, box_rect.bottom - 45, 110, 35)
    pygame.draw.rect(surface, BUTTON_BG, close_btn, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORDER, close_btn, width=2, border_radius=8)
    c_txt = fonts["main"].render("Закрити", True, TEXT_WHITE)
    surface.blit(c_txt, (close_btn.centerx - c_txt.get_width() // 2, close_btn.centery - c_txt.get_height() // 2))

# --- 4. Меню Налаштувань ---
def draw_settings_page(surface, mouse_pos):
    surface.fill((18, 14, 18))

    box_w = min(560, cur_w - 60)
    box_h = min(520, cur_h - 60)
    box_rect = pygame.Rect(cur_w // 2 - box_w // 2, cur_h // 2 - box_h // 2, box_w, box_h)
    pygame.draw.rect(surface, (28, 22, 26), box_rect, border_radius=16)
    pygame.draw.rect(surface, (140, 90, 110), box_rect, width=2, border_radius=16)

    title = fonts["title"].render("Меню & Налаштування", True, ACCENT_GOLD)
    surface.blit(title, (box_rect.x + 35, box_rect.y + 25))

    mode_lbl = fonts["main"].render("Режим Екрана:", True, TEXT_WHITE)
    surface.blit(mode_lbl, (box_rect.x + 35, box_rect.y + 75))

    fs_btn = pygame.Rect(box_rect.x + 190, box_rect.y + 68, 130, 36)
    win_btn = pygame.Rect(box_rect.x + 335, box_rect.y + 68, 130, 36)

    pygame.draw.rect(surface, (90, 70, 40) if temp_fullscreen else BUTTON_BG, fs_btn, border_radius=8)
    pygame.draw.rect(surface, ACCENT_GOLD if temp_fullscreen else PANEL_BORDER, fs_btn, width=2, border_radius=8)
    fs_txt = fonts["small"].render("Повний екран", True, TEXT_WHITE)
    surface.blit(fs_txt, (fs_btn.centerx - fs_txt.get_width() // 2, fs_btn.centery - fs_txt.get_height() // 2))

    pygame.draw.rect(surface, (90, 70, 40) if not temp_fullscreen else BUTTON_BG, win_btn, border_radius=8)
    pygame.draw.rect(surface, ACCENT_GOLD if not temp_fullscreen else PANEL_BORDER, win_btn, width=2, border_radius=8)
    win_txt = fonts["small"].render("У вікні", True, TEXT_WHITE)
    surface.blit(win_txt, (win_btn.centerx - win_txt.get_width() // 2, win_btn.centery - win_txt.get_height() // 2))

    res_lbl = fonts["main"].render("Роздільна Здатність:", True, TEXT_WHITE if not temp_fullscreen else (120, 110, 115))
    surface.blit(res_lbl, (box_rect.x + 35, box_rect.y + 125))

    res_y = box_rect.y + 155
    for i, res in enumerate(RESOLUTIONS):
        btn_r = pygame.Rect(box_rect.x + 35 + (i % 2) * 240, res_y + (i // 2) * 44, 225, 36)
        is_active = (temp_res_idx == i) and (not temp_fullscreen)
        bg = (80, 60, 40) if is_active else (BUTTON_BG if not temp_fullscreen else (35, 28, 32))
        border = ACCENT_GOLD if is_active else (PANEL_BORDER if not temp_fullscreen else (55, 45, 50))
        pygame.draw.rect(surface, bg, btn_r, border_radius=8)
        pygame.draw.rect(surface, border, btn_r, width=2, border_radius=8)
        txt_col = TEXT_WHITE if not temp_fullscreen else (100, 95, 100)
        r_txt = fonts["small"].render(f"{res[0]} x {res[1]}", True, txt_col)
        surface.blit(r_txt, (btn_r.centerx - r_txt.get_width() // 2, btn_r.centery - r_txt.get_height() // 2))

    snd_lbl = fonts["main"].render("Звукові Ефекти:", True, TEXT_WHITE)
    surface.blit(snd_lbl, (box_rect.x + 35, box_rect.y + 260))
    snd_btn = pygame.Rect(box_rect.x + 220, box_rect.y + 252, 140, 36)
    pygame.draw.rect(surface, (60, 100, 60) if audio.enabled else (100, 50, 50), snd_btn, border_radius=8)
    pygame.draw.rect(surface, ACCENT_GOLD if audio.enabled else PANEL_BORDER, snd_btn, width=2, border_radius=8)
    s_state_txt = fonts["small"].render("Увімкнено" if audio.enabled else "Вимкнено", True, TEXT_WHITE)
    surface.blit(s_state_txt, (snd_btn.centerx - s_state_txt.get_width() // 2, snd_btn.centery - s_state_txt.get_height() // 2))

    reset_btn = pygame.Rect(box_rect.x + 35, box_rect.y + 310, 240, 40)
    pygame.draw.rect(surface, (120, 35, 45) if reset_confirm_timer > 0 else (75, 40, 45), reset_btn, border_radius=8)
    pygame.draw.rect(surface, (240, 80, 80), reset_btn, width=2, border_radius=8)
    rst_txt = fonts["small"].render("ПІДТВЕРДИТИ СКИДАННЯ!" if reset_confirm_timer > 0 else "Скинути збереження", True, TEXT_WHITE)
    surface.blit(rst_txt, (reset_btn.centerx - rst_txt.get_width() // 2, reset_btn.centery - rst_txt.get_height() // 2))

    exit_btn = pygame.Rect(box_rect.right - 185, box_rect.y + 310, 150, 40)
    pygame.draw.rect(surface, (60, 30, 35), exit_btn, border_radius=8)
    pygame.draw.rect(surface, (120, 60, 70), exit_btn, width=2, border_radius=8)
    ex_txt = fonts["main"].render("Вийти з гри", True, TEXT_WHITE)
    surface.blit(ex_txt, (exit_btn.centerx - ex_txt.get_width() // 2, exit_btn.centery - ex_txt.get_height() // 2))

    apply_btn = pygame.Rect(box_rect.x + 35, box_rect.bottom - 60, 240, 42)
    pygame.draw.rect(surface, (95, 65, 30), apply_btn, border_radius=8)
    pygame.draw.rect(surface, ACCENT_GOLD, apply_btn, width=2, border_radius=8)
    a_txt = fonts["main"].render("ЗАСТОСУВАТИ ГРАФІКУ", True, TEXT_WHITE)
    surface.blit(a_txt, (apply_btn.centerx - a_txt.get_width() // 2, apply_btn.centery - a_txt.get_height() // 2))

    back_btn = pygame.Rect(box_rect.right - 165, box_rect.bottom - 60, 130, 42)
    pygame.draw.rect(surface, BUTTON_BG, back_btn, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORDER, back_btn, width=2, border_radius=8)
    b_txt = fonts["main"].render("Назад", True, TEXT_WHITE)
    surface.blit(b_txt, (back_btn.centerx - b_txt.get_width() // 2, back_btn.centery - b_txt.get_height() // 2))

# --- 5. Дерево Престижу ---
def draw_radial_prestige_tree(surface, mouse_pos):
    global selected_perk_id, tree_pan_x, tree_pan_y

    overlay = pygame.Surface((cur_w, cur_h), pygame.SRCALPHA)
    overlay.fill((10, 8, 12, 240))
    surface.blit(overlay, (0, 0))

    box_rect = pygame.Rect(40, 30, cur_w - 80, cur_h - 60)
    pygame.draw.rect(surface, (25, 20, 24), box_rect, border_radius=16)
    pygame.draw.rect(surface, (120, 80, 95), box_rect, width=2, border_radius=16)

    title = fonts["title"].render("Дерево Еволюції & Обмінник Сухариків", True, ACCENT_GOLD)
    surface.blit(title, (box_rect.x + 25, box_rect.y + 18))
    
    top_stat_str = f"Золоті Сухарики: {format_number(game.prestige.relics)}"
    relic_txt = fonts["main"].render(top_stat_str, True, (255, 220, 120))
    surface.blit(relic_txt, (box_rect.right - relic_txt.get_width() - 25, box_rect.y + 20))

    viewport_rect = pygame.Rect(box_rect.x + 10, box_rect.y + 55, box_rect.w - 20, box_rect.h - 225)
    view_surf = pygame.Surface((viewport_rect.w, viewport_rect.h))
    view_surf.fill((18, 14, 18))

    grid_spacing = 40
    start_gx = int(tree_pan_x) % grid_spacing
    start_gy = int(tree_pan_y) % grid_spacing
    for gx in range(start_gx, viewport_rect.w, grid_spacing):
        pygame.draw.line(view_surf, (28, 22, 28), (gx, 0), (gx, viewport_rect.h), 1)
    for gy in range(start_gy, viewport_rect.h, grid_spacing):
        pygame.draw.line(view_surf, (28, 22, 28), (0, gy), (viewport_rect.w, gy), 1)

    origin_x = viewport_rect.w // 2 + int(tree_pan_x)
    origin_y = viewport_rect.h // 2 + int(tree_pan_y)

    hovered_perk_id = None
    mouse_rel = (mouse_pos[0] - viewport_rect.x, mouse_pos[1] - viewport_rect.y)
    is_mouse_in_view = viewport_rect.collidepoint(mouse_pos)

    for key, perk in game.prestige.tree_config.items():
        if not game.prestige.is_perk_visible(key):
            continue
        px = origin_x + perk["rel_pos"][0]
        py = origin_y + perk["rel_pos"][1]
        for req_id in perk["reqs"]:
            if not game.prestige.is_perk_visible(req_id):
                continue
            req_perk = game.prestige.tree_config[req_id]
            rx = origin_x + req_perk["rel_pos"][0]
            ry = origin_y + req_perk["rel_pos"][1]
            is_active = (game.prestige.get_perk_level(key) > 0 and game.prestige.get_perk_level(req_id) > 0)
            pygame.draw.line(view_surf, ACCENT_GOLD if is_active else (70, 50, 60), (rx, ry), (px, py), 3 if is_active else 2)

    node_w, node_h = 155, 72

    for key, perk in game.prestige.tree_config.items():
        if not game.prestige.is_perk_visible(key):
            continue
        px = origin_x + perk["rel_pos"][0]
        py = origin_y + perk["rel_pos"][1]
        node_rect = pygame.Rect(px - node_w // 2, py - node_h // 2, node_w, node_h)
        
        is_hover = is_mouse_in_view and node_rect.collidepoint(mouse_rel)
        if is_hover:
            hovered_perk_id = key

        lvl = game.prestige.get_perk_level(key)
        max_l = perk["max_level"]
        is_max = (lvl >= max_l)
        can_buy = game.prestige.can_buy_perk(key)
        is_selected = (selected_perk_id == key)

        if is_max:
            bg_col = (45, 110, 65)
            border_col = (120, 240, 150)
        elif lvl > 0:
            bg_col = (65, 88, 55)
            border_col = ACCENT_GOLD if can_buy else (140, 180, 130)
        elif can_buy:
            bg_col = (110, 85, 40)
            border_col = ACCENT_GOLD
        else:
            bg_col = (40, 32, 36)
            border_col = (70, 55, 60)

        if (is_hover or is_selected) and not is_dragging_tree:
            border_col = (255, 255, 255)

        pygame.draw.rect(view_surf, bg_col, node_rect, border_radius=10)
        pygame.draw.rect(view_surf, border_col, node_rect, width=2 if not is_selected else 3, border_radius=10)

        short_name = perk["name"] if len(perk["name"]) <= 16 else perk["name"][:15] + ".."
        n_surf = fonts["small"].render(short_name, True, TEXT_WHITE)

        lvl_str = f"Рівень: {lvl}/{max_l}" if not is_max else "МАКС. РІВЕНЬ"
        l_surf = fonts["small"].render(lvl_str, True, (190, 240, 190) if lvl > 0 else (175, 165, 170))

        cost_str = "ВІДКРИТО" if is_max else f"Ціна: {format_number(game.prestige.get_perk_cost(key))} Сух."
        c_surf = fonts["small"].render(cost_str, True, (255, 220, 130) if not is_max else (160, 220, 160))

        view_surf.blit(n_surf, (node_rect.x + (node_w - n_surf.get_width()) // 2, node_rect.y + 8))
        view_surf.blit(l_surf, (node_rect.x + (node_w - l_surf.get_width()) // 2, node_rect.y + 28))
        view_surf.blit(c_surf, (node_rect.x + (node_w - c_surf.get_width()) // 2, node_rect.y + 48))

    surface.blit(view_surf, (viewport_rect.x, viewport_rect.y))
    pygame.draw.rect(surface, (80, 60, 70), viewport_rect, width=1, border_radius=4)

    active_detail_id = hovered_perk_id or selected_perk_id
    info_rect = pygame.Rect(box_rect.x + 25, box_rect.bottom - 160, box_rect.w - 50, 95)
    pygame.draw.rect(surface, (18, 14, 16), info_rect, border_radius=10)
    pygame.draw.rect(surface, (80, 60, 70), info_rect, width=1, border_radius=10)

    if active_detail_id and active_detail_id in game.prestige.tree_config and game.prestige.is_perk_visible(active_detail_id):
        info_perk = game.prestige.tree_config[active_detail_id]
        cur_l = game.prestige.get_perk_level(active_detail_id)
        max_l = info_perk["max_level"]
        cost_info = " [МАКСИМАЛЬНИЙ РІВЕНЬ]" if cur_l >= max_l else f" (Наступний рівень: {format_number(game.prestige.get_perk_cost(active_detail_id))} Сух.)"
        
        h_surf = fonts["main"].render(f"Гілка: {info_perk['branch']} | {info_perk['name']} [{cur_l}/{max_l}]{cost_info}", True, ACCENT_GOLD)
        d_surf = fonts["desc"].render(f"{info_perk['desc']} (Бонус діє миттєво)", True, TEXT_WHITE)
        
        surface.blit(h_surf, (info_rect.x + 15, info_rect.y + 12))
        surface.blit(d_surf, (info_rect.x + 15, info_rect.y + 38))

        req_names = [game.prestige.tree_config[r]["name"] for r in info_perk["reqs"]]
        req_str = f"Вимоги: {', '.join(req_names)}" if req_names else "Вимоги: Початкове зерно"
        r_surf = fonts["small"].render(req_str, True, (160, 150, 160))
        surface.blit(r_surf, (info_rect.x + 15, info_rect.y + 66))
    else:
        hint = fonts["desc"].render("Клікайте по вузлу для підвищення рівня. Бонуси починають діяти одразу!", True, (150, 140, 150))
        surface.blit(hint, (info_rect.x + 15, info_rect.y + 35))

    is_fully_cursed = (game.curse_level >= 100.0)

    # Кнопка Переродження
    prestige_btn = pygame.Rect(box_rect.x + 25, box_rect.bottom - 55, 300, 42)
    if is_fully_cursed:
        btn_col = (140, 45, 60)
        p_label = "ПЕРЕРОДИТИСЯ (Очистити цвіль)"
        border_col = ACCENT_GOLD
    else:
        btn_col = (38, 30, 35)
        p_label = "[!] ПОТРІБНО 100% ЦВІЛІ"
        border_col = (65, 50, 55)

    pygame.draw.rect(surface, btn_col, prestige_btn, border_radius=8)
    pygame.draw.rect(surface, border_col, prestige_btn, width=2, border_radius=8)
    p_txt = fonts["main"].render(p_label, True, TEXT_WHITE if is_fully_cursed else (140, 130, 135))
    surface.blit(p_txt, (prestige_btn.centerx - p_txt.get_width() // 2, prestige_btn.centery - p_txt.get_height() // 2))

    # Кнопка Купівлі Золотого Сухарика
    relic_buy_cost = game.get_relic_buy_cost()
    can_buy_relic = is_fully_cursed and (game.crumbs >= relic_buy_cost)
    buy_relic_btn = pygame.Rect(box_rect.x + 340, box_rect.bottom - 55, 360, 42)
    
    if is_fully_cursed:
        pygame.draw.rect(surface, (95, 65, 25) if can_buy_relic else (45, 35, 25), buy_relic_btn, border_radius=8)
        pygame.draw.rect(surface, ACCENT_GOLD if can_buy_relic else (80, 65, 40), buy_relic_btn, width=2, border_radius=8)
        r_buy_label = f"Купити +1 Сухарик: {format_number(relic_buy_cost)} кр."
        r_buy_txt = fonts["small"].render(r_buy_label, True, (255, 235, 140) if can_buy_relic else (160, 145, 130))
    else:
        pygame.draw.rect(surface, (38, 30, 35), buy_relic_btn, border_radius=8)
        pygame.draw.rect(surface, (65, 50, 55), buy_relic_btn, width=2, border_radius=8)
        r_buy_label = "[!] ОБМІН ВІДКРИЄТЬСЯ ПРИ 100% ЦВІЛІ"
        r_buy_txt = fonts["small"].render(r_buy_label, True, (140, 130, 135))

    surface.blit(r_buy_txt, (buy_relic_btn.centerx - r_buy_txt.get_width() // 2, buy_relic_btn.centery - r_buy_txt.get_height() // 2))

    close_btn = pygame.Rect(box_rect.right - 130, box_rect.bottom - 55, 105, 42)
    pygame.draw.rect(surface, BUTTON_BG, close_btn, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORDER, close_btn, width=2, border_radius=8)
    c_txt = fonts["main"].render("Закрити", True, TEXT_WHITE)
    surface.blit(c_txt, (close_btn.centerx - c_txt.get_width() // 2, close_btn.centery - c_txt.get_height() // 2))

# --- Сплеш-скрін ---
def draw_splash_screen(surface, t, mouse_pos):
    surface.fill((16, 12, 16))
    
    logo_rect = logo_surf.get_rect(center=(cur_w // 2, cur_h // 2 - 80))
    scale_anim = 1.0 + 0.03 * math.sin(t * 3.0)
    scaled_logo = pygame.transform.smoothscale(logo_surf, (int(logo_rect.width * scale_anim), int(logo_rect.height * scale_anim)))
    surface.blit(scaled_logo, scaled_logo.get_rect(center=(cur_w // 2, cur_h // 2 - 80)))

    title = fonts["splash_title"].render("BREAD SIMULATOR", True, ACCENT_GOLD)
    sub = fonts["main"].render("Hardcore Achievements & Artifacts Edition", True, (210, 190, 200))
    surface.blit(title, (cur_w // 2 - title.get_width() // 2, cur_h // 2 + 70))
    surface.blit(sub, (cur_w // 2 - sub.get_width() // 2, cur_h // 2 + 120))

    start_btn = pygame.Rect(cur_w // 2 - 140, cur_h // 2 + 165, 280, 46)
    is_hover = start_btn.collidepoint(mouse_pos)
    pygame.draw.rect(surface, (95, 65, 30) if is_hover else (65, 45, 25), start_btn, border_radius=10)
    pygame.draw.rect(surface, ACCENT_GOLD if is_hover else (160, 120, 50), start_btn, width=2, border_radius=10)
    btn_txt = fonts["main"].render("ПОЧАТИ ВИПІЧКУ", True, TEXT_WHITE)
    surface.blit(btn_txt, (start_btn.centerx - btn_txt.get_width() // 2, start_btn.centery - btn_txt.get_height() // 2))

    sett_btn = pygame.Rect(cur_w // 2 - 140, cur_h // 2 + 220, 280, 36)
    is_sett_hover = sett_btn.collidepoint(mouse_pos)
    pygame.draw.rect(surface, BUTTON_HOVER if is_sett_hover else BUTTON_BG, sett_btn, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORDER, sett_btn, width=1, border_radius=8)
    sett_txt = fonts["small"].render("Меню & Налаштування", True, TEXT_WHITE)
    surface.blit(sett_txt, (sett_btn.centerx - sett_txt.get_width() // 2, sett_btn.centery - sett_txt.get_height() // 2))

# --- Головний Цикл ---
running = True
horror_cta_btn_rect = None

while running:
    dt = clock.tick(60) / 1000.0
    mouse_pos = pygame.mouse.get_pos()

    if reset_confirm_timer > 0:
        reset_confirm_timer -= dt

    if click_anim_timer > 0:
        click_anim_timer -= dt

    auto_save_timer += dt
    if auto_save_timer >= 15.0:
        SaveManager.save_game(game)
        auto_save_timer = 0.0

    notification_banner.update(dt)

    shop_w = min(420, max(310, int(cur_w * 0.28)))
    shop_x = cur_w - shop_w - 20
    
    left_panel_w = 300
    left_panel_x = 20

    center_space_left = left_panel_x + left_panel_w
    center_space_right = shop_x
    bread_center = (center_space_left + (center_space_right - center_space_left) // 2, cur_h // 2 + 35)

    base_bread_size = (
        min(380, max(260, int((center_space_right - center_space_left) * 0.55))),
        min(220, max(150, int(cur_h * 0.28)))
    )

    if game_state_mode == "SPLASH":
        splash_timer += dt
    elif game_state_mode == "PLAYING":
        if horror_ending.active:
            horror_ending.update(dt)
        elif not show_prestige_menu and not show_locations_hub and not show_achievements_hub and not show_artifacts_hub:
            game.update_passive(dt)

            if game.curse_level >= 100.0 and not horror_ending.active:
                game.total_jumpscares += 1
                trigger_achievement_check()
                horror_ending.trigger(game.current_location.horror_type)
                audio.play("horror")

    # Тряска камери під час хорору
    if game_state_mode == "PLAYING":
        if horror_ending.active and horror_ending.timer < 1.2:
            shake_x, shake_y = random.randint(-16, 16), random.randint(-16, 16)
        elif game.curse_level > 60 and not horror_ending.active:
            shake_x, shake_y = random.randint(-2, 2), random.randint(-2, 2)
        else:
            shake_x, shake_y = 0, 0
    else:
        shake_x, shake_y = 0, 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SaveManager.save_game(game)
            running = False

        elif event.type == pygame.VIDEORESIZE:
            if not is_fullscreen:
                cur_w, cur_h = event.w, event.h
                screen = pygame.display.set_mode((cur_w, cur_h), pygame.RESIZABLE)
                fonts = get_fonts(cur_h)
                horror_ending = HorrorEndingSequence(cur_w, cur_h)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state_mode == "SETTINGS_PAGE":
                    game_state_mode = "PLAYING"
                elif show_prestige_menu:
                    show_prestige_menu = False
                elif show_locations_hub:
                    show_locations_hub = False
                elif show_achievements_hub:
                    show_achievements_hub = False
                elif show_artifacts_hub:
                    show_artifacts_hub = False
                elif game_state_mode == "SPLASH":
                    running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if horror_ending.active:
                if horror_cta_btn_rect and horror_cta_btn_rect.collidepoint(mouse_pos):
                    horror_ending.active = False
                    show_prestige_menu = True

            elif show_artifacts_hub:
                box_w = min(840, cur_w - 60)
                box_h = min(620, cur_h - 60)
                box_rect = pygame.Rect(cur_w // 2 - box_w // 2, cur_h // 2 - box_h // 2, box_w, box_h)
                scroll_top = box_rect.y + 55
                scroll_bottom = box_rect.bottom - 120

                card_y = scroll_top + 5 + art_scroll_y
                for art_key in MEDAL_ARTIFACTS:
                    btn_rect = pygame.Rect(box_rect.x + box_w - 180, card_y + 16, 130, 36)
                    if btn_rect.collidepoint(mouse_pos) and (scroll_top <= mouse_pos[1] <= scroll_bottom):
                        if game.buy_artifact(art_key):
                            audio.play("buy")
                            SaveManager.save_game(game)
                            floating_texts.append(FloatingText("АРТЕФАКТ АКТИВОВАНО!", mouse_pos[0], mouse_pos[1] - 20, fonts["main"], (140, 240, 160)))
                    card_y += 76

                close_btn = pygame.Rect(box_rect.right - 135, box_rect.bottom - 98, 110, 38)
                if close_btn.collidepoint(mouse_pos):
                    show_artifacts_hub = False

            elif show_achievements_hub:
                box_w = min(840, cur_w - 60)
                box_h = min(620, cur_h - 60)
                box_rect = pygame.Rect(cur_w // 2 - box_w // 2, cur_h // 2 - box_h // 2, box_w, box_h)
                scroll_top = box_rect.y + 55
                scroll_bottom = box_rect.bottom - 55

                card_y = scroll_top + 5 + ach_scroll_y
                for ach in ACHIEVEMENTS_DATA:
                    btn_rect = pygame.Rect(box_rect.x + box_w - 180, card_y + 16, 130, 36)
                    if btn_rect.collidepoint(mouse_pos) and (scroll_top <= mouse_pos[1] <= scroll_bottom):
                        claimed_ach = game.claim_achievement_reward(ach["id"])
                        if claimed_ach:
                            audio.play("buy")
                            SaveManager.save_game(game)
                            floating_texts.append(FloatingText(f"+{format_number(claimed_ach.get('reward_medals', 1))} МЕДАЛЕЙ!", mouse_pos[0], mouse_pos[1] - 20, fonts["main"], ACCENT_GOLD))
                    card_y += 76

                close_btn = pygame.Rect(box_rect.right - 135, box_rect.bottom - 46, 110, 36)
                if close_btn.collidepoint(mouse_pos):
                    show_achievements_hub = False

            elif show_locations_hub:
                box_w = min(780, cur_w - 60)
                box_h = min(580, cur_h - 60)
                box_rect = pygame.Rect(cur_w // 2 - box_w // 2, cur_h // 2 - box_h // 2, box_w, box_h)
                
                card_y = box_rect.y + 55 + loc_scroll_y
                for i, loc in enumerate(game.locations):
                    c_rect = pygame.Rect(box_rect.x + 25, card_y, box_w - 50, 68)
                    if loc.unlocked:
                        btn_rect = pygame.Rect(c_rect.right - 135, c_rect.y + 16, 120, 36)
                        if btn_rect.collidepoint(mouse_pos) and (box_rect.y + 50 <= mouse_pos[1] <= box_rect.bottom - 50):
                            game.current_location_idx = i
                            audio.play("click")
                    else:
                        btn_rect = pygame.Rect(c_rect.right - 185, c_rect.y + 16, 170, 36)
                        if btn_rect.collidepoint(mouse_pos) and (box_rect.y + 50 <= mouse_pos[1] <= box_rect.bottom - 50):
                            if game.can_unlock_location(i):
                                if game.unlock_location(i):
                                    game.current_location_idx = i
                                    audio.play("buy")
                                    trigger_achievement_check()
                    card_y += 76

                close_btn = pygame.Rect(box_rect.right - 135, box_rect.bottom - 45, 110, 35)
                if close_btn.collidepoint(mouse_pos):
                    show_locations_hub = False

            elif game_state_mode == "SETTINGS_PAGE":
                box_w = min(560, cur_w - 60)
                box_h = min(520, cur_h - 60)
                box_rect = pygame.Rect(cur_w // 2 - box_w // 2, cur_h // 2 - box_h // 2, box_w, box_h)

                fs_btn = pygame.Rect(box_rect.x + 190, box_rect.y + 68, 130, 36)
                win_btn = pygame.Rect(box_rect.x + 335, box_rect.y + 68, 130, 36)
                if fs_btn.collidepoint(mouse_pos):
                    temp_fullscreen = True
                elif win_btn.collidepoint(mouse_pos):
                    temp_fullscreen = False

                if not temp_fullscreen:
                    res_y = box_rect.y + 155
                    for i in range(len(RESOLUTIONS)):
                        btn_r = pygame.Rect(box_rect.x + 35 + (i % 2) * 240, res_y + (i // 2) * 44, 225, 36)
                        if btn_r.collidepoint(mouse_pos):
                            temp_res_idx = i

                snd_btn = pygame.Rect(box_rect.x + 220, box_rect.y + 252, 140, 36)
                if snd_btn.collidepoint(mouse_pos):
                    audio.enabled = not audio.enabled

                reset_btn = pygame.Rect(box_rect.x + 35, box_rect.y + 310, 240, 40)
                if reset_btn.collidepoint(mouse_pos):
                    if reset_confirm_timer > 0:
                        SaveManager.reset_save(game)
                        reset_confirm_timer = 0.0
                    else:
                        reset_confirm_timer = 3.0

                exit_btn = pygame.Rect(box_rect.right - 185, box_rect.y + 310, 150, 40)
                if exit_btn.collidepoint(mouse_pos):
                    SaveManager.save_game(game)
                    running = False

                apply_btn = pygame.Rect(box_rect.x + 35, box_rect.bottom - 60, 240, 42)
                if apply_btn.collidepoint(mouse_pos):
                    apply_display_settings()

                back_btn = pygame.Rect(box_rect.right - 165, box_rect.bottom - 60, 130, 42)
                if back_btn.collidepoint(mouse_pos):
                    temp_fullscreen = is_fullscreen
                    temp_res_idx = selected_res_idx
                    game_state_mode = "PLAYING"

            elif game_state_mode == "SPLASH":
                start_btn = pygame.Rect(cur_w // 2 - 140, cur_h // 2 + 165, 280, 46)
                sett_btn = pygame.Rect(cur_w // 2 - 140, cur_h // 2 + 220, 280, 36)
                
                if start_btn.collidepoint(mouse_pos):
                    game_state_mode = "PLAYING"
                elif sett_btn.collidepoint(mouse_pos):
                    temp_fullscreen = is_fullscreen
                    temp_res_idx = selected_res_idx
                    game_state_mode = "SETTINGS_PAGE"

            elif show_prestige_menu:
                box_rect = pygame.Rect(40, 30, cur_w - 80, cur_h - 60)
                viewport_rect = pygame.Rect(box_rect.x + 10, box_rect.y + 55, box_rect.w - 20, box_rect.h - 225)
                
                if viewport_rect.collidepoint(mouse_pos):
                    is_dragging_tree = True
                    drag_start_mouse = mouse_pos
                    drag_start_pan = (tree_pan_x, tree_pan_y)
                    has_dragged = False

                prestige_btn = pygame.Rect(box_rect.x + 25, box_rect.bottom - 55, 300, 42)
                if prestige_btn.collidepoint(mouse_pos) and (game.curse_level >= 100.0):
                    if game.trigger_prestige():
                        SaveManager.save_game(game)
                        show_prestige_menu = False
                        trigger_achievement_check()

                buy_relic_btn = pygame.Rect(box_rect.x + 340, box_rect.bottom - 55, 360, 42)
                if buy_relic_btn.collidepoint(mouse_pos) and (game.curse_level >= 100.0):
                    if game.buy_relic_with_crumbs():
                        audio.play("buy")
                        SaveManager.save_game(game)
                        floating_texts.append(FloatingText("+1 СУХАРИК!", mouse_pos[0], mouse_pos[1] - 25, fonts["main"], (255, 230, 80)))

                close_btn = pygame.Rect(box_rect.right - 130, box_rect.bottom - 55, 105, 42)
                if close_btn.collidepoint(mouse_pos):
                    show_prestige_menu = False
            else:
                # 1. Кнопка Карти
                map_btn_rect = pygame.Rect(left_panel_x + 10, 18, left_panel_w - 20, 30)
                if map_btn_rect.collidepoint(mouse_pos):
                    show_locations_hub = True

                # 2. Ряд 1: Досягнення та Скарбниця Артефактів
                btn_half_w = (left_panel_w - 30) // 2
                ach_btn_rect = pygame.Rect(left_panel_x + 10, 196, btn_half_w, 32)
                if ach_btn_rect.collidepoint(mouse_pos):
                    show_achievements_hub = True

                art_btn_rect = pygame.Rect(left_panel_x + 10 + btn_half_w + 10, 196, btn_half_w, 32)
                if art_btn_rect.collidepoint(mouse_pos):
                    show_artifacts_hub = True

                # 3. Ряд 2: Дерево Престижу та Меню
                p_open_rect = pygame.Rect(left_panel_x + 10, 234, btn_half_w, 32)
                if p_open_rect.collidepoint(mouse_pos):
                    show_prestige_menu = True

                s_open_rect = pygame.Rect(left_panel_x + 10 + btn_half_w + 10, 234, btn_half_w, 32)
                if s_open_rect.collidepoint(mouse_pos):
                    temp_fullscreen = is_fullscreen
                    temp_res_idx = selected_res_idx
                    game_state_mode = "SETTINGS_PAGE"

                # Фізичний клік по батону
                current_center = (bread_center[0] + shake_x, bread_center[1] + shake_y)
                bread_rect = pygame.Rect(
                    current_center[0] - (base_bread_size[0] * scale_factor) / 2,
                    current_center[1] - (base_bread_size[1] * scale_factor) / 2,
                    base_bread_size[0] * scale_factor,
                    base_bread_size[1] * scale_factor,
                )

                if bread_rect.collidepoint(mouse_pos):
                    audio.play("click")
                    click_val, is_crit, relic_dropped = game.manual_click()
                    scale_factor = 0.85
                    click_anim_timer = 0.15
                    
                    is_dark = game.curse_level > 40
                    num_p = random.randint(8, 12) if is_crit else random.randint(4, 7)
                    for _ in range(num_p):
                        particles.append(Particle(mouse_pos[0], mouse_pos[1], is_horror=is_dark))
                    
                    if relic_dropped:
                        floating_texts.append(FloatingText("+1 СУХАРИК!", mouse_pos[0], mouse_pos[1] - 25, fonts["main"], (255, 230, 100)))
                        audio.play("buy")

                    label = f"КРИТ! +{format_number(click_val)}" if is_crit else f"+{format_number(click_val)}"
                    txt_color = (255, 50, 50) if is_crit else ((255, 80, 80) if game.curse_level > 60 else ACCENT_GOLD)
                    floating_texts.append(FloatingText(label, mouse_pos[0], mouse_pos[1], fonts["main"], txt_color))
                    
                    trigger_achievement_check()

                cur_btn_y = 90 + scroll_y
                cur_upgrades = game.current_location.upgrades
                for key in cur_upgrades:
                    btn_rect = pygame.Rect(shop_x + 15, cur_btn_y, shop_w - 30, 80)
                    if btn_rect.collidepoint(mouse_pos) and 80 <= mouse_pos[1] <= cur_h - 30:
                        if game.buy_upgrade(key):
                            audio.play("buy")
                            trigger_achievement_check()
                    cur_btn_y += 90

        elif event.type == pygame.MOUSEMOTION:
            if show_prestige_menu and is_dragging_tree:
                dx = mouse_pos[0] - drag_start_mouse[0]
                dy = mouse_pos[1] - drag_start_mouse[1]
                if abs(dx) > 3 or abs(dy) > 3:
                    has_dragged = True
                tree_pan_x = drag_start_pan[0] + dx
                tree_pan_y = drag_start_pan[1] + dy

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if show_prestige_menu and is_dragging_tree:
                is_dragging_tree = False
                if not has_dragged:
                    box_rect = pygame.Rect(40, 30, cur_w - 80, cur_h - 60)
                    viewport_rect = pygame.Rect(box_rect.x + 10, box_rect.y + 55, box_rect.w - 20, box_rect.h - 225)
                    origin_x = viewport_rect.w // 2 + int(tree_pan_x)
                    origin_y = viewport_rect.h // 2 + int(tree_pan_y)
                    mouse_rel = (mouse_pos[0] - viewport_rect.x, mouse_pos[1] - viewport_rect.y)

                    for key, perk in game.prestige.tree_config.items():
                        if not game.prestige.is_perk_visible(key):
                            continue
                        px = origin_x + perk["rel_pos"][0]
                        py = origin_y + perk["rel_pos"][1]
                        node_rect = pygame.Rect(px - 155 // 2, py - 72 // 2, 155, 72)
                        
                        if node_rect.collidepoint(mouse_rel):
                            selected_perk_id = key
                            if game.prestige.unlock_perk(key):
                                audio.play("buy")
                                SaveManager.save_game(game)
                                trigger_achievement_check()
                            break

        elif event.type == pygame.MOUSEWHEEL:
            if show_artifacts_hub:
                box_h_cur = min(620, cur_h - 60)
                view_h_cur = (box_h_cur - 120) - 55
                max_s = get_max_art_scroll(view_h_cur)
                art_scroll_y = max(max_s, min(0, art_scroll_y + event.y * 40))
            elif show_achievements_hub:
                box_h_cur = min(620, cur_h - 60)
                view_h_cur = (box_h_cur - 55) - 55
                max_s = get_max_ach_scroll(view_h_cur)
                ach_scroll_y = max(max_s, min(0, ach_scroll_y + event.y * 40))
            elif show_locations_hub:
                box_h_cur = min(580, cur_h - 60)
                view_h_cur = box_h_cur - 105
                max_s = get_max_loc_scroll(view_h_cur)
                loc_scroll_y = max(max_s, min(0, loc_scroll_y + event.y * 35))
            elif not show_prestige_menu and game_state_mode == "PLAYING" and not horror_ending.active:
                shop_rect = pygame.Rect(shop_x, 20, shop_w, cur_h - 40)
                if shop_rect.collidepoint(mouse_pos):
                    scroll_y = max(-600, min(0, scroll_y + event.y * 25))

    # --- Отрисовка на екран ---
    if game_state_mode == "SPLASH":
        draw_splash_screen(screen, splash_timer, mouse_pos)
    elif game_state_mode == "SETTINGS_PAGE":
        draw_settings_page(screen, mouse_pos)
    else:
        scale_factor += (1.0 - scale_factor) * 0.15
        particles = [p for p in particles if p.life > 0]
        for p in particles:
            p.update()
        floating_texts = [ft for ft in floating_texts if ft.life > 0]
        for ft in floating_texts:
            ft.update()

        current_loc_data = LOCATIONS_DATA[game.current_location_idx]
        bg_surface = assets.get_background(current_loc_data["id"])
        if bg_surface.get_size() != (cur_w, cur_h):
            bg_surface = pygame.transform.smoothscale(bg_surface, (cur_w, cur_h))
        screen.blit(bg_surface, (0, 0))

        # Панель статистики ліворуч (300px)
        ui_overlay = pygame.Surface((left_panel_w, 280), pygame.SRCALPHA)
        ui_overlay.fill((15, 12, 15, 215))
        screen.blit(ui_overlay, (left_panel_x, 10))
        pygame.draw.rect(screen, (70, 60, 65), (left_panel_x, 10, left_panel_w, 280), width=1, border_radius=10)

        map_btn_rect = pygame.Rect(left_panel_x + 10, 18, left_panel_w - 20, 30)
        pygame.draw.rect(screen, BUTTON_BG, map_btn_rect, border_radius=6)
        pygame.draw.rect(screen, ACCENT_GOLD, map_btn_rect, width=1, border_radius=6)
        m_txt = fonts["small"].render(f"Світ: {game.current_location.name} [Змінити]", True, ACCENT_GOLD)
        screen.blit(m_txt, (map_btn_rect.centerx - m_txt.get_width() // 2, map_btn_rect.centery - m_txt.get_height() // 2))

        crumb_title = fonts["title"].render(f"Крихти: {format_number(game.crumbs)}", True, ACCENT_GOLD)
        stat_cps = fonts["main"].render(f"Всього пасив: {format_number(game.get_total_passive_income())}/с", True, TEXT_WHITE)
        stat_click = fonts["main"].render(f"Сила кліку: +{format_number(game.get_effective_click_power())}", True, TEXT_WHITE)
        screen.blit(crumb_title, (left_panel_x + 15, 56))
        screen.blit(stat_cps, (left_panel_x + 15, 88))
        screen.blit(stat_click, (left_panel_x + 15, 114))

        curse_val = game.curse_level
        if curse_val > 0 or game.current_location.curse_rate > 0:
            bar_w, bar_h = left_panel_w - 30, 10
            pygame.draw.rect(screen, (30, 30, 30), (left_panel_x + 15, 146, bar_w, bar_h), border_radius=4)
            fill_w = int((min(100.0, curse_val) / 100.0) * bar_w)
            pygame.draw.rect(screen, (170, 30, 45), (left_panel_x + 15, 146, fill_w, bar_h), border_radius=4)
            curse_lbl = fonts["small"].render(f"Цвіль світу: {int(curse_val)}%", True, (220, 100, 100))
            screen.blit(curse_lbl, (left_panel_x + 15, 162))
        else:
            safe_lbl = fonts["small"].render("Цвіль: 0% (Стерильна зона)", True, (140, 220, 150))
            screen.blit(safe_lbl, (left_panel_x + 15, 162))

        # Ряд 1: Досягнення та Скарбниця
        btn_half_w = (left_panel_w - 30) // 2
        ach_btn_rect = pygame.Rect(left_panel_x + 10, 196, btn_half_w, 32)
        unclaimed_count = len(game.unlocked_achievements - game.claimed_achievements)
        btn_ach_col = (85, 60, 30) if unclaimed_count > 0 else (55, 45, 60)
        pygame.draw.rect(screen, btn_ach_col, ach_btn_rect, border_radius=6)
        pygame.draw.rect(screen, ACCENT_GOLD if unclaimed_count > 0 else (150, 110, 170), ach_btn_rect, width=2 if unclaimed_count > 0 else 1, border_radius=6)
        ach_badge = f" (+{unclaimed_count})" if unclaimed_count > 0 else ""
        ach_txt = fonts["small"].render(f"Досягн.{ach_badge}", True, ACCENT_GOLD if unclaimed_count > 0 else TEXT_WHITE)
        screen.blit(ach_txt, (ach_btn_rect.centerx - ach_txt.get_width() // 2, ach_btn_rect.centery - ach_txt.get_height() // 2))

        art_btn_rect = pygame.Rect(left_panel_x + 10 + btn_half_w + 10, 196, btn_half_w, 32)
        pygame.draw.rect(screen, (45, 65, 50), art_btn_rect, border_radius=6)
        pygame.draw.rect(screen, (120, 220, 140), art_btn_rect, width=1, border_radius=6)
        art_btn_txt = fonts["small"].render(f"Артефакти ({game.medals})", True, (190, 240, 190))
        screen.blit(art_btn_txt, (art_btn_rect.centerx - art_btn_txt.get_width() // 2, art_btn_rect.centery - art_btn_txt.get_height() // 2))

        # Ряд 2: Дерево Престижу та Меню
        p_btn_rect = pygame.Rect(left_panel_x + 10, 234, btn_half_w, 32)
        is_ready = (curse_val >= 100.0)
        pygame.draw.rect(surface=screen, color=(75, 45, 60) if is_ready else (45, 35, 42), rect=p_btn_rect, border_radius=6)
        pygame.draw.rect(surface=screen, color=ACCENT_GOLD if is_ready else (85, 70, 78), rect=p_btn_rect, width=2 if is_ready else 1, border_radius=6)
        p_btn_txt = fonts["small"].render(f"Дерево ({format_number(game.prestige.relics)})", True, TEXT_WHITE)
        screen.blit(p_btn_txt, (p_btn_rect.centerx - p_btn_txt.get_width() // 2, p_btn_rect.centery - p_btn_txt.get_height() // 2))

        s_btn_rect = pygame.Rect(left_panel_x + 10 + btn_half_w + 10, 234, btn_half_w, 32)
        pygame.draw.rect(screen, BUTTON_BG, s_btn_rect, border_radius=6)
        pygame.draw.rect(screen, PANEL_BORDER, s_btn_rect, width=1, border_radius=6)
        s_txt = fonts["small"].render("Меню", True, TEXT_WHITE)
        screen.blit(s_txt, (s_btn_rect.centerx - s_txt.get_width() // 2, s_btn_rect.centery - s_txt.get_height() // 2))

        # --- Центровані Віджети Зверху ---
        widget_w = min(200, (center_space_right - center_space_left - 30) // 2)
        widget_h = 48
        center_mid_x = center_space_left + (center_space_right - center_space_left) // 2
        
        # 1. Віджет Фізичних Кліків
        clicks_rect = pygame.Rect(center_mid_x - widget_w - 8, 15, widget_w, widget_h)
        pulse_clicks_bg = (90, 65, 30) if click_anim_timer > 0 else (28, 22, 26)
        pygame.draw.rect(screen, pulse_clicks_bg, clicks_rect, border_radius=10)
        pygame.draw.rect(screen, ACCENT_GOLD if click_anim_timer > 0 else PANEL_BORDER, clicks_rect, width=2, border_radius=10)

        clicks_str = f"Кліків: {format_number(game.total_clicks)}"
        clicks_txt = fonts["title"].render(clicks_str, True, (255, 235, 140) if click_anim_timer > 0 else TEXT_WHITE)
        screen.blit(clicks_txt, (clicks_rect.centerx - clicks_txt.get_width() // 2, clicks_rect.centery - clicks_txt.get_height() // 2))

        # 2. Віджет Загального Видобутку за всю гру
        total_baked_rect = pygame.Rect(center_mid_x + 8, 15, widget_w, widget_h)
        pygame.draw.rect(screen, (32, 24, 28), total_baked_rect, border_radius=10)
        pygame.draw.rect(screen, (160, 120, 60), total_baked_rect, width=2, border_radius=10)

        top_baked_str = f"Всього: {format_number(game.total_baked)}"
        top_baked_txt = fonts["title"].render(top_baked_str, True, ACCENT_GOLD)
        screen.blit(top_baked_txt, (total_baked_rect.centerx - top_baked_txt.get_width() // 2, total_baked_rect.centery - top_baked_txt.get_height() // 2))

        # Батон
        bread_surf = AssetManager.generate_bread_surface(base_bread_size[0], base_bread_size[1], curse_val)
        scaled_w = int(base_bread_size[0] * scale_factor)
        scaled_h = int(base_bread_size[1] * scale_factor)
        scaled_bread = pygame.transform.smoothscale(bread_surf, (scaled_w, scaled_h))
        screen.blit(scaled_bread, scaled_bread.get_rect(center=(bread_center[0] + shake_x, bread_center[1] + shake_y)))

        for p in particles:
            p.draw(screen)
        for ft in floating_texts:
            ft.draw(screen)

        # Магазин праворуч
        panel_rect = pygame.Rect(shop_x, 20, shop_w, cur_h - 40)
        pygame.draw.rect(screen, PANEL_BG, panel_rect, border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, panel_rect, width=2, border_radius=12)

        shop_header = fonts["title"].render(f"Ринок: {game.current_location.name[:16]}", True, TEXT_WHITE)
        screen.blit(shop_header, (shop_x + 20, 35))

        shop_clip = pygame.Rect(shop_x + 10, 75, shop_w - 20, cur_h - 105)
        screen.set_clip(shop_clip)

        cur_y = 90 + scroll_y
        for key, upg in game.current_location.upgrades.items():
            btn_rect = pygame.Rect(shop_x + 15, cur_y, shop_w - 30, 80)
            is_hover = btn_rect.collidepoint(mouse_pos)
            is_secret_open = game.is_upgrade_secret_unlocked(upg.get("secret_req"))
            can_afford = (game.crumbs >= upg["cost"]) and is_secret_open

            if is_secret_open:
                bg_col = BUTTON_HOVER if (is_hover and can_afford) else (BUTTON_BG if can_afford else BUTTON_DISABLED)
                border_col = ACCENT_GOLD if can_afford else (70, 60, 65)
            else:
                bg_col = (30, 22, 26)
                border_col = (65, 45, 50)

            pygame.draw.rect(screen, bg_col, btn_rect, border_radius=8)
            pygame.draw.rect(screen, border_col, btn_rect, width=2, border_radius=8)

            if is_secret_open:
                name_txt = fonts["main"].render(f"{upg['name']} [{format_number(upg['count'])}]", True, TEXT_WHITE)
                desc_txt = fonts["small"].render(upg["desc"], True, (170, 160, 165))
                cost_txt = fonts["small"].render(f"Ціна: {format_number(upg['cost'])} кр.", True, ACCENT_GOLD if can_afford else (170, 90, 90))

                screen.blit(name_txt, (btn_rect.x + 12, btn_rect.y + 8))
                screen.blit(desc_txt, (btn_rect.x + 12, btn_rect.y + 32))
                screen.blit(cost_txt, (btn_rect.x + 12, btn_rect.y + 54))
            else:
                sec_txt = fonts["main"].render("[!] СЕКРЕТНА БУДІВЛЯ", True, (210, 130, 140))
                req_perk_name = game.prestige.tree_config[upg['secret_req']]['name']
                desc_s = fonts["small"].render(f"Потрібен перк: {req_perk_name}", True, (140, 110, 120))
                screen.blit(sec_txt, (btn_rect.x + 12, btn_rect.y + 18))
                screen.blit(desc_s, (btn_rect.x + 12, btn_rect.y + 44))

            cur_y += 90

        screen.set_clip(None)

        notification_banner.draw(screen, fonts["main"], fonts["small"], cur_w)

        # Модалки
        if show_artifacts_hub:
            draw_artifacts_hub(screen, mouse_pos)
        elif show_achievements_hub:
            draw_achievements_hub(screen, mouse_pos)
        elif show_locations_hub:
            draw_locations_hub(screen, mouse_pos)
        elif show_prestige_menu:
            draw_radial_prestige_tree(screen, mouse_pos)
        elif horror_ending.active:
            horror_cta_btn_rect = horror_ending.draw(screen, fonts["horror"], fonts["main"], mouse_pos)

    pygame.display.flip()

SaveManager.save_game(game)
pygame.quit()
sys.exit()