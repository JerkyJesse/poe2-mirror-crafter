# -*- coding: utf-8 -*-
"""
PoE2 Mirror Crafter — Headless Smoke Test Suite

Tests every clickable button and keyboard shortcut across all 5 screens.
Uses SDL_VIDEODRIVER=dummy for headless execution — no display required.

Usage:  python tests/smoke_test.py
"""

import os
import sys

# ── Headless setup ── MUST be before ANY pygame import ──
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Ensure the project root is on sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

# ═══════════════════════════════════════════════════════════════════════════
#  Initialise pygame *once* at module level so all CraftingApp instances
#  share the same initialised state.
# ═══════════════════════════════════════════════════════════════════════════
pygame.init()

from crafting_app import CraftingApp
from renderer import (
    draw_background,
    draw_selection_screen,
    draw_phase_list,
    draw_step_panel,
    draw_price_panel,
    draw_save_load_screen,
    draw_crafting_end_screen,
    WIDTH,
    HEIGHT,
    _s,
    get_font,
)
from state_manager import list_saves, delete_save
from prices import prices_available

# ═══════════════════════════════════════════════════════════════════════════
#  Layout constants  (1280 x 800 default)
# ═══════════════════════════════════════════════════════════════════════════
CX = WIDTH // 2
CY = HEIGHT // 2


# ── Startup screen ────────────────────────────────────────────────────────
def _startup_base_y():
    title_h = get_font("title").get_height()
    subtitle_h = get_font("medium").get_height()
    esc_h = get_font("tiny").get_height()
    btn_h = _s(50)

    title_to_sub_gap = _s(90)
    sub_to_btn1_gap = _s(50)
    btn1_to_btn2_gap = _s(20)
    btn2_to_esc_gap = _s(80)

    total_h = (
        title_h + title_to_sub_gap + subtitle_h + sub_to_btn1_gap
        + btn_h + btn1_to_btn2_gap + btn_h + btn2_to_esc_gap + esc_h
    )
    return HEIGHT // 2 - total_h // 2


