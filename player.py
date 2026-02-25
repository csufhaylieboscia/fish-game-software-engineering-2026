import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=3):
        super().__init__()

        self.scale = scale
        self.frame_width  = 96
        self.frame_height = 64

        # idle and run animation strips
        idle_sheet = pygame.image.load("assets/Sprites/spr_idle_strip9.png").convert_alpha()
        run_sheet  = pygame.image.load("assets/Sprites/spr_run_strip8.png").convert_alpha()

        self.animations = {
            "idle": self._load_strip(idle_sheet, num_frames=9),
            "run":  self._load_strip(run_sheet,  num_frames=8),
        }

        self.current_anim    = "idle"
        self.frame_index     = 0
        self.animation_speed = 100      
        self.last_update     = pygame.time.get_ticks()
        self.facing_right    = True

        self.image = self.animations["idle"][0]
        self.rect  = self.image.get_rect(topleft=(x, y))

    def _load_strip(self, sheet, num_frames):
        """Slice every frame from a horizontal strip and scale it."""
        frames = []
        for i in range(num_frames):
            frame = sheet.subsurface((
                i * self.frame_width,
                0,
                self.frame_width,
                self.frame_height
            ))
            scaled = pygame.transform.scale(
                frame,
                (self.frame_width * self.scale, self.frame_height * self.scale)
            )
            frames.append(scaled)
        return frames

    def set_animation(self, name):
        """Switch animation, restarting from frame 0 if it changed."""
        if name != self.current_anim and name in self.animations:
            self.current_anim = name
            self.frame_index  = 0

    def update(self, keys):
        # Movement input handling
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x     -= 4
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x     += 4
            self.facing_right = True
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= 4
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += 4
            moving = True

        self.set_animation("run" if moving else "idle")

        # Handle animation frame updates
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])

        # Flip frame if facing left
        frame = self.animations[self.current_anim][self.frame_index]
        self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)
