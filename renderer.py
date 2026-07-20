import pygame
import math
import os
import random
from phases.base_phases import ORB_COLORS
from icon_loader import get_orb_icon

WIDTH, HEIGHT = 1280, 800
MIN_W, MIN_H = 960, 600
PANEL_LEFT = 320
PANEL_RIGHT_W = 280
PANEL_CENTER_X = PANEL_LEFT
PANEL_CENTER_W = WIDTH - PANEL_LEFT - PANEL_RIGHT_W


def update_layout(w, h):
    global WIDTH, HEIGHT, PANEL_CENTER_X, PANEL_CENTER_W
    WIDTH = max(w, MIN_W)
    HEIGHT = max(h, MIN_H)
    PANEL_CENTER_X = PANEL_LEFT
    PANEL_CENTER_W = WIDTH - PANEL_LEFT - PANEL_RIGHT_W

BG_DARK = (3, 2, 2)
BG_PANEL = (8, 5, 5)
BG_HEADER = (14, 9, 9)
BORDER_GOLD = (160, 20, 20)
BORDER_GOLD_DIM = (70, 10, 10)
TEXT_GOLD = (220, 50, 40)
TEXT_WHITE = (150, 140, 135)
TEXT_DIM = (80, 75, 70)
TEXT_BRIGHT = (230, 60, 50)
GREEN_GLOW = (60, 200, 80)
RED_GLOW = (180, 35, 35)
BLUE_GLOW = (45, 75, 130)
ORANGE_GLOW = (180, 95, 30)
PURPLE_GLOW = (150, 30, 30)
PINK_GLOW = (140, 25, 25)

FONT_SIZES = {
    "tiny": 12,
    "small": 14,
    "medium": 17,
    "large": 22,
    "huge": 28,
    "title": 34,
    "header": 20,
}

fonts = {}

_particles = []


# =============================================================================
#  Font system
# =============================================================================

def init_fonts():
    global fonts
    pygame.font.init()
    font_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "assets", "fonts", "gothic.ttf",
    )
    for name, size in FONT_SIZES.items():
        if os.path.isfile(font_path):
            try:
                fonts[name] = pygame.font.Font(font_path, size)
            except Exception:
                fonts[name] = pygame.font.Font(None, size)
        else:
            fonts[name] = pygame.font.Font(None, size)


def get_font(size_name):
    return fonts.get(size_name, fonts.get("small"))


# =============================================================================
#  Drawing helpers
# =============================================================================

def draw_text(surface, text, x, y, color, size_name="small", centered=False):
    font = get_font(size_name)
    lines = text.split("\n")
    y_off = y
    for line in lines:
        rendered = font.render(line, True, color)
        if centered:
            rect = rendered.get_rect(centerx=x, top=y_off)
            surface.blit(rendered, rect)
        else:
            surface.blit(rendered, (x, y_off))
        y_off += font.get_height() + 2


def draw_rect(surface, rect, color, border=0, radius=0):
    if radius > 0:
        pygame.draw.rect(surface, color, rect, border, border_radius=radius)
    else:
        pygame.draw.rect(surface, color, rect, border)


def draw_panel(surface, x, y, w, h, header_text=""):
    draw_rect(surface, (x, y, w, h), BG_PANEL)
    draw_rect(surface, (x, y, w, h), BORDER_GOLD_DIM, border=1)
    if header_text:
        header_h = 28
        draw_rect(surface, (x, y, w, header_h), BG_HEADER)
        draw_rect(surface, (x, y, w, header_h), BORDER_GOLD_DIM, border=1)
        draw_text(surface, header_text, x + 8, y + 5, TEXT_GOLD, "small")


# =============================================================================
#  Runic border decorations
# =============================================================================

def draw_runic_border(surface, x, y, w, h):
    half = 7
    color = BORDER_GOLD_DIM

    def diamond(cx, cy, half_sz):
        pts = [
            (cx, cy - half_sz),
            (cx + half_sz, cy),
            (cx, cy + half_sz),
            (cx - half_sz, cy),
        ]
        pygame.draw.polygon(surface, color, pts, 1)

    def cross(cx, cy, half_sz):
        pygame.draw.line(surface, color, (cx - half_sz, cy - half_sz), (cx + half_sz, cy + half_sz), 1)
        pygame.draw.line(surface, color, (cx + half_sz, cy - half_sz), (cx - half_sz, cy + half_sz), 1)

    diamond(x + 12, y + 12, half)
    cross(x + 24, y + 12, half - 1)

    diamond(x + w - 12, y + 12, half)
    cross(x + w - 24, y + 12, half - 1)

    diamond(x + 12, y + h - 12, half)
    cross(x + 24, y + h - 12, half - 1)

    diamond(x + w - 12, y + h - 12, half)
    cross(x + w - 24, y + h - 12, half - 1)


