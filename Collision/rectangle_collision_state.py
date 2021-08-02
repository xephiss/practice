import pygame

class RectangleCollisionState:
    def __init__(self, window_surface):
        self.transition_target = None
        self.window_surface = window_surface

        self.title_font = pygame.font.Font(None, 64)
        self.instructions_font = pygame.font.Font(None, 32)

        self.background_surf = None
        self.title_text = None
        self.title_pos_rect = None
        self.instructions_text = None
        self.instructions_text_pos_rect = None

    def start(self):
        self.transition_target = None
        self.background_surf = pygame.Surface((800, 600))
        self.background_surf.fill((0, 0, 0))

        self.title_text = self.title_font.render('Rectangle Collision', True, (255, 255, 255))
        self.title_pos_rect = self.title_text.get_rect()
        self.title_pos_rect.center = (400, 50)

        self.instructions_text = self.instructions_font.render('Press ESC to return to main menu',
                                                               True, (255, 255, 255))

        self.instructions_text_pos_rect = self.instructions_text.get_rect()
        self.instructions_text_pos_rect.center = (400, 100)

    def stop(self):
        self.background_surf = None
        self.title_text = None
        self.title_pos_rect = None
        self.instructions_text = None
        self.instructions_text_pos_rect = None

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.transition_target = 'main_menu'

    def update(self, time_delta):
        # clear the window to the background surface
        self.window_surface.blit(self.background_surf, (0, 0))
        # stick the title at the top
        self.window_surface.blit(self.title_text, self.title_pos_rect)
        # stick the instructions below
        self.window_surface.blit(self.instructions_text, self.instructions_text_pos_rect)


