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

    def grow(self):
        if self.is_collision_w_self():
            self.length += 1

    def is_collision_w_self(self):
        head = self
        current_segment = self.child

        while current_segment is not None:
            if head.rect.colliderect(current_segment.rect):
                return True
            current_segment = current_segment.child
        else:
            return False

    @staticmethod
    def is_collision_w_feed():
        if pygame.sprite.spritecollide(feed, snake_sprites, False):
            print("Feed Collision")
            return True
        else:
            return False

    def is_collision_w_frame(self):
        if (self.rect.colliderect(setup.game_frame.top_frame_rect) or
                self.rect.colliderect(setup.game_frame.bottom_frame_rect) or
                self.rect.colliderect(setup.game_frame.left_frame_rect) or
                self.rect.colliderect(setup.game_frame.right_frame_rect)):
            print("Frame collision")
            return True
        else:
            return False

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


class Feed(pygame.sprite.Sprite):  # 28x24
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/feed.png').convert_alpha()
        self.rect = self.image.get_rect(center=(randint(40+self.image.get_width()//2, 760-self.image.get_width()//2),
                                                randint(75+self.image.get_height()//2, 620-self.image.get_height()//2)))


class Frame:
    def __init__(self, surface):
        self.surface = surface
        # self.rect = self.surface.get_rect()
        self.dash_len = 4
        self.frame_thickness = 6
        self.top_frame_start = (40, 75)
        self.bottom_frame_start = (40, 620)
        self.left_frame_start = (40, 75)
        self.right_frame_start = (754, 75)
        self.frame_width = 720
        self.frame_height = 580
        # drawing custom Rects for the frame segments
        self.top_frame_rect = pygame.Rect(self.top_frame_start, (self.frame_width, self.frame_thickness))
        self.bottom_frame_rect = pygame.Rect(self.bottom_frame_start, (self.frame_width, self.frame_thickness))
        self.left_frame_rect = pygame.Rect(self.left_frame_start, (self.frame_thickness, self.frame_height))
        self.right_frame_rect = pygame.Rect(self.right_frame_start, (self.frame_thickness, self.frame_height))
        self._draw_frame()

    def _draw_horizontal_dashed_line(self, start: int, end: int, distance_from_top: int):
        dash_gap = 0
        while start + dash_gap < end:
            pygame.draw.line(self.surface, 'black', (start + dash_gap, distance_from_top),
                             (start + dash_gap + self.dash_len, distance_from_top), self.frame_thickness)
            dash_gap += 6

    def _draw_vertical_dashed_line(self, start: int, end: int, distance_from_left: int):
        dash_gap = 0
        while distance_from_left + dash_gap < end:
            pygame.draw.line(self.surface, 'black', (start, distance_from_left + dash_gap),
                             (start + self.dash_len, distance_from_left + dash_gap), self.frame_thickness)
            dash_gap += 7

    def _draw_frame(self):
        self._draw_horizontal_dashed_line(40, 760, 75)
        self._draw_horizontal_dashed_line(40, 760, 620)
        self._draw_vertical_dashed_line(40, 620, 75)
        self._draw_vertical_dashed_line(754, 620, 75)


score = 0


class GameConfig:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 672))
        self.background_surf = pygame.image.load('assets/background.png').convert()
        self.game_frame = Frame(self.background_surf)
        self.game_font = pygame.font.Font('fonts/Minimal3x5.ttf', 60)
        self.score_board = None
        self.score_rect = None
        self._set_window_caption()
        self.render_score_board(f'0{score}' if score < 10 else f'{score}')  ## to be refactored
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
        # print(is_collision_w_frame())
        # print(is_collision_w_feed())

    setup.clock.tick(60)
    pygame.display.update()