# =============================================================================
#  Particle system
# =============================================================================

def spawn_particle(x, y):
    vx = random.uniform(-1.2, 1.2)
    vy = random.uniform(-2.5, -0.3)
    life = random.randint(60, 120)
    _particles.append([float(x), float(y), vx, vy, 255.0, life, life])


def update_particles():
    for i in range(len(_particles) - 1, -1, -1):
        p = _particles[i]
        p[0] += p[2]
        p[1] += p[3]
        p[4] = max(0, int(255 * (p[5] / p[6])))
        p[5] -= 1
        if p[5] <= 0:
            del _particles[i]


def draw_particles(surface):
    base_r, base_g, base_b = TEXT_GOLD
    for p in _particles:
        alpha = max(0, min(255, p[4]))
        radius = max(1, int(3 * (p[5] / p[6])))
        s = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(
            s,
            (base_r, base_g, base_b, alpha),
            (radius + 1, radius + 1),
            radius,
        )
        surface.blit(s, (int(p[0]) - radius, int(p[1]) - radius))


# =============================================================================
#  Background
# =============================================================================

def draw_background(surface, tick):
    surface.fill(BG_DARK)

    for i in range(0, WIDTH, 60):
        for j in range(0, HEIGHT, 60):
            shade = 12 + int(
                3 * math.sin(i * 0.01 + tick * 0.001 + j * 0.005)
            )
            shade = max(8, min(18, shade))
            c = (shade, shade // 3, shade // 3)
            pygame.draw.rect(surface, c, (i, j, 58, 58), width=1)

    for i in range(6):
        angle = tick * 0.0003 + i * 1.047
        rx = WIDTH // 2 + int(300 * math.cos(angle))
        ry = HEIGHT // 2 + int(200 * math.sin(angle * 0.7))
        for ring in range(3):
            r = 40 + ring * 25
            alpha = 40 - ring * 12
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                s,
                (BORDER_GOLD_DIM[0], BORDER_GOLD_DIM[1], BORDER_GOLD_DIM[2],
                 alpha),
                (r, r),
                r,
                width=1,
            )
            surface.blit(s, (rx - r, ry - r))

    update_particles()
    draw_particles(surface)

    header_x = PANEL_LEFT + PANEL_CENTER_W // 2
    draw_text(
        surface,
        "PoE2 Mirror Crafter",
        header_x,
        48,
        TEXT_GOLD,
        "title",
        centered=True,
    )
    draw_text(
        surface,
        "MIRROR-TIER CRAFTING GUIDE",
        header_x,
        86,
        TEXT_GOLD,
        "medium",
        centered=True,
    )


# =============================================================================
#  Selection screen
# =============================================================================

