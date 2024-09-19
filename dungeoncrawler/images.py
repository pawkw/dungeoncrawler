from dungeoncrawler.constants import *
import pygame

def scale_image(image, scale_factor):
    width = image.get_width() * scale_factor
    height = image.get_height() * scale_factor
    return pygame.transform.scale(image, (width, height))


def load_images(path, use_offset):
    images = []
    images_flipped = []
    for number in range(4):
        image = scale_image(pygame.image.load(f'{path}{number}.png').convert_alpha(), IMAGE_SCALE)
        if use_offset:
            rect = image.get_rect()
            new_image = pygame.Surface((ITEM_SIZE, ITEM_SIZE+10), pygame.SRCALPHA)
            new_image.blit(image, (0,0), (0, OFFSET*IMAGE_SCALE, rect.width, rect.height))
            image = new_image
        images.append(image)
        images_flipped.append(pygame.transform.flip(images[-1], True, False))
    return [images, images_flipped]

def load_tiles(path):
    images = []
    for number in range(18):
        image = pygame.transform.scale(pygame.image.load(f'{path}{number}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
        images.append(image)
    return images

def load_image(path):
    return pygame.image.load(path+'.png').convert_alpha()