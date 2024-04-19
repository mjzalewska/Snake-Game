from time import sleep

import pygame
from random import randint

GRIDSIZE = 21


class StartScreen:
    def __init__(self):
        self.title_font = pygame.font.Font('fonts/Minimal3x5.ttf', 100)
        self.message_font = pygame.font.Font('fonts/Minimal3x5.ttf', 50)
        self.game_title = self.title_font.render('SNAKE', False, (55, 125, 34))
        self.game_title_rect = self.game_title.get_rect(center=(400, 135))
        self.start_message = self.message_font.render('Press Enter to start', False, (55, 125, 34))
        self.start_message_rect = self.start_message.get_rect(center=(400, 450))
        self.quit_message = self.message_font.render('Press Esc to quit', False, (55, 125, 34))
        self.quit_message_rect = self.quit_message.get_rect(center=(400, 500))
        self.logo = pygame.image.load('assets/snake_logo.png').convert_alpha()
        self.logo_rect = self.logo.get_rect(center=(400, 290))

    def show(self):
        game.screen.fill((169, 224, 0))
        game.screen.blit(self.game_title, self.game_title_rect)
        game.screen.blit(self.logo, self.logo_rect)
        game.screen.blit(self.start_message, self.start_message_rect)
        game.screen.blit(self.quit_message, self.quit_message_rect)


