import pygame
import os
import math
import random
from pygame import mixer

AUQUA = (0, 123, 173)
RED = (255, 0, 0)
NAVY = (0, 0, 128)
GREEN = (102, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

Base_Dir = os.path.dirname(os.path.abspath(__file__))
Assets_Dir = os.path.join(Base_Dir, "assets")
Backgroun_Dir = os.path.join(Assets_Dir, "UnderWater")
caught_fish_sound = os.path.join(Assets_Dir, "MUSIC/SoundEffects/getItemLOZ.mp3")

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
allObjectsList = pygame.sprite.Group()


# Sparkle class for the celebration screen
class Sparkle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(150, 650)
        self.y = random.randint(150, 450)
        self.radius = random.uniform(2, 6)
        self.alpha = random.randint(180, 255)
        self.fade_speed = random.uniform(3, 7)
        self.drift_x = random.uniform(-0.5, 0.5)
        self.drift_y = random.uniform(-1.5, -0.3)
        # 40% chance to be a star shape instead of a circle
        self.is_star = random.random() > 0.4
        # Colour: gold, white, cyan, or pink sparkles
        self.color = random.choice([
            (255, 255, 180),   # pale gold
            (255, 255, 255),   # white
            (180, 255, 255),   # ice blue
            (255, 180, 255),   # pink
            (255, 220, 80),    # bright gold
        ])

    def update(self):
        self.x += self.drift_x
        self.y += self.drift_y
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.reset()

    def draw(self, surf):
        if self.alpha <= 0:
            return
        color = (*self.color, int(self.alpha))
        tmp = pygame.Surface((int(self.radius * 2 + 4), int(self.radius * 2 + 4)), pygame.SRCALPHA)
        cx = cy = int(self.radius + 2)

        if self.is_star:
            _draw_star(tmp, color, cx, cy, int(self.radius), int(self.radius * 0.4))
        else:
            pygame.draw.circle(tmp, color, (cx, cy), int(self.radius))

        surf.blit(tmp, (int(self.x - self.radius - 2), int(self.y - self.radius - 2)))


# Helper function to draw a star shape
def _draw_star(surf, color, cx, cy, outer, inner, points=5):
    verts = []
    for i in range(points * 2):
        angle = math.pi / points * i - math.pi / 2
        r = outer if i % 2 == 0 else inner
        verts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    if len(verts) >= 3:
        pygame.draw.polygon(surf, color, verts)


# "You Caught It!" celebration screen
def you_caught_it_screen(scaled_bg):
    clock = pygame.time.Clock()
    timer = 0.0

    # Pre-build a pool of sparkles
    sparkles = [Sparkle() for _ in range(60)]
    # Stagger their starting alpha so they don't all appear at once
    for sp in sparkles:
        sp.alpha = random.randint(0, 255)

    # Font settings
    base_font_size = 64
    font_path = None  # use system font

    bg_index = 0
    bg_timer = 0
    bg_interval = 15  # frames between background swaps

    frame = 0

    while True:
        dt = clock.tick(60) / 1000.0
        timer += dt
        frame += 1

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return          # dismiss and continue
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        # update background animation
        bg_timer += 1
        if bg_timer >= bg_interval:
            bg_timer = 0
            bg_index = (bg_index + 1) % len(scaled_bg)
        surface.blit(scaled_bg[bg_index], (0, 0))

        # semi-transparent dark overlay to make text pop
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        # sparkles
        for sp in sparkles:
            sp.update()
            sp.draw(surface)

        # Bouncy text
        pulse = 1.0 + 0.18 * math.sin(timer * 4.5)
        # Secondary wobble: fast little jiggles
        wobble = 1.0 + 0.05 * math.sin(timer * 13.0)
        scale_factor = pulse * wobble

        font_size = max(12, int(base_font_size * scale_factor))
        font = pygame.font.SysFont("Arial", font_size, bold=True)

        # Rainbow colour cycle
        r = int(127 + 127 * math.sin(timer * 2.5))
        g = int(127 + 127 * math.sin(timer * 2.5 + 2.1))
        b = int(127 + 127 * math.sin(timer * 2.5 + 4.2))
        text_color = (r, g, b)

        # Gold outline / shadow for depth
        shadow_font = pygame.font.SysFont("Arial", font_size, bold=True)
        shadow_surf = shadow_font.render("You Caught It!", True, (80, 60, 0))
        main_surf   = font.render("You Caught It!", True, text_color)

        cx, cy = SCREEN_WIDTH // 2, 80

        # Draw shadow offset slightly
        shadow_rect = shadow_surf.get_rect(center=(cx + 3, cy + 3))
        surface.blit(shadow_surf, shadow_rect)

        # Draw main text
        main_rect = main_surf.get_rect(center=(cx, cy))
        surface.blit(main_surf, main_rect)

        # 'press space' hint with a gentle fade in/out
        hint_alpha = int(180 + 75 * math.sin(timer * 3))
        hint_font  = pygame.font.SysFont("Arial", 22)
        hint_surf  = hint_font.render("Press SPACE to continue", True, (220, 220, 220))
        hint_surf.set_alpha(hint_alpha)
        hint_rect = hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        surface.blit(hint_surf, hint_rect)

        pygame.display.flip()


def runBackgroundAnimation(bg_index, scaled_bg):
    bg_index += 1
    if bg_index >= len(scaled_bg):
        bg_index = 0
    return bg_index           