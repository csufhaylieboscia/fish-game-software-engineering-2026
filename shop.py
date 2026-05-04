import pygame
import math
import os

# ── Pixel-art colour palette (matches the warm wood/parchment reference) ──────
WOOD_DARK   = (101,  67,  33)
WOOD_MID    = (139,  90,  43)
WOOD_LIGHT  = (188, 143,  87)
WOOD_HILIT  = (210, 170, 110)
PARCH_DARK  = (205, 180, 140)
PARCH_MID   = (225, 200, 160)
PARCH_LIGHT = (240, 218, 182)
PARCH_PAPER = (248, 232, 200)
RED_CORNER  = (180,  40,  40)
BTN_DARK    = ( 50, 130, 160)
BTN_MID     = ( 80, 170, 200)
BTN_LIGHT   = (140, 210, 230)
BTN_TEXT    = (255, 255, 255)
SELL_DARK   = ( 40, 140,  60)
SELL_MID    = ( 70, 180,  90)
SELL_LIGHT  = (130, 220, 150)
NAV_DARK    = ( 80,  60,  30)
NAV_MID     = (120,  90,  45)
NAV_LIGHT   = (160, 120,  60)
TEXT_DARK   = ( 80,  55,  25)
TEXT_MID    = (120,  85,  40)
CLOSE_RED   = (180,  40,  40)
CLOSE_LITE  = (220,  80,  80)
LEAF_DARK   = ( 40, 100,  30)
LEAF_MID    = ( 70, 140,  50)
LEAF_LIGHT  = (110, 180,  70)
BLACK       = (  0,   0,   0)
WHITE       = (255, 255, 255)
SHADOW      = (  0,   0,   0, 80)

# ── Shop item definitions ──────────────────────────────────────────────────────
SHOP_TABS = {
    "SELL": [
        # difficulty 1 - common fish (10 coins)
        {"name": "Goldfish",    "color": (220, 160,  40), "price": 10,  "owned": 0},
        {"name": "Green Fish",  "color": ( 80, 180,  80), "price": 10,  "owned": 0},
        {"name": "Moss Ball",   "color": ( 90, 140,  70), "price": 10,  "owned": 0},
        {"name": "Sea Snail",   "color": (180, 140, 100), "price": 10,  "owned": 0},
        {"name": "Shell",       "color": (230, 200, 150), "price": 10,  "owned": 0},
        # difficulty 2 - uncommon fish (25 coins)
        {"name": "Black Fish",  "color": ( 60,  60,  60), "price": 25,  "owned": 0},
        {"name": "Flat Fish",   "color": (200, 180, 100), "price": 25,  "owned": 0},
        {"name": "Noc",         "color": ( 80,  80, 160), "price": 25,  "owned": 0},
        # difficulty 3 - rare fish (60 coins)
        {"name": "Beta Fish",   "color": (180,  60, 200), "price": 60,  "owned": 0},
        {"name": "Clown Fish",  "color": (220,  90,  30), "price": 60,  "owned": 0},
        {"name": "Plastic Bag", "color": (200, 220, 240), "price": 60,  "owned": 0},
        {"name": "Cal",         "color": ( 60, 160, 200), "price": 60,  "owned": 0},
        {"name": "Jelly",       "color": (200, 150, 220), "price": 60,  "owned": 0},
        # difficulty 4 - epic fish (120 coins)
        {"name": "Axolotl",     "color": (230, 150, 170), "price": 120, "owned": 0},
        {"name": "Octopus",     "color": (160,  80, 160), "price": 120, "owned": 0},
        {"name": "Piranha",     "color": (200,  50,  50), "price": 120, "owned": 0},
        {"name": "Starfish",    "color": (220, 140,  50), "price": 120, "owned": 0},
        {"name": "Hay",         "color": (220, 200,  60), "price": 120, "owned": 0},
        {"name": "Uhh",         "color": (100, 180, 160), "price": 120, "owned": 0},
        # difficulty 5 - legendary fish (300 coins)
        {"name": "Angler",      "color": ( 40,  40,  80), "price": 300, "owned": 0},
    ],
    "RODS & BAIT": [
        {"name": "Basic Rod",   "color": (160, 110,  60), "price": 50,  "owned": 1},
        {"name": "Steel Rod",   "color": (160, 170, 180), "price": 150, "owned": 0},
        {"name": "Magic Rod",   "color": (120,  80, 220), "price": 400, "owned": 0},
        {"name": "Worm Bait",   "color": (150, 100,  60), "price": 15,  "owned": 5},
        {"name": "Shiny Lure",  "color": (200, 200,  60), "price": 40,  "owned": 2},
        {"name": "Magic Bait",  "color": ( 80, 180, 200), "price": 100, "owned": 0},
    ],
    "DECOR": [
        {"name": "Coral",       "color": (220,  90, 110), "price": 30,  "owned": 2},
        {"name": "Treasure Chest","color":(160, 130,  60),"price": 80,  "owned": 0},
        {"name": "Sea Castle",  "color": (140, 140, 200), "price": 200, "owned": 0},
        {"name": "Seaweed",     "color": ( 60, 160,  80), "price": 20,  "owned": 3},
        {"name": "Shipwreck",   "color": (110,  90,  70), "price": 350, "owned": 0},
        {"name": "Pearl",       "color": (230, 230, 240), "price": 500, "owned": 0},
    ],
}

