import pygame
import pytmx # type: ignore
import os


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
        """
        Draw every layer of the map onto a single large surface once at load time.
        Every frame we just blit this surface offset by the camera.
        """
        tw = self.tmx.tilewidth  * self.scale   # tile draw width
        th = self.tmx.tileheight * self.scale   # tile draw height

        # Create a surface big enough to hold the whole map
        self.surface = pygame.Surface(
            (self.pixel_width, self.pixel_height),
            pygame.SRCALPHA
        )

        # Loop through every tile layer in your Tiled map
        for layer in self.tmx.visible_layers:
            # only process tile layers, skip object layers etc
            if not isinstance(layer, pytmx.TiledTileLayer):
                continue

            # loop through every tile in the layer. pytmx gives us the tile image and its column/row.
            for x, y, image in layer.tiles():
                if image is None:
                    continue
                # scale the tile image to the desired draw size
                scaled_image = pygame.transform.scale(image, (tw, th))
                # blit the tile image to the correct position on the surface
                self.surface.blit(scaled_image, (x * tw, y * th))

    def draw(self, screen, camera_x, camera_y):
        """
        Draw the pre-rendered map surface onto the screen, offset by the camera.
        """
        screen.blit(self.surface, (-camera_x, -camera_y))

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

    def center_on(self, world_x, world_y):
        self.x = world_x - self.screen_w // 2
        self.y = world_y - self.screen_h // 2
        self.x = max(0, min(self.x, self.map_pixel_w - self.screen_w))
        self.y = max(0, min(self.y, self.map_pixel_h - self.screen_h))


def game_screen(screen):
    """
    The main in-game screen. Called from main-menu.py when Start is clicked.
    Press ESC to return to the main menu.
    """

    clock    = pygame.time.Clock()
    screen_w = screen.get_width()
    screen_h = screen.get_height()

    here = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(here, "assets", "map.tmx")

    if not os.path.exists(map_path):
        print(f"ERROR: Could not find map.tmx at {map_path}")
        print("Export your Tiled map as map.tmx into your project folder.")
        return

    tilemap = TileMap(map_path, scale=SCALE)
    camera  = Camera(screen_w, screen_h, tilemap.pixel_width, tilemap.pixel_height)

    player_x = tilemap.pixel_width  // 2
    player_y = tilemap.pixel_height // 2
    player_speed = 4

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_x += player_speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]: player_y -= player_speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: player_y += player_speed

        player_x = max(0, min(player_x, tilemap.pixel_width))
        player_y = max(0, min(player_y, tilemap.pixel_height))

        camera.center_on(player_x, player_y)

        screen.fill((30, 30, 30))
        tilemap.draw(screen, camera.x, camera.y)

        pygame.draw.circle(screen, (255, 80, 80), (screen_w // 2, screen_h // 2), 8)

        # TODO: replace dot with player sprite, add HUD on top

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
