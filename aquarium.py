import pygame

def aquarium_loop(screen, clock):
    """
    Placeholder aquarium interior screen.
    Press ESC or ENTER to leave and return to the overworld.
    """
    font_hint = pygame.font.SysFont("Arial", 28)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return None  # return to overworld

        screen_w, screen_h = screen.get_size()
        screen.fill((30, 80, 180))  # blue placeholder

        hint = font_hint.render("Press ESC or ENTER to leave", True, (255, 255, 255))
        screen.blit(hint, hint.get_rect(center=(screen_w // 2, screen_h // 2)))

        pygame.display.flip()
        clock.tick(60)
        