ITEMS_PER_PAGE = 4


def draw_pixel_rect(surf, color, rect, border=2, shadow=True):
    """Filled rect with a darker pixel border."""
    if shadow:
        shadow_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width, rect.height)
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 60))
        surf.blit(s, shadow_rect.topleft)
    pygame.draw.rect(surf, color, rect)
    dark = tuple(max(0, c - 50) for c in color[:3])
    pygame.draw.rect(surf, dark, rect, border)


def draw_pixel_button(surf, rect, label, font, base_col, light_col, dark_col,
                      text_col=WHITE, hovered=False, pressed=False):
    """Chunky pixel-art style button."""
    col = light_col if hovered else base_col
    if pressed:
        col = dark_col

    # shadow
    s_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width, rect.height)
    shadow_s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    shadow_s.fill((0, 0, 0, 70))
    surf.blit(shadow_s, s_rect.topleft)

    pygame.draw.rect(surf, col, rect, border_radius=4)
    pygame.draw.rect(surf, dark_col, rect, 2, border_radius=4)

    # inner highlight (top-left edge)
    hl = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, 3)
    pygame.draw.rect(surf, light_col, hl, border_radius=2)

    txt = font.render(label, True, text_col)
    surf.blit(txt, txt.get_rect(center=rect.center))


