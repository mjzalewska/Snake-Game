import pygame
from random import randint


class Snake(pygame.sprite.Sprite):
    pass


class Feed(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/feed.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(100, 300))

    def _set_location(self):
        pass


class IntroScreen:
    pass


class GameOverScreen:
    pass


class PixelFrame:
    def __init__(self, surface):
        self.surface = surface
        self._draw_frame()

    def _draw_horizontal_dashed_line(self, start: int, end: int, distance_from_top: int):
        gap = 0
        dash_len = 3
        while start + gap < end:
            pygame.draw.line(self.surface, 'black', (start + gap, distance_from_top),
                             (start + gap + dash_len, distance_from_top), 5)
            gap += 5

    def _draw_vertical_dashed_line(self, start: int, end: int, distance_from_left: int):
        gap = 0
        dash_len = 3
        while distance_from_left + gap < end:
            pygame.draw.line(self.surface, 'black', (start, distance_from_left + gap),
                             (start + dash_len, distance_from_left + gap), 5)
            gap += 7

    def _draw_frame(self):
        self._draw_horizontal_dashed_line(40, 760, 70)
        self._draw_horizontal_dashed_line(40, 760, 87)
        self._draw_horizontal_dashed_line(40, 760, 620)
        self._draw_vertical_dashed_line(40, 620, 94)
        self._draw_vertical_dashed_line(755, 620, 94)


class GameConfig:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 672))
        self.background_surf = pygame.image.load('assets/background.png').convert()
        self.game_frame = PixelFrame(self.background_surf)
        self.game_font = pygame.font.Font('fonts/01Digit.ttf', 50)
        self.score_board = None
        self.score_rect = None
        self._set_window_caption()
        self.render_score_board('36') ## to do przemyślenia
        self.clock = pygame.time.Clock()
        self.game_active = True

    @staticmethod
    def _set_window_caption():
        pygame.display.set_caption("Retro Snake")

    def render_score_board(self, score):
        self.score_board = self.game_font.render(score, False, 'black')
        self.score_rect = self.score_board.get_rect(center=(95, 42))


setup = GameConfig()
feed = pygame.sprite.GroupSingle()
feed.add(Feed())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if setup.game_active:
        setup.screen.blit(setup.background_surf, (0, 0))
        setup.screen.blit(setup.score_board, setup.score_rect)
        feed.draw(setup.screen)

    pygame.display.update()
    setup.clock.tick(60)
