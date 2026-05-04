import pygame
import pytmx # type: ignore
import os

import display
import player
from player import Player
from ui import UIElement, create_surface_with_text
from inventory import Inventory

from fishDiffuculty import fishingStart

from aquarium import aquarium_loop
from shop import shop_loop
from sky import Rain

TILE_SIZE = 16      # Each tile in the PNG is 16×16 pixels
SCALE = 3           # Scale up 3x
TILE_DRAW = TILE_SIZE * SCALE   # 48 pixels per tile on screen

class TileMap:
    """
    Loads a Tiled map and pre-renders it to a surface for fast drawing.
    Uses pytmx.
    """

    def __init__(self, map_path, scale):
        self.scale = scale

        # automatically loads the associated tileset images.
        self.tmx = pytmx.load_pygame(map_path, pixelalpha=True)

        # Map dimensions in tiles
        self.map_width  = self.tmx.width   # number of tile columns
        self.map_height = self.tmx.height  # number of tile rows

        # Map dimensions in pixels
        self.pixel_width  = self.map_width  * self.tmx.tilewidth  * scale
        self.pixel_height = self.map_height * self.tmx.tileheight * scale

        # render the map to a surface once at load time
        self._render()

    def _render(self):
        tw = self.tmx.tilewidth * self.scale
        th = self.tmx.tileheight * self.scale

        self.background = pygame.Surface((self.pixel_width, self.pixel_height), pygame.SRCALPHA)
        self.foreground = pygame.Surface((self.pixel_width, self.pixel_height), pygame.SRCALPHA)

        for layer in self.tmx.visible_layers:
            if not isinstance(layer, pytmx.TiledTileLayer):
                continue

            for x, y, image in layer.tiles():
                if image is None:
                    continue

                scaled = pygame.transform.scale(image, (tw, th))

                if layer.name == "foreground":
                    self.foreground.blit(scaled, (x * tw, y * th))
                else:
                    self.background.blit(scaled, (x * tw, y * th))

    def draw_background(self, screen, camera_x, camera_y):
        screen.blit(self.background, (-camera_x, -camera_y))

    def draw_foreground(self, screen, camera_x, camera_y):
        screen.blit(self.foreground, (-camera_x, -camera_y))

class Camera:
    """
    Keeps the camera centred on the player, clamped to map boundaries
    so no black bars appear.
    """

    def __init__(self, screen_w, screen_h, map_pixel_w, map_pixel_h):
        self.screen_w    = screen_w
        self.screen_h    = screen_h
        self.map_pixel_w = map_pixel_w
        self.map_pixel_h = map_pixel_h
        self.x = 0
        self.y = 0

        # Dead Zone Box
        box_w = screen_w // 6
        box_h = screen_h // 6
        self.box = pygame.Rect(
            screen_w // 2 - box_w // 2,
            screen_h // 2 - box_h // 2,
            box_w,
            box_h
        )

    def update(self, world_x, world_y):
        # Convert world position to screen position
        screen_x = world_x - self.x
        screen_y = world_y - self.y

        # Only move camera if player leaves the dead zone box
        if screen_x < self.box.left:
            self.x -= self.box.left - screen_x
        elif screen_x > self.box.right:
            self.x += screen_x - self.box.right

        if screen_y < self.box.top:
            self.y -= self.box.top - screen_y
        elif screen_y > self.box.bottom:
            self.y += screen_y - self.box.bottom

        # Clamp to map boundaries
        self.x = max(0, min(self.x, self.map_pixel_w - self.screen_w))
        self.y = max(0, min(self.y, self.map_pixel_h - self.screen_h))

def get_collision_rects(tmx_data, layer_name = "collision"):
    rects = []
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == layer_name:
            for obj in layer:
                rects.append(pygame.Rect(
                    int(obj.x * SCALE), int(obj.y * SCALE), int(obj.width * SCALE), int(obj.height * SCALE)
                ))
    return rects

def get_trigger_rect(tmx_data, layer_name = "triggers", object_name = "aquarium"):
    """Find a named object inside a Tiled object layer and return it as a pygame.Rect."""
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == layer_name:
            for obj in layer:
                if obj.name == object_name:
                    return pygame.Rect(
                        int(obj.x * SCALE), int(obj.y * SCALE),
                        int(obj.width * SCALE), int(obj.height * SCALE)
                    )
    return None

