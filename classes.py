import pygame


class Snake(pygame.sprite.Sprite):
    pass


class Feed(pygame.sprite.Sprite):
    pass


class GameOverScreen:
    pass


class Game:
    pass


# setup
pygame.init()
screen = pygame.display.set_mode((800, 672))
pygame.display.set_caption("Retro Snake")
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/MobileFont.ttf', 50)
game_active = True


def draw_dashed_line(start, end, v_distance):
    counter = 0
    while start + counter < end:
        pygame.draw.line(background_surf, 'black', (start + counter, v_distance), (start + counter + 3, v_distance), 5)
        counter += 5


def draw_dashed_line_vertical(start, end, h_distance):
    counter = 0
    while h_distance + counter < end:
        pygame.draw.line(background_surf, 'black', (start, h_distance + counter), (start+3, h_distance + counter), 5)
        counter += 7
# (40, 70) (41, 70)
# (40, 71) (41, 71)

background_surf = pygame.image.load('assets/background.png').convert()
# game frame
draw_dashed_line(40, 760, 70)
draw_dashed_line(40, 760, 87)
draw_dashed_line(40, 760, 620)
draw_dashed_line_vertical(40, 620, 94)
draw_dashed_line_vertical(755, 620, 94)
# pygame.draw.line(background_surf, 'black', (40, 94), (43, 94), 5)
# pygame.draw.line(background_surf, 'black', (40, 101), (43, 101), 5)

# score board
score_sur = game_font.render('0036', False, 'black')
score_rect = score_sur.get_rect(center=(110, 45))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if game_active:
        screen.blit(background_surf, (0, 0))
        screen.blit(score_sur, score_rect)

    pygame.display.update()
    clock.tick(60)