def draw_item_icon(surf, center, color, size=20):
    """Draw a tiny gem-like pixel icon."""
    x, y = center
    r = size // 2

    # hexagon-ish shape
    points = [
        (x,     y - r),
        (x + r, y - r // 2),
        (x + r, y + r // 2),
        (x,     y + r),
        (x - r, y + r // 2),
        (x - r, y - r // 2),
    ]
    pygame.draw.polygon(surf, color, points)
    dark = tuple(max(0, c - 60) for c in color[:3])
    light = tuple(min(255, c + 80) for c in color[:3])
    pygame.draw.polygon(surf, dark, points, 2)
    # shine
    pygame.draw.line(surf, light, (x - r // 2, y - r // 2), (x, y - r + 2), 2)


def draw_leaf(surf, x, y, flip=False):
    """Simple 3-leaf cluster for decoration."""
    for dx, dy, col in [(-8, 0, LEAF_MID), (0, -10, LEAF_LIGHT), (8, 0, LEAF_MID)]:
        cx, cy = (x - dx if flip else x + dx), y + dy
        pygame.draw.circle(surf, col, (cx, cy), 8)
        pygame.draw.circle(surf, LEAF_DARK, (cx, cy), 8, 1)


def draw_wood_plank(surf, rect, horizontal=True):
    """Draw a textured wood plank."""
    pygame.draw.rect(surf, WOOD_MID, rect)
    # grain lines
    if horizontal:
        for i in range(rect.y + 4, rect.bottom - 4, 6):
            pygame.draw.line(surf, WOOD_DARK, (rect.x + 2, i), (rect.right - 2, i), 1)
    else:
        for i in range(rect.x + 4, rect.right - 4, 6):
            pygame.draw.line(surf, WOOD_DARK, (i, rect.y + 2), (i, rect.bottom - 2), 1)
    pygame.draw.rect(surf, WOOD_DARK, rect, 2)
    # highlight
    pygame.draw.line(surf, WOOD_HILIT, (rect.x + 2, rect.y + 2), (rect.right - 2, rect.y + 2), 1)


def draw_shop_panel(surf, panel_rect):
    """Draw the full wood-framed parchment panel."""
    px, py, pw, ph = panel_rect

    # ── parchment background ─────────────────────────────────
    parch = pygame.Rect(px + 18, py + 18, pw - 36, ph - 36)
    pygame.draw.rect(surf, PARCH_PAPER, parch)
    # subtle inner texture lines
    for i in range(parch.y + 8, parch.bottom, 12):
        pygame.draw.line(surf, PARCH_DARK, (parch.x + 6, i), (parch.right - 6, i), 1)
    pygame.draw.rect(surf, PARCH_DARK, parch, 2)

    # ── left & right wood columns ────────────────────────────
    left_col  = pygame.Rect(px,      py + 20, 22, ph - 40)
    right_col = pygame.Rect(px + pw - 22, py + 20, 22, ph - 40)
    draw_wood_plank(surf, left_col,  horizontal=False)
    draw_wood_plank(surf, right_col, horizontal=False)

    # column rivets
    for col_rect in (left_col, right_col):
        for ry in (col_rect.y + 10, col_rect.centery, col_rect.bottom - 10):
            pygame.draw.circle(surf, WOOD_DARK,  (col_rect.centerx, ry), 5)
            pygame.draw.circle(surf, WOOD_HILIT, (col_rect.centerx - 1, ry - 1), 2)

    # ── top & bottom horizontal planks ───────────────────────
    top_plank = pygame.Rect(px + 10, py, pw - 20, 22)
    bot_plank = pygame.Rect(px + 10, py + ph - 22, pw - 20, 22)
    draw_wood_plank(surf, top_plank)
    draw_wood_plank(surf, bot_plank)

    # ── corner brackets ──────────────────────────────────────
    corners = [
        (px + 10, py + 10), (px + pw - 30, py + 10),
        (px + 10, py + ph - 30), (px + pw - 30, py + ph - 30),
    ]
    for cx_, cy_ in corners:
        pygame.draw.rect(surf, WOOD_DARK,  (cx_, cy_, 20, 20))
        pygame.draw.rect(surf, WOOD_HILIT, (cx_ + 2, cy_ + 2, 8, 8))
        pygame.draw.rect(surf, WOOD_DARK,  (cx_, cy_, 20, 20), 2)

    # ── decorative leaves ────────────────────────────────────
    draw_leaf(surf, px + 14,      py + ph // 2)
    draw_leaf(surf, px + pw - 14, py + ph // 2, flip=True)
    draw_leaf(surf, px + pw // 2, py + ph - 10)

    # ── SHOP title sign ──────────────────────────────────────
    sign = pygame.Rect(px + pw // 2 - 48, py - 28, 96, 36)
    draw_wood_plank(surf, sign)
    # sign shadow bolts
    for bx in (sign.x + 6, sign.right - 10):
        pygame.draw.circle(surf, WOOD_DARK, (bx, sign.centery), 3)

def shop_loop(screen, clock, player_coins=200):
    """
    Full pixel-art shop screen.
    Returns None to go back to overworld, or "quit".
    """
    pygame.font.init()

    # Load background image once before the loop
    here = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(here, "assets", "Sprites", "shop_bg.webp")
    screen_w, screen_h = screen.get_size()
    if os.path.exists(bg_path):
        shop_bg = pygame.image.load(bg_path).convert()
        shop_bg = pygame.transform.scale(shop_bg, (screen_w, screen_h))
    else:
        shop_bg = None

    # ── fonts (pixel-style fallbacks) ────────────────────────
    try:
        font_title = pygame.font.SysFont("Courier New", 20, bold=True)
        font_tab   = pygame.font.SysFont("Courier New", 13, bold=True)
        font_item  = pygame.font.SysFont("Courier New", 14, bold=True)
        font_price = pygame.font.SysFont("Courier New", 12, bold=True)
        font_btn   = pygame.font.SysFont("Courier New", 12, bold=True)
        font_nav   = pygame.font.SysFont("Courier New", 13, bold=True)
        font_hint  = pygame.font.SysFont("Courier New", 11)
        font_coins = pygame.font.SysFont("Courier New", 13, bold=True)
    except Exception:
        font_title = font_tab = font_item = font_price = \
            font_btn = font_nav = font_hint = font_coins = \
            pygame.font.SysFont(None, 18)

    coins = player_coins
    active_tab  = "SELL"
    page        = 0
    tab_keys    = list(SHOP_TABS.keys())

    # inventory copy so sells/buys mutate state
    inventory = {tab: [dict(i) for i in items] for tab, items in SHOP_TABS.items()}

    anim_timer  = 0.0
    flash_msg   = ""
    flash_timer = 0.0

    # button press state
    btn_pressed = {}

    while True:
        dt = clock.tick(60) / 1000.0
        anim_timer  += dt
        flash_timer  = max(0.0, flash_timer - dt)

        screen_w, screen_h = screen.get_size()

        # ── panel geometry (centred, fixed 300×440) ───────────
        PW, PH = 300, 440
        px = screen_w // 2 - PW // 2
        py = screen_h // 2 - PH // 2
        panel_rect = (px, py, PW, PH)

        # ── event handling ────────────────────────────────────
        mouse_pos = pygame.mouse.get_pos()
        mouse_up  = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_pressed[event.pos] = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                btn_pressed.clear()

        # ── compute rects ─────────────────────────────────────
        inner_x = px + 26
        inner_w = PW - 52

        # close button
        close_rect = pygame.Rect(px + PW - 32, py + 8, 22, 22)

        # tab buttons
        tab_rects = {}
        tab_w = inner_w // len(tab_keys)
        for i, tk in enumerate(tab_keys):
            tab_rects[tk] = pygame.Rect(inner_x + i * tab_w, py + 30, tab_w - 2, 22)

        # items list
        items = inventory[active_tab]
        page_items = items[page * ITEMS_PER_PAGE: (page + 1) * ITEMS_PER_PAGE]

        item_rects     = []
        action_rects   = []
        item_start_y   = py + 60

        for i, item in enumerate(page_items):
            row_y   = item_start_y + i * 72
            row_rect = pygame.Rect(inner_x, row_y, inner_w, 64)
            item_rects.append(row_rect)

            # action button label
            if active_tab == "SELL":
                lbl = "SELL"
            else:
                lbl = "BUY"
            btn_rect = pygame.Rect(row_rect.right - 60, row_rect.centery - 14, 55, 28)
            action_rects.append((btn_rect, lbl, item))

        # nav buttons
        max_pages = math.ceil(len(items) / ITEMS_PER_PAGE)
        prev_rect = pygame.Rect(inner_x,              py + PH - 42, 80, 28)
        next_rect = pygame.Rect(inner_x + inner_w - 80, py + PH - 42, 80, 28)

        # ── mouse interactions ────────────────────────────────
        if mouse_up:
            # close
            if close_rect.collidepoint(mouse_pos):
                return None

            # tabs
            for tk, tr in tab_rects.items():
                if tr.collidepoint(mouse_pos):
                    active_tab = tk
                    page = 0

            # nav
            if prev_rect.collidepoint(mouse_pos) and page > 0:
                page -= 1
            if next_rect.collidepoint(mouse_pos) and page < max_pages - 1:
                page += 1

            # action buttons
            for btn_rect, lbl, item in action_rects:
                if btn_rect.collidepoint(mouse_pos):
                    if lbl == "SELL" and item["owned"] > 0:
                        item["owned"] -= 1
                        coins += item["price"]
                        flash_msg   = f"+{item['price']} coins!"
                        flash_timer = 1.5
                    elif lbl == "BUY":
                        if coins >= item["price"]:
                            coins -= item["price"]
                            item["owned"] += 1
                            flash_msg   = f"Bought {item['name']}!"
                            flash_timer = 1.5
                        else:
                            flash_msg   = "Not enough coins!"
                            flash_timer = 1.5

        # ── draw ──────────────────────────────────────────────
        # draw shop background, or dim the game world if image not found
        if shop_bg is not None:
            screen.blit(shop_bg, (0, 0))
        else:
            overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

        # draw main panel
        draw_shop_panel(screen, panel_rect)

        # SHOP title text
        title_surf = font_title.render("SHOP", True, WOOD_DARK)
        screen.blit(title_surf, title_surf.get_rect(center=(px + PW // 2, py - 10)))

        # close button
        ch = close_rect.collidepoint(mouse_pos)
        draw_pixel_button(screen, close_rect, "X", font_btn, CLOSE_RED, CLOSE_LITE,
                          WOOD_DARK, text_col=WHITE, hovered=ch)

        # tabs
        for tk, tr in tab_rects.items():
            is_active = (tk == active_tab)
            base = BTN_MID if is_active else PARCH_MID
            lite = BTN_LIGHT if is_active else PARCH_LIGHT
            dark = BTN_DARK if is_active else PARCH_DARK
            tcol = WHITE if is_active else TEXT_DARK
            hov  = tr.collidepoint(mouse_pos)
            draw_pixel_button(screen, tr, tk, font_tab, base, lite, dark,
                              text_col=tcol, hovered=(hov and not is_active))

        # red corner accents (like in reference)
        for corner in [(inner_x - 4, item_start_y - 4), (inner_x + inner_w - 6, item_start_y - 4)]:
            pygame.draw.rect(screen, RED_CORNER, (corner[0], corner[1], 8, 8))
            pygame.draw.rect(screen, (220, 80, 80), (corner[0] + 1, corner[1] + 1, 4, 4))

        # item rows
        for i, item in enumerate(page_items):
            row_rect = item_rects[i]
            btn_rect, lbl, _ = action_rects[i]

            # row background alternating
            row_col = PARCH_LIGHT if i % 2 == 0 else PARCH_MID
            bg_surf = pygame.Surface((row_rect.width, row_rect.height), pygame.SRCALPHA)
            bg_surf.fill((*row_col, 180))
            screen.blit(bg_surf, row_rect.topleft)
            pygame.draw.rect(screen, PARCH_DARK, row_rect, 1)

            # icon
            icon_cx = row_rect.x + 22
            icon_cy = row_rect.centery
            draw_item_icon(screen, (icon_cx, icon_cy), item["color"], size=18)

            # name
            name_surf = font_item.render(item["name"], True, TEXT_DARK)
            screen.blit(name_surf, (row_rect.x + 46, row_rect.y + 10))

            # price / owned
            if active_tab == "SELL":
                sub_txt = f"Owned: {item['owned']}  |  {item['price']}c ea"
            else:
                sub_txt = f"Price: {item['price']}c  |  Have: {item['owned']}"
            sub_surf = font_price.render(sub_txt, True, TEXT_MID)
            screen.blit(sub_surf, (row_rect.x + 46, row_rect.y + 32))

            # action button
            can_act = (item["owned"] > 0) if lbl == "SELL" else (coins >= item["price"])
            b_base  = SELL_MID if lbl == "SELL" else BTN_MID
            b_lite  = SELL_LIGHT if lbl == "SELL" else BTN_LIGHT
            b_dark  = SELL_DARK if lbl == "SELL" else BTN_DARK
            if not can_act:
                b_base = b_lite = b_dark = PARCH_DARK
            hov = btn_rect.collidepoint(mouse_pos) and can_act
            draw_pixel_button(screen, btn_rect, lbl, font_btn,
                              b_base, b_lite, b_dark, hovered=hov)

        # coins display (bottom of parchment)
        coin_y = py + PH - 72
        coin_txt = font_coins.render(f"Coins: {coins}", True, TEXT_DARK)
        screen.blit(coin_txt, (inner_x + 4, coin_y))

        # flash message
        if flash_timer > 0:
            alpha = int(min(255, flash_timer * 300))
            pulse = 1.0 + 0.1 * math.sin(anim_timer * 8)
            fsize = max(10, int(14 * pulse))
            ff = pygame.font.SysFont("Courier New", fsize, bold=True)
            fc = (80, 160, 60) if "coins" in flash_msg or "Bought" in flash_msg else (180, 40, 40)
            fs = ff.render(flash_msg, True, fc)
            fs.set_alpha(alpha)
            screen.blit(fs, fs.get_rect(center=(px + PW // 2, coin_y)))

        # nav buttons
        has_prev = page > 0
        has_next = page < max_pages - 1
        draw_pixel_button(screen, prev_rect, "< PREV", font_nav,
                          NAV_MID if has_prev else PARCH_DARK,
                          NAV_LIGHT if has_prev else PARCH_MID,
                          NAV_DARK,
                          text_col=WHITE if has_prev else TEXT_MID,
                          hovered=prev_rect.collidepoint(mouse_pos) and has_prev)
        draw_pixel_button(screen, next_rect, "NEXT >", font_nav,
                          NAV_MID if has_next else PARCH_DARK,
                          NAV_LIGHT if has_next else PARCH_MID,
                          NAV_DARK,
                          text_col=WHITE if has_next else TEXT_MID,
                          hovered=next_rect.collidepoint(mouse_pos) and has_next)

        # page indicator
        page_txt = font_hint.render(f"{page + 1} / {max_pages}", True, TEXT_MID)
        screen.blit(page_txt, page_txt.get_rect(center=(px + PW // 2, py + PH - 28)))

        # ESC hint
        hint_surf = font_hint.render("ESC to leave", True, PARCH_DARK)
        screen.blit(hint_surf, hint_surf.get_rect(center=(px + PW // 2, py + PH + 14)))

        pygame.display.flip()
        