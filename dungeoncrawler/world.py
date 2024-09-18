from dungeoncrawler.constants import *
import pygame
from dataclasses import dataclass

@dataclass
class Tile:
    def __init__(self, image, image_rect):
        self.image = image
        self.rect = image_rect

class World:
    def __init__(self):
        self.map_tiles = []

    def process_data(self, data, tile_image_list):
        self.level_length = len(data)

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image: pygame.surface.Surface = tile_image_list[tile]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.center = (image_x, image_y)

                if tile >= 0:
                    self.map_tiles.append(Tile(image, image_rect))

    def draw(self, surface: pygame.surface.Surface):
        for tile in self.map_tiles:
            surface.blit(tile.image, tile.rect)