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


def draw_dashed_line(start, end, height):
    counter = 0
    while start + counter < end:
        pygame.draw.line(background_surf, 'black', (start + counter, height), (start + counter + 3, height), 5)
        counter += 5


background_surf = pygame.image.load('assets/background.png').convert()
# game frame
draw_dashed_line(40, 760, 70)
draw_dashed_line(40, 760, 85)
draw_dashed_line(40, 760, 620)


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
