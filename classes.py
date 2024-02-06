import pygame
from random import randint


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        snake_head = pygame.image.load('assets/snake_head.png').convert_alpha()
        snake_head_jaws = pygame.image.load('assets/snake_eat.png').convert_alpha()
        snake_tail = pygame.image.load('assets/snake_tail.png').convert_alpha()
        snake_belly = pygame.image.load('assets/snake_body.png').convert_alpha()
        self.snake_eat = [snake_head, snake_head_jaws]
        self.snake_head_idx = 0
        self.snake_full_body = [self.snake_eat[self.snake_head_idx], snake_belly, snake_tail]
        self.image = None
        self.rect = None
        self.draw_snake()

    def draw_snake(self):
        total_height = max([item.get_height() for item in self.snake_full_body])
        total_width = sum([item.get_width() for item in self.snake_full_body])
        self.image = pygame.Surface((total_width, total_height))
        self.image.fill((169, 224, 0))
        self.image.blit(self.snake_full_body[0], (0,0))
        self.image.blit(self.snake_full_body[1], (self.snake_full_body[0].get_width()-10, 12))
        self.image.blit(self.snake_full_body[2], (self.snake_full_body[0].get_width()+self.snake_full_body[1].get_width()-15, 12))
        self.rect = self.image.get_rect(midbottom=(200, 200))


    def move(self):
        pass


class Feed(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/feed.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(randint(88, 759), randint(95, 619)))

    # a method to keep adding new sprites at random locations within the frame and deleting when collision occurs


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
        dash_len = 4
        while start + gap < end:
            pygame.draw.line(self.surface, 'black', (start + gap, distance_from_top),
                             (start + gap + dash_len, distance_from_top), 6)
            gap += 6

    def _draw_vertical_dashed_line(self, start: int, end: int, distance_from_left: int):
        gap = 0
        dash_len = 4
        while distance_from_left + gap < end:
            pygame.draw.line(self.surface, 'black', (start, distance_from_left + gap),
                             (start + dash_len, distance_from_left + gap), 6)
            gap += 7

    def _draw_frame(self):
        self._draw_horizontal_dashed_line(40, 760, 70)
        self._draw_horizontal_dashed_line(40, 760, 87)
        self._draw_horizontal_dashed_line(40, 760, 620)
        self._draw_vertical_dashed_line(40, 620, 94)
        self._draw_vertical_dashed_line(754, 620, 94)


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
        self.render_score_board('36')  ## to be refactored
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

snake = pygame.sprite.GroupSingle()
snake.add(Snake())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if setup.game_active:
        setup.screen.blit(setup.background_surf, (0, 0))
        setup.screen.blit(setup.score_board, setup.score_rect)
        feed.draw(setup.screen)
        snake.draw(setup.screen)

    pygame.display.update()
    setup.clock.tick(60)
