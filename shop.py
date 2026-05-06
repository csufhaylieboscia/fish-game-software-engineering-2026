import pygame
import math
import os
from models import FishInventory

# ── Pixel-art colour palette ───────────────────────────────────────────────────
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
WHITE       = (255, 255, 255)

# ── Shop item definitions ──────────────────────────────────────────────────────
# "key" must exactly match the name string used in fish.py Fish("name", ...)
# "name" is the display label shown in the shop UI
SHOP_TABS = {
    "SELL": [
        # difficulty 1 - common (10 coins)
        {"key": "goldfish",   "name": "Goldfish",    "color": (220, 160,  40), "price": 10,  "owned": 0},
        {"key": "greenfish",  "name": "Green Fish",  "color": ( 80, 180,  80), "price": 10,  "owned": 0},
        {"key": "mossball",   "name": "Moss Ball",   "color": ( 90, 140,  70), "price": 10,  "owned": 0},
        {"key": "sea snail",  "name": "Sea Snail",   "color": (180, 140, 100), "price": 10,  "owned": 0},
        {"key": "shell",      "name": "Shell",       "color": (230, 200, 150), "price": 10,  "owned": 0},
        # difficulty 2 - uncommon (25 coins)
        {"key": "blackfish",  "name": "Black Fish",  "color": ( 60,  60,  60), "price": 25,  "owned": 0},
        {"key": "flatfish",   "name": "Flat Fish",   "color": (200, 180, 100), "price": 25,  "owned": 0},
        {"key": "Noc",        "name": "Noc",         "color": ( 80,  80, 160), "price": 25,  "owned": 0},
        # difficulty 3 - rare (60 coins)
        {"key": "betafish",   "name": "Beta Fish",   "color": (180,  60, 200), "price": 60,  "owned": 0},
        {"key": "clownfish",  "name": "Clown Fish",  "color": (220,  90,  30), "price": 60,  "owned": 0},
        {"key": "plasticbag", "name": "Plastic Bag", "color": (200, 220, 240), "price": 60,  "owned": 0},
        {"key": "Cal",        "name": "Cal",         "color": ( 60, 160, 200), "price": 60,  "owned": 0},
        {"key": "Jelly",      "name": "Jelly",       "color": (200, 150, 220), "price": 60,  "owned": 0},
        # difficulty 4 - epic (120 coins)
        {"key": "axolotl",    "name": "Axolotl",     "color": (230, 150, 170), "price": 120, "owned": 0},
        {"key": "octopus",    "name": "Octopus",     "color": (160,  80, 160), "price": 120, "owned": 0},
        {"key": "pirahna",    "name": "Piranha",     "color": (200,  50,  50), "price": 120, "owned": 0},
        {"key": "Starfish",   "name": "Starfish",    "color": (220, 140,  50), "price": 120, "owned": 0},
        {"key": "Hay",        "name": "Hay",         "color": (220, 200,  60), "price": 120, "owned": 0},
        {"key": "Uhh",        "name": "Uhh",         "color": (100, 180, 160), "price": 120, "owned": 0},
        # difficulty 5 - legendary (300 coins)
        {"key": "Angler",     "name": "Angler",      "color": ( 40,  40,  80), "price": 300, "owned": 0},
    ],
    "RODS & BAIT": [
        {"key": None, "name": "Basic Rod",   "color": (160, 110,  60), "price": 50,  "owned": 1},
        {"key": None, "name": "Steel Rod",   "color": (160, 170, 180), "price": 150, "owned": 0},
        {"key": None, "name": "Magic Rod",   "color": (120,  80, 220), "price": 400, "owned": 0},
        {"key": None, "name": "Worm Bait",   "color": (150, 100,  60), "price": 15,  "owned": 5},
        {"key": None, "name": "Shiny Lure",  "color": (200, 200,  60), "price": 40,  "owned": 2},
        {"key": None, "name": "Magic Bait",  "color": ( 80, 180, 200), "price": 100, "owned": 0},
    ],
    "DECOR": [
        {"key": None, "name": "Coral",           "color": (220,  90, 110), "price": 30,  "owned": 2},
        {"key": None, "name": "Treasure Chest",  "color": (160, 130,  60), "price": 80,  "owned": 0},
        {"key": None, "name": "Sea Castle",      "color": (140, 140, 200), "price": 200, "owned": 0},
        {"key": None, "name": "Seaweed",         "color": ( 60, 160,  80), "price": 20,  "owned": 3},
        {"key": None, "name": "Shipwreck",       "color": (110,  90,  70), "price": 350, "owned": 0},
        {"key": None, "name": "Pearl",           "color": (230, 230, 240), "price": 500, "owned": 0},
    ],
}

