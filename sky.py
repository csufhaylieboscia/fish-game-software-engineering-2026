"""
Sky and weather effects (rain system)
"""
import pygame 
from settings import LAYERS
from support import import_folder
from weather_sprites import Generic
from random import randint, choice


class Drop(Generic):
    """
    Individual rain drop sprite that falls and disappears after a lifetime.
    """
    
    def __init__(self, surf, pos, moving, groups, z):
        # general setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # moving 
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        """Update drop position and handle lifetime."""
        # movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    """
    Rain system that creates and manages rain drops.
    """
    
    def __init__(self, all_sprites, map_width=None, map_height=None):
        """
        Initialize the rain system.
        
        Args:
            all_sprites: Pygame sprite group to add rain drops to
            map_width: Width of the tilemap in pixels (optional)
            map_height: Height of the tilemap in pixels (optional)
        """
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('assets/rain/drops/')
        self.rain_floor = import_folder('assets/rain/floor/')
        
        # Use provided map dimensions, or fallback to defaults
        if map_width and map_height:
            self.floor_w = map_width
            self.floor_h = map_height
        else:
            # Fallback to default size if not provided
            self.floor_w, self.floor_h = 1200, 800
            
        # Weather cycle timing
        self.start_time = pygame.time.get_ticks()
        self.is_raining = False
        self.rain_duration = 180000  # 3 minutes = 180,000 ms
        self.next_rain_time = self.start_time + randint(10000, 30000)  # First rain starts 10-30 seconds later
        self.rain_end_time = 0

    def create_floor(self):
        """Create a rain drop that lands on the floor (stationary)."""
        if self.rain_floor:
            Drop(
                surf=choice(self.rain_floor), 
                pos=(randint(0, self.floor_w), randint(0, self.floor_h)), 
                moving=False, 
                groups=self.all_sprites, 
                z=LAYERS['rain floor'])

    def create_drops(self):
        """Create a moving rain drop."""
        if self.rain_drops:
            Drop(
                surf=choice(self.rain_drops), 
                pos=(randint(0, self.floor_w), randint(0, self.floor_h)), 
                moving=True, 
                groups=self.all_sprites, 
                z=LAYERS['rain drops'])

    def update(self):
        """Create new rain drops based on weather cycle timing."""
        current_time = pygame.time.get_ticks()
        
        if self.is_raining:
            # Currently raining - check if 3 minutes are up
            if current_time >= self.rain_end_time:
                self.is_raining = False
                # Schedule next rain period (random delay between 2-8 minutes)
                self.next_rain_time = current_time + randint(120000, 480000)  # 2-8 minutes
        else:
            # Not raining - check if it's time to start raining
            if current_time >= self.next_rain_time:
                self.is_raining = True
                self.rain_end_time = current_time + self.rain_duration  # 3 minutes from now
        
        # Only spawn rain drops if currently raining
        if self.is_raining:
            self.create_floor()
            self.create_drops()
