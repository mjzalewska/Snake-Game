import pygame
from random import randint


class IntroScreen:
    pass


class GameOverScreen:
    pass


class Snake(pygame.sprite.Sprite):
    def __init__(self, group, position, length, parent=None):
        super().__init__()
        self.length = length
        self.parent = parent
        self.child = None
        self.image = pygame.image.load('assets/element.png').convert_alpha()
        self.position = position
        self.direction = (0, 0)
        self.rect = self.image.get_rect(x=position[0], y=position[1])
        if length > 1:
            self.child = Snake(group, (position[0]+21, position[1]), self.length - 1, self)
            group.add(self.child)

    def grow(self, eat_feed: bool):
        if eat_feed:
            self.length += 1

    def get_player_input(self):
        if not self.parent:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction = (0, -1)
            elif keys[pygame.K_DOWN]:
                self.direction = (0, 1)
            elif keys[pygame.K_LEFT]:
                self.direction = (-1, 0)
            elif keys[pygame.K_RIGHT]:
                self.direction = (1, 0)

    def move(self):
        parent_direction = self.parent.direction if self.parent else None
        new_position = self.position[0] + self.direction[0], self.position[1] + self.direction[1]
        self.position = new_position
        self.rect = self.image.get_rect(x=self.position[0], y=self.position[1])

        if self.child:
            self.child.move()

        if parent_direction:
            self.direction = parent_direction

    def has_collision(self, other_object):
        pass
        # self.rect.top > 87
        # self.rect.bottom < 620
        # self.rect.left > 44
        # self.rect.right < 758

    def update(self):
        self.get_player_input()
        self.move()


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
        self.score_rect = self.score_board.get_rect(center=(95, 42))


setup = GameConfig()

snake_sprites = pygame.sprite.Group()
snake = Snake(snake_sprites, (100, 400), 5)
snake_sprites.add(snake)

feed_sprite = pygame.sprite.GroupSingle()
feed = Feed()
feed_sprite.add(feed)

# key_press = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if setup.game_active:
        setup.screen.blit(setup.background_surf, (0, 0))
        setup.screen.blit(setup.score_board, setup.score_rect)
        feed_sprite.draw(setup.screen)
        snake_sprites.update()
        snake_sprites.draw(setup.screen)

    pygame.display.update()
    setup.clock.tick(60)