class GameOverScreen:
    def __init__(self):
        self.go_font = pygame.font.Font('fonts/Minimal3x5.ttf', 100)
        self.message_font = pygame.font.Font('fonts/Minimal3x5.ttf', 50)
        self.go_sign = self.go_font.render('Game over', False, (55, 125, 34))
        self.message_rect = self.go_sign.get_rect(center=(400, 300))
        self.restart_message = self.message_font.render('Press Space to restart', False, (55, 125, 34))
        self.restart_message_rect = self.restart_message.get_rect(center=(400, 450))
        self.quit_message = self.message_font.render('Press Esc to quit', False, (55, 125, 34))
        self.quit_message_rect = self.quit_message.get_rect(center=(400, 500))

    def show(self):
        game.screen.fill((169, 224, 0))
        game.screen.blit(self.go_sign, self.message_rect)
        game.screen.blit(self.restart_message, self.restart_message_rect)
        game.screen.blit(self.quit_message, self.quit_message_rect)


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
        self.rect.height = 20
        self.rect.width = 20
        if length > 1:
            self.child = Snake(group, (position[0], position[1]), self.length - 1, self)
            # self.child = Snake(group, (position[0], position[1] + 1), self.length - 1, self)

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
        tail = self
        while tail.child:
            tail = tail.child

        new_segment = Snake(self.groups(), (tail.position[0], tail.position[1] + 1), 1, tail)

        tail.child = new_segment

    def is_collision_w_self(self):
        segment = self.child
        while segment:
            if self.position == segment.position:
                return True
            segment = segment.child
        return False

    def is_collision_w_food(self, food_obj):
        if food_obj.rect.colliderect(self.rect):
            return True
        else:
            return False

    def is_collision_w_frame(self):
        if (self.rect.colliderect(game.game_frame.top_frame_rect) or
                self.rect.colliderect(game.game_frame.bottom_frame_rect) or
                self.rect.colliderect(game.game_frame.left_frame_rect) or
                self.rect.colliderect(game.game_frame.right_frame_rect)):
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


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/feed.png').convert_alpha()
        self.position = self._generate_coordinates()
        self.rect = self.image.get_rect(x=self.position[0] * GRIDSIZE, y=self.position[1] * GRIDSIZE)

    def _generate_coordinates(self):
        # generate new food coordinates adjusted by the food image width and height and frame thickness (6) to avoid
        # collision with frame
        x_pos = randint((40 + 6 + self.image.get_width()) // GRIDSIZE, (760 - 6 - self.image.get_width()) // GRIDSIZE)
        y_pos = randint((75 + 6 + self.image.get_height()) // GRIDSIZE, (620 - 6 - self.image.get_height()) // GRIDSIZE)
        return x_pos, y_pos

    def add_food(self, food_sprite_gr, snake_sprite_gr):  # test
        food_coordinates = self._generate_coordinates()
        self.rect = self.image.get_rect(x=food_coordinates[0] * GRIDSIZE, y=food_coordinates[1] * GRIDSIZE)
        food_sprite_gr.add(self)
        food_sprite = [sprite for sprite in food_sprite_gr][0]
        if pygame.sprite.spritecollideany(food_sprite, snake_sprite_gr):
            self.add_food(food_sprite_gr, snake_sprite_gr)


class Frame:
    def __init__(self, surface):
        self.surface = surface
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


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        # screen setup
        self.screen = pygame.display.set_mode((800, 672))
        self.background_surf = pygame.image.load('assets/background.png').convert()
        self.game_frame = Frame(self.background_surf)
        # game font setup
        self.game_font = pygame.font.Font('fonts/Minimal3x5.ttf', 60)
        # score board setup
        self.score = 0
        self.score_board = self.game_font.render(f"0{self.score}" if self.score < 10 else f"{self.score}",
                                                 False, 'black')
        self.score_rect = self.score_board.get_rect(center=(70, 50))
        # snake and food setup
        self.food = None
        self.snake_sprites = None
        self.snake = None
        self.food_sprites = None
        self._add_sprites()
        # game clock setup
        self.clock = pygame.time.Clock()
        # snake timer setup
        self.speed = 350
        self.snake_movement = pygame.USEREVENT + 1
        self._setup_snake_timer()
        # game state setup
        self.game_active = False
        self.start = True
        self.replay = False
        # start screen setup
        self.start_screen = StartScreen()
        # game over screen setup
        self.game_over_screen = GameOverScreen()

    def _setup_snake_timer(self):
        pygame.time.set_timer(self.snake_movement, self.speed)

    def increase_game_speed(self, increment):
        self.speed += increment

    def update_score(self):
        self.score += 1
        self.score_board = self.game_font.render(f"0{self.score}" if self.score < 10 else f"{self.score}",
                                                 False, 'black')

    def _add_sprites(self):
        # snake sprites
        self.snake_sprites = pygame.sprite.Group()
        self.snake = Snake(self.snake_sprites, (30, 15), 1)
        # food sprites
        self.food_sprites = pygame.sprite.GroupSingle()
        self.food = Food()
        self.food_sprites.add(self.food)

    def check_game_state(self):
        if self.snake.is_collision_w_frame():
            return False
        if self.snake.is_collision_w_self():
            return False
        else:
            return True

    def reset_game(self):
        # Reset score
        self.score = 0
        self.update_score()

        # Reset game speed
        self.speed = 350
        self._setup_snake_timer()

        # Reset snake and food
        self.snake_sprites = None
        self.food_sprites = None
        self._add_sprites()

        # Reset game state
        self.game_active = False
        self.replay = False
        self.start = True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == self.snake_movement:
                    self.snake.move()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.replay = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.game_active = True
                    self.start = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            if self.snake.is_collision_w_food(self.food):
                self.food.kill()
                self.snake.grow()
                self.update_score()
                self.food.add_food(self.food_sprites, self.snake_sprites)
                self.increase_game_speed(10)

            if self.game_active:
                self.screen.blit(self.background_surf, (0, 0))
                self.screen.blit(self.score_board, self.score_rect)
                self.food_sprites.draw(self.screen)
                self.snake_sprites.update()
                self.snake_sprites.draw(self.screen)
                self.game_active = self.check_game_state()

            else:
                if self.start:
                    self.start_screen.show()
                else:
                    self.game_over_screen.show()
                    if self.replay:
                        self.reset_game()
                        self.run()
            game.clock.tick(60)
            pygame.display.update()


game = Game()
game.run()

# grow() - change the additional movement of the added segment
# add bite sound
# add game over and intro screens
# fill readme
# refactor - GRIDSIZE, etc
