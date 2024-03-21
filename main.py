import pygame


def load_snake_images():
    snake_parts = ('head', 'eating_head', 'body', 'turn', 'tail')
    images = [pygame.image.load(f"assets/{part}.png").convert_alpha() for part in snake_parts]
    head_img, eating_head_img, body_img, turn_img, tail_img = images

    directions = ('L', 'R', 'U', 'D')
    angles = (0, 180, -90, 90)
    snake_parts_dict = {f'{part}_{direction}': pygame.transform.rotate(image, angle) for part in snake_parts for
                        direction in directions for image in images for angle in angles}

    return snake_parts_dict

print(load_snake_images())