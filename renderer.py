import pygame
import math
import os
import random
from phases.base_phases import ORB_COLORS
from icon_loader import get_orb_icon
import modref

WIDTH, HEIGHT = 1280, 800
FONT_SCALE = 1.0
MIN_W, MIN_H = 960, 600
PANEL_LEFT = 320
PANEL_RIGHT_W = 280
PANEL_CENTER_X = PANEL_LEFT
PANEL_CENTER_W = WIDTH - PANEL_LEFT - PANEL_RIGHT_W

FONT_SIZES_BASE = {
    "tiny": 12,
    "small": 14,
    "medium": 17,
    "large": 22,
    "huge": 28,
    "title": 34,
    "header": 20,
}
FONT_SIZES = dict(FONT_SIZES_BASE)


def _s(n):
    return int(n * FONT_SCALE)


def update_layout(w, h):
    global WIDTH, HEIGHT, PANEL_CENTER_X, PANEL_CENTER_W, FONT_SCALE
    global PANEL_LEFT, PANEL_RIGHT_W, FONT_SIZES
    WIDTH = max(w, MIN_W)
    HEIGHT = max(h, MIN_H)
    FONT_SCALE = min(WIDTH / 1280.0, HEIGHT / 800.0)
    FONT_SCALE = max(0.65, min(2.0, FONT_SCALE))
    for name, base_size in FONT_SIZES_BASE.items():
        FONT_SIZES[name] = max(8, int(base_size * FONT_SCALE))
    PANEL_LEFT = _s(320)
    PANEL_RIGHT_W = _s(280)
    PANEL_CENTER_X = PANEL_LEFT
    PANEL_CENTER_W = WIDTH - PANEL_LEFT - PANEL_RIGHT_W
    init_fonts()


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

fonts = {}

_particles = []


# =============================================================================
#  Font system
# =============================================================================

def init_fonts():
    global fonts
    pygame.font.init()
    from resource_path import resource_path
    font_path = resource_path(os.path.join("assets", "fonts", "gothic.ttf"))
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
        y_off += font.get_height() + _s(2)


def draw_rect(surface, rect, color, border=0, radius=0):
    if radius > 0:
        pygame.draw.rect(surface, color, rect, border, border_radius=radius)
    else:
        pygame.draw.rect(surface, color, rect, border)


def draw_panel(surface, x, y, w, h, header_text=""):
    draw_rect(surface, (x, y, w, h), BG_PANEL)
    draw_rect(surface, (x, y, w, h), BORDER_GOLD_DIM, border=1)
    if header_text:
        header_h = _s(28)
        draw_rect(surface, (x, y, w, header_h), BG_HEADER)
        draw_rect(surface, (x, y, w, header_h), BORDER_GOLD_DIM, border=1)
        draw_text(surface, header_text, x + _s(8), y + _s(5), TEXT_GOLD, "small")


# =============================================================================
#  Runic border decorations
# =============================================================================

