import pygame
from phases import get_phases, get_categories
from prices import fetch_prices_async, prices_available, get_icon_urls
from icon_loader import load_cached_icons, set_icon_urls, download_icons_async
from renderer import (
    WIDTH, HEIGHT, PANEL_LEFT, PANEL_RIGHT_W, update_layout,
    init_fonts, draw_background, draw_selection_screen, draw_phase_list,
    draw_step_panel, draw_price_panel, draw_crafting_end_screen,
    draw_save_load_screen, spawn_particle,
    draw_text, draw_rect, _s, get_font,
    TEXT_GOLD, TEXT_DIM, TEXT_WHITE, BORDER_GOLD, BORDER_GOLD_DIM,
    BG_PANEL, BG_HEADER, GREEN_GLOW,
)
from state_manager import list_saves, save_state, load_state, delete_save, auto_save_filename, migrate_saves_from_legacy
import random


class CraftingApp:
    def __init__(self, init_w=WIDTH, init_h=HEIGHT):
        self.screen = pygame.display.set_mode((init_w, init_h), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.tick = 0

        # App modes
        # "startup" -> "select" -> "crafting" -> "complete"
        # "startup" shows New Craft / Resume Craft choice
        # "select" shows category/sub-type selection
        # "crafting" shows the phase guide
        # "complete" shows completion screen
        # "save_load" shows save/load screen
        self.mode = "startup"

        # Selection state
        self.categories = get_categories()
        self.selected_category = None
        self.selected_subtype = None
        self.category_keys = list(self.categories.keys())

        # Crafting state
        self.phases = []
        self.current_phase = 0
        self.current_step = 0
        self.completed_steps = set()
        self.choices_made = {}  # step_id -> chosen alternative index
        self.pending_choice = None  # currently hovered/selected alternative index

        # UI hitboxes
        self.confirm_btn_rect = None
        self.back_btn_rect = None
        self.reset_btn_rect = None
        self.choice_btn_rects = []
        self.selection_hitboxes = {}
        self.save_load_hitboxes = {}

        # Messages
        self.message = ""
        self.message_timer = 0

        # State machine flags
        self.crafting_complete = False
        self.price_fetch_done = False
        self.show_save_load = False
        self.save_load_mode = "load"  # "load" or "save"
        self.save_slots = []
        self.selected_save = -1

        # Budget tracking
        self.total_estimated_cost = 0

        # Mod search
        self.mod_search_query = ""
        self.mod_search_active = False
        self.mod_search_rect = None
        self._search_skip_slash = False
        pygame.key.start_text_input()

        init_fonts()
        load_cached_icons()
        migrate_saves_from_legacy()
        self._start_price_fetch()

    def _start_price_fetch(self):
        def on_fetch(result):
            self.price_fetch_done = result is not None
            if result is not None:
                icon_urls = get_icon_urls()
                if icon_urls:
                    set_icon_urls(icon_urls)
                self._update_budget_estimate()
            download_icons_async()
        fetch_prices_async(callback=on_fetch)

    def _begin_crafting(self):
        """Transition from selection to crafting mode."""
        if not self.selected_category or not self.selected_subtype:
            return
        self.phases = get_phases(self.selected_category, self.selected_subtype)
        self.current_phase = 0
        self.current_step = 0
        self.completed_steps = set()
        self.choices_made = {}
        self.pending_choice = None
        self.crafting_complete = False
        self.mode = "crafting"
        self.message = f"Crafting: {self.selected_subtype}"
        self.message_timer = 60
        self._auto_save()

    def _auto_save(self):
        if self.mode != "crafting":
            return
        filename = auto_save_filename(self.selected_category, self.selected_subtype)
        state = {
            "version": 2,
            "category": self.selected_category,
            "sub_type": self.selected_subtype,
            "current_phase": self.current_phase,
            "current_step": self.current_step,
            "completed_steps": list(self.completed_steps),
            "choices_made": dict(self.choices_made),
            "display_name": f"{self.selected_category} — {self.selected_subtype}",
            "total_estimated_cost": self.total_estimated_cost,
        }
        save_state(filename, state)

    def _current_step_data(self):
        if self.current_phase >= len(self.phases):
            return None
        phase = self.phases[self.current_phase]
        if self.current_step >= len(phase["steps"]):
            return None
        return phase["steps"][self.current_step]

    def _current_phase_steps(self):
        if self.current_phase >= len(self.phases):
            return []
        return self.phases[self.current_phase]["steps"]

    def _confirm_step(self):
        step = self._current_step_data()
        if step is None:
            return
        step_id = step["id"]
        if step_id in self.completed_steps:
            return

        # If step has alternatives and none chosen, require a choice first
        if "alternatives" in step and step_id not in self.choices_made:
            if self.pending_choice is not None:
                self.choices_made[step_id] = self.pending_choice
                self.pending_choice = None
            else:
                self.message = "Choose an alternative first!"
                self.message_timer = 60
                return

        self.completed_steps.add(step_id)
        self._update_budget_estimate()
        self._start_price_fetch()
        self.message = f"Step {step_id} complete! Prices updated."
        self.message_timer = 120
        self._advance_step()
        self._auto_save()

    def _update_budget_estimate(self):
        from prices import get_price

        _ORB_ATTEMPTS = {
            "Fracturing Orb": 4,
            "Omen of Whittling": 20,
            "Perfect Chaos Orb": 20,
            "Perfect Exalted Orb": 10,
            "Divine Orb": 30,
            "Hinekora's Lock": 1,
            "Omen of Dextral Coronation": 2,
            "Omen of Sinistral Coronation": 2,
            "Omen of Dextral Erasure": 3,
            "Omen of Sinistral Erasure": 3,
            "Omen of Dextral Annulment": 2,
            "Omen of Sinistral Annulment": 2,
            "Omen of Dextral Exaltation": 3,
            "Omen of Sinistral Exaltation": 3,
            "Omen of Greater Exaltation": 2,
            "Omen of Greater Annulment": 2,
            "Omen of Abyssal Echoes": 1,
            "Omen of Sanctification": 1,
            "Orb of Annulment": 3,
            "Perfect Orb of Transmutation": 20,
            "Perfect Orb of Augmentation": 20,
            "Perfect Regal Orb": 8,
            "Vaal Blacksmith's Infuser": 2,
            "Artificer's Orb": 2,
            "Blacksmith's Whetstone": 20,
            "Armourer's Scrap": 20,
            "Catalyst": 20,
            "Distilled Emotion": 3,
        }

        total = 0.0
        for phase in self.phases:
            for step in phase["steps"]:
                orbs = step.get("orbs_used", [])
                for orb_name in orbs:
                    price = get_price(orb_name)
                    if price:
                        attempts = _ORB_ATTEMPTS.get(orb_name, 3)
                        total += price.get("divine", 0) * attempts
        self.total_estimated_cost = total

    def _advance_step(self):
        phase_steps = self._current_phase_steps()
        if self.current_step + 1 < len(phase_steps):
            self.current_step += 1
        else:
            self.current_step = 0
            self.current_phase += 1
            if self.current_phase >= len(self.phases):
                self.crafting_complete = True
                self.mode = "complete"

    def _reset(self):
        self.current_phase = 0
        self.current_step = 0
        self.completed_steps = set()
        self.choices_made = {}
        self.pending_choice = None
        self.crafting_complete = False
        self.total_estimated_cost = 0
        self.mode = "crafting"
        self.message = "Crafting session reset."
        self.message_timer = 90

    def _skip_phase(self):
        if self.crafting_complete or self.mode != "crafting":
            return
        phase = self.phases[self.current_phase]
        for step in phase["steps"]:
            self.completed_steps.add(step["id"])
        self.current_step = 0
        self.current_phase += 1
        if self.current_phase >= len(self.phases):
            self.crafting_complete = True
            self.mode = "complete"
        else:
            self.message = f"Phase {phase['number']} skipped."
            self.message_timer = 90
        self._auto_save()

    def _go_to_phase(self, target):
        if 0 <= target < len(self.phases):
            self.current_phase = target
            self.current_step = 0
            self.message = f"Jumped to Phase {target + 1}"
            self.message_timer = 90

    def _open_save_load(self, mode):
        self.show_save_load = True
        self.save_load_mode = mode
        self.save_slots = list_saves()
        self.selected_save = 0 if self.save_slots else -1

    def _close_save_load(self):
        self.show_save_load = False
        self.save_slots = []
        self.selected_save = -1

    def _load_selected_save(self):
        if self.selected_save < 0 or self.selected_save >= len(self.save_slots):
            return
        slot = self.save_slots[self.selected_save]
        state = load_state(slot["filename"])
        if state:
            self.selected_category = state.get("category")
            self.selected_subtype = state.get("sub_type")
            self.phases = get_phases(self.selected_category, self.selected_subtype)
            self.current_phase = state.get("current_phase", 0)
            self.current_step = state.get("current_step", 0)
            self.completed_steps = set(state.get("completed_steps", []))
            self.choices_made = state.get("choices_made", {})
            self.total_estimated_cost = state.get("total_estimated_cost", 0)
            self.pending_choice = None
            self.crafting_complete = False
            self._update_budget_estimate()
            self.mode = "crafting"
            self.message = f"Loaded: {slot['display_name']}"
            self.message_timer = 90

    def _delete_selected_save(self):
        if self.selected_save < 0 or self.selected_save >= len(self.save_slots):
            return
        slot = self.save_slots[self.selected_save]
        delete_save(slot["filename"])
        self.save_slots = list_saves()
        self.selected_save = min(self.selected_save, len(self.save_slots) - 1)
        self.message = f"Deleted save."
        self.message_timer = 60

    def _back_to_selection(self):
        self.mode = "select"
        self.selected_category = None
        self.selected_subtype = None
        self.phases = []
        self.current_phase = 0
        self.current_step = 0
        self.completed_steps = set()
        self.choices_made = {}
        self.pending_choice = None
        self.crafting_complete = False
        self.total_estimated_cost = 0

    def _back_one_step(self):
        if self.current_step > 0:
            self.current_step -= 1
        elif self.current_phase > 0:
            self.current_phase -= 1
            phase_steps = self._current_phase_steps()
            self.current_step = max(0, len(phase_steps) - 1)
        else:
            self._back_to_selection()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.VIDEORESIZE:
            from renderer import update_layout, init_fonts
            import renderer as _renderer
            update_layout(event.w, event.h)
            init_fonts()
            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            globals()["WIDTH"] = _renderer.WIDTH
            globals()["HEIGHT"] = _renderer.HEIGHT
            return

        if self.mod_search_active and event.type == pygame.TEXTINPUT:
            if self._search_skip_slash and event.text == "/":
                self._search_skip_slash = False
                return
            self.mod_search_query += event.text
            return

        if self.mode == "startup":
            self._handle_startup_event(event)
        elif self.show_save_load:
            self._handle_save_load_event(event)
        elif self.mode == "select":
            self._handle_selection_event(event)
        elif self.mode == "crafting":
            self._handle_crafting_event(event)
        elif self.mode == "complete":
            self._handle_complete_event(event)

    def _handle_startup_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_n:
                self.mode = "select"
            elif event.key == pygame.K_l:
                self._open_save_load("load")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            hitboxes = self.selection_hitboxes
            if "new_btn" in hitboxes and hitboxes["new_btn"] and hitboxes["new_btn"].collidepoint(mx, my):
                self.mode = "select"
            elif "resume_btn" in hitboxes and hitboxes["resume_btn"] and hitboxes["resume_btn"].collidepoint(mx, my):
                self._open_save_load("load")

    def _handle_selection_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = "startup"
            elif event.key == pygame.K_RETURN:
                if self.selected_category and self.selected_subtype:
                    self._begin_crafting()
            elif event.key == pygame.K_l:
                self._open_save_load("load")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            hitboxes = self.selection_hitboxes
            # Check sub-type item clicks first (they sit inside category panels)
            for st_name, rect in hitboxes.get("subtype_items", {}).items():
                if rect.collidepoint(mx, my):
                    self.selected_subtype = st_name
                    # Auto-select the parent category if not already set
                    if self.selected_category is None:
                        for cat_name, cat_data in self.categories.items():
                            if st_name in cat_data.get("sub_types", []):
                                self.selected_category = cat_name
                                break
                    return
            # Check category panel clicks (only if not clicking a sub-type)
            for cat_name, rect in hitboxes.get("category_panels", {}).items():
                if rect.collidepoint(mx, my):
                    self.selected_category = cat_name
                    self.selected_subtype = None
                    return
            # Check begin button
            begin_btn = hitboxes.get("begin_btn")
            if begin_btn and begin_btn.collidepoint(mx, my):
                if self.selected_category and self.selected_subtype:
                    self._begin_crafting()
                    return

    def _handle_save_load_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._close_save_load()
            elif event.key == pygame.K_RETURN:
                if self.save_load_mode == "load":
                    self._load_selected_save()
                    self._close_save_load()
                else:
                    # Save mode
                    self._auto_save()
                    self._close_save_load()
            elif event.key == pygame.K_DELETE:
                self._delete_selected_save()
            elif event.key == pygame.K_UP:
                if self.selected_save > 0:
                    self.selected_save -= 1
            elif event.key == pygame.K_DOWN:
                if self.selected_save < len(self.save_slots) - 1:
                    self.selected_save += 1
            elif event.key == pygame.K_n:
                self._close_save_load()
                self.mode = "select"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            hitboxes = self.save_load_hitboxes
            # Check save slot clicks
            for i, slot in enumerate(self.save_slots):
                if str(i) in hitboxes and hitboxes[str(i)].collidepoint(mx, my):
                    self.selected_save = i
                    # Double-click to load
                    if self.save_load_mode == "load":
                        self._load_selected_save()
                        self._close_save_load()
                    return
            # Check new craft button
            if "new_btn" in hitboxes and hitboxes["new_btn"].collidepoint(mx, my):
                self._close_save_load()
                self.mode = "select"
            # Check delete button
            if "delete_btn" in hitboxes and hitboxes["delete_btn"].collidepoint(mx, my):
                self._delete_selected_save()
            # Check back button
            if "back_btn" in hitboxes and hitboxes["back_btn"].collidepoint(mx, my):
                self._close_save_load()

    def _handle_crafting_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.mod_search_rect and self.mod_search_rect.collidepoint(mx, my):
                self.mod_search_active = True
                self.mod_search_query = ""
                self._search_skip_slash = False
                pygame.key.set_text_input_rect(self.mod_search_rect)
                return
            # Reset button
            if self.reset_btn_rect and self.reset_btn_rect.collidepoint(mx, my):
                self._reset()
                return
            # Confirm button
            if self.confirm_btn_rect and self.confirm_btn_rect.collidepoint(mx, my):
                step = self._current_step_data()
                if step and step["id"] not in self.completed_steps:
                    self._confirm_step()
                return
            # Back button
            if self.back_btn_rect and self.back_btn_rect.collidepoint(mx, my):
                self._back_one_step()
                return
            # Choice buttons
            for i, rect in enumerate(self.choice_btn_rects):
                if rect.collidepoint(mx, my):
                    self.pending_choice = i
                    return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.mod_search_active:
                    self.mod_search_active = False
                    self.mod_search_query = ""
                    self._search_skip_slash = False
                    pygame.key.set_text_input_rect(pygame.Rect(0, 0, 0, 0))
                    return
                else:
                    self._reset()
            elif event.key == pygame.K_SLASH:
                self.mod_search_active = not self.mod_search_active
                if self.mod_search_active:
                    self.mod_search_query = ""
                    self._search_skip_slash = True
                    if self.mod_search_rect:
                        pygame.key.set_text_input_rect(self.mod_search_rect)
                else:
                    self.mod_search_query = ""
                    self._search_skip_slash = False
                    pygame.key.set_text_input_rect(pygame.Rect(0, 0, 0, 0))
                return
            elif self.mod_search_active and event.key == pygame.K_BACKSPACE:
                self.mod_search_query = self.mod_search_query[:-1]
                return
            elif self.mod_search_active:
                return
            elif event.key == pygame.K_SPACE:
                step = self._current_step_data()
                if step and step["id"] not in self.completed_steps:
                    self._confirm_step()
                else:
                    self._advance_step()
            elif event.key in (pygame.K_RETURN, pygame.K_RIGHT):
                step = self._current_step_data()
                if step and step["id"] not in self.completed_steps:
                    self._confirm_step()
                else:
                    self._advance_step()
            elif event.key == pygame.K_LEFT:
                if self.current_step > 0:
                    self.current_step -= 1
                elif self.current_phase > 0:
                    self.current_phase -= 1
                    phase_steps = self._current_phase_steps()
                    self.current_step = max(0, len(phase_steps) - 1)
            elif event.key == pygame.K_TAB:
                self._skip_phase()
            elif event.key == pygame.K_r:
                self._start_price_fetch()
                self.message = "Refreshing prices..."
                self.message_timer = 60
            elif event.key == pygame.K_s:
                self._open_save_load("save")
            elif event.key == pygame.K_l:
                self._open_save_load("load")
            elif event.key == pygame.K_b:
                self._back_one_step()
            elif event.key == pygame.K_1: self._go_to_phase(0)
            elif event.key == pygame.K_2: self._go_to_phase(1)
            elif event.key == pygame.K_3: self._go_to_phase(2)
            elif event.key == pygame.K_4: self._go_to_phase(3)
            elif event.key == pygame.K_5: self._go_to_phase(4)
            elif event.key == pygame.K_6: self._go_to_phase(5)
            elif event.key == pygame.K_7: self._go_to_phase(6)
            elif event.key == pygame.K_8: self._go_to_phase(7)
            elif event.key == pygame.K_9: self._go_to_phase(8)
            elif event.key == pygame.K_0: self._go_to_phase(9)

    def _handle_complete_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_r:
                self._reset()
            elif event.key == pygame.K_b:
                self._back_to_selection()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.screen.fill((0, 0, 0))

            if self.show_save_load:
                self.save_slots = list_saves()
                hitboxes = draw_save_load_screen(
                    self.screen, self.tick, self.save_slots,
                    self.save_load_mode, selected_save=self.selected_save
                )
                self.save_load_hitboxes = hitboxes
            elif self.mode == "startup":
                self._draw_startup_screen()
            elif self.mode == "select":
                draw_background(self.screen, self.tick)
                hitboxes = draw_selection_screen(
                    self.screen, self.tick,
                    self.categories, self.selected_category, self.selected_subtype,
                )
                self.selection_hitboxes = hitboxes
            elif self.mode == "crafting":
                draw_background(self.screen, self.tick)

                phase_hitboxes = draw_phase_list(
                    self.screen, self.phases, self.current_phase,
                    self.completed_steps,
                )
                if phase_hitboxes:
                    self.reset_btn_rect = phase_hitboxes.get("reset_btn")
                else:
                    self.reset_btn_rect = None

                step = self._current_step_data()
                if step:
                    hitboxes = draw_step_panel(
                        self.screen, step, self.current_step,
                        self._current_phase_steps(), self.completed_steps,
                        pending_choice=self.pending_choice,
                    )
                    self.confirm_btn_rect = hitboxes.get("confirm_btn")
                    self.back_btn_rect = hitboxes.get("back_btn")
                    self.choice_btn_rects = hitboxes.get("choice_btns", [])
                    price_hitboxes = draw_price_panel(
                        self.screen, step, prices_available(),
                        running_total=self.total_estimated_cost,
                        category=self.selected_category,
                        mod_search_query=self.mod_search_query,
                        mod_search_active=self.mod_search_active,
                        item_type=self.selected_subtype,
                    )
                    if price_hitboxes:
                        self.mod_search_rect = price_hitboxes.get("mod_search_rect")
                else:
                    self.confirm_btn_rect = None
                    self.back_btn_rect = None
                    self.choice_btn_rects = []

                self._draw_help_bar()

            elif self.mode == "complete":
                draw_background(self.screen, self.tick)
                draw_crafting_end_screen(self.screen)

            if self.message_timer > 0:
                self._draw_message()
                self.message_timer -= 1

            pygame.display.flip()
            self.clock.tick(60)
            self.tick += 1

            # Spawn ambient particles occasionally
            if self.tick % 8 == 0:
                spawn_particle(random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def _draw_startup_screen(self):
        self.screen.fill((8, 4, 2))
        cx = WIDTH // 2

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
        base_y = HEIGHT // 2 - total_h // 2

        draw_text(self.screen, "PoE2 Mirror Crafter", cx, base_y, TEXT_GOLD, "title", centered=True)

        draw_text(self.screen, "Weapons  |  Armour  |  Jewellery",
                  cx, base_y + title_to_sub_gap, TEXT_WHITE, "medium", centered=True)

        btn_new_y = base_y + title_to_sub_gap + subtitle_h + sub_to_btn1_gap
        btn_w = _s(300)
        new_btn = pygame.Rect(cx - btn_w // 2, btn_new_y, btn_w, btn_h)
        draw_rect(self.screen, new_btn, (50, 20, 10), radius=6)
        draw_rect(self.screen, new_btn, BORDER_GOLD, border=2, radius=6)
        draw_text(self.screen, "[N]  NEW CRAFT", cx, btn_new_y + _s(12), (220, 200, 120), "large", centered=True)

        btn_resume_y = btn_new_y + btn_h + btn1_to_btn2_gap
        resume_btn = pygame.Rect(cx - btn_w // 2, btn_resume_y, btn_w, btn_h)
        draw_rect(self.screen, resume_btn, (20, 10, 40), radius=6)
        draw_rect(self.screen, resume_btn, BORDER_GOLD_DIM, border=2, radius=6)
        draw_text(self.screen, "[L]  RESUME CRAFT", cx, btn_resume_y + _s(12), TEXT_GOLD, "large", centered=True)

        draw_text(self.screen, "ESC to quit", cx, btn_resume_y + btn_h + btn2_to_esc_gap, TEXT_DIM, "tiny", centered=True)
        from main import __version__
        draw_text(self.screen, f"v{__version__}", WIDTH - _s(12), HEIGHT - _s(12), TEXT_DIM, "tiny", centered=False)

        self.selection_hitboxes = {
            "category_panels": {},
            "subtype_items": {},
            "begin_btn": None,
            "new_btn": new_btn,
            "resume_btn": resume_btn,
        }

    def _draw_help_bar(self):
        from renderer import WIDTH as win_w, _truncate_to_fit
        bar_h = _s(22)
        y = max(bar_h, HEIGHT - bar_h)
        draw_rect(self.screen, (0, y, win_w, bar_h), BG_HEADER)
        draw_rect(self.screen, (0, y, win_w, bar_h), BORDER_GOLD_DIM, border=1)
        help_text = (
            "[SPACE] Confirm | [Enter] Next | [Tab] Skip Phase | "
            "[1-0] Phase | [/] Search Mods | [S] Save | [L] Load | [B] Back | [Esc] Reset"
        )
        tiny_f = get_font("tiny")
        max_w = win_w - _s(16)
        if tiny_f.size(help_text)[0] >= max_w:
            help_text = _truncate_to_fit(help_text, tiny_f, max_w)
        draw_text(self.screen, help_text, _s(8), y + _s(4), TEXT_DIM, "tiny")

    def _draw_message(self):
        alpha = min(255, self.message_timer * 2)
        msg_h = _s(30)
        s = pygame.Surface((WIDTH, msg_h), pygame.SRCALPHA)
        s.fill((8, 4, 4, min(200, alpha)))
        msg_y = HEIGHT - _s(56)
        self.screen.blit(s, (0, msg_y))
        draw_text(
            self.screen, self.message, WIDTH // 2, msg_y + _s(4),
            (220, 50, min(255, alpha)), "small", centered=True,
        )
