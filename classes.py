import pygame
from random import randint

GRIDSIZE = 21


class IntroScreen:
    pass


class GameOverScreen:
    pass


class Snake(pygame.sprite.Sprite):
    def __init__(self, group, position, length, parent=None):
        super().__init__(group)
        self.length = length
        self.parent = parent
        self.child = None
        self.direction = 'UP'
        self.image = pygame.image.load('assets/element.png').convert_alpha()
        self.position = position
        self.rect = self.image.get_rect(x=self.position[0] * GRIDSIZE, y=self.position[1] * GRIDSIZE)
        if length > 1:
            self.child = Snake(group, (position[0], position[1] + 1), length - 1, self)

    def move(self):
        parent_direction = self.parent.direction if self.parent else None

        if self.direction == 'UP':
            self.position = self.position[0], self.position[1] - 1
        elif self.direction == 'DOWN':
            self.position = self.position[0], self.position[1] + 1
        elif self.direction == 'LEFT':
            self.position = self.position[0] - 1, self.position[1]
        elif self.direction == 'RIGHT':
            self.position = self.position[0] + 1, self.position[1]

        self.rect = self.image.get_rect(x=self.position[0] * GRIDSIZE, y=self.position[1] * GRIDSIZE)

        if self.child:
            self.child.move()

        if parent_direction:
            self.direction = parent_direction

    def grow(self, eat_feed: bool):
        if eat_feed:
            self.length += 1

    def update(self):
        if not self.parent:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction = 'UP'
            elif keys[pygame.K_DOWN]:
                self.direction = 'DOWN'
            elif keys[pygame.K_LEFT]:
                self.direction = 'LEFT'
            elif keys[pygame.K_RIGHT]:
                self.direction = 'RIGHT'

    def is_collision(self, other_object):
        pass
        # self.rect.top > 87
        # self.rect.bottom < 620
        # self.rect.left > 44
        # self.rect.right < 758

    # def update(self): # sprawdzić też to
    #     self.get_direction()
    # self.move()


class Feed(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/feed.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(randint(88, 759), randint(95, 619)))
    # fix so that new feed doesn't collide with the frame
    # a method to keep adding new sprites at random locations within the frame and deleting when collision occurs


class Frame:
    def __init__(self, surface):
        self.surface = surface
        self.rect = self.surface.get_rect()
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
        self._draw_horizontal_dashed_line(40, 760, 75)
        self._draw_horizontal_dashed_line(40, 760, 620)
        self._draw_vertical_dashed_line(40, 620, 75)
        self._draw_vertical_dashed_line(754, 620, 75)


class GameConfig:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 672))
        self.background_surf = pygame.image.load('assets/background.png').convert()
        self.game_frame = Frame(self.background_surf)
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
        self.score_rect = self.score_board.get_rect(center=(70, 50))


setup = GameConfig()

snake_sprites = pygame.sprite.Group()
snake = Snake(snake_sprites, (10, 10), 4)
snake_sprites.add(snake)

feed_sprite = pygame.sprite.GroupSingle()
feed = Feed()
feed_sprite.add(feed)

MOVE = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE, 300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == MOVE:
            snake.move()

    if setup.game_active:
        setup.screen.blit(setup.background_surf, (0, 0))
        setup.screen.blit(setup.score_board, setup.score_rect)
        feed_sprite.draw(setup.screen)
        snake_sprites.update()
        snake_sprites.draw(setup.screen)

    setup.clock.tick(60)
    pygame.display.update()