def settings_menu(screen, clock):

    # build buttons and offsets; volume is manipulated directly via mixer
    screen_w, screen_h = screen.get_size()
    resume_btn = UIElement((screen_w//2, screen_h//2 - 60), "Resume", 30, (50,50,50), (255,255,255), action="resume")
    menu_btn   = UIElement((screen_w//2, screen_h//2),       "Main Menu", 30, (50,50,50), (255,255,255), action="main_menu")
    quit_btn   = UIElement((screen_w//2, screen_h//2 + 60),  "Quit", 30, (50,50,50), (255,255,255), action="quit")
    vol_up     = UIElement((screen_w//2 + 100, screen_h//2 - 120), "+", 40, (50,50,50), (255,255,255), action="vol_up")
    vol_down   = UIElement((screen_w//2 - 100, screen_h//2 - 120), "-", 40, (50,50,50), (255,255,255), action="vol_down")

    buttons = [resume_btn, menu_btn, quit_btn, vol_up, vol_down]
    offsets = [-60, 0, 60, -120 + 0, -120 + 0]  # y offsets for centering later

    while True:
        dt = clock.tick(60) / 1000.0
        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.KEYDOWN:
                # pressing P or ESC here resumes
                if event.key in (pygame.K_p, pygame.K_ESCAPE):
                    return None

        # Update button centers in case window changed
        screen_w, screen_h = screen.get_size()
        resume_btn.set_center((screen_w//2, screen_h//2 - 60))
        menu_btn.set_center((screen_w//2, screen_h//2))
        quit_btn.set_center((screen_w//2, screen_h//2 + 60))
        vol_up.set_center((screen_w//2 + 100, screen_h//2 - 120))
        vol_down.set_center((screen_w//2 - 100, screen_h//2 - 120))

        # draw translucent background
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        for btn in buttons:
            action = btn.update(pygame.mouse.get_pos(), mouse_up)
            if action == "resume":
                return None
            if action == "main_menu":
                return "main_menu"
            if action == "quit":
                return "quit"
            if action == "vol_up":
                newv = min(1.0, pygame.mixer.music.get_volume() + 0.1)
                pygame.mixer.music.set_volume(newv)
            if action == "vol_down":
                newv = max(0.0, pygame.mixer.music.get_volume() - 0.1)
                pygame.mixer.music.set_volume(newv)

        for btn in buttons:
            btn.draw(screen)

        # display current volume
        vol_text = create_surface_with_text(f"Volume: {pygame.mixer.music.get_volume():.1f}", 24, (255,255,255), (0,0,0))
        screen.blit(vol_text, (10, 10))

        pygame.display.flip()


# Aquarium proximity prompt helper
AQUARIUM_PROXIMITY = 150  # pixels from centre of trigger before prompt appears
SHOP_PROXIMITY     = 150  # pixels from centre of shop trigger before prompt appears

def draw_aquarium_prompt(screen, player_screen_x, player_screen_y):
    """Draw 'Aquarium' label + enter hint above the player's head."""
    font_label = pygame.font.SysFont("Arial", 20, bold=True)
    font_hint  = pygame.font.SysFont("Arial", 15)

    label = font_label.render("Aquarium", True, (255, 255, 255))
    hint  = font_hint.render("[ Enter ]", True, (220, 220, 100))

    pad   = 8
    box_w = max(label.get_width(), hint.get_width()) + pad * 2
    box_h = label.get_height() + hint.get_height() + pad * 2 + 4

    box_x = player_screen_x - box_w // 2
    box_y = player_screen_y - 80 - box_h

    box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    pygame.draw.rect(box_surf, (0, 0, 0, 160), box_surf.get_rect(), border_radius=6)
    box_surf.blit(label, label.get_rect(centerx=box_w // 2, top=pad))
    box_surf.blit(hint,  hint.get_rect(centerx=box_w // 2, top=pad + label.get_height() + 4))

    screen.blit(box_surf, (box_x, box_y))


def draw_shop_prompt(screen, player_screen_x, player_screen_y):
    """Draw 'Shop' label + enter hint above the player's head."""
    font_label = pygame.font.SysFont("Arial", 20, bold=True)
    font_hint  = pygame.font.SysFont("Arial", 15)

    label = font_label.render("Shop", True, (255, 255, 255))
    hint  = font_hint.render("[ Enter ]", True, (220, 220, 100))

    pad   = 8
    box_w = max(label.get_width(), hint.get_width()) + pad * 2
    box_h = label.get_height() + hint.get_height() + pad * 2 + 4

    box_x = player_screen_x - box_w // 2
    box_y = player_screen_y - 80 - box_h

    box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    pygame.draw.rect(box_surf, (0, 0, 0, 160), box_surf.get_rect(), border_radius=6)
    box_surf.blit(label, label.get_rect(centerx=box_w // 2, top=pad))
    box_surf.blit(hint,  hint.get_rect(centerx=box_w // 2, top=pad + label.get_height() + 4))

    screen.blit(box_surf, (box_x, box_y))


def gameLoop(screen):
    """
    The main in-game screen. Called from main-menu.py when Start is clicked.
    Key controls:
      * ESC  - toggle fullscreen / resolution
      * P    - open in-game settings (pause)
    """

    clock    = pygame.time.Clock()
    # initial values; these may change if the window is resized or toggled to
    # fullscreen, so we refresh them inside the game loop below.
    screen_w = screen.get_width()
    screen_h = screen.get_height()

    # base directory for file paths in this module
    here = os.path.dirname(os.path.abspath(__file__))

    # -- background music -------------------------------------------------
    # initialize the mixer if it hasn't been already, then load & play
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except Exception:
        # if the mixer fails to init for some reason, just continue without music
        pass

    
    music_path = os.path.join(here, "assets", "MUSIC", "ingame.ogg")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  
    # ----------------------------------------------------------------------

    map_path = os.path.join(here, "assets", "InGameBG", "map.tmx")

    if not os.path.exists(map_path):
        print(f"ERROR: Could not find map.tmx at {map_path}")
        print("Export your Tiled map as map.tmx into your project folder.")
        return

    tilemap = TileMap(map_path, scale=SCALE)
    camera  = Camera(screen_w, screen_h, tilemap.pixel_width, tilemap.pixel_height)

    inventory = Inventory(
        os.path.join(here, "assets", "Sprites", "Inv_slots.png"),
        num_slots=8,
        visible_slot_count=5,
        initial_items=["Rod"],
    )

    # Create sprite group for dynamic entities (rain, etc.)
    all_sprites = pygame.sprite.LayeredUpdates()
    
    # Initialize rain system with full tilemap dimensions
    rain = Rain(all_sprites, map_width=tilemap.pixel_width, map_height=tilemap.pixel_height)

    # load collision rects
    collision_rects = get_collision_rects(tilemap.tmx, layer_name="collision")
    water_rects = get_collision_rects(tilemap.tmx, layer_name="water")

    # load aquarium trigger rect from the "triggers" object layer in Tiled
    aquarium_rect = get_trigger_rect(tilemap.tmx, layer_name="triggers", object_name="aquarium")
    if aquarium_rect is None:
        print("WARNING: No 'aquarium' object found in 'triggers' layer in Tiled map.")

    # load shop trigger rect from the "triggers" object layer in Tiled
    shop_rect = get_trigger_rect(tilemap.tmx, layer_name="triggers", object_name="shop")
    if shop_rect is None:
        print("WARNING: No 'shop' object found in 'triggers' layer in Tiled map.")

    player_x = tilemap.pixel_width  // 2
    player_y = tilemap.pixel_height // 2
    player_speed = 4

    running = True
    player = Player(x=tilemap.pixel_width // 2, y=tilemap.pixel_height // 2)

    near_aquarium = False  # tracked outside event loop so K_RETURN can read it
    near_shop     = False  # tracked outside event loop so K_RETURN can read it

    while running:
        dt = clock.tick(60) / 1000.0  # Calculate delta time once per frame
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"

            if event.type == pygame.KEYDOWN:
                # check for settings overlay first
                if event.key == pygame.K_p:
                    result = settings_menu(screen, clock)
                    if result == "main_menu":
                        pygame.mixer.music.stop()
                        return "menu"
                    if result == "quit":
                        # stop any playing music then bubble up quit request
                        pygame.mixer.music.stop()
                        return "quit"
                    # otherwise resume the game

                # ESC used to toggle fullscreen, now does nothing here
                elif event.key == pygame.K_ESCAPE:
                    pass

                # enter aquarium when the prompt is visible
                elif event.key == pygame.K_RETURN and near_aquarium:
                    result = aquarium_loop(screen, clock)
                    if result == "quit":
                        pygame.mixer.music.stop()
                        return "quit"

                # enter shop when the prompt is visible
                elif event.key == pygame.K_RETURN and near_shop:
                    result = shop_loop(screen, clock)
                    if result == "quit":
                        pygame.mixer.music.stop()
                        return "quit"
                else:
                    selected_item = inventory.handle_key_event(event)
                    if selected_item is not None or event.key in Inventory.SLOT_KEYS:
                        print(f"Selected slot {inventory.selected_slot + 1}: {selected_item or 'Empty'}")

            # for testing        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    near_water = any(player_world_rect.colliderect(r) for r in water_rects)
                    if near_water:
                        player.set_animation("fishing")
                        player.frame_index = 0
                        player.is_fishing = True
                        player.animation_speed = 100
    
                        fishing_done = False
                        while not fishing_done:
                            clock.tick(60)
                            player.update(pygame.key.get_pressed())
    
                            if player.frame_index >= len(player.animations["fishing"]) - 1:
                                fishing_done = True
    
                            screen.fill((30, 30, 30))
                            tilemap.draw_background(screen, camera.x, camera.y)
                            screen.blit(player.image, (
                                player_x - camera.x - player.rect.width // 2,
                                player_y - camera.y - player.rect.height // 2
                            ))
                            tilemap.draw_foreground(screen, camera.x, camera.y)
                            pygame.display.flip()
    
                        player.is_fishing = False
                        player.set_animation("idle")
                        #rhythmGameStart()
                        fishingStart(rain.is_raining)

        # window size might have changed (fullscreen toggle) so update
        screen_w, screen_h = screen.get_size()

        # save position so we can roll back if we collide with a wall
        old_x, old_y = player_x, player_y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_x += player_speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]: player_y -= player_speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: player_y += player_speed

        half_w = player.hitbox.width // 2
        half_h = player.hitbox.height // 2

        player_x = max(half_w, min(player_x, tilemap.pixel_width - half_w))
        player_y = max(half_h, min(player_y, tilemap.pixel_height - half_h))

        # player's hit box
        player_w = player.hitbox.width
        player_h = player.hitbox.height
        player_world_rect = pygame.Rect(
            player_x - player_w // 2,
            player_y - player_h // 2,
            player_w,
            player_h
        )

        # revert movement if we collide with a wall
        for collision_rect in collision_rects:
            if player_world_rect.colliderect(collision_rect):
                player_x, player_y = old_x, old_y
                break

        # check proximity to aquarium trigger from Tiled
        if aquarium_rect is not None:
            dist = ((player_x - aquarium_rect.centerx) ** 2 + (player_y - aquarium_rect.centery) ** 2) ** 0.5
            near_aquarium = dist < AQUARIUM_PROXIMITY
        else:
            near_aquarium = False

        # check proximity to shop trigger from Tiled
        if shop_rect is not None:
            dist = ((player_x - shop_rect.centerx) ** 2 + (player_y - shop_rect.centery) ** 2) ** 0.5
            near_shop = dist < SHOP_PROXIMITY
        else:
            near_shop = False

        camera.update(player_x, player_y)

        screen.fill((30, 30, 30))
        tilemap.draw_background(screen, camera.x, camera.y)

        '''
        # debug tiles
        for rect in collision_rects:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(rect.x - camera.x, rect.y - camera.y, rect.width, rect.height), 2)
        '''

        player.update(keys)

        # Update rain system and all sprites
        rain.update()
        all_sprites.update(dt)

        # player screen coords used for both drawing and the prompt position
        player_screen_x = player_x - camera.x
        player_screen_y = player_y - camera.y

        # draw player in centre of current window size
        screen.blit(player.image, (player_screen_x - player.rect.width // 2,
                                   player_screen_y - player.rect.height // 2))
        
        tilemap.draw_foreground(screen, camera.x, camera.y)

        # Draw all sprites (rain, etc.) with camera offset
        for sprite in all_sprites:
            offset_x = sprite.rect.x - camera.x
            offset_y = sprite.rect.y - camera.y
            screen.blit(sprite.image, (offset_x, offset_y))

        # Weather indicator
        if rain.is_raining:
            rain_icon = pygame.image.load(os.path.join(here, "assets", "Sprites", "rain_icon.png")).convert_alpha()
            rain_icon = pygame.transform.scale(rain_icon, (50, 50))  # Scale to 20x20 pixels
            icon_rect = rain_icon.get_rect(topleft=(10, 10))
            screen.blit(rain_icon, icon_rect)

        # draw prompt above player's head when near the aquarium
        if near_aquarium:
            draw_aquarium_prompt(screen, player_screen_x, player_screen_y)

        # draw prompt above player's head when near the shop
        if near_shop:
            draw_shop_prompt(screen, player_screen_x, player_screen_y)

        inventory.draw_panel(screen, screen_w, screen_h)
        inventory.draw_selected_item_label(screen, screen_w, screen_h)

        pygame.display.flip()

# Just for testing *remove this before submitting* - allows you to run game_screen.py directly without going through main.py
"""if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game_screen(screen)"""
