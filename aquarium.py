import pygame
import os
import math
import random

Base_Dir = os.path.dirname(os.path.abspath(__file__))
Assets_Dir = os.path.join(Base_Dir, "assets")
FishSprite_Dir = os.path.join(Assets_Dir, "Sprites", "FishSprites")

# Fish objects added here will swim in the aquarium.
caught_fish_registry = []   # list of Fish objects caught this session


def add_caught_fish(fish):
    """Call this after a successful catch to register the fish in the aquarium."""
    # avoid exact duplicates of the same object instance
    if fish not in caught_fish_registry:
        caught_fish_registry.append(fish)



# Fish swimming sprite and background drawing code
FISH_SIZE = 80   # target height in pixels for aquarium display

class SwimmingFish(pygame.sprite.Sprite):
    """A caught fish that "swims" back and forth in the aquarium."""

    def __init__(self, fish_obj, screen_w, screen_h, index, total):
        super().__init__()
        self.fish_obj = fish_obj
        self.screen_w = screen_w
        self.screen_h = screen_h

        # Load & scale sprite
        path = os.path.join(FishSprite_Dir, fish_obj.imagePath)
        raw = pygame.image.load(path).convert_alpha()
        tw, th = raw.get_size()
        ratio = tw / th
        self.base_image = pygame.transform.scale(raw, (int(FISH_SIZE * ratio), FISH_SIZE))
        self.image = self.base_image

        # Spread fish vertically so they don't all stack
        band_h = (screen_h - 160) // max(total, 1)
        base_y = 80 + index * band_h + band_h // 2
        self.y = float(base_y + random.randint(-20, 20))
        self.x = float(random.randint(80, screen_w - 80))

        # Horizontal drift speed & direction
        self.speed = random.uniform(0.6, 1.6)
        self.direction = random.choice([-1, 1])

        # Sine-wave bobbing
        self.bob_offset = random.uniform(0, math.pi * 2)
        self.bob_amp    = random.uniform(6, 18)
        self.bob_speed  = random.uniform(0.8, 1.6)

        self.timer = 0.0
        self.rect = self.image.get_rect()

    def update(self, dt, screen_w, screen_h):
        self.timer += dt
        self.screen_w = screen_w
        self.screen_h = screen_h

        # Horizontal movement
        self.x += self.speed * self.direction
        margin = self.image.get_width() // 2 + 20
        if self.x > screen_w - margin:
            self.x = screen_w - margin
            self.direction = -1
        elif self.x < margin:
            self.x = margin
            self.direction = 1

        # Vertical bobbing
        bob_y = self.bob_amp * math.sin(self.timer * self.bob_speed + self.bob_offset)
        draw_y = self.y + bob_y

        # Flip image based on swim direction
        if self.direction == -1:
            self.image = self.base_image
        else:
            self.image = pygame.transform.flip(self.base_image, True, False)

        self.rect = self.image.get_rect(center=(int(self.x), int(draw_y)))