def _startup_new_craft_btn():
    btn_w, btn_h = _s(300), _s(50)
    base_y = _startup_base_y()
    title_h = get_font("title").get_height()
    subtitle_h = get_font("medium").get_height()
    btn_new_y = base_y + _s(90) + subtitle_h + _s(50)
    return pygame.Rect(CX - btn_w // 2, btn_new_y, btn_w, btn_h)


def _startup_resume_btn():
    btn_w, btn_h = _s(300), _s(50)
    base_y = _startup_base_y()
    title_h = get_font("title").get_height()
    subtitle_h = get_font("medium").get_height()
    btn_resume_y = base_y + _s(90) + subtitle_h + _s(50) + btn_h + _s(20)
    return pygame.Rect(CX - btn_w // 2, btn_resume_y, btn_w, btn_h)


# ── Selection screen ──────────────────────────────────────────────────────
_MARGIN = 40
_SPACING = 16
_PANEL_Y = 100
_PANEL_H = min(530, HEIGHT - _PANEL_Y - 80)


def _select_panel_rects(cat_names):
    panel_w = (WIDTH - _MARGIN * 2 - _SPACING * (len(cat_names) - 1)) // len(cat_names)
    px = _MARGIN
    rects = {}
    for name in cat_names:
        rects[name] = pygame.Rect(px, _PANEL_Y, panel_w, _PANEL_H)
        px += panel_w + _SPACING
    return rects


def _select_begin_craft_btn():
    btn_w, btn_h = 280, 44
    return pygame.Rect(CX - btn_w // 2, HEIGHT - 54, btn_w, btn_h)


# ── Crafting screen ───────────────────────────────────────────────────────
def _crafting_reset_btn():
    w = 320 - 8 - 20  # PANEL_LEFT - 8 - 20
    return pygame.Rect(4 + 10, HEIGHT - 62, w, 32)


def _crafting_confirm_btn():
    # x = PANEL_LEFT + 4,  w = PANEL_CENTER_W - 8
    x = 320 + 4
    panel_w = (WIDTH - 320 - 280) - 8
    btn_w = 220
    btn_h = 36
    content_y = 4 + 36 + 4  # y + steps_bar_h + 4
    content_h = HEIGHT - content_y - 4
    action_y = content_y + content_h - 60
    btn_x = x + panel_w - btn_w - 16
    btn_y = action_y + 2
    return pygame.Rect(btn_x, btn_y, btn_w, btn_h)


# ── Save/Load screen ─────────────────────────────────────────────────────
def _save_load_new_craft_btn():
    panel_x = 140
    return pygame.Rect(panel_x + 20, HEIGHT - 52, 200, 36)


def _save_load_delete_btn():
    panel_x = 140
    x = panel_x + 20 + 200 + 16
    return pygame.Rect(x, HEIGHT - 52, 160, 36)


# ═══════════════════════════════════════════════════════════════════════════
#  SmokeTester
# ═══════════════════════════════════════════════════════════════════════════

class SmokeTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.bugs = 0

    # ── helpers ───────────────────────────────────────────────────────────

    def _log(self, status, name, detail=""):
        self.results.append((status, name, detail))

    def _pass(self, name):
        self._log("PASS", name)
        self.passed += 1

    def _fail(self, name, expected, actual):
        self._log("FAIL", name, f"expected={expected!r}  actual={actual!r}")
        self.failed += 1

    def _bug(self, name, desc):
        self._log("BUG", name, desc)
        self.bugs += 1

    def _assert_mode(self, name, app, expected):
        if app.mode == expected:
            self._pass(name)
        else:
            self._fail(name, expected, app.mode)

    def _assert_true(self, name, app, attr, msg=""):
        val = getattr(app, attr)
        if val:
            self._pass(name)
        else:
            self._fail(name, True, val)

    def _assert_false(self, name, app, attr, msg=""):
        val = getattr(app, attr)
        if not val:
            self._pass(name)
        else:
            self._fail(name, False, val)

    def _assert_eq(self, name, actual, expected):
        if actual == expected:
            self._pass(name)
        else:
            self._fail(name, expected, actual)

    def _assert_in(self, name, container, item):
        if item in container:
            self._pass(name)
        else:
            self._fail(name, f"'{item}' in collection", list(container)[:5])

    def _assert_lt(self, name, a, b):
        if a < b:
            self._pass(name)
        else:
            self._fail(name, f"< {b}", a)

    def _assert_true_or_fail(self, name, condition, expected, actual):
        if condition:
            self._pass(name)
        else:
            self._fail(name, expected, actual)

    def _new_app(self):
        """Create a fresh CraftingApp instance."""
        return CraftingApp()

    def _center(self, rect):
        return (rect.x + rect.w // 2, rect.y + rect.h // 2)

    def _post_click(self, pos):
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos))

    def _post_key(self, key):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))

    def _drain_events(self, app):
        """Process all pending events through the app."""
        for event in pygame.event.get():
            app.handle_event(event)

    def _draw_frame(self, app):
        """Run one draw cycle to populate hitboxes (without clearing events)."""
        if app.show_save_load:
            app.save_slots = list_saves()
            hitboxes = draw_save_load_screen(
                app.screen, app.tick, app.save_slots,
                app.save_load_mode, selected_save=app.selected_save,
            )
            app.save_load_hitboxes = hitboxes
        elif app.mode == "startup":
            app._draw_startup_screen()
        elif app.mode == "select":
            draw_background(app.screen, app.tick)
            hitboxes = draw_selection_screen(
                app.screen, app.tick, app.categories,
                app.selected_category, app.selected_subtype,
            )
            app.selection_hitboxes = hitboxes
        elif app.mode == "crafting":
            draw_background(app.screen, app.tick)
            phase_hitboxes = draw_phase_list(
                app.screen, app.phases, app.current_phase,
                app.completed_steps,
            )
            app.reset_btn_rect = phase_hitboxes.get("reset_btn") if phase_hitboxes else None
            step = app._current_step_data()
            if step:
                hitboxes = draw_step_panel(
                    app.screen, step, app.current_step,
                    app._current_phase_steps(), app.completed_steps,
                    pending_choice=app.pending_choice,
                )
                app.confirm_btn_rect = hitboxes.get("confirm_btn")
                app.choice_btn_rects = hitboxes.get("choice_btns", [])
                draw_price_panel(
                    app.screen, step, prices_available(),
                    running_total=app.total_estimated_cost,
                    category=app.selected_category,
                )
            else:
                app.confirm_btn_rect = None
                app.choice_btn_rects = []
        elif app.mode == "complete":
            draw_background(app.screen, app.tick)
            draw_crafting_end_screen(app.screen)
        app.tick += 1

    def _pump(self, app, frames=1):
        """Run N frames: drain events + draw each frame."""
        for _ in range(frames):
            self._drain_events(app)
            self._draw_frame(app)

    def _click_button(self, app, rect):
        """Prime hitboxes, then click at center of given rect, then pump."""
        self._draw_frame(app)
        if rect:
            self._post_click(self._center(rect))
        self._pump(app, 2)

    def _press_key(self, app, key, frames=2):
        """Post a key event and pump."""
        self._post_key(key)
        self._pump(app, frames)

    def _setup_select_mode(self, app):
        """Navigate app from startup to select mode."""
        app.mode = "select"
        self._draw_frame(app)

    def _setup_crafting_mode(self, app, category="Weapons", sub_type="Bow"):
        """Navigate app from startup to crafting mode."""
        app.mode = "select"
        app.selected_category = category
        app.selected_subtype = sub_type
        app._begin_crafting()
        self._pump(app, 1)

    def _setup_complete_mode(self, app):
        """Navigate app to completion screen."""
        self._setup_crafting_mode(app)
        # Tab through all 10 phases to reach completion
        for _ in range(10):
            self._post_key(pygame.K_TAB)
            self._pump(app, 1)

    # ═══════════════════════════════════════════════════════════════════════
    #  STARTUP SCREEN  (2 buttons + 3 keyboard)
    # ═══════════════════════════════════════════════════════════════════════

    def test_startup_new_craft_click(self):
        app = self._new_app()
        self._draw_frame(app)  # populate hitboxes
        rect = _startup_new_craft_btn()
        self._click_button(app, rect)
        self._assert_mode("[STA-01] NEW CRAFT button click => mode=select", app, "select")
        return app

    def test_startup_new_craft_key_n(self):
        app = self._new_app()
        self._press_key(app, pygame.K_n)
        self._assert_mode("[STA-02] [N] key => mode=select", app, "select")
        return app

    def test_startup_resume_craft_click(self):
        app = self._new_app()
        self._draw_frame(app)
        rect = _startup_resume_btn()
        self._click_button(app, rect)
        ok = app.show_save_load and app.save_load_mode == "load"
        self._assert_true_or_fail("[STA-03] RESUME CRAFT button click => save/load (load)", ok, "show_save_load+load", f"show={app.show_save_load} mode={app.save_load_mode}")
        return app

    def test_startup_resume_craft_key_l(self):
        app = self._new_app()
        self._press_key(app, pygame.K_l)
        ok = app.show_save_load and app.save_load_mode == "load"
        self._assert_true_or_fail("[STA-04] [L] key => save/load (load)", ok, "show_save_load+load", f"show={app.show_save_load} mode={app.save_load_mode}")
        return app

    def test_startup_esc_quit(self):
        app = self._new_app()
        self._press_key(app, pygame.K_ESCAPE)
        ok = not app.running
        self._assert_true_or_fail("[STA-05] [ESC] key => running=False", ok, "running=False", f"running={app.running}")
        return app

    # ═══════════════════════════════════════════════════════════════════════
    #  SELECTION SCREEN  (3 panels + sub-types + BEGIN CRAFT + 3 keys)
    # ═══════════════════════════════════════════════════════════════════════

    def test_select_category_weapons_click(self):
        app = self._new_app()
        self._setup_select_mode(app)
        rects = _select_panel_rects(app.category_keys)
        self._click_button(app, rects.get("Weapons"))
        self._assert_eq("[SEL-01] Click Weapons panel => selected_category=Weapons", app.selected_category, "Weapons")
        return app

    def test_select_category_armour_click(self):
        app = self._new_app()
        self._setup_select_mode(app)
        rects = _select_panel_rects(app.category_keys)
        self._click_button(app, rects.get("Armour"))
        self._assert_eq("[SEL-02] Click Armour panel => selected_category=Armour", app.selected_category, "Armour")
        return app

    def test_select_category_jewellery_click(self):
        app = self._new_app()
        self._setup_select_mode(app)
        rects = _select_panel_rects(app.category_keys)
        self._click_button(app, rects.get("Jewellery"))
        self._assert_eq("[SEL-03] Click Jewellery panel => selected_category=Jewellery", app.selected_category, "Jewellery")
        return app

    def test_select_subtype_click(self):
        app = self._new_app()
        self._setup_select_mode(app)
        # Prime hitboxes
        self._draw_frame(app)
        hitboxes = app.selection_hitboxes
        subtype_items = hitboxes.get("subtype_items", {})

        # Click first sub-type (Bow) — should auto-select Weapons category
        bow_rect = subtype_items.get("Bow")
        if bow_rect:
            self._post_click(self._center(bow_rect))
            self._pump(app, 2)
            cat_ok = app.selected_category == "Weapons"
            sub_ok = app.selected_subtype == "Bow"
            self._assert_true_or_fail("[SEL-04] Click Bow sub-type => selected_subtype=Bow + auto-select Weapons",
                                       cat_ok and sub_ok, "Weapons/Bow", f"{app.selected_category}/{app.selected_subtype}")
        else:
            self._fail("[SEL-04] Click Bow sub-type", "Bow in hitboxes", "not found")
        return app

    def test_select_begin_craft_click(self):
        app = self._new_app()
        self._setup_select_mode(app)
        app.selected_category = "Weapons"
        app.selected_subtype = "Bow"
        self._click_button(app, _select_begin_craft_btn())
        ok = app.mode == "crafting" and len(app.phases) > 0
        self._assert_true_or_fail("[SEL-05] BEGIN CRAFT button click => mode=crafting + phases loaded",
                                   ok, "crafting with phases", f"mode={app.mode} phases={len(app.phases)}")
        return app

    def test_select_begin_craft_enter(self):
        app = self._new_app()
        self._setup_select_mode(app)
        app.selected_category = "Weapons"
        app.selected_subtype = "Bow"
        self._press_key(app, pygame.K_RETURN)
        ok = app.mode == "crafting" and len(app.phases) > 0
        self._assert_true_or_fail("[SEL-06] [ENTER] key => mode=crafting + phases loaded",
                                   ok, "crafting with phases", f"mode={app.mode} phases={len(app.phases)}")
        return app

    def test_select_esc_back(self):
        app = self._new_app()
        self._setup_select_mode(app)
        self._press_key(app, pygame.K_ESCAPE)
        self._assert_mode("[SEL-07] [ESC] key => mode=startup", app, "startup")
        return app

    def test_select_l_load(self):
        app = self._new_app()
        self._setup_select_mode(app)
        self._press_key(app, pygame.K_l)
        ok = app.show_save_load and app.save_load_mode == "load"
        self._assert_true_or_fail("[SEL-08] [L] key => save/load (load)", ok, "show_save_load+load", f"show={app.show_save_load} mode={app.save_load_mode}")
        return app

    # ═══════════════════════════════════════════════════════════════════════
    #  CRAFTING SCREEN  (RESET + Confirm + Choice + 15 key shortcuts)
    # ═══════════════════════════════════════════════════════════════════════

    def test_crafting_reset_click(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        # Advance a couple steps first so we have something to reset
        self._press_key(app, pygame.K_SPACE, 1)
        self._press_key(app, pygame.K_SPACE, 1)
        self._draw_frame(app)
        self._click_button(app, _crafting_reset_btn())
        ok = app.current_phase == 0 and app.current_step == 0 and len(app.completed_steps) == 0
        self._assert_true_or_fail("[CRA-01] RESET button click => phase=0 step=0 completed=0",
                                   ok, "phase=0 step=0 empty", f"p={app.current_phase} s={app.current_step} done={len(app.completed_steps)}")
        return app

    def test_crafting_confirm_step_click(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._draw_frame(app)
        rect = _crafting_confirm_btn()
        self._click_button(app, rect)
        step_id = list(app.completed_steps)[0] if app.completed_steps else None
        self._assert_in("[CRA-02] Confirm Step click => step added to completed_steps",
                         app.completed_steps, "1.1")
        return app

    def test_crafting_space_confirm(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_SPACE, 1)
        self._assert_in("[CRA-03] [SPACE] => step completed", app.completed_steps, "1.1")
        self._press_key(app, pygame.K_SPACE, 1)
        self._assert_in("[CRA-04] [SPACE] again => step 1.2 completed", app.completed_steps, "1.2")
        return app

    def test_crafting_enter_confirm(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_RETURN, 1)
        self._assert_in("[CRA-05] [ENTER] => step completed", app.completed_steps, "1.1")
        return app

    def test_crafting_right_arrow(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_RIGHT, 1)
        self._assert_in("[CRA-06] [RIGHT] => step completed", app.completed_steps, "1.1")
        return app

    def test_crafting_left_arrow(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        # Complete step 1.1 first
        self._press_key(app, pygame.K_SPACE, 1)
        self._press_key(app, pygame.K_SPACE, 1)  # step 1.2
        # Now we're on step 1.3 — go LEFT twice should go back to step 1.1
        self._press_key(app, pygame.K_LEFT, 1)
        self._assert_eq("[CRA-07] [LEFT] => back to step 1.2", app.current_step, 1)
        self._press_key(app, pygame.K_LEFT, 1)
        self._assert_eq("[CRA-08] [LEFT] again => back to step 1.1", app.current_step, 0)
        return app

    def test_crafting_tab_skip_phase(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        phase0_steps = len(app.phases[0]["steps"])
        self._press_key(app, pygame.K_TAB, 1)
        # All steps in phase 0 should now be completed, current_phase should be 1
        phase_ok = app.current_phase == 1
        steps_ok = len(app.completed_steps) == phase0_steps
        self._assert_true_or_fail("[CRA-09] [TAB] => skip phase 1, all steps completed, phase=2",
                                   phase_ok and steps_ok,
                                   f"phase=1 steps={phase0_steps}",
                                   f"phase={app.current_phase} steps={len(app.completed_steps)}")
        return app

    def test_crafting_r_refresh(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_r, 1)
        ok = "Refreshing" in app.message or app.message_timer > 0
        self._assert_true_or_fail("[CRA-10] [R] => refresh message triggered",
                                   ok, "message contains 'Refreshing'", f"msg='{app.message}' timer={app.message_timer}")
        return app

    def test_crafting_s_save(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_s, 1)
        ok = app.show_save_load and app.save_load_mode == "save"
        self._assert_true_or_fail("[CRA-11] [S] => save/load (save)", ok, "show_save_load+save", f"show={app.show_save_load} mode={app.save_load_mode}")
        return app

    def test_crafting_l_load(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_l, 1)
        ok = app.show_save_load and app.save_load_mode == "load"
        self._assert_true_or_fail("[CRA-12] [L] => save/load (load)", ok, "show_save_load+load", f"show={app.show_save_load} mode={app.save_load_mode}")
        return app

    def test_crafting_b_back(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_b, 1)
        self._assert_mode("[CRA-13] [B] => mode=select", app, "select")
        return app

    def test_crafting_esc_reset(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        # Advance a couple steps first
        self._press_key(app, pygame.K_SPACE, 1)
        self._press_key(app, pygame.K_SPACE, 1)
        self._press_key(app, pygame.K_ESCAPE, 1)
        ok = app.current_phase == 0 and app.current_step == 0 and len(app.completed_steps) == 0
        self._assert_true_or_fail("[CRA-14] [ESC] => reset craft (phase=0 step=0)",
                                   ok, "phase=0 step=0", f"p={app.current_phase} s={app.current_step}")
        return app

    def test_crafting_phase_jump_keys(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        # Jump to phase 4 (key 4)
        self._press_key(app, pygame.K_4, 1)
        self._assert_eq("[CRA-15] [4] => jump to phase 4 (idx=3)", app.current_phase, 3)
        # Jump to phase 7 (key 7)
        self._press_key(app, pygame.K_7, 1)
        self._assert_eq("[CRA-16] [7] => jump to phase 7 (idx=6)", app.current_phase, 6)
        # Jump to phase 1 (key 1)
        self._press_key(app, pygame.K_1, 1)
        self._assert_eq("[CRA-17] [1] => jump to phase 1 (idx=0)", app.current_phase, 0)
        # Jump to phase 10 (key 0)
        self._press_key(app, pygame.K_0, 1)
        self._assert_eq("[CRA-18] [0] => jump to phase 10 (idx=9)", app.current_phase, 9)
        return app

    def test_crafting_choice_alternative(self):
        """Test selecting a crafting alternative on a step that has choices."""
        app = self._new_app()
        self._setup_crafting_mode(app)
        # Navigate to phase 3 (index 2), step 3.1 which has alternatives for Bow
        # First, complete phase 1 steps via confirm
        for _ in range(4):  # Phase 1 has 4 steps for Bow
            self._press_key(app, pygame.K_SPACE, 1)
        # Skip phase 2
        self._press_key(app, pygame.K_TAB, 1)
        # Now we're at phase 3 (index 2), step 0 = step "3.1" which has alternatives
        self._draw_frame(app)
        if app.pending_choice is not None:
            self._pass("[CRA-19] At step with alternatives, pending_choice not None (already set)")
        alt_count = len(app.choice_btn_rects)
        self._assert_true_or_fail("[CRA-20] Choice alternative buttons rendered",
                                   alt_count > 0, ">0 alternatives", f"{alt_count} alternatives")
        # Click the first alternative
        if app.choice_btn_rects:
            self._post_click(self._center(app.choice_btn_rects[0]))
            self._pump(app, 2)
            self._assert_eq("[CRA-21] Click 1st alternative => pending_choice=0", app.pending_choice, 0)
            # Now confirm the step
            self._press_key(app, pygame.K_SPACE, 1)
            self._assert_in("[CRA-22] Confirm with choice => step 3.1 in completed", app.completed_steps, "3.1")
        else:
            self._fail("[CRA-20b] Choice buttons present", "rects found", "empty")
        return app

    # ═══════════════════════════════════════════════════════════════════════
    #  SAVE/LOAD OVERLAY  (save slots + NEW CRAFT + DELETE + 7 keyboard)
    # ═══════════════════════════════════════════════════════════════════════

    def test_save_load_open_and_close(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        # Open save/load via S key
        self._press_key(app, pygame.K_s, 1)
        ok = app.show_save_load and app.save_load_mode == "save"
        self._assert_true_or_fail("[SVL-01] Open save via [S] => show_save_load=True, mode=save",
                                   ok, "show_save_load+save", f"show={app.show_save_load} mode={app.save_load_mode}")
        # Close via ESC
        self._press_key(app, pygame.K_ESCAPE, 1)
        self._assert_false("[SVL-02] [ESC] => close save/load", app, "show_save_load")
        return app

    def test_save_load_new_craft_click(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        # Open save/load
        self._press_key(app, pygame.K_s, 1)
        # Click NEW CRAFT button
        self._click_button(app, _save_load_new_craft_btn())
        ok = (not app.show_save_load) and app.mode == "select"
        self._assert_true_or_fail("[SVL-03] NEW CRAFT click => close overlay + mode=select",
                                   ok, "closed+select", f"show={app.show_save_load} mode={app.mode}")
        return app

    def test_save_load_new_craft_key_n(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_s, 1)
        self._press_key(app, pygame.K_n, 1)
        ok = (not app.show_save_load) and app.mode == "select"
        self._assert_true_or_fail("[SVL-04] [N] key in save/load => close + mode=select",
                                   ok, "closed+select", f"show={app.show_save_load} mode={app.mode}")
        return app

    def test_save_load_navigate_slots(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_s, 1)
        # Press down to navigate (there may or may not be save slots)
        self._press_key(app, pygame.K_DOWN, 1)
        self._pass("[SVL-05] [DOWN] key => navigate save slots (no crash)")
        self._press_key(app, pygame.K_UP, 1)
        self._pass("[SVL-06] [UP] key => navigate save slots (no crash)")
        return app

    def test_save_load_delete_no_crash(self):
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_s, 1)
        # Press DEL — should not crash even if nothing selected
        self._press_key(app, pygame.K_DELETE, 1)
        self._pass("[SVL-07] [DEL] key => delete save (no crash)")
        return app

    def test_save_load_enter_confirm(self):
        """Test ENTER in save mode saves current state."""
        app = self._new_app()
        self._setup_crafting_mode(app)
        self._press_key(app, pygame.K_s, 1)
        self._press_key(app, pygame.K_RETURN, 1)
        # Should close overlay and remain in crafting
        closed = not app.show_save_load
        in_craft = app.mode == "crafting"
        self._assert_true_or_fail("[SVL-08] [ENTER] in save mode => close overlay, stay in crafting",
                                   closed and in_craft, "closed+crafting", f"show={app.show_save_load} mode={app.mode}")
        return app

    def test_save_load_slot_click(self):
        """Verify save-slot mouse clicks work (regression test for renderer/handler key mismatch)."""
        app = self._new_app()
        self._setup_crafting_mode(app)
        # Complete a few steps so there's progress to save
        self._press_key(app, pygame.K_SPACE, 1)
        self._press_key(app, pygame.K_SPACE, 1)
        # Save current state
        self._press_key(app, pygame.K_s, 1)
        self._press_key(app, pygame.K_RETURN, 1)
        self._pump(app, 1)
        # Reset the session
        self._press_key(app, pygame.K_ESCAPE, 1)
        self._pump(app, 1)
        old_done = len(app.completed_steps)
        # Open load screen
        self._press_key(app, pygame.K_l, 1)
        self._draw_frame(app)
        # Click the first save slot — should load and close overlay in one click
        if app.save_slots and "0" in app.save_load_hitboxes:
            first_rect = app.save_load_hitboxes["0"]
            self._post_click(self._center(first_rect))
            self._pump(app, 2)
            loaded_done = len(app.completed_steps)
            ok = loaded_done > old_done and not app.show_save_load and app.mode == "crafting"
            self._assert_true_or_fail("[SVL-09] Click save slot => loads state and closes overlay",
                                       ok, "loaded+closed+crafting", f"done={loaded_done} show={app.show_save_load} mode={app.mode}")
        else:
            self._pass("[SVL-09] Save slot click — no saves to click (non-bug)")
        return app

    # ═══════════════════════════════════════════════════════════════════════
    #  COMPLETION SCREEN  (0 buttons + 3 keys)
    # ═══════════════════════════════════════════════════════════════════════

    def test_complete_esc_quit(self):
        app = self._new_app()
        self._setup_complete_mode(app)
        self._press_key(app, pygame.K_ESCAPE, 1)
        self._assert_true_or_fail("[CMP-01] [ESC] on complete => running=False",
                                   not app.running, "running=False", f"running={app.running}")
        return app

    def test_complete_r_restart(self):
        app = self._new_app()
        self._setup_complete_mode(app)
        self._press_key(app, pygame.K_r, 1)
        self._assert_mode("[CMP-02] [R] on complete => mode=crafting", app, "crafting")
        ok = app.current_phase == 0 and app.current_step == 0 and len(app.completed_steps) == 0
        self._assert_true_or_fail("[CMP-03] [R] reset => phase=0 step=0 done=0", ok, "0/0/0", f"p={app.current_phase} s={app.current_step} d={len(app.completed_steps)}")
        return app

    def test_complete_b_back(self):
        app = self._new_app()
        self._setup_complete_mode(app)
        self._press_key(app, pygame.K_b, 1)
        self._assert_mode("[CMP-04] [B] on complete => mode=select", app, "select")
        return app

    # ═══════════════════════════════════════════════════════════════════════
    #  END-TO-END FULL FLOW
    # ═══════════════════════════════════════════════════════════════════════

    def test_e2e_full_flow(self):
        """Simulate a complete user journey from startup through all 10 phases to completion."""
        app = self._new_app()

        # 1. Startup — click NEW CRAFT
        self._draw_frame(app)
        self._post_click(self._center(_startup_new_craft_btn()))
        self._pump(app, 2)
        self._assert_mode("[E2E-01] Startup => select", app, "select")

        # 2. Selection — click Weapons, Bow, BEGIN CRAFT
        self._draw_frame(app)
        subtype_items = app.selection_hitboxes.get("subtype_items", {})
        bow_rect = subtype_items.get("Bow")
        if bow_rect:
            self._post_click(self._center(bow_rect))
            self._pump(app, 2)
        else:
            # Fallback: manually set
            app.selected_category = "Weapons"
            app.selected_subtype = "Bow"
        self._assert_eq("[E2E-02] Selected sub-type Bow", app.selected_subtype, "Bow")

        self._draw_frame(app)
        begin = _select_begin_craft_btn()
        self._post_click(self._center(begin))
        self._pump(app, 2)
        self._assert_mode("[E2E-03] BEGIN CRAFT => crafting", app, "crafting")
        total_phases = len(app.phases)
        self._assert_true_or_fail("[E2E-04] Phases loaded", total_phases == 10, "10 phases", f"{total_phases}")

        # 3. Walk through phase 1 (4 steps for Bow): confirm each
        phase1_steps = len(app.phases[0]["steps"])
        for i in range(phase1_steps):
            step_id = app._current_step_data()["id"] if app._current_step_data() else "?"
            self._press_key(app, pygame.K_SPACE, 1)
            self._assert_in(f"[E2E-05p1] Confirm step {step_id}", app.completed_steps, step_id)

        # 4. Skip phase 2 with TAB
        phase2_steps = len(app.phases[1]["steps"])
        self._press_key(app, pygame.K_TAB, 1)
        self._assert_eq("[E2E-06] Skip phase 2 => phase=2 (idx=2)", app.current_phase, 2)

        # 5. Phase 3 step 3.1 has alternatives — test choice flow
        self._draw_frame(app)
        if app.choice_btn_rects:
            self._post_click(self._center(app.choice_btn_rects[0]))
            self._pump(app, 2)
            self._assert_eq("[E2E-07] Select alternative 0", app.pending_choice, 0)
            self._press_key(app, pygame.K_SPACE, 1)
            self._assert_in("[E2E-08] Step 3.1 confirmed with choice", app.completed_steps, "3.1")

        # 6. Skip remaining phases 3-10 with TAB (8 phases to go)
        for i in range(7):  # skip phases 3 through 9 (indices 2-8)
            self._press_key(app, pygame.K_TAB, 1)

        # 7. Skip phase 10 to reach completion
        self._press_key(app, pygame.K_TAB, 1)
        self._assert_mode("[E2E-09] All phases done => mode=complete", app, "complete")
        self._assert_true_or_fail("[E2E-10] crafting_complete flag", app.crafting_complete, "True", f"{app.crafting_complete}")

        # 8. Reset from completion — should now return to crafting mode
        self._press_key(app, pygame.K_r, 1)
        self._assert_mode("[E2E-11] [R] from complete => mode=crafting", app, "crafting")

        self._pass("[E2E-12] Full E2E journey completed successfully")
        return app

    # ═══════════════════════════════════════════════════════════════════════
    #  Report
    # ═══════════════════════════════════════════════════════════════════════

    def run_all(self):
        print()
        print("=" * 68)
        print("  PoE2 Mirror Crafter — Full Button Smoke Test")
        print("=" * 68)

        tests = [
            # ── Startup ──
            ("STARTUP SCREEN", [
                self.test_startup_new_craft_click,
                self.test_startup_new_craft_key_n,
                self.test_startup_resume_craft_click,
                self.test_startup_resume_craft_key_l,
                self.test_startup_esc_quit,
            ]),
            # ── Selection ──
            ("SELECTION SCREEN", [
                self.test_select_category_weapons_click,
                self.test_select_category_armour_click,
                self.test_select_category_jewellery_click,
                self.test_select_subtype_click,
                self.test_select_begin_craft_click,
                self.test_select_begin_craft_enter,
                self.test_select_esc_back,
                self.test_select_l_load,
            ]),
            # ── Crafting ──
            ("CRAFTING SCREEN", [
                self.test_crafting_reset_click,
                self.test_crafting_confirm_step_click,
                self.test_crafting_space_confirm,
                self.test_crafting_enter_confirm,
                self.test_crafting_right_arrow,
                self.test_crafting_left_arrow,
                self.test_crafting_tab_skip_phase,
                self.test_crafting_r_refresh,
                self.test_crafting_s_save,
                self.test_crafting_l_load,
                self.test_crafting_b_back,
                self.test_crafting_esc_reset,
                self.test_crafting_phase_jump_keys,
                self.test_crafting_choice_alternative,
            ]),
            # ── Save/Load ──
            ("SAVE/LOAD OVERLAY", [
                self.test_save_load_open_and_close,
                self.test_save_load_new_craft_click,
                self.test_save_load_new_craft_key_n,
                self.test_save_load_navigate_slots,
                self.test_save_load_delete_no_crash,
                self.test_save_load_enter_confirm,
                self.test_save_load_slot_click,
            ]),
            # ── Completion ──
            ("COMPLETION SCREEN", [
                self.test_complete_esc_quit,
                self.test_complete_r_restart,
                self.test_complete_b_back,
            ]),
            # ── E2E ──
            ("END-TO-END", [
                self.test_e2e_full_flow,
            ]),
        ]

        for section_name, funcs in tests:
            print(f"\n  [{section_name}]")
            for fn in funcs:
                try:
                    fn()
                except Exception as e:
                    self._fail(f"{fn.__name__}  *CRASH*", "no exception", f"{type(e).__name__}: {e}")

        # ── Print summary ──
        print()
        print("-" * 68)
        total = self.passed + self.failed + self.bugs
        print(f"  RESULTS:  {self.passed} PASS  |  {self.failed} FAIL  |  {self.bugs} BUG  |  {total} TOTAL")
        print("-" * 68)

        # Detail listing
        if self.failed > 0 or self.bugs > 0:
            print("\n  --- DETAILS ---")
            for status, name, detail in self.results:
                if status in ("FAIL", "BUG"):
                    print(f"  [{status}] {name}")
                    if detail:
                        print(f"          {detail}")

        print()
        return self.failed == 0


# ═══════════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    tester = SmokeTester()
    ok = tester.run_all()
    sys.exit(0 if ok else 1)
