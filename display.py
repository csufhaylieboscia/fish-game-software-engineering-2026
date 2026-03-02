import pygame

BASE_W = 800
BASE_H = 600

class Display:
    def __init__(self):
        self.window = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)
        self.render_surface = pygame.Surface((BASE_W, BASE_H)).convert_alpha()

        self.is_fullscreen = False
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.recalculate()

    def recalculate(self):
        w, h = self.window.get_size()
        self.scale = min(w / BASE_W, h / BASE_H)
        scaled_w = int(BASE_W * self.scale)
        scaled_h = int(BASE_H * self.scale)
        self.offset_x = (w - scaled_w) // 2
        self.offset_y = (h - scaled_h) // 2

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE and not self.is_fullscreen:
            self.window = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            self.recalculate()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            self.toggle_fullscreen()

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.window.display.quit()
            self.window.display.init()
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window.display.quit()
            self.window.display.init()
            self.window = pygame.display.set_mode((BASE_W, BASE_H), pygame.SCALED)
        self.recalculate()

    def present(self):
        self.window.fill((0, 0, 0))
        scaled_w = int(BASE_W * self.scale)
        scaled_h = int(BASE_H * self.scale)
        frame = pygame.transform.smoothscale(self.render_surface, (scaled_w, scaled_h))
        self.window.blit(frame, (self.offset_x, self.offset_y))
        pygame.display.flip()

    def get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        x = (mx - self.offset_x) / self.scale
        y = (my - self.offset_y) / self.scale
        return (x, y)