ITEMS_PER_PAGE = 4


def _sync_sell_from_inventory(inventory, fish_inv):
    """Copy owned counts from FishInventory into the SELL tab."""
    for item in inventory["SELL"]:
        if item["key"] is not None:
            item["owned"] = fish_inv.fish_counts.get(item["key"], 0)


def _save_sell_to_inventory(inventory, fish_inv):
    """Write current SELL owned counts back to FishInventory and save to disk."""
    for item in inventory["SELL"]:
        if item["key"] is not None:
            fish_inv.fish_counts[item["key"]] = item["owned"]
    fish_inv.save()


def draw_pixel_button(surf, rect, label, font, base_col, light_col, dark_col,
                      text_col=WHITE, hovered=False):
    col = light_col if hovered else base_col
    s_rect   = pygame.Rect(rect.x + 3, rect.y + 3, rect.width, rect.height)
    shadow_s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    shadow_s.fill((0, 0, 0, 70))
    surf.blit(shadow_s, s_rect.topleft)
    pygame.draw.rect(surf, col, rect, border_radius=4)
    pygame.draw.rect(surf, dark_col, rect, 2, border_radius=4)
    hl = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, 3)
    pygame.draw.rect(surf, light_col, hl, border_radius=2)
    txt = font.render(label, True, text_col)
    surf.blit(txt, txt.get_rect(center=rect.center))