# Bubble particle class for background effect
class Bubble:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self._spawn()

    def _spawn(self):
        self.x = random.randint(20, self.screen_w - 20)
        self.y = float(self.screen_h + random.randint(0, 80))
        self.radius = random.randint(3, 9)
        self.speed  = random.uniform(0.4, 1.2)
        self.drift  = random.uniform(-0.3, 0.3)
        self.alpha  = random.randint(60, 140)

    def update(self, dt):
        self.y -= self.speed * 60 * dt
        self.x += self.drift
        if self.y < -self.radius * 2:
            self._spawn()

    def draw(self, surface):
        tmp = pygame.Surface((self.radius * 2 + 2, self.radius * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(tmp, (200, 230, 255, self.alpha),
                           (self.radius + 1, self.radius + 1), self.radius)
        pygame.draw.circle(tmp, (220, 245, 255, max(0, self.alpha - 40)),
                           (self.radius + 1, self.radius + 1), self.radius, 1)
        surface.blit(tmp, (int(self.x) - self.radius - 1, int(self.y) - self.radius - 1))


# Background drawing functions for the aquarium screen

def _draw_water_background(surface, screen_w, screen_h, timer):
    """Layered gradient water background with a shimmer."""
    # Deep gradient: top (mid-blue) -> bottom (dark navy)
    top_color = (20,  70, 130)
    bottom_color = (5,   20,  55)
    for y in range(screen_h):
        t = y / screen_h
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (screen_w, y))

    # gleaming light shafts
    shaft_surf = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
    num_shafts = 6
    for i in range(num_shafts):
        phase = timer * 0.4 + i * (math.pi * 2 / num_shafts)
        cx = int(screen_w * (0.1 + 0.8 * (i / (num_shafts - 1))) +
                 30 * math.sin(phase))
        width = int(40 + 20 * math.sin(phase * 1.3))
        alpha = int(18 + 12 * math.sin(phase * 0.7))
        pts = [(cx - width, 0), (cx + width, 0),
               (cx + width * 2, screen_h), (cx - width * 2, screen_h)]
        pygame.draw.polygon(shaft_surf, (180, 220, 255, alpha), pts)
    surface.blit(shaft_surf, (0, 0))

    # Seabed strip at bottom
    seabed_h = int(screen_h * 0.12)
    seabed_rect = pygame.Rect(0, screen_h - seabed_h, screen_w, seabed_h)
    pygame.draw.rect(surface, (40, 28, 15), seabed_rect)

    # Sand ripples
    for i in range(0, screen_w, 28):
        sx = i + int(6 * math.sin(timer * 0.5 + i * 0.1))
        sy = screen_h - seabed_h + 6
        pygame.draw.arc(surface, (70, 50, 25),
                        pygame.Rect(sx, sy, 26, 10), 0, math.pi, 2)

    # seaweed along the bottom
    weed_positions = [int(screen_w * f) for f in [0.08, 0.22, 0.45, 0.67, 0.85]]
    for wx in weed_positions:
        _draw_seaweed(surface, wx, screen_h - seabed_h, timer)


# seaweed drawing helper
def _draw_seaweed(surface, x, base_y, timer):
    segments = 7
    seg_len  = 14
    for i in range(segments):
        t   = i / segments
        sway = 8 * math.sin(timer * 1.2 + x * 0.05 + i * 0.6)
        x1  = x + int(sway * t)
        y1  = base_y - i * seg_len
        x2  = x + int(sway * (t + 1 / segments))
        y2  = y1 - seg_len
        green = (20 + int(40 * t), 110 + int(50 * t), 30)
        pygame.draw.line(surface, green, (x1, y1), (x2, y2), max(1, 4 - i // 2))


# UI drawing functions for the aquarium screen
def _draw_ui_frame(surface, screen_w, screen_h, font):
    """Semi-transparent top bar with title and hint."""
    bar = pygame.Surface((screen_w, 48), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 140))
    surface.blit(bar, (0, 0))

    title = font.render("My Aquarium", True, (200, 240, 255))
    surface.blit(title, (16, 10))

    hint_font = pygame.font.SysFont("Arial", 16)
    hint = hint_font.render("Press ESC or ENTER to leave", True, (160, 200, 220))
    surface.blit(hint, hint.get_rect(topright=(screen_w - 12, 14)))


def _draw_empty_message(surface, screen_w, screen_h):
    font = pygame.font.SysFont("Arial", 26, italic=True)
    msg = font.render("Catch some fish to fill your aquarium!", True, (140, 190, 230))
    surface.blit(msg, msg.get_rect(center=(screen_w // 2, screen_h // 2)))


# Main loop for the aquarium screen
def aquarium_loop(screen, clock):
    """
    Aquarium interior screen.  Shows all fish caught this session swimming
    in a decorated water environment.  Press ESC or ENTER to return to the
    overworld.
    """
    screen_w, screen_h = screen.get_size()

    title_font = pygame.font.SysFont("Arial", 24, bold=True)

    # Build swimming sprites from the registry
    def _build_sprites(sw, sh):
        group = pygame.sprite.Group()
        total = len(caught_fish_registry)
        for i, fish in enumerate(caught_fish_registry):
            group.add(SwimmingFish(fish, sw, sh, i, total))
        return group

    fish_group = _build_sprites(screen_w, screen_h)

    # bubbles
    bubbles = [Bubble(screen_w, screen_h) for _ in range(30)]

    timer = 0.0

    while True:
        dt = clock.tick(60) / 1000.0
        timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return None  # back to overworld

        # If window resized, rebuild sprites for new size
        new_w, new_h = screen.get_size()
        if (new_w, new_h) != (screen_w, screen_h):
            screen_w, screen_h = new_w, new_h
            fish_group = _build_sprites(screen_w, screen_h)
            bubbles = [Bubble(screen_w, screen_h) for _ in range(30)]

        # Draw background, fish, and UI
        _draw_water_background(screen, screen_w, screen_h, timer)

        for bubble in bubbles:
            bubble.update(dt)
            bubble.draw(screen)

        fish_group.update(dt, screen_w, screen_h)
        fish_group.draw(screen)

        if not caught_fish_registry:
            _draw_empty_message(screen, screen_w, screen_h)

        _draw_ui_frame(screen, screen_w, screen_h, title_font)

        pygame.display.flip()