def draw_selection_screen(surface, tick, categories, selected_category, selected_subtype):
    update_particles()
    draw_particles(surface)

    cx = WIDTH // 2
    draw_text(surface, "CHOOSE  YOUR  CRAFT", cx, 30, TEXT_GOLD, "huge", centered=True)
    draw_text(
        surface,
        "Select an item type to begin your journey toward mirror-tier perfection.",
        cx, 66, TEXT_DIM, "tiny", centered=True,
    )

    cat_names = list(categories.keys())
    margin = 40
    spacing = 16
    panel_w = (WIDTH - margin * 2 - spacing * (len(cat_names) - 1)) // len(cat_names)
    panel_y = 100
    panel_h = min(530, HEIGHT - panel_y - 80)
    panel_x = margin

    category_panels = {}
    subtype_items = {}
    begin_btn = None

    for cat_name in cat_names:
        cat = categories[cat_name]
        is_selected_cat = selected_category == cat_name
        bx = panel_x
        by = panel_y
        bw = panel_w
        bh = panel_h

        draw_panel(surface, bx, by, bw, bh, f" {cat_name} ")
        draw_runic_border(surface, bx, by, bw, bh)

        if is_selected_cat:
            draw_rect(surface, (bx, by, bw, bh), BORDER_GOLD, border=2)
            draw_rect(surface, (bx, by, bw, 28), BORDER_GOLD, border=2)

        desc = cat.get("description", "")
        if desc:
            desc_font = get_font("tiny")
            words = desc.split(" ")
            lines = []
            line = ""
            for word in words:
                test = line + (" " if line else "") + word
                if desc_font.size(test)[0] < bw - 16:
                    line = test
                else:
                    lines.append(line)
                    line = word
            if line:
                lines.append(line)
            desc_y = by + 36
            for line in lines:
                draw_text(surface, line, bx + 8, desc_y, TEXT_DIM, "tiny")
                desc_y += get_font("tiny").get_height() + 1

        sub_types = cat.get("sub_types", [])
        sub_start_y = by + 80
        sub_item_h = 28

        if is_selected_cat and sub_types:
            draw_text(surface, "Sub-types:", bx + 8, sub_start_y - 16, TEXT_GOLD, "small")

        for sti, st in enumerate(sub_types):
            sty = sub_start_y + sti * sub_item_h
            if sty + sub_item_h > by + bh - 20:
                break

            is_selected_sub = is_selected_cat and selected_subtype == st
            st_rect = pygame.Rect(bx + 6, sty, bw - 12, sub_item_h - 2)

            if is_selected_sub:
                draw_rect(surface, st_rect, (30, 10, 10), radius=3)
                draw_rect(surface, st_rect, BORDER_GOLD, border=1, radius=3)
                st_color = TEXT_BRIGHT
            else:
                st_color = TEXT_WHITE
                if is_selected_cat:
                    draw_rect(surface, st_rect, (15, 6, 6), radius=2)

            draw_text(surface, f"  {st}", st_rect.x + 4, st_rect.y + 5, st_color, "tiny")
            subtype_items[st] = st_rect

        category_panels[cat_name] = pygame.Rect(bx, by, bw, bh)
        panel_x += panel_w + spacing

    if selected_category and selected_subtype:
        btn_w = 280
        btn_h = 44
        btn_x = cx - btn_w // 2
        btn_y = HEIGHT - 54
        draw_rect(surface, (btn_x, btn_y, btn_w, btn_h), (40, 90, 30), radius=6)
        draw_rect(surface, (btn_x, btn_y, btn_w, btn_h), GREEN_GLOW, border=2, radius=6)
        draw_text(
            surface, "BEGIN  CRAFT",
            btn_x + btn_w // 2, btn_y + 10, TEXT_BRIGHT, "large", centered=True,
        )
        begin_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

    bot_y = HEIGHT - 18
    if selected_category and selected_subtype:
        draw_text(surface, "Press ENTER or click BEGIN CRAFT to start", cx, bot_y, GREEN_GLOW, "tiny", centered=True)
    elif selected_category:
        draw_text(surface, "Now select a sub-type \u2191", cx, bot_y, TEXT_GOLD, "tiny", centered=True)
    else:
        draw_text(surface, "Click a category above to begin", cx, bot_y, TEXT_DIM, "tiny", centered=True)

    return {
        "category_panels": category_panels,
        "subtype_items": subtype_items,
        "begin_btn": begin_btn,
    }


# =============================================================================
#  Phase list (sidebar)
# =============================================================================