def draw_item_icon(surf, center, color, size=20):
    x, y = center
    r = size // 2
    points = [
        (x,     y - r), (x + r, y - r // 2), (x + r, y + r // 2),
        (x,     y + r), (x - r, y + r // 2), (x - r, y - r // 2),
    ]
    pygame.draw.polygon(surf, color, points)
    dark  = tuple(max(0, c - 60) for c in color[:3])
    light = tuple(min(255, c + 80) for c in color[:3])
    pygame.draw.polygon(surf, dark, points, 2)
    pygame.draw.line(surf, light, (x - r // 2, y - r // 2), (x, y - r + 2), 2)


def draw_leaf(surf, x, y, flip=False):
    for dx, dy, col in [(-8, 0, LEAF_MID), (0, -10, LEAF_LIGHT), (8, 0, LEAF_MID)]:
        cx, cy = (x - dx if flip else x + dx), y + dy
        pygame.draw.circle(surf, col, (cx, cy), 8)
        pygame.draw.circle(surf, LEAF_DARK, (cx, cy), 8, 1)


def draw_wood_plank(surf, rect, horizontal=True):
    pygame.draw.rect(surf, WOOD_MID, rect)
    if horizontal:
        for i in range(rect.y + 4, rect.bottom - 4, 6):
            pygame.draw.line(surf, WOOD_DARK, (rect.x + 2, i), (rect.right - 2, i), 1)
    else:
        for i in range(rect.x + 4, rect.right - 4, 6):
            pygame.draw.line(surf, WOOD_DARK, (i, rect.y + 2), (i, rect.bottom - 2), 1)
    pygame.draw.rect(surf, WOOD_DARK, rect, 2)
    pygame.draw.line(surf, WOOD_HILIT, (rect.x + 2, rect.y + 2), (rect.right - 2, rect.y + 2), 1)


def draw_shop_panel(surf, panel_rect):
    px, py, pw, ph = panel_rect

    parch = pygame.Rect(px + 18, py + 18, pw - 36, ph - 36)
    pygame.draw.rect(surf, PARCH_PAPER, parch)
    for i in range(parch.y + 8, parch.bottom, 12):
        pygame.draw.line(surf, PARCH_DARK, (parch.x + 6, i), (parch.right - 6, i), 1)
    pygame.draw.rect(surf, PARCH_DARK, parch, 2)

    left_col  = pygame.Rect(px,           py + 20, 22, ph - 40)
    right_col = pygame.Rect(px + pw - 22, py + 20, 22, ph - 40)
    draw_wood_plank(surf, left_col,  horizontal=False)
    draw_wood_plank(surf, right_col, horizontal=False)
    for col_rect in (left_col, right_col):
        for ry in (col_rect.y + 10, col_rect.centery, col_rect.bottom - 10):
            pygame.draw.circle(surf, WOOD_DARK,  (col_rect.centerx, ry), 5)
            pygame.draw.circle(surf, WOOD_HILIT, (col_rect.centerx - 1, ry - 1), 2)

    draw_wood_plank(surf, pygame.Rect(px + 10, py,           pw - 20, 22))
    draw_wood_plank(surf, pygame.Rect(px + 10, py + ph - 22, pw - 20, 22))

    for cx_, cy_ in [(px+10, py+10), (px+pw-30, py+10), (px+10, py+ph-30), (px+pw-30, py+ph-30)]:
        pygame.draw.rect(surf, WOOD_DARK,  (cx_, cy_, 20, 20))
        pygame.draw.rect(surf, WOOD_HILIT, (cx_ + 2, cy_ + 2, 8, 8))
        pygame.draw.rect(surf, WOOD_DARK,  (cx_, cy_, 20, 20), 2)

    draw_leaf(surf, px + 14,      py + ph // 2)
    draw_leaf(surf, px + pw - 14, py + ph // 2, flip=True)
    draw_leaf(surf, px + pw // 2, py + ph - 10)

    sign = pygame.Rect(px + pw // 2 - 48, py - 28, 96, 36)
    draw_wood_plank(surf, sign)
    for bx in (sign.x + 6, sign.right - 10):
        pygame.draw.circle(surf, WOOD_DARK, (bx, sign.centery), 3)


def shop_loop(screen, clock, player_coins=200):
    """
    Full pixel-art shop screen.
    Returns None to go back to overworld, or "quit".
    """
    pygame.font.init()

    # Load background image once before the loop
    here    = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(here, "assets", "Sprites", "shop_bg.webp")
    screen_w, screen_h = screen.get_size()
    if os.path.exists(bg_path):
        shop_bg = pygame.image.load(bg_path).convert()
        shop_bg = pygame.transform.scale(shop_bg, (screen_w, screen_h))
    else:
        shop_bg = None

    # Fonts
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

    coins      = player_coins
    active_tab = "SELL"
    page       = 0
    tab_keys   = list(SHOP_TABS.keys())

    # Load player's caught fish and sync into the SELL tab
    fish_inv  = FishInventory.load()
    inventory = {tab: [dict(i) for i in items] for tab, items in SHOP_TABS.items()}
    _sync_sell_from_inventory(inventory, fish_inv)

    anim_timer  = 0.0
    flash_msg   = ""
    flash_timer = 0.0
    btn_pressed = {}

    while True:
        dt = clock.tick(60) / 1000.0
        anim_timer  += dt
        flash_timer  = max(0.0, flash_timer - dt)

        screen_w, screen_h = screen.get_size()

        PW, PH = 300, 440
        px = screen_w // 2 - PW // 2
        py = screen_h // 2 - PH // 2
        panel_rect = (px, py, PW, PH)

        mouse_pos = pygame.mouse.get_pos()
        mouse_up  = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_pressed[event.pos] = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                btn_pressed.clear()

        inner_x = px + 26
        inner_w = PW - 52

        close_rect = pygame.Rect(px + PW - 32, py + 8, 22, 22)

        tab_rects = {}
        tab_w = inner_w // len(tab_keys)
        for i, tk in enumerate(tab_keys):
            tab_rects[tk] = pygame.Rect(inner_x + i * tab_w, py + 30, tab_w - 2, 22)

        items        = inventory[active_tab]
        page_items   = items[page * ITEMS_PER_PAGE: (page + 1) * ITEMS_PER_PAGE]
        item_rects   = []
        action_rects = []
        item_start_y = py + 60

        for i, item in enumerate(page_items):
            row_rect = pygame.Rect(inner_x, item_start_y + i * 72, inner_w, 64)
            item_rects.append(row_rect)
            lbl      = "SELL" if active_tab == "SELL" else "BUY"
            btn_rect = pygame.Rect(row_rect.right - 60, row_rect.centery - 14, 55, 28)
            action_rects.append((btn_rect, lbl, item))

        max_pages = math.ceil(len(items) / ITEMS_PER_PAGE)
        prev_rect = pygame.Rect(inner_x,                py + PH - 42, 80, 28)
        next_rect = pygame.Rect(inner_x + inner_w - 80, py + PH - 42, 80, 28)

        # Mouse interactions
        if mouse_up:
            if close_rect.collidepoint(mouse_pos):
                return None
            for tk, tr in tab_rects.items():
                if tr.collidepoint(mouse_pos):
                    active_tab = tk
                    page = 0
            if prev_rect.collidepoint(mouse_pos) and page > 0:
                page -= 1
            if next_rect.collidepoint(mouse_pos) and page < max_pages - 1:
                page += 1
            for btn_rect, lbl, item in action_rects:
                if btn_rect.collidepoint(mouse_pos):
                    if lbl == "SELL" and item["owned"] > 0:
                        item["owned"] -= 1
                        coins += item["price"]
                        flash_msg   = f"+{item['price']} coins!"
                        flash_timer = 1.5
                        # Persist updated fish count to player_fish.json
                        _save_sell_to_inventory(inventory, fish_inv)
                    elif lbl == "BUY":
                        if coins >= item["price"]:
                            coins -= item["price"]
                            item["owned"] += 1
                            flash_msg   = f"Bought {item['name']}!"
                            flash_timer = 1.5
                        else:
                            flash_msg   = "Not enough coins!"
                            flash_timer = 1.5

        # Draw
        if shop_bg is not None:
            screen.blit(shop_bg, (0, 0))
        else:
            overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

        draw_shop_panel(screen, panel_rect)

        title_surf = font_title.render("SHOP", True, WOOD_DARK)
        screen.blit(title_surf, title_surf.get_rect(center=(px + PW // 2, py - 10)))

        draw_pixel_button(screen, close_rect, "X", font_btn, CLOSE_RED, CLOSE_LITE,
                          WOOD_DARK, text_col=WHITE, hovered=close_rect.collidepoint(mouse_pos))

        for tk, tr in tab_rects.items():
            is_active = (tk == active_tab)
            draw_pixel_button(screen, tr, tk, font_tab,
                              BTN_MID   if is_active else PARCH_MID,
                              BTN_LIGHT if is_active else PARCH_LIGHT,
                              BTN_DARK  if is_active else PARCH_DARK,
                              text_col=WHITE if is_active else TEXT_DARK,
                              hovered=(tr.collidepoint(mouse_pos) and not is_active))

        for corner in [(inner_x - 4, item_start_y - 4), (inner_x + inner_w - 6, item_start_y - 4)]:
            pygame.draw.rect(screen, RED_CORNER, (corner[0], corner[1], 8, 8))
            pygame.draw.rect(screen, (220, 80, 80), (corner[0] + 1, corner[1] + 1, 4, 4))

        for i, item in enumerate(page_items):
            row_rect         = item_rects[i]
            btn_rect, lbl, _ = action_rects[i]

            row_col = PARCH_LIGHT if i % 2 == 0 else PARCH_MID
            bg_surf = pygame.Surface((row_rect.width, row_rect.height), pygame.SRCALPHA)
            bg_surf.fill((*row_col, 180))
            screen.blit(bg_surf, row_rect.topleft)
            pygame.draw.rect(screen, PARCH_DARK, row_rect, 1)

            draw_item_icon(screen, (row_rect.x + 22, row_rect.centery), item["color"], size=18)
            screen.blit(font_item.render(item["name"], True, TEXT_DARK),
                        (row_rect.x + 46, row_rect.y + 10))

            sub_txt = (f"Owned: {item['owned']}  |  {item['price']}c ea"
                       if active_tab == "SELL"
                       else f"Price: {item['price']}c  |  Have: {item['owned']}")
            screen.blit(font_price.render(sub_txt, True, TEXT_MID),
                        (row_rect.x + 46, row_rect.y + 32))

            can_act = (item["owned"] > 0) if lbl == "SELL" else (coins >= item["price"])
            b_base  = SELL_MID   if lbl == "SELL" else BTN_MID
            b_lite  = SELL_LIGHT if lbl == "SELL" else BTN_LIGHT
            b_dark  = SELL_DARK  if lbl == "SELL" else BTN_DARK
            if not can_act:
                b_base = b_lite = b_dark = PARCH_DARK
            draw_pixel_button(screen, btn_rect, lbl, font_btn, b_base, b_lite, b_dark,
                              hovered=(btn_rect.collidepoint(mouse_pos) and can_act))

        coin_y = py + PH - 72
        screen.blit(font_coins.render(f"Coins: {coins}", True, TEXT_DARK), (inner_x + 4, coin_y))

        if flash_timer > 0:
            alpha = int(min(255, flash_timer * 300))
            pulse = 1.0 + 0.1 * math.sin(anim_timer * 8)
            ff    = pygame.font.SysFont("Courier New", max(10, int(14 * pulse)), bold=True)
            fc    = (80, 160, 60) if "coins" in flash_msg or "Bought" in flash_msg else (180, 40, 40)
            fs    = ff.render(flash_msg, True, fc)
            fs.set_alpha(alpha)
            screen.blit(fs, fs.get_rect(center=(px + PW // 2, coin_y)))

        has_prev = page > 0
        has_next = page < max_pages - 1
        draw_pixel_button(screen, prev_rect, "< PREV", font_nav,
                          NAV_MID   if has_prev else PARCH_DARK,
                          NAV_LIGHT if has_prev else PARCH_MID,
                          NAV_DARK,
                          text_col=WHITE   if has_prev else TEXT_MID,
                          hovered=prev_rect.collidepoint(mouse_pos) and has_prev)
        draw_pixel_button(screen, next_rect, "NEXT >", font_nav,
                          NAV_MID   if has_next else PARCH_DARK,
                          NAV_LIGHT if has_next else PARCH_MID,
                          NAV_DARK,
                          text_col=WHITE   if has_next else TEXT_MID,
                          hovered=next_rect.collidepoint(mouse_pos) and has_next)

        screen.blit(font_hint.render(f"{page + 1} / {max_pages}", True, TEXT_MID),
                    font_hint.render(f"{page + 1} / {max_pages}", True, TEXT_MID)
                    .get_rect(center=(px + PW // 2, py + PH - 28)))

        screen.blit(font_hint.render("ESC to leave", True, PARCH_DARK),
                    font_hint.render("ESC to leave", True, PARCH_DARK)
                    .get_rect(center=(px + PW // 2, py + PH + 14)))

        pygame.display.flip()
        