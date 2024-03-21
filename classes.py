import pygame
from random import randint


class IntroScreen:
    pass


class GameOverScreen:
    pass


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.element = pygame.image.load('assets/element.png').convert_alpha()
        # snake image elements
        self.body = [self.element, self.element]
        self.element_x = 0
        self.element_y = 0
        # snake sprite image and rect
        self.image = None
        self.rect = None
        # draw snake at object creation
        self.draw_snake()

    def draw_snake(self):
        image_height = max([item.get_height() for item in self.body])
        image_width = sum([item.get_width() for item in self.body])
        self.image = pygame.Surface((image_width, image_height))
        self.image.fill((169, 224, 0))
        for body_element in self.body:
            self.image.blit(body_element, (self.element_x, self.element_y))
        self.element_x += image_width
        self.element_y += image_height
        self.rect = self.image.get_rect(midbottom=(680, 400))

    def has_collision(self, other_object):
        if isinstance(other_object, PixelFrame):
            if pygame.Rect.colliderect(self.rect, other_object.rect):
                return True
            return False
        else:
            if pygame.sprite.spritecollide(snake.sprite, other_object, True):
                return True
            return False

    def grow(self, eat_feed: bool):
        if eat_feed:
            self.body.append(self.element)

    # make the snake "break" on turn
    # when snake in horizontal position - should turn around
    # work on the collision with frame
    def get_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.rect.top > 87:
                self.rect.move_ip(0, -1)
        elif keys[pygame.K_DOWN]:
            if self.rect.bottom < 620:
                self.rect.move_ip(0, 1)
        elif keys[pygame.K_LEFT] and self.rect.left > 44:
            self.rect.move_ip(-1, 0)
        elif keys[pygame.K_RIGHT] and self.rect.right < 758:
            self.rect.move_ip(1, 0)

    def animate(self):
        pass

    def update(self):
        self.get_player_input()


class Feed(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/feed.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(randint(88, 759), randint(95, 619)))

    # fix so that new feed doesn't collide with the frame
    # a method to keep adding new sprites at random locations within the frame and deleting when collision occurs


class PixelFrame:
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

key_press = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_DOWN):
            key_press += 1
    if setup.game_active:
        setup.screen.blit(setup.background_surf, (0, 0))
        setup.screen.blit(setup.score_board, setup.score_rect)
        feed.draw(setup.screen)
        snake.draw(setup.screen)
        snake.update()

    pygame.display.update()
    setup.clock.tick(60)
