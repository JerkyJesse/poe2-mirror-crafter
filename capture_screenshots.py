"""Capture screenshots of each app screen mode for the landing page."""
import os
import pygame
from phases import get_categories, get_phases
from renderer import (
    WIDTH, HEIGHT, MIN_W, MIN_H,
    init_fonts, draw_background, draw_selection_screen, draw_phase_list,
    draw_step_panel, draw_price_panel, draw_crafting_end_screen,
    draw_save_load_screen,
    draw_text, draw_rect,
    TEXT_GOLD, TEXT_DIM, TEXT_WHITE, BORDER_GOLD, BORDER_GOLD_DIM,
    BG_PANEL, BG_HEADER,
)
from state_manager import list_saves

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

def save_screenshot(screen, name):
    path = os.path.join(OUT_DIR, name)
    pygame.image.save(screen, path)
    print(f"  Saved: {path}")

def main():
    pygame.init()
    screen = pygame.Surface((1280, 800))
    tick = 120
    init_fonts()
    categories = get_categories()

    # ── 1. Startup Screen ──
    print("Capturing startup screen...")
    screen.fill((8, 4, 2))
    cx, cy = 640, 400
    draw_text(screen, "PoE2 Mirror Crafter", cx, cy - 140, TEXT_GOLD, "title", centered=True)
    draw_text(screen, "Weapons  |  Armour  |  Jewellery", cx, cy - 50, TEXT_WHITE, "medium", centered=True)
    new_btn = pygame.Rect(cx - 150, cy, 300, 50)
    draw_rect(screen, new_btn, (50, 20, 10), radius=6)
    draw_rect(screen, new_btn, BORDER_GOLD, border=2, radius=6)
    draw_text(screen, "[N]  NEW CRAFT", cx, cy + 12, (220, 200, 120), "large", centered=True)
    resume_btn = pygame.Rect(cx - 150, cy + 70, 300, 50)
    draw_rect(screen, resume_btn, (20, 10, 40), radius=6)
    draw_rect(screen, resume_btn, BORDER_GOLD_DIM, border=2, radius=6)
    draw_text(screen, "[L]  RESUME CRAFT", cx, cy + 82, TEXT_GOLD, "large", centered=True)
    draw_text(screen, "ESC to quit", cx, cy + 150, TEXT_DIM, "tiny", centered=True)
    save_screenshot(screen, "01-startup.png")

    # ── 2. Selection Screen ──
    print("Capturing selection screen...")
    draw_background(screen, tick)
    draw_selection_screen(screen, tick, categories, "Weapons", "Bow")
    save_screenshot(screen, "02-selection.png")

    # ── 3. Crafting Screen ──
    print("Capturing crafting screen...")
    phases = get_phases("Weapons", "Bow")
    draw_background(screen, tick)
    draw_phase_list(screen, phases, 2, {"P1S1", "P1S2", "P1S3", "P2S1", "P2S2", "P2S3", "P3S1"})
    step = phases[2]["steps"][1] if len(phases) > 2 and len(phases[2]["steps"]) > 1 else phases[2]["steps"][0]
    phase_steps = phases[2]["steps"]
    draw_step_panel(screen, step, 1, phase_steps, {"P1S1", "P1S2", "P1S3", "P2S1", "P2S2", "P2S3", "P3S1"}, pending_choice=None)
    draw_price_panel(screen, step, False, running_total=12.5, category="Weapons")
    y = max(22, 800 - 22)
    draw_rect(screen, (0, y, 1280, 22), BG_HEADER)
    draw_rect(screen, (0, y, 1280, 22), BORDER_GOLD_DIM, border=1)
    help_text = "[SPACE] Confirm | [Enter] Next | [Tab] Skip Phase | [1-0] Phase | [S] Save | [L] Load | [B] Back | [Esc] Reset"
    draw_text(screen, help_text, 8, y + 4, TEXT_DIM, "tiny")
    save_screenshot(screen, "03-crafting.png")

    # ── 4. Complete Screen ──
    print("Capturing complete screen...")
    draw_background(screen, tick)
    draw_crafting_end_screen(screen)
    save_screenshot(screen, "04-complete.png")

    # ── 5. Save/Load Screen ──
    print("Capturing save/load screen...")
    saves = list_saves()
    draw_save_load_screen(screen, tick, saves, "load", selected_save=0)
    save_screenshot(screen, "05-saveload.png")

    print(f"\nDone! {len(os.listdir(OUT_DIR))} screenshots in {OUT_DIR}")

if __name__ == "__main__":
    main()