def draw_runic_border(surface, x, y, w, h):
    half = _s(7)
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

    diamond(x + _s(12), y + _s(12), half)
    cross(x + _s(24), y + _s(12), half - 1)
    diamond(x + _s(w) - _s(12), y + _s(12), half)
    cross(x + _s(w) - _s(24), y + _s(12), half - 1)
    diamond(x + _s(12), y + _s(h) - _s(12), half)
    cross(x + _s(24), y + _s(h) - _s(12), half - 1)
    diamond(x + _s(w) - _s(12), y + _s(h) - _s(12), half)
    cross(x + _s(w) - _s(24), y + _s(h) - _s(12), half - 1)


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

    grid_sz = _s(60)
    for i in range(0, WIDTH, grid_sz):
        for j in range(0, HEIGHT, grid_sz):
            shade = 12 + int(
                3 * math.sin(i * 0.01 + tick * 0.001 + j * 0.005)
            )
            shade = max(8, min(18, shade))
            c = (shade, shade // 3, shade // 3)
            pygame.draw.rect(surface, c, (i, j, grid_sz - 2, grid_sz - 2), width=1)

    for i in range(6):
        angle = tick * 0.0003 + i * 1.047
        rx = WIDTH // 2 + int(_s(300) * math.cos(angle))
        ry = HEIGHT // 2 + int(_s(200) * math.sin(angle * 0.7))
        for ring in range(3):
            r = _s(40) + ring * _s(25)
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
        _s(48),
        TEXT_GOLD,
        "title",
        centered=True,
    )
    draw_text(
        surface,
        "MIRROR-TIER CRAFTING GUIDE",
        header_x,
        _s(92),
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
    title_y = _s(30)
    subtitle_y = _s(66)
    draw_text(surface, "CHOOSE  YOUR  CRAFT", cx, title_y, TEXT_GOLD, "huge", centered=True)
    draw_text(
        surface,
        "Select an item type to begin your journey toward mirror-tier perfection.",
        cx, subtitle_y, TEXT_DIM, "tiny", centered=True,
    )

    cat_names = list(categories.keys())
    margin = _s(40)
    spacing = _s(16)
    panel_w = (WIDTH - margin * 2 - spacing * (len(cat_names) - 1)) // len(cat_names)

    subtype_items = {}
    subtype_row_y = subtitle_y + _s(24)
    subtype_row_h = _s(36)
    has_subtype_row = selected_category is not None

    panel_y = subtype_row_y + subtype_row_h + _s(12) if has_subtype_row else subtitle_y + _s(34)
    panel_h = min(_s(530), HEIGHT - panel_y - _s(80))
    panel_x = margin

    if has_subtype_row:
        cat = categories.get(selected_category, {})
        sub_types = cat.get("sub_types", [])
        total_st = len(sub_types)
        if total_st > 0:
            row_width = WIDTH - margin * 2
            item_spacing = _s(8)
            max_item_w = _s(150)
            usable = row_width - item_spacing * (total_st - 1)
            st_item_w = min(max_item_w, usable // total_st)
            total_row_w = st_item_w * total_st + item_spacing * (total_st - 1)
            st_start_x = cx - total_row_w // 2

            label_y = subtype_row_y - _s(16)
            draw_text(surface, "\u25BC  Select sub-type:", cx, label_y, TEXT_GOLD, "small", centered=True)

            for sti, st in enumerate(sub_types):
                sx = st_start_x + sti * (st_item_w + item_spacing)
                sy = subtype_row_y
                st_rect = pygame.Rect(sx, sy, st_item_w, subtype_row_h)

                is_selected_sub = selected_subtype == st
                if is_selected_sub:
                    draw_rect(surface, st_rect, (30, 10, 10), radius=4)
                    draw_rect(surface, st_rect, BORDER_GOLD, border=2, radius=4)
                    st_color = TEXT_BRIGHT
                else:
                    draw_rect(surface, st_rect, (15, 6, 6), radius=3)
                    draw_rect(surface, st_rect, BORDER_GOLD_DIM, border=1, radius=3)
                    st_color = TEXT_WHITE

                st_font = get_font("tiny")
                st_text = st
                tw = st_font.size(st_text)[0]
                draw_text(surface, st_text, sx + st_item_w // 2, sy + _s(9), st_color, "tiny", centered=True)
                subtype_items[st] = st_rect

    category_panels = {}
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

        header_h = _s(28)
        if is_selected_cat:
            draw_rect(surface, (bx, by, bw, bh), BORDER_GOLD, border=2)
            draw_rect(surface, (bx, by, bw, header_h), BORDER_GOLD, border=2)

        desc = cat.get("description", "")
        if desc:
            desc_font = get_font("tiny")
            words = desc.split(" ")
            lines = []
            line = ""
            for word in words:
                test = line + (" " if line else "") + word
                if desc_font.size(test)[0] < bw - _s(16):
                    line = test
                else:
                    lines.append(line)
                    line = word
            if line:
                lines.append(line)
            desc_y = by + _s(36)
            max_desc_y = min(by + _s(80), by + bh - _s(20))
            line_h = desc_font.get_height() + 1
            for i, line in enumerate(lines):
                if desc_y + line_h > max_desc_y:
                    break
                draw_text(surface, line, bx + _s(8), desc_y, TEXT_DIM, "tiny")
                desc_y += line_h

        category_panels[cat_name] = pygame.Rect(bx, by, bw, bh)
        panel_x += panel_w + spacing

    if selected_category and selected_subtype:
        btn_w = _s(280)
        btn_h = _s(44)
        btn_x = cx - btn_w // 2
        btn_y = HEIGHT - _s(70)
        draw_rect(surface, (btn_x, btn_y, btn_w, btn_h), (40, 90, 30), radius=6)
        draw_rect(surface, (btn_x, btn_y, btn_w, btn_h), GREEN_GLOW, border=2, radius=6)
        draw_text(
            surface, "BEGIN  CRAFT",
            btn_x + btn_w // 2, btn_y + _s(10), TEXT_BRIGHT, "large", centered=True,
        )
        begin_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

    if selected_category and selected_subtype:
        text_y = btn_y + btn_h + _s(6)
        draw_text(surface, "Press ENTER or click BEGIN CRAFT to start", cx, text_y, GREEN_GLOW, "tiny", centered=True)
    elif selected_category:
        bot_y = HEIGHT - _s(24)
        draw_text(surface, "Now select a sub-type above \u2191", cx, bot_y, TEXT_GOLD, "tiny", centered=True)
    else:
        bot_y = HEIGHT - _s(24)
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
    x = _s(4)
    y = _s(4)
    w = PANEL_LEFT - _s(8)
    draw_panel(surface, x, y, w, HEIGHT - _s(8), " Crafting Phases ")
    draw_runic_border(surface, x, y, w, HEIGHT - _s(8))
    item_h = _s(42)
    start_y = y + _s(34)
    view_h = HEIGHT - _s(50)
    visible_max = view_h // item_h

    for i in range(min(len(phases), visible_max)):
        iy = start_y + i * item_h

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
            draw_rect(surface, (x + _s(2), iy, w - _s(4), item_h), (28, 8, 8))
            draw_rect(
                surface, (x + _s(2), iy, w - _s(4), item_h), BORDER_GOLD, border=1
            )
        elif is_done:
            draw_rect(
                surface, (x + _s(2), iy, w - _s(4), item_h), (20, 50, 20), radius=3
            )

        color = TEXT_GOLD if is_current else (
            GREEN_GLOW if is_done else TEXT_DIM
        )
        draw_text(
            surface,
            f"P{pnum}: {pname}",
            x + _s(10),
            iy + _s(2),
            color,
            "tiny",
        )

        bar_x = x + _s(10)
        bar_y = iy + item_h - _s(6)
        bar_w = w - _s(20)
        bar_h = _s(3)
        draw_rect(surface, (bar_x, bar_y, bar_w, bar_h), (18, 14, 14))
        if total_steps > 0:
            fill_w = int(bar_w * done_steps / total_steps)
            fill_c = GREEN_GLOW if is_done else BORDER_GOLD
            draw_rect(surface, (bar_x, bar_y, fill_w, bar_h), fill_c)

    if len(phases) > visible_max:
        draw_text(
            surface,
            f"  +{len(phases) - visible_max} more phases offline",
            x + _s(10),
            start_y + visible_max * item_h + _s(2),
            TEXT_DIM,
            "tiny",
        )

    reset_btn_w = w - _s(20)
    reset_btn_h = _s(32)
    reset_btn_x = x + _s(10)
    reset_btn_y = HEIGHT - _s(62)
    draw_rect(surface, (reset_btn_x, reset_btn_y, reset_btn_w, reset_btn_h), (50, 15, 10), radius=4)
    draw_rect(surface, (reset_btn_x, reset_btn_y, reset_btn_w, reset_btn_h), BORDER_GOLD, border=2, radius=4)
    draw_text(surface, "RESET", reset_btn_x + reset_btn_w // 2, reset_btn_y + _s(6), TEXT_BRIGHT, "medium", centered=True)

    return {"reset_btn": pygame.Rect(reset_btn_x, reset_btn_y, reset_btn_w, reset_btn_h)}


# =============================================================================
#  Step panel (center)
# =============================================================================

def draw_step_panel(
    surface, step, step_index, phase_steps, completed_steps, pending_choice=None
):
    x = PANEL_LEFT + _s(4)
    y = _s(4)
    w = PANEL_CENTER_W - _s(8)
    step_h = _s(30)
    steps_bar_h = step_h + _s(6)
    head_h = _s(28)

    draw_panel(surface, x, y, w, steps_bar_h, "")
    draw_rect(surface, (x, y, w, steps_bar_h), BORDER_GOLD_DIM, border=1)

    n_steps = max(len(phase_steps), 1)
    for i, s in enumerate(phase_steps):
        sx = x + _s(4) + i * ((w - _s(8)) // n_steps)
        sw = (w - _s(8)) // n_steps - _s(4)
        sy = y + _s(2)
        sh = steps_bar_h - _s(4)

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
        tiny_f = get_font("tiny")
        step_text = f"Step {short_id}"
        avail_text_w = sw - _s(8)
        if tiny_f.size(step_text)[0] >= avail_text_w:
            step_text = _truncate_to_fit(step_text, tiny_f, avail_text_w)
        draw_text(
            surface,
            step_text,
            sx + _s(4),
            sy + _s(6),
            color,
            "tiny",
        )

    content_y = y + steps_bar_h + _s(4)
    content_h = HEIGHT - content_y - _s(4)
    draw_panel(surface, x, content_y, w, content_h, f" {step['title']} ")

    desc_y = content_y + _s(32)
    action_bar_h = _s(60)
    alt_header_h = _s(28)
    alternatives = step.get("alternatives", None)
    step_id = step["id"]
    has_alternatives = alternatives and step_id not in completed_steps

    if has_alternatives:
        max_desc_bottom = content_y + content_h - action_bar_h - _s(100)
    else:
        max_desc_bottom = content_y + content_h - action_bar_h - _s(20)

    font_s = get_font("small")
    max_desc_w = w - _s(24)
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
    line_h_s = avatar_font.get_height() + _s(2)
    fit_lines = max(1, int((max_desc_bottom - desc_y) / line_h_s))
    use_tiny = len(desc_lines) > fit_lines
    if use_tiny:
        avatar_font = get_font("tiny")
        line_h_s = avatar_font.get_height() + _s(2)
        fit_lines = max(1, int((max_desc_bottom - desc_y) / line_h_s))

    rendered_lines = 0
    for i in range(min(len(desc_lines), fit_lines)):
        line = desc_lines[i]
        if i == fit_lines - 1 and i < len(desc_lines) - 1:
            line = _truncate_to_fit(line.rstrip() + " [...]", avatar_font, max_desc_w)
        size_name = "small" if not use_tiny else "tiny"
        draw_text(surface, line, x + _s(12), desc_y, TEXT_WHITE if not use_tiny else TEXT_DIM, size_name)
        desc_y += line_h_s
        rendered_lines += 1

    if rendered_lines < len(desc_lines):
        remaining = len(desc_lines) - rendered_lines
        draw_text(surface, f"[+{remaining} more lines]", x + _s(12), desc_y, TEXT_DIM, "tiny")
        desc_y += get_font("tiny").get_height() + _s(2)

    desc_bottom = desc_y

    choice_btns = []
    confirm_btn = None

    alt_y = desc_bottom + _s(10)

    if has_alternatives:
        max_alt_bottom = content_y + content_h - action_bar_h - _s(10)
        alt_y_needed = alt_y
        for alt_idx, alt in enumerate(alternatives):
            btn_h = _s(44)
            if alt_y_needed + btn_h > max_alt_bottom:
                break
            alt_y_needed += btn_h + _s(4)

        draw_rect(surface, (x + _s(8), alt_y, w - _s(16), 1), BORDER_GOLD_DIM)
        alt_y += _s(6)
        draw_text(surface, "Choose your approach:", x + _s(12), alt_y, TEXT_GOLD, "small")
        alt_y += get_font("small").get_height() + _s(6)

        drawn_alternatives = 0
        for alt_idx, alt in enumerate(alternatives):
            btn_x = x + _s(20)
            btn_w_val = w - _s(40)
            btn_h = _s(44)
            is_sel = pending_choice == alt_idx

            if alt_y + btn_h > max_alt_bottom:
                break

            risk_color = {
                "low": GREEN_GLOW,
                "very low": GREEN_GLOW,
                "medium": ORANGE_GLOW,
                "high": RED_GLOW,
            }.get(alt.get("risk", "medium"), ORANGE_GLOW)

            if is_sel:
                draw_rect(surface, (btn_x, alt_y, btn_w_val, btn_h), (30, 10, 10), radius=4)
                draw_rect(surface, (btn_x, alt_y, btn_w_val, btn_h), BORDER_GOLD, border=2, radius=4)
            else:
                draw_rect(surface, (btn_x, alt_y, btn_w_val, btn_h), BG_HEADER, radius=4)
                draw_rect(surface, (btn_x, alt_y, btn_w_val, btn_h), BORDER_GOLD_DIM, border=1, radius=4)

            label_text = alt.get("label", f"Option {alt_idx + 1}")
            cost_text = alt.get("cost", "")
            risk_text = alt.get("risk", "medium")

            draw_text(surface, label_text, btn_x + _s(8), alt_y + _s(4), TEXT_WHITE if is_sel else TEXT_GOLD, "tiny")
            draw_text(
                surface, f"Cost: {cost_text}   Risk: {risk_text}",
                btn_x + _s(8), alt_y + _s(24), risk_color, "tiny",
            )

            r = pygame.Rect(btn_x, alt_y, btn_w_val, btn_h)
            choice_btns.append(r)
            alt_y += btn_h + _s(4)
            drawn_alternatives += 1

        if drawn_alternatives < len(alternatives):
            remaining_alts = len(alternatives) - drawn_alternatives
            draw_text(
                surface,
                f"  [+{remaining_alts} more choices]",
                x + _s(12),
                alt_y,
                TEXT_DIM,
                "tiny",
            )
            alt_y += get_font("tiny").get_height() + _s(4)

    is_done_step = step_id in completed_steps

    action_y = content_y + content_h - action_bar_h
    draw_rect(surface, (x + _s(8), action_y, w - _s(16), _s(40)), BG_HEADER)
    draw_rect(
        surface, (x + _s(8), action_y, w - _s(16), _s(40)), BORDER_GOLD_DIM, border=1
    )
    draw_text(
        surface,
        f"ACTION: {step['action']}",
        x + _s(16),
        action_y + _s(6),
        TEXT_GOLD,
        "medium",
    )

    back_btn_w = _s(100)
    btn_w = _s(220)
    btn_h = _s(36)
    btn_x = x + w - btn_w - _s(16)
    btn_y = action_y + _s(2)
    back_btn_x = btn_x - back_btn_w - _s(8)

    draw_rect(
        surface, (back_btn_x, btn_y, back_btn_w, btn_h), (20, 10, 30), radius=4
    )
    draw_rect(
        surface,
        (back_btn_x, btn_y, back_btn_w, btn_h),
        BORDER_GOLD_DIM,
        border=2,
        radius=4,
    )
    draw_text(
        surface,
        "Back",
        back_btn_x + back_btn_w // 2,
        btn_y + _s(8),
        TEXT_BRIGHT,
        "medium",
        centered=True,
    )
    back_btn = pygame.Rect(back_btn_x, btn_y, back_btn_w, btn_h)

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
            btn_y + _s(8),
            TEXT_BRIGHT,
            "medium",
            centered=True,
        )
    else:
        if alternatives and pending_choice is not None:
            clamped = min(max(pending_choice, 0), len(alternatives) - 1)
            if clamped != pending_choice:
                pending_choice = clamped
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
            btn_y + _s(8),
            TEXT_BRIGHT,
            "medium",
            centered=True,
        )

    confirm_btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h) if not is_done_step else None

    return {
        "confirm_btn": confirm_btn,
        "choice_btns": choice_btns,
        "back_btn": back_btn,
    }


# =============================================================================
#  Price panel (right)
# =============================================================================

def draw_price_panel(surface, step, prices_available_flag, running_total=0.0,
                    category=None, mod_search_query="", mod_search_active=False,
                    item_type=None, mod_search_scroll=0):
    x = WIDTH - PANEL_RIGHT_W + _s(4)
    y = _s(4)
    w = PANEL_RIGHT_W - _s(8)
    draw_panel(surface, x, y, w, HEIGHT - _s(8), " Marketplace ")
    draw_runic_border(surface, x, y, w, HEIGHT - _s(8))

    from prices import get_price, price_source

    source_label = price_source()
    source_color = GREEN_GLOW if source_label == "live" else TEXT_DIM
    source_text = f"Source: {source_label}"
    source_font = get_font("tiny")
    avail_w = w - _s(20)
    if source_font.size(source_text)[0] >= avail_w:
        source_text = _truncate_to_fit(source_text, source_font, avail_w)
    text_w = source_font.size(source_text)[0]
    draw_text(
        surface,
        source_text,
        x + w - _s(8) - text_w,
        y + _s(6),
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
        draw_text(surface, "(No orbs in this step)", x + _s(12), y + _s(40), TEXT_DIM, "tiny")
        if running_total > 0:
            _draw_budget_tier(surface, x, y, w, running_total, tier_thresholds)
        mod_rect, scroll_used, total = draw_mod_search(surface, x, y, w, mod_search_query, mod_search_active, category, item_type, mod_search_scroll)
        return {"mod_search_rect": mod_rect, "mod_search_scroll": scroll_used, "mod_search_total": total}

    orb_y = y + _s(40)
    orb_inc = _s(50)
    max_orb_y = HEIGHT - _s(230)
    orb_icon_sz = _s(18)
    pad_left = _s(30)
    orb_name_x = x + _s(56)
    price_x = x + _s(60)

    orbs_shown = 0
    total_orbs = len(orbs)

    for orb_name in orbs:
        if orb_y > max_orb_y:
            break
        draw_orb(surface, x + pad_left, orb_y + _s(14), orb_icon_sz, orb_name)
        draw_text(surface, orb_name, orb_name_x, orb_y + _s(6), TEXT_WHITE, "tiny")

        p = get_price(orb_name)
        if p:
            chaos = p["chaos"]
            divine = p["divine"]
            draw_text(
                surface,
                f"{chaos:.1f} chaos  |  {divine:.4f} div",
                price_x,
                orb_y + _s(22),
                TEXT_GOLD,
                "tiny",
            )
        else:
            draw_text(
                surface,
                "price not found",
                price_x,
                orb_y + _s(22),
                TEXT_DIM,
                "tiny",
            )
        orb_y += orb_inc
        orbs_shown += 1

    if orbs_shown < total_orbs:
        draw_text(
            surface,
            f"... and {total_orbs - orbs_shown} more orb types",
            x + _s(12),
            orb_y + _s(4),
            TEXT_DIM,
            "tiny",
        )
        orb_y += get_font("tiny").get_height() + _s(8)

    if len(orbs) > 1:
        draw_rect(
            surface, (x + _s(8), orb_y, w - _s(16), 1), BORDER_GOLD_DIM, border=1
        )
        step_total_chaos = 0
        for orb_name in orbs:
            p = get_price(orb_name)
            if p:
                step_total_chaos += p["chaos"]
        divine_price = 0
        from prices import CACHED_PRICES
        dv = CACHED_PRICES.get("Divine Orb", {}).get("chaos", 0)
        if dv > 0:
            divine_price = step_total_chaos / dv
        draw_text(
            surface,
            f"Step Orb Total: {step_total_chaos:.1f}c = {divine_price:.3f} div",
            x + _s(12),
            orb_y + _s(8),
            TEXT_GOLD,
            "tiny",
        )

    if running_total > 0:
        _draw_budget_tier(surface, x, y, w, running_total, tier_thresholds)

    mod_rect, scroll_used, total = draw_mod_search(surface, x, y, w, mod_search_query, mod_search_active, category, item_type, mod_search_scroll)
    return {"mod_search_rect": mod_rect, "mod_search_scroll": scroll_used, "mod_search_total": total}


def _truncate_to_fit(text, font, max_w):
    while len(text) > 4 and font.size(text)[0] >= max_w:
        text = text[:-4].rstrip() + "..."
    return text


def _draw_budget_tier(surface, x, y, w, running_total, tier_thresholds=None):
    tot_y = _draw_budget_tier_y()
    panel_bottom = HEIGHT - _s(8)
    draw_rect(surface, (x + _s(8), tot_y - _s(4), w - _s(16), 1), BORDER_GOLD)

    if tier_thresholds is None:
        from phases import default_tier_thresholds
        tier_thresholds = default_tier_thresholds()

    t = tier_thresholds[0] if tier_thresholds else {"label": "Mirror Craft", "description": "", "color": "red"}
    tier_label = t["label"]
    tier_desc = t.get("description", "")

    draw_text(surface, f"Est. Total Cost: {running_total:.1f} div", x + _s(12), tot_y + _s(4), TEXT_GOLD, "small")
    draw_text(surface, f"Tier: {tier_label}", x + _s(12), tot_y + _s(24), RED_GLOW, "tiny")
    if tier_desc:
        y_desc = tot_y + _s(44)
        font_t = get_font("tiny")
        max_w = w - _s(30)
        line_h = font_t.get_height() + _s(2)
        avail_h = panel_bottom - y_desc - _s(4)
        max_lines = max(1, avail_h // line_h)
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
            draw_text(surface, line, x + _s(12), y_desc, TEXT_DIM, "tiny")
            y_desc += line_h


# =============================================================================
#  Mod search widget (right panel, between orb prices and budget tier)
# =============================================================================

def draw_mod_search(surface, panel_x, panel_y, panel_w, query, active, category=None, item_type=None, scroll_offset=0):
    inp_y = HEIGHT - _s(222)
    inp_h = _s(22)
    rect = pygame.Rect(panel_x + _s(8), inp_y, panel_w - _s(16), inp_h)

    draw_rect(surface, rect, BG_HEADER, radius=3)
    border_color = BORDER_GOLD if active else BORDER_GOLD_DIM
    draw_rect(surface, rect, border_color, border=1, radius=3)

    placeholder = "Search prefixes & suffixes..."
    display = query if query else placeholder
    color = TEXT_GOLD if query else TEXT_DIM
    padx = _s(6)
    pygame.draw.rect(surface, BG_PANEL, (rect.x + 1, rect.y + 1, rect.w - 2, rect.h - 2))

    font_t = get_font("tiny")
    text_surf = font_t.render(display, True, color)
    surface.blit(text_surf, (rect.x + padx, rect.y + (inp_h - text_surf.get_height()) // 2))

    if active and (pygame.time.get_ticks() // 500) % 2 == 0:
        cursor_x = rect.x + padx + (font_t.size(display)[0] if query else 0)
        draw_rect(surface, (cursor_x, rect.y + _s(4), 1, inp_h - _s(8)), TEXT_GOLD)

    if not query and not active:
        draw_text(
            surface, "Press / to search",
            panel_x + panel_w // 2, rect.y - _s(14), TEXT_DIM, "tiny", centered=True,
        )

    if not query and not active:
        return rect, 0, 0

    if query:
        results = sorted(modref.search_mods(query, category, item_type=item_type), key=lambda m: m["name"].lower())
    elif item_type:
        results = sorted(modref.mods_for_item_type(item_type), key=lambda m: m["name"].lower())
    elif category:
        results = sorted(modref.all_mods_for_category(category), key=lambda m: m["name"].lower())
    else:
        results = sorted(modref._MODS, key=lambda m: m["name"].lower())

    if not results:
        return rect, 0, 0

    res_y = rect.y + inp_h + _s(4)
    max_res_h = _draw_budget_tier_y() - res_y - _s(8)
    font_t = get_font("tiny")
    line_h = font_t.get_height() + _s(3)
    max_lines = max(0, max_res_h // line_h)

    from math import ceil
    total_results = len(results)
    max_offset = max(0, total_results - max_lines)
    scroll_offset = max(0, min(scroll_offset, max_offset))

    if scroll_offset > 0:
        draw_text(
            surface,
            f"\u25b2  {scroll_offset} more above",
            panel_x + _s(12), res_y, TEXT_DIM, "tiny",
        )
        res_y += line_h
        max_lines -= 1

    shown = 0
    for i in range(scroll_offset, min(total_results, scroll_offset + max_lines)):
        mod = results[i]

        badge_label, badge_color = modref.get_affix_badge(mod)
        badge_w = _s(52)
        badge_h = line_h
        badge_rect = pygame.Rect(panel_x + _s(12), res_y, badge_w, badge_h)
        draw_rect(surface, badge_rect, badge_color, radius=2)

        badge_font = get_font("tiny")
        badge_surf = badge_font.render(badge_label, True, (240, 240, 240))
        surface.blit(
            badge_surf,
            (
                badge_rect.x + (badge_w - badge_surf.get_width()) // 2,
                badge_rect.y + (badge_h - badge_surf.get_height()) // 2,
            ),
        )

        name_x = badge_rect.x + badge_w + _s(6)
        max_name_w = panel_w - _s(24) - badge_w - _s(6)
        name_text = mod["name"]
        if font_t.size(name_text)[0] > max_name_w:
            name_text = _truncate_to_fit(name_text, font_t, max_name_w)
        draw_text(surface, name_text, name_x, res_y, TEXT_WHITE, "tiny")

        res_y += line_h
        shown += 1

    remaining_below = total_results - scroll_offset - shown
    if remaining_below > 0:
        draw_text(
            surface,
            f"\u25bc  {remaining_below} more below",
            panel_x + _s(12), res_y, TEXT_DIM, "tiny",
        )

    return rect, scroll_offset, total_results


def _draw_budget_tier_y():
    return HEIGHT - _s(100)


# =============================================================================
#  Save / load screen
# =============================================================================

def draw_save_load_screen(surface, tick, saves_list, mode="load", selected_save=-1):
    update_particles()
    draw_particles(surface)

    title_text = "RESUME  CRAFT" if mode == "load" else "SAVE  YOUR  CRAFT"
    draw_text(surface, title_text, WIDTH // 2, _s(28), TEXT_GOLD, "huge", centered=True)
    draw_text(
        surface,
        "Select a save slot and press ENTER, or start a New Craft.",
        WIDTH // 2, _s(64), TEXT_DIM, "tiny", centered=True,
    )

    panel_x = _s(140)
    panel_w = WIDTH - _s(280)
    panel_h = HEIGHT - _s(130)
    panel_y = _s(90)
    draw_panel(surface, panel_x, panel_y, panel_w, panel_h, " Save Slots ")
    draw_runic_border(surface, panel_x, panel_y, panel_w, panel_h)

    small_font = get_font("small")
    tiny_font = get_font("tiny")
    slot_pad_top = _s(4)
    slot_pad_bottom = _s(4)
    line1_h = small_font.get_height()
    line2_h = tiny_font.get_height()
    slot_h = line1_h + line2_h + slot_pad_top + slot_pad_bottom + _s(12)
    slot_h = max(slot_h, _s(48))

    slot_y = panel_y + _s(32)
    slot_rects = []
    selected_index = selected_save

    if not saves_list:
        draw_text(
            surface,
            "(No saves found)",
            panel_x + panel_w // 2,
            panel_y + panel_h // 2 - _s(20),
            TEXT_DIM,
            "medium",
            centered=True,
        )
    else:
        bottom_limit = panel_y + panel_h - _s(60)
        for si, save in enumerate(saves_list):
            if slot_y + slot_h > bottom_limit:
                draw_text(
                    surface,
                    f"[+{len(saves_list) - si} more saves offline]",
                    panel_x + _s(8),
                    slot_y + _s(4),
                    TEXT_DIM,
                    "tiny",
                )
                break
            sr = pygame.Rect(panel_x + _s(8), slot_y, panel_w - _s(16), slot_h - _s(4))

            draw_rect(surface, sr, BG_HEADER, radius=3)
            draw_rect(surface, sr, BORDER_GOLD_DIM, border=1, radius=3)

            name = save.get("display_name", save.get("filename", "???"))
            date = save.get("date", "")[:19].replace("T", " ")
            cat = save.get("category", "")
            sub = save.get("sub_type", "")
            phase = save.get("phase", 0)
            step = save.get("step", 0)
            done = save.get("steps_complete", 0)

            line1_y = sr.y + slot_pad_top
            line2_y = line1_y + line1_h + _s(2)

            draw_text(surface, name, sr.x + _s(10), line1_y, TEXT_GOLD, "small")

            meta_text = f"{date}  |  {cat} / {sub}  |  Phase {phase+1} Step {step+1}  |  {done} steps done"
            avail_w = sr.w - _s(20)
            if tiny_font.size(meta_text)[0] >= avail_w:
                meta_text = _truncate_to_fit(meta_text, tiny_font, avail_w)
            draw_text(surface, meta_text, sr.x + _s(10), line2_y, TEXT_DIM, "tiny")

            slot_rects.append(sr)
            slot_y += slot_h

    new_btn_w = _s(200)
    new_btn_h = _s(36)
    new_btn_x = panel_x + _s(20)
    new_btn_y = HEIGHT - _s(52)
    draw_rect(surface, (new_btn_x, new_btn_y, new_btn_w, new_btn_h), (40, 100, 40), radius=4)
    draw_rect(surface, (new_btn_x, new_btn_y, new_btn_w, new_btn_h), GREEN_GLOW, border=2, radius=4)
    draw_text(
        surface, "NEW  CRAFT",
        new_btn_x + new_btn_w // 2, new_btn_y + _s(8), TEXT_BRIGHT, "medium", centered=True,
    )

    del_btn_x = new_btn_x + new_btn_w + _s(16)
    del_btn_w = _s(160)
    del_btn_h = _s(36)
    if saves_list and selected_index >= 0:
        draw_rect(surface, (del_btn_x, new_btn_y, del_btn_w, del_btn_h), (50, 15, 10), radius=4)
    else:
        draw_rect(surface, (del_btn_x, new_btn_y, del_btn_w, del_btn_h), (20, 10, 10), radius=4)
    draw_rect(surface, (del_btn_x, new_btn_y, del_btn_w, del_btn_h), BORDER_GOLD_DIM, border=1, radius=4)
    draw_text(
        surface, "DELETE",
        del_btn_x + del_btn_w // 2, new_btn_y + _s(8), TEXT_DIM, "small", centered=True,
    )

    esc_y = HEIGHT - _s(24)
    instruct = "[ENTER] Confirm   [ESC] Cancel   [Del] Delete selected"
    if mode == "save":
        instruct = "[ENTER] Save   [ESC] Cancel   [Del] Delete selected"
    tiny_f = get_font("tiny")
    if tiny_f.size(instruct)[0] >= WIDTH - _s(40):
        instruct = _truncate_to_fit(instruct, tiny_f, WIDTH - _s(40))
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
        cy - _s(60),
        TEXT_BRIGHT,
        "title",
        centered=True,
    )

    if sub_type:
        line = f"Your 6x T1 mirror-tier {sub_type} is ready for service."
    else:
        line = f"Your 6x T1 mirror-tier {category.replace('a ','')} is ready for service."
    draw_text(surface, line, cx, cy + _s(4), TEXT_GOLD, "medium", centered=True)

    draw_text(
        surface,
        "GG, Exile.",
        cx,
        cy + _s(44),
        TEXT_WHITE,
        "large",
        centered=True,
    )
    draw_text(
        surface,
        "[ESC] Exit   [R] Start Over   [S] Save   [L] Load",
        cx,
        cy + _s(90),
        TEXT_DIM,
        "small",
        centered=True,
    )

    for i in range(12):
        angle = pygame.time.get_ticks() * 0.001 + i * 0.523
        rx = cx + int(_s(250) * math.cos(angle))
        ry = cy + int(_s(120) * math.sin(angle * 1.5))
        r = _s(3) + int(_s(2) * math.sin(pygame.time.get_ticks() * 0.003 + i))
        draw_orb(surface, rx, ry, r, "Divine Orb")


# =============================================================================
#  Orb drawing
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