def draw_phase_list(surface, phases, current_phase, completed_steps):
    x, y, w = 4, 4, PANEL_LEFT - 8
    draw_panel(surface, x, y, w, HEIGHT - 8, " Crafting Phases ")
    draw_runic_border(surface, x, y, w, HEIGHT - 8)
    item_h = 42
    start_y = y + 34
    view_h = HEIGHT - 50
    visible = view_h // item_h

    for i in range(len(phases)):
        iy = start_y + i * item_h
        if iy + item_h < y + 30 or iy > HEIGHT - 10:
            continue

        phase = phases[i]
        pnum = phase["number"]
        pname = phase["name"]
        total_steps = len(phase["steps"])
        done_steps = len(
            [s for s in phase["steps"] if s["id"] in completed_steps]
        )

        is_current = i == current_phase
        is_done = done_steps == total_steps and total_steps > 0

        if is_current:
            draw_rect(surface, (x + 2, iy, w - 4, item_h), (28, 8, 8))
            draw_rect(
                surface, (x + 2, iy, w - 4, item_h), BORDER_GOLD, border=1
            )
        elif is_done:
            draw_rect(
                surface, (x + 2, iy, w - 4, item_h), (20, 50, 20), radius=3
            )

        color = TEXT_GOLD if is_current else (
            GREEN_GLOW if is_done else TEXT_DIM
        )
        draw_text(
            surface,
            f"P{pnum}: {pname}",
            x + 10,
            iy + 2,
            color,
            "tiny",
        )

        bar_x = x + 10
        bar_y = iy + item_h - 6
        bar_w = w - 20
        bar_h = 3
        draw_rect(surface, (bar_x, bar_y, bar_w, bar_h), (18, 14, 14))
        if total_steps > 0:
            fill_w = int(bar_w * done_steps / total_steps)
            fill_c = GREEN_GLOW if is_done else BORDER_GOLD
            draw_rect(surface, (bar_x, bar_y, fill_w, bar_h), fill_c)

    reset_btn_w = w - 20
    reset_btn_h = 32
    reset_btn_x = x + 10
    reset_btn_y = HEIGHT - 62
    draw_rect(surface, (reset_btn_x, reset_btn_y, reset_btn_w, reset_btn_h), (50, 15, 10), radius=4)
    draw_rect(surface, (reset_btn_x, reset_btn_y, reset_btn_w, reset_btn_h), BORDER_GOLD, border=2, radius=4)
    draw_text(surface, "RESET", reset_btn_x + reset_btn_w // 2, reset_btn_y + 6, TEXT_BRIGHT, "medium", centered=True)

    return {"reset_btn": pygame.Rect(reset_btn_x, reset_btn_y, reset_btn_w, reset_btn_h)}


# =============================================================================
#  Step panel (center) — now with choice alternatives
# =============================================================================

def draw_step_panel(
    surface, step, step_index, phase_steps, completed_steps, pending_choice=None
):
    x = PANEL_LEFT + 4
    y = 4
    w = PANEL_CENTER_W - 8
    step_h = 30
    steps_bar_h = step_h + 6
    head_h = 28

    draw_panel(surface, x, y, w, steps_bar_h, "")
    draw_rect(surface, (x, y, w, steps_bar_h), BORDER_GOLD_DIM, border=1)

    for i, s in enumerate(phase_steps):
        sx = x + 4 + i * ((w - 8) // max(len(phase_steps), 1))
        sw = (w - 8) // max(len(phase_steps), 1) - 4
        sy = y + 2
        sh = steps_bar_h - 4

        is_done = s["id"] in completed_steps
        is_this = i == step_index

        if is_this:
            draw_rect(surface, (sx, sy, sw, sh), (28, 8, 8))
            draw_rect(surface, (sx, sy, sw, sh), BORDER_GOLD, border=1)
        elif is_done:
            draw_rect(
                surface, (sx, sy, sw, sh), (30, 70, 30), border=1, radius=2
            )
        else:
            draw_rect(
                surface, (sx, sy, sw, sh), BG_HEADER, border=1, radius=2
            )

        color = TEXT_GOLD if is_this else (
            GREEN_GLOW if is_done else TEXT_DIM
        )
        short_id = s["id"].split(".")[-1]
        draw_text(
            surface,
            f"Step {short_id}",
            sx + 4,
            sy + 6,
            color,
            "tiny",
        )

    content_y = y + steps_bar_h + 4
    content_h = HEIGHT - content_y - 4
    draw_panel(surface, x, content_y, w, content_h, f" {step['title']} ")

    desc_y = content_y + 32
    max_desc_y = content_y + content_h - 55

    font_s = get_font("small")
    max_desc_w = w - 24
    desc_lines = []
    for paragraph in step["description"].split("\n"):
        words = paragraph.split(" ")
        line = ""
        for word in words:
            test = line + (" " if line else "") + word
            if font_s.size(test)[0] < max_desc_w:
                line = test
            else:
                desc_lines.append(line)
                line = word
        if line:
            desc_lines.append(line)

    avatar_font = font_s
    line_h_s = avatar_font.get_height() + 2
    fit_lines = int((max_desc_y - desc_y) / line_h_s)
    use_tiny = len(desc_lines) > fit_lines
    if use_tiny:
        avatar_font = get_font("tiny")
        line_h_s = avatar_font.get_height() + 2
        fit_lines = int((max_desc_y - desc_y) / line_h_s)

    for i in range(min(len(desc_lines), fit_lines)):
        line = desc_lines[i]
        if i == fit_lines - 1 and i < len(desc_lines) - 1:
            line = _truncate_to_fit(line.rstrip() + " [...]", avatar_font, max_desc_w)
        draw_text(surface, line, x + 12, desc_y, TEXT_WHITE if not use_tiny else TEXT_DIM, "small" if not use_tiny else "tiny")
        desc_y += line_h_s

    desc_bottom = desc_y

    alternatives = step.get("alternatives", None)
    choice_btns = []
    confirm_btn = None
    step_id = step["id"]
    has_alternatives = alternatives and step_id not in completed_steps

    alt_y = desc_bottom + 10

    if has_alternatives:
        draw_rect(surface, (x + 8, alt_y, w - 16, 1), BORDER_GOLD_DIM)
        alt_y += 6
        draw_text(surface, "Choose your approach:", x + 12, alt_y, TEXT_GOLD, "small")
        alt_y += get_font("small").get_height() + 6

        for alt_idx, alt in enumerate(alternatives):
            btn_x = x + 20
            btn_w = w - 40
            btn_h = 44
            is_sel = pending_choice == alt_idx

            risk_color = {
                "low": GREEN_GLOW,
                "very low": GREEN_GLOW,
                "medium": ORANGE_GLOW,
                "high": RED_GLOW,
            }.get(alt.get("risk", "medium"), ORANGE_GLOW)

            if is_sel:
                draw_rect(surface, (btn_x, alt_y, btn_w, btn_h), (30, 10, 10), radius=4)
                draw_rect(surface, (btn_x, alt_y, btn_w, btn_h), BORDER_GOLD, border=2, radius=4)
            else:
                draw_rect(surface, (btn_x, alt_y, btn_w, btn_h), BG_HEADER, radius=4)
                draw_rect(surface, (btn_x, alt_y, btn_w, btn_h), BORDER_GOLD_DIM, border=1, radius=4)

            label_text = alt.get("label", f"Option {alt_idx + 1}")
            cost_text = alt.get("cost", "")
            risk_text = alt.get("risk", "medium")

            draw_text(surface, label_text, btn_x + 8, alt_y + 4, TEXT_WHITE if is_sel else TEXT_GOLD, "tiny")
            draw_text(
                surface, f"Cost: {cost_text}   Risk: {risk_text}",
                btn_x + 8, alt_y + 24, risk_color, "tiny",
            )

            r = pygame.Rect(btn_x, alt_y, btn_w, btn_h)
            choice_btns.append(r)
            alt_y += btn_h + 4

            if alt_y + btn_h > content_y + content_h - 80:
                break

    is_done_step = step_id in completed_steps

    action_y = content_y + content_h - 60
    draw_rect(surface, (x + 8, action_y, w - 16, 40), BG_HEADER)
    draw_rect(
        surface, (x + 8, action_y, w - 16, 40), BORDER_GOLD_DIM, border=1
    )
    draw_text(
        surface,
        f"ACTION: {step['action']}",
        x + 16,
        action_y + 6,
        TEXT_GOLD,
        "medium",
    )

    btn_w = 220
    btn_h = 36
    btn_x = x + w - btn_w - 16
    btn_y = action_y + 2

    if is_done_step:
        draw_rect(
            surface, (btn_x, btn_y, btn_w, btn_h), (30, 90, 30), radius=4
        )
        draw_rect(
            surface,
            (btn_x, btn_y, btn_w, btn_h),
            GREEN_GLOW,
            border=2,
            radius=4,
        )
        draw_text(
            surface,
            "STEP COMPLETE",
            btn_x + btn_w // 2,
            btn_y + 8,
            TEXT_BRIGHT,
            "medium",
            centered=True,
        )
    else:
        if alternatives and pending_choice is not None:
            clamped = min(max(pending_choice, 0), len(alternatives) - 1)
            if clamped != pending_choice:
                pending_choice = clamped
        else:
            draw_rect(
                surface, (btn_x, btn_y, btn_w, btn_h), (50, 25, 10), radius=4
            )
            draw_rect(
                surface,
                (btn_x, btn_y, btn_w, btn_h),
                BORDER_GOLD,
                border=2,
                radius=4,
            )
            draw_text(
                surface,
                "Confirm Step",
                btn_x + btn_w // 2,
                btn_y + 8,
                TEXT_BRIGHT,
                "medium",
                centered=True,
            )

    confirm_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h) if not is_done_step else None

    return {
        "confirm_btn": confirm_btn,
        "choice_btns": choice_btns,
    }


# =============================================================================
#  Price panel (right) — with running total and budget tier
# =============================================================================

def draw_price_panel(surface, step, prices_available_flag, running_total=0.0, category=None):
    x = WIDTH - PANEL_RIGHT_W + 4
    y = 4
    w = PANEL_RIGHT_W - 8
    draw_panel(surface, x, y, w, HEIGHT - 8, " Marketplace ")
    draw_runic_border(surface, x, y, w, HEIGHT - 8)

    from prices import get_price, price_source

    source_label = price_source()
    source_color = GREEN_GLOW if source_label == "live" else TEXT_DIM
    draw_text(
        surface,
        f"Source: {source_label}",
        x + w - 80,
        y + 6,
        source_color,
        "tiny",
    )

    if category:
        from phases import calculate_tier_thresholds
        tier_thresholds = calculate_tier_thresholds(category)
    else:
        tier_thresholds = None

    orbs = step.get("orbs_used", [])
    if not orbs:
        if running_total > 0:
            draw_text(surface, "(No orbs in this step)", x + 12, y + 40, TEXT_DIM, "tiny")
        else:
            draw_text(surface, "(No orbs in this step)", x + 12, y + 40, TEXT_DIM, "tiny")
        if running_total > 0:
            _draw_budget_tier(surface, x, y, w, running_total, tier_thresholds)
        return

    orb_y = y + 40
    step_total_chaos = 0
    orbs_shown = 0
    total_orbs = len(orbs)

    for orb_name in orbs:
        if orb_y > HEIGHT - 160:
            break
        draw_orb(surface, x + 30, orb_y + 14, 18, orb_name)
        draw_text(surface, orb_name, x + 56, orb_y + 6, TEXT_WHITE, "tiny")

        p = get_price(orb_name)
        if p:
            chaos = p["chaos"]
            divine = p["divine"]
            draw_text(
                surface,
                f"{chaos:.1f} chaos  |  {divine:.4f} div",
                x + 60,
                orb_y + 22,
                TEXT_GOLD,
                "tiny",
            )
            step_total_chaos += chaos
        else:
            draw_text(
                surface,
                "price not found",
                x + 60,
                orb_y + 22,
                TEXT_DIM,
                "tiny",
            )
        orb_y += 50
        orbs_shown += 1

    if orbs_shown < total_orbs:
        draw_text(
            surface,
            f"... and {total_orbs - orbs_shown} more orb types",
            x + 12,
            orb_y + 4,
            TEXT_DIM,
            "tiny",
        )

    if len(orbs) > 1:
        draw_rect(
            surface, (x + 8, orb_y, w - 16, 1), BORDER_GOLD_DIM, border=1
        )
        divine_price = 0
        from prices import CACHED_PRICES
        dv = CACHED_PRICES.get("Divine Orb", {}).get("chaos", 0)
        if dv > 0:
            divine_price = step_total_chaos / dv
        draw_text(
            surface,
            f"Step Orb Total: {step_total_chaos:.1f}c = {divine_price:.3f} div",
            x + 12,
            orb_y + 8,
            TEXT_GOLD,
            "tiny",
        )

    if running_total > 0:
        _draw_budget_tier(surface, x, y, w, running_total, tier_thresholds)


def _truncate_to_fit(text, font, max_w):
    while len(text) > 4 and font.size(text)[0] >= max_w:
        text = text[:-4].rstrip() + "..."
    return text


def _draw_budget_tier(surface, x, y, w, running_total, tier_thresholds=None):
    tot_y = HEIGHT - 100
    panel_bottom = HEIGHT - 8
    draw_rect(surface, (x + 8, tot_y - 4, w - 16, 1), BORDER_GOLD)

    if tier_thresholds is None:
        from phases import default_tier_thresholds
        tier_thresholds = default_tier_thresholds()

    t = tier_thresholds[0] if tier_thresholds else {"label": "Mirror Craft", "description": "", "color": "red"}
    tier_label = t["label"]
    tier_desc = t.get("description", "")

    draw_text(surface, f"Est. Total Cost: {running_total:.1f} div", x + 12, tot_y + 4, TEXT_GOLD, "small")
    draw_text(surface, f"Tier: {tier_label}", x + 12, tot_y + 24, RED_GLOW, "tiny")
    if tier_desc:
        y_desc = tot_y + 44
        font_t = get_font("tiny")
        max_w = w - 30
        line_h = font_t.get_height() + 2
        avail_h = panel_bottom - y_desc - 4
        max_lines = max(0, avail_h // line_h)
        words = tier_desc.split(" ")
        lines = []
        line = ""
        for word in words:
            test = line + (" " if line else "") + word
            if font_t.size(test)[0] < max_w:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        for i, line in enumerate(lines):
            if i >= max_lines:
                break
            if i == max_lines - 1 and i < len(lines) - 1:
                line = _truncate_to_fit(line + "...", font_t, max_w)
            draw_text(surface, line, x + 12, y_desc, TEXT_DIM, "tiny")
            y_desc += line_h


# =============================================================================
#  Save / load screen
# =============================================================================

def draw_save_load_screen(surface, tick, saves_list, mode="load", selected_save=-1):
    update_particles()
    draw_particles(surface)

    title_text = "RESUME  CRAFT" if mode == "load" else "SAVE  YOUR  CRAFT"
    draw_text(surface, title_text, WIDTH // 2, 28, TEXT_GOLD, "huge", centered=True)
    draw_text(
        surface,
        "Select a save slot and press ENTER, or start a New Craft.",
        WIDTH // 2, 64, TEXT_DIM, "tiny", centered=True,
    )

    panel_x = 140
    panel_w = WIDTH - 280
    panel_h = HEIGHT - 130
    panel_y = 90
    draw_panel(surface, panel_x, panel_y, panel_w, panel_h, " Save Slots ")
    draw_runic_border(surface, panel_x, panel_y, panel_w, panel_h)

    slot_h = 60
    slot_y = panel_y + 32
    slot_rects = []
    selected_index = selected_save

    if not saves_list:
        draw_text(
            surface,
            "(No saves found)",
            panel_x + panel_w // 2,
            panel_y + panel_h // 2 - 20,
            TEXT_DIM,
            "medium",
            centered=True,
        )
    else:
        for si, save in enumerate(saves_list):
            if slot_y + slot_h > panel_y + panel_h - 60:
                break
            sr = pygame.Rect(panel_x + 8, slot_y, panel_w - 16, slot_h - 4)

            draw_rect(surface, sr, BG_HEADER, radius=3)
            draw_rect(surface, sr, BORDER_GOLD_DIM, border=1, radius=3)

            name = save.get("display_name", save.get("filename", "???"))
            date = save.get("date", "")[:19].replace("T", " ")
            cat = save.get("category", "")
            sub = save.get("sub_type", "")
            phase = save.get("phase", 0)
            step = save.get("step", 0)
            done = save.get("steps_complete", 0)

            draw_text(surface, name, sr.x + 10, sr.y + 4, TEXT_GOLD, "small")
            draw_text(
                surface,
                f"{date}  |  {cat} / {sub}  |  Phase {phase+1} Step {step+1}  |  {done} steps done",
                sr.x + 10, sr.y + 30, TEXT_DIM, "tiny",
            )

            slot_rects.append(sr)
            slot_y += slot_h

    if mode == "save":
        auto_name = save.get("filename", "craft_save.json") if saves_list else "craft_save.json"
    else:
        auto_name = ""

    new_btn_w = 200
    new_btn_h = 36
    new_btn_x = panel_x + 20
    new_btn_y = HEIGHT - 52
    draw_rect(surface, (new_btn_x, new_btn_y, new_btn_w, new_btn_h), (40, 100, 40), radius=4)
    draw_rect(surface, (new_btn_x, new_btn_y, new_btn_w, new_btn_h), GREEN_GLOW, border=2, radius=4)
    draw_text(
        surface, "NEW  CRAFT",
        new_btn_x + new_btn_w // 2, new_btn_y + 8, TEXT_BRIGHT, "medium", centered=True,
    )

    del_btn_x = new_btn_x + new_btn_w + 16
    del_btn_w = 160
    del_btn_h = 36
    if saves_list and selected_index >= 0:
        draw_rect(surface, (del_btn_x, new_btn_y, del_btn_w, del_btn_h), (50, 15, 10), radius=4)
    else:
        draw_rect(surface, (del_btn_x, new_btn_y, del_btn_w, del_btn_h), (20, 10, 10), radius=4)
    draw_rect(surface, (del_btn_x, new_btn_y, del_btn_w, del_btn_h), BORDER_GOLD_DIM, border=1, radius=4)
    draw_text(
        surface, "DELETE",
        del_btn_x + del_btn_w // 2, new_btn_y + 8, TEXT_DIM, "small", centered=True,
    )

    esc_y = HEIGHT - 16
    instruct = "[ENTER] Confirm   [ESC] Cancel   [Del] Delete selected"
    if mode == "save":
        instruct = "[ENTER] Save   [ESC] Cancel   [Del] Delete selected"
    draw_text(surface, instruct, WIDTH // 2, esc_y, TEXT_DIM, "tiny", centered=True)

    result = {
        "new_btn": pygame.Rect(new_btn_x, new_btn_y, new_btn_w, new_btn_h),
        "delete_btn": pygame.Rect(del_btn_x, new_btn_y, del_btn_w, del_btn_h),
        "selected_index": selected_index,
    }
    for i, sr in enumerate(slot_rects):
        result[str(i)] = sr
    return result


# =============================================================================
#  Completion screen
# =============================================================================

def draw_crafting_end_screen(surface, category="a weapon", sub_type=""):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    cx, cy = WIDTH // 2, HEIGHT // 2
    draw_text(
        surface,
        "CRAFTING  COMPLETE",
        cx,
        cy - 60,
        TEXT_BRIGHT,
        "title",
        centered=True,
    )

    if sub_type:
        line = f"Your 6x T1 mirror-tier {sub_type} is ready for service."
    else:
        line = f"Your 6x T1 mirror-tier {category.replace('a ','')} is ready for service."
    draw_text(surface, line, cx, cy + 4, TEXT_GOLD, "medium", centered=True)

    draw_text(
        surface,
        "GG, Exile.",
        cx,
        cy + 44,
        TEXT_WHITE,
        "large",
        centered=True,
    )
    draw_text(
        surface,
        "[ESC] Exit   [R] Start Over   [S] Save   [L] Load",
        cx,
        cy + 90,
        TEXT_DIM,
        "small",
        centered=True,
    )

    for i in range(12):
        angle = pygame.time.get_ticks() * 0.001 + i * 0.523
        rx = cx + int(250 * math.cos(angle))
        ry = cy + int(120 * math.sin(angle * 1.5))
        r = 3 + int(2 * math.sin(pygame.time.get_ticks() * 0.003 + i))
        draw_orb(surface, rx, ry, r, "Divine Orb")


# =============================================================================
#  Orb drawing — unchanged from original
# =============================================================================

def draw_orb(surface, cx, cy, radius, orb_name):
    icon = get_orb_icon(orb_name, radius * 2)
    if icon is not None:
        base_color = ORB_COLORS.get(orb_name, (90, 82, 95))
        r, g, b = base_color
        for layer in range(4):
            glow_r = radius + 6 + layer * 4
            alpha = 30 - layer * 8
            s = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                s,
                (r, g, b, alpha),
                (glow_r, glow_r),
                glow_r,
            )
            surface.blit(s, (cx - glow_r, cy - glow_r))
        icon_rect = icon.get_rect(center=(cx, cy))
        surface.blit(icon, icon_rect)
        return

    base_color = ORB_COLORS.get(orb_name, (90, 82, 95))
    r, g, b = base_color

    for i in range(radius, 0, -1):
        frac = i / radius
        shade_r = int(r * (0.3 + 0.7 * frac))
        shade_g = int(g * (0.3 + 0.7 * frac))
        shade_b = int(b * (0.3 + 0.7 * frac))
        pygame.draw.circle(surface, (shade_r, shade_g, shade_b), (cx, cy), i)

    highlight_r = min(255, r + 120)
    highlight_g = min(255, g + 120)
    highlight_b = min(255, b + 120)
    pygame.draw.circle(
        surface,
        (highlight_r, highlight_g, highlight_b),
        (cx - radius // 3, cy - radius // 3),
        radius // 3,
    )

    pygame.draw.circle(
        surface, (r // 2, g // 2, b // 2), (cx, cy), radius, width=2
    )

    icon_chars = {
        "Perfect Orb of Transmutation": "T",
        "Perfect Orb of Augmentation": "+",
        "Perfect Regal Orb": "R",
        "Perfect Chaos Orb": "C",
        "Perfect Exalted Orb": "E",
        "Orb of Annulment": "-",
        "Divine Orb": "D",
        "Fracturing Orb": "F",
        "Omen of Whittling": "W",
        "Artificer's Orb": "A",
        "Blacksmith's Whetstone": "Q",
        "Vaal Blacksmith's Infuser": "V",
        "Omen of Dextral Coronation": "DC",
        "Omen of Dextral Erasure": "DE",
        "Omen of Dextral Annulment": "DA",
        "Omen of Dextral Exaltation": "DX",
        "Omen of Sinistral Coronation": "SC",
        "Omen of Sinistral Erasure": "SE",
        "Omen of Sinistral Annulment": "SA",
        "Omen of Sinistral Exaltation": "SX",
        "Omen of Greater Exaltation": "GE",
        "Omen of Greater Annulment": "GA",
        "Omen of Abyssal Echoes": "AE",
        "Omen of Sanctification": "OS",
        "Hinekora's Lock": "HL",
    }
    icon = icon_chars.get(orb_name, "?")
    gothic_font = get_font("small")
    icon_surf = gothic_font.render(icon, True, TEXT_BRIGHT)
    icon_rect = icon_surf.get_rect(center=(cx, cy))
    surface.blit(icon_surf, icon_rect)



