import pygame
import pytmx # type: ignore
import os

import display
import player
from player import Player
from ui import UIElement, create_surface_with_text

# for testing purposes
from rhythm import rhythmGameStart

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

def get_collision_rects(tmx_data, layer_name="collision"):
    rects = []
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == layer_name:
            for obj in layer:
                rects.append(pygame.Rect(
                    int(obj.x * SCALE), int(obj.y * SCALE), int(obj.width * SCALE), int(obj.height * SCALE)
                ))
    return rects

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

    # load collision rects
    collision_rects = get_collision_rects(tilemap.tmx, layer_name="collision")
    print(f"Loaded {len(collision_rects)} collision rects from Tiled map.")

    player_x = tilemap.pixel_width  // 2
    player_y = tilemap.pixel_height // 2
    player_speed = 4

    running = True
    player = Player(x=tilemap.pixel_width // 2, y=tilemap.pixel_height // 2)
    
    while running:
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

            # for testing        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rhythmGameStart()

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

        camera.update(player_x, player_y)

        screen.fill((30, 30, 30))
        tilemap.draw_background(screen, camera.x, camera.y)

        # debug tiles
        for rect in collision_rects:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(rect.x - camera.x, rect.y - camera.y, rect.width, rect.height), 2)

        player.update(keys)
        # draw player in centre of current window size
        screen.blit(player.image, (player_x - camera.x - player.rect.width // 2,
                                   player_y - camera.y - player.rect.height // 2))
        
        tilemap.draw_foreground(screen, camera.x, camera.y)
        
        pygame.display.flip()
        clock.tick(60)

# Just for testing *remove this before submitting* - allows you to run game_screen.py directly without going through main.py
"""if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game_screen(screen)"